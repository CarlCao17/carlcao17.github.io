#!/usr/bin/env python3
"""Export only explicitly approved Obsidian notes. Default: dry run."""
import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

import yaml


class ExportError(ValueError):
    pass


def frontmatter(text):
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not match:
        return {}, text
    try:
        data = yaml.safe_load(match[1]) or {}
    except yaml.YAMLError as exc:
        raise ExportError("Invalid YAML front matter") from exc
    if not isinstance(data, dict):
        raise ExportError("Front matter must be a mapping")
    return data, text[match.end():]


def safe_files(vault):
    """Do not follow symlinks or read Obsidian/plugin/Git hidden files."""
    return sorted(p for p in vault.rglob('*') if p.is_file()
                  and not p.is_symlink()
                  and not any(part.startswith('.') for part in p.relative_to(vault).parts)
                  and p.resolve().is_relative_to(vault))


def approved_notes(vault, files):
    notes = []
    slugs = set()
    for path in files:
        if path.suffix.lower() != '.md':
            continue
        metadata, body = frontmatter(path.read_text(encoding='utf-8'))
        # Boolean true is required; strings such as "true" never approve a note.
        if metadata.get('publish') is not True:
            continue
        slug = metadata.get('slug', '')
        if not isinstance(slug, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
            raise ExportError(f'{path.name}: publish:true requires a stable lowercase slug')
        if slug in slugs:
            raise ExportError(f'Duplicate slug: {slug}')
        slugs.add(slug)
        date = metadata.get('date')
        if isinstance(date, (dt.date, dt.datetime)):
            date = date.isoformat()
        try:
            dt.datetime.fromisoformat(str(date).replace('Z', '+00:00'))
        except ValueError as exc:
            raise ExportError(f'{path.name}: date must be an ISO date or timestamp') from exc
        title = metadata.get('title', path.stem)
        tags = metadata.get('tags', [])
        draft = metadata.get('draft', False)
        if not isinstance(title, str) or not title.strip():
            raise ExportError(f'{path.name}: title must be a non-empty string')
        if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
            raise ExportError(f'{path.name}: tags must be a list of strings')
        if not isinstance(draft, bool):
            raise ExportError(f'{path.name}: draft must be a boolean')
        public = {'title': title, 'date': date, 'draft': draft, 'tags': tags}
        for key in ('description', 'summary'):
            if key in metadata:
                if not isinstance(metadata[key], str):
                    raise ExportError(f'{path.name}: {key} must be a string')
                public[key] = metadata[key]
        if 'math' in metadata:
            if not isinstance(metadata['math'], bool):
                raise ExportError(f'{path.name}: math must be a boolean')
            public['math'] = metadata['math']
        notes.append({'path': path, 'slug': slug, 'metadata': public, 'body': body})
    return notes


def find_target(vault, source, target, files, extensions=None):
    target = unquote(target).replace('\\', '/')
    if not target or target.startswith('/'):
        raise ExportError('Empty or absolute local link')
    # First use explicit relative paths; reject links escaping the vault.
    candidate = (source.parent / target).resolve()
    if not candidate.is_relative_to(vault):
        raise ExportError('Local link escapes the vault')
    variants = [candidate]
    if extensions and not candidate.suffix:
        variants += [candidate.with_suffix(s) for s in extensions]
    for item in variants:
        if item in files:
            return item
    names = [target]
    if extensions and not Path(target).suffix:
        names += [target + s for s in extensions]
    matches = [p for p in files if any(
        p.relative_to(vault).as_posix() == n or p.relative_to(vault).as_posix().endswith('/' + n)
        for n in names)]
    if len(matches) != 1:
        raise ExportError(f'Local link missing or ambiguous: {target}')
    return matches[0]


def anchor(value):
    if value.startswith('^'):
        raise ExportError('Obsidian block references require conversion before export')
    return quote(re.sub(r'[^\w\s-]', '', value.lower()).strip().replace(' ', '-'))


def convert_note(note, vault, files, approved):
    assets = {}
    source = note['path']

    def asset(target):
        path = find_target(vault, source, target, files)
        if path.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.avif', '.pdf'}:
            raise ExportError(f'Unsupported attachment type: {path.suffix}')
        digest = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
        name = 'assets/' + digest + path.suffix.lower()
        assets[name] = path
        return name

    def page_link(target):
        name, sep, heading = target.partition('#')
        if not name:
            return '#' + anchor(heading)
        path = find_target(vault, source, name, files, extensions=['.md'])
        if path not in approved:
            raise ExportError('Link points to a note without publish:true; approve it or remove the link')
        linked = approved[path]
        if linked['metadata']['draft'] and not note['metadata']['draft']:
            raise ExportError('Published note links to a draft; publish the target or remove the link')
        url = '/posts/obsidian/' + linked['slug'] + '/'
        return url + ('#' + anchor(heading) if sep else '')

    def wiki(match):
        embed, inside = match.groups()
        target, separator, label = inside.partition('|')
        if embed:
            if Path(target).suffix.lower() == '.md' or not Path(target).suffix:
                raise ExportError('Embedded notes are not exported automatically; use an ordinary link')
            alt = '' if not separator or label.isdigit() or re.fullmatch(r'\d+x\d+', label) else label
            return '![' + alt + '](' + asset(target) + ')'
        label = label if separator else target.split('#', 1)[0]
        label = label or target.split('#', 1)[-1]
        return '[' + label.replace(']', '\\]') + '](' + page_link(target) + ')'

    def markdown(match):
        prefix, label, raw = match.groups()
        # Keep optional Markdown link title.
        parsed = re.fullmatch(r'(<[^>]+>|[^\s]+)(\s+[\"\'].*[\"\'])?', raw)
        if not parsed:
            raise ExportError('Local Markdown URLs with spaces must use angle brackets')
        target = parsed[1].strip('<>')
        suffix = parsed[2] or ''
        parts = urlsplit(target)
        if parts.scheme or target.startswith(('//', '#')):
            return match[0]
        path = unquote(parts.path)
        if Path(path).suffix.lower() == '.md' or not Path(path).suffix:
            url = page_link(path + ('#' + unquote(parts.fragment) if parts.fragment else ''))
        else:
            url = asset(path)
        return prefix + '[' + label + '](' + url + suffix + ')'

    def transform(text):
        # Convert ordinary Markdown first so emitted wiki links are not processed twice.
        text = re.sub(r'(!?)\[([^\]\n]*)\]\(([^)\n]+)\)', markdown, text)
        return re.sub(r'(!?)\[\[([^\]\n]+)\]\]', wiki, text)

    # Code fences, inline code and indented code remain byte-for-byte intact.
    protected = re.compile(r'(^[ \t]*(`{3,}|~{3,})[^\n]*\n.*?^[ \t]*\2[ \t]*$|`+[^`\n]*`+|^(?: {4}|\t)[^\n]*$)', re.M | re.S)
    body = note['body']
    pieces = []
    cursor = 0
    for match in protected.finditer(body):
        pieces.append(transform(body[cursor:match.start()]))
        pieces.append(match[0])
        cursor = match.end()
    pieces.append(transform(body[cursor:]))
    header = yaml.safe_dump(note['metadata'], allow_unicode=True, sort_keys=False).strip()
    return '---\n' + header + '\n---\n\n' + ''.join(pieces).lstrip('\r\n'), assets


def export(vault, output, write=False):
    if Path(output).is_symlink():
        raise ExportError('Output must not be a symlink')
    vault, output = Path(vault).resolve(), Path(output).resolve()
    if not vault.is_dir():
        raise ExportError('Vault directory does not exist')
    if output.is_relative_to(vault) or vault.is_relative_to(output):
        raise ExportError('Export output and vault must be separate directories')
    files = safe_files(vault)
    notes = approved_notes(vault, files)
    approved = {n['path']: n for n in notes}
    payload = []
    for note in notes:
        body, assets = convert_note(note, vault, files, approved)
        payload.append((note, body, assets))
    manifest = {'version': 1, 'posts': [n['slug'] for n in notes]}
    if write:
        # This is a fully managed directory: never overwrite unrelated files.
        old_manifest = output / '.export-manifest.json'
        if output.exists() and any(output.iterdir()) and not old_manifest.is_file():
            raise ExportError('Non-empty output is not an exporter-managed directory')
        old = json.loads(old_manifest.read_text()) if old_manifest.exists() else {'posts': []}
        if old.get('version', 1) != 1 or not isinstance(old.get('posts'), list):
            raise ExportError('Invalid export manifest')
        allowed = set(old['posts']) | {'.export-manifest.json'}
        if output.exists() and any(p.name not in allowed or p.is_symlink() for p in output.iterdir()):
            raise ExportError('Unmanaged files or symlinks found in output')
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.obsidian-export-', dir=output.parent) as tmp:
            stage = Path(tmp) / 'export'
            stage.mkdir()
            for note, body, assets in payload:
                bundle = stage / note['slug']
                bundle.mkdir()
                (bundle / 'index.md').write_text(body, encoding='utf-8')
                for name, path in assets.items():
                    target = bundle / name
                    target.parent.mkdir(exist_ok=True)
                    shutil.copy2(path, target)
            (stage / '.export-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
            # Retain the previous output until the staged output has been promoted.
            backup = Path(tmp) / 'previous'
            if output.exists():
                output.rename(backup)
            try:
                stage.rename(output)
            except OSError:
                if backup.exists():
                    backup.rename(output)
                raise
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vault', required=True, type=Path)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1] / 'content/posts/obsidian')
    parser.add_argument('--write', action='store_true', help='Write the validated export; default is dry run')
    args = parser.parse_args()
    try:
        result = export(args.vault, args.output, args.write)
    except (ExportError, OSError, ValueError) as exc:
        parser.exit(1, f'Export stopped: {exc}\n')
    print(json.dumps({'mode': 'write' if args.write else 'dry-run', **result}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
