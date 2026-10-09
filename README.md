# Carl’s notes

个人博客：Hugo + Typo。简洁中文排版、文章列表、专题、公开项目、全文搜索与 RSS。

网站地址：https://carlcao17.github.io/

## 使用

安装 Hugo **0.167.0**，以及 Python 3.10+。Typo 已随仓库保存，无需另行安装主题。

```sh
python3 -m pip install -r scripts/requirements.txt
./scripts/blog.sh new my-article
./scripts/blog.sh preview
./scripts/blog.sh check
```

详细说明：[管理博客](docs-maintenance/管理博客.md)。

## Obsidian

私人笔记只按明确的 `publish: true` 标记在本地导出。默认命令只检查，不写入。CI 不访问私人仓库。

```sh
./scripts/blog.sh import /path/to/ObsidianRepo
./scripts/blog.sh import /path/to/ObsidianRepo --write
```

## 发布

PR 运行测试、构建与内部链接检查。合并到 `main` 后使用 GitHub Pages Actions 部署；首次上线需将仓库 Pages 的 Source 设置为 GitHub Actions。

## 来源

- [Hugo](https://gohugo.io/)
- [Typo](https://github.com/tomfran/typo)，MIT，版本见 `themes/typo/UPSTREAM.md`
- 页面风格参考 [codedump notes](https://www.codedump.info/en/)，未复制该站文章或个人资料。

旧 MkDocs 资料仍保留在仓库，详见 [旧站说明](legacy/README.md)。
