#!/usr/bin/env bash
set -euo pipefail
BLOG_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$BLOG_ROOT"
if command -v hugo >/dev/null 2>&1; then
  BLOG_HUGO="$(command -v hugo)"
elif [[ -x "$BLOG_ROOT/.local/bin/hugo" ]]; then
  BLOG_HUGO="$BLOG_ROOT/.local/bin/hugo"
else
  echo '请先安装 Hugo：https://gohugo.io/installation/' >&2
  exit 1
fi
case "${1:-help}" in
  new)
    BLOG_SLUG="${2:-}"
    if [[ ! "$BLOG_SLUG" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
      echo '用法：./scripts/blog.sh new my-article（小写英文、数字和短横线）' >&2
      exit 1
    fi
    "$BLOG_HUGO" new content "posts/$BLOG_SLUG/index.md" --kind posts
    ;;
  preview)
    "$BLOG_HUGO" server --bind 127.0.0.1 --disableFastRender --buildDrafts
    ;;
  import)
    if [[ $# -lt 2 ]]; then
      echo '用法：./scripts/blog.sh import /path/to/vault [--write]（默认只检查）' >&2
      exit 1
    fi
    BLOG_VAULT="$2"
    shift 2
    python3 scripts/export_obsidian.py --vault "$BLOG_VAULT" "$@"
    ;;
  check)
    python3 -m unittest discover -s tests -v
    "$BLOG_HUGO" --gc --minify --cleanDestinationDir
    python3 scripts/check_site.py public
    ;;
  *)
    echo 'new <slug>  新建草稿'
    echo 'preview     本地预览（含草稿）'
    echo 'import <vault> [--write]  检查 / 导出已批准笔记'
    echo 'check       测试、构建和链接检查'
    ;;
esac
