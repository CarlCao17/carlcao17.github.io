import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/export_obsidian.py'
spec = importlib.util.spec_from_file_location('export_obsidian', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.vault = self.root / 'vault'
        self.vault.mkdir()
        self.output = self.root / 'content'

    def tearDown(self):
        self.tmp.cleanup()

    def note(self, name, slug, body='', extra=''):
        p = self.vault / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f'---\npublish: true\nslug: {slug}\ndate: 2024-01-01\ntags: [Go]\n{extra}---\n{body}')
        return p

    def test_whitelist_hidden_files_and_dry_run(self):
        (self.vault / 'private.md').write_text('private note')
        (self.vault / 'string.md').write_text('---\npublish: "true"\n---\nprivate')
        self.note('.obsidian/hidden.md', 'hidden')
        self.note('approved.md', 'approved')
        self.assertEqual(m.export(self.vault, self.output)['posts'], ['approved'])
        self.assertFalse(self.output.exists())

    def test_wiki_links_assets_and_code_preservation(self):
        self.note('one.md', 'one', '[[two|第二篇]] ![[picture.png|300]]\n`[[private]]`\n```md\n[[private]]\n```\n')
        self.note('two.md', 'two')
        (self.vault / 'picture.png').write_bytes(b'fixture-image')
        m.export(self.vault, self.output, True)
        body = (self.output / 'one/index.md').read_text()
        self.assertIn('[第二篇](/posts/obsidian/two/)', body)
        self.assertIn('![](assets/', body)
        self.assertIn('`[[private]]`', body)
        self.assertIn('```md\n[[private]]\n```', body)
        self.assertEqual(len(list((self.output / 'one/assets').iterdir())), 1)

    def test_private_link_blocks_entire_export(self):
        self.note('one.md', 'one', '[[private]]')
        (self.vault / 'private.md').write_text('secret')
        with self.assertRaises(m.ExportError):
            m.export(self.vault, self.output, True)
        self.assertFalse(self.output.exists())

    def test_duplicate_slug_and_ambiguous_attachment(self):
        self.note('one.md', 'same')
        self.note('two.md', 'same')
        with self.assertRaises(m.ExportError):
            m.export(self.vault, self.output)
        self.note('two.md', 'two', '![[image.png]]')
        for folder in ('a', 'b'):
            (self.vault / folder).mkdir()
            (self.vault / folder / 'image.png').write_bytes(b'image')
        with self.assertRaises(m.ExportError):
            m.export(self.vault, self.output)

    def test_retraction_removes_previous_export_and_missing_asset_is_transactional(self):
        p = self.note('one.md', 'one', 'public text')
        m.export(self.vault, self.output, True)
        self.note('one.md', 'one', '![[missing.png]]')
        with self.assertRaises(m.ExportError):
            m.export(self.vault, self.output, True)
        self.assertIn('public text', (self.output / 'one/index.md').read_text())
        p.write_text('---\npublish: false\n---\nprivate now')
        m.export(self.vault, self.output, True)
        self.assertFalse((self.output / 'one').exists())

    def test_escape_symlinks_and_unmanaged_output(self):
        (self.root / 'secret.png').write_bytes(b'secret')
        (self.vault / 'link.png').symlink_to(self.root / 'secret.png')
        self.note('one.md', 'one', '![[link.png]]')
        with self.assertRaises(m.ExportError):
            m.export(self.vault, self.output)
        self.note('one.md', 'one', '![x](../secret.png)')
        with self.assertRaises(m.ExportError):
            m.export(self.vault, self.output)
        self.note('one.md', 'one', 'ok')
        self.output.mkdir()
        (self.output / 'manual.md').write_text('retain')
        with self.assertRaises(m.ExportError):
            m.export(self.vault, self.output, True)
        self.assertTrue((self.output / 'manual.md').exists())

    def test_markdown_links_and_draft_dependency(self):
        self.note('one.md', 'one', '[第二篇](two.md#Some Heading)')
        self.note('two.md', 'two')
        with self.assertRaises(m.ExportError):
            m.export(self.vault, self.output)
        self.note('one.md', 'one', '[第二篇](two.md#Some%20Heading)')
        m.export(self.vault, self.output, True)
        self.assertIn('/two/#some-heading', (self.output / 'one/index.md').read_text())
        self.note('two.md', 'two', extra='draft: true\n')
        with self.assertRaises(m.ExportError):
            m.export(self.vault, self.output)

    def test_indented_code_does_not_hide_following_links(self):
        self.note('one.md', 'one', '    [[private]]\n\n[[two]]\n')
        self.note('two.md', 'two')
        m.export(self.vault, self.output, True)
        body = (self.output / 'one/index.md').read_text()
        self.assertIn('    [[private]]', body)
        self.assertIn('[two](/posts/obsidian/two/)', body)

    def test_output_symlink_is_rejected(self):
        self.note('one.md', 'one')
        real = self.root / 'real'
        real.mkdir()
        self.output.symlink_to(real, target_is_directory=True)
        with self.assertRaises(m.ExportError):
            m.export(self.vault, self.output, True)


if __name__ == '__main__':
    unittest.main()
