---
title: 我的 Ubuntu24.04
tags: [tools]
math:
modified: 星期日, 三月 16日 2025, 7:51:37 晚上
---

## 软件

1. 社交软件：
    1. QQ、微信：这俩都用 flatpak 安装，防止扫硬盘
    2. Telegram：用 appimage，用于一些国外的群聊
2. 浏览器：
    1. Google Chrome 和 Edge：因为 Chrome 在学校的一些网页上会有问题，Edge 就用来应急
3. 办公、科研：
    1. 飞书：官网有 deb 包，在 ipads 实习的时候用过
    2. evolution：收发邮件，用 apt 装
    3. 腾讯会议：只能在 x11 下使用，官网有 deb 包
    4. WPS Linux：注意不要装错成 WPS2019 了，官网在 <https://linux.wps.cn/>
    5. Zotero：用来管理论文，不过目前为止还没完全熟练
    6. Zoom：用来和国外教授开会
    7. Cohesion：notion 的第三方客户端，用来记录科研进展；也可以用 obsidian 代替，但是多人协作更方便些
    8. xmind、drawio：论文画图、思维导图
4. 代码：
    1. vscode：远程主力，以及写 jupyter notebook 的时候用
    2. neovim：本地写小项目、改配置用，配置在 GitHub 上；
    3. neovide：偶尔用 neovide 当 neovim 的 GUI，用 AppImage 装，因为
    4. JetBrains 系列：写大型项目用，但是基本没打开过，可以装一个 JetBrains Toolbox 来集中管理不同的 IDE
    5. Cursor：白嫖版的，用来读大型项目
    6. vim：用来改需要 root 权限的文件，用 apt 装，配置在 GitHub 上
5. 终端：
    1. Wezterm：比原生的 gnome-terminal 重一点，但是毕竟好看些（
    2. zsh + oh-my-zsh：非常好看好用好吧
    3. tmux：分屏操作
6. 笔记：
    1. Obsidian：用 markdown 记笔记，目前是在用 Onedrive 进行笔记同步，用 GitHub 进行配置保存；用 deb 包可以安装（见 [GitHub - obsidianmd/obsidian-releases: Community plugins list, theme list, and releases of Obsidian.](https://github.com/obsidianmd/obsidian-releases)）
    2. Neovim：偶尔用 neovim 写写笔记，用官网装最新版的
7. 娱乐：
    1. Bilibili：用的第三方客户端 [GitHub - msojocs/bilibili-linux: 基于哔哩哔哩官方客户端移植的Linux版本 支持漫游](https://github.com/msojocs/bilibili-linux)
    2. 音乐：
        1. Yesplaymusic：网易云音乐的第三方客户端，非常纯净，在 GitHub 上装 [GitHub - qier222/YesPlayMusic: 高颜值的第三方网易云播放器，支持 Windows / macOS / Linux](https://github.com/qier222/YesPlayMusic)
        2. Amberol：用来放本地音乐，用 apt 装
        3. QQmusic：用 flatpak 装，听网易云没有版权的歌
8. 阅读：
    1. Koodo Reader：用来读 EPUB 格式的电子书
    2. Newsflash：RSS 阅读器，用来订阅一些大佬的博客，用 flatpak 装
9. 系统：
    1. Flatseal：用来管理 flatpak 装的软件，权限设置等，用 flatpak 装
    2. Font downloader：用来便捷的装字体，但是没怎么用过，用 apt 装
    3. Clash Verge：vpn，有点小 bug 但是能将就用
    4. Fcitx5 + 雾凇输入法：系统自带的 ibus 无法在腾讯会议和微信中输入中文，所以换了这个组合
    5. BleachBit、Czkawka：用来清理垃圾文件
    6. Gparted：磁盘管理
    7. Software：需要把原来的软件商店给卸载了（因为是 snap），然后重新装 gnome-software
    8. flatpak：装一些 apt 里面没有的软件，以及用来隔离一些流氓的国产软件
    9. Tweaks：用来自定义系统
    10. tlp：更好的电源管理
10. 文件管理：
    1. nautilus：系统自带的文件管理器
    2. meld：nautilus 的一个插件，可以显示 Git 仓库的状态
    3. lazygit：终端 git 的 GUI，一般就用来看看仓库状态
    4. yazi：终端文件管理器，很方便，官方有下载指南 [Installation \| Yazi](https://yazi-rs.github.io/docs/installation/)，配置保存在 github 上，用了三个插件 git、mediainfo、miller
    5. 文件查看器：
        1. Image Viewer：系统自带的图片查看器
        2. mpv：查看视频
    6. Onedrive：用来同步文件，配合 onedrive-tray 使用，并且设置为开机自启
11. 效率：
    1. Pomorodo：番茄钟，用 apt 装
    2. Dialect：小翻译软件，实质上调用的是 google 翻译，配上快捷键之后很方便，用 apt 装
    3. Kuro：微软 todo 的第三方客户端，在 GitHub 上下载
    4. Characters：系统自带，有很多表情包，便于查找
    5. Picgo：图床管理
12. 其他工具：
    1. obs studio：用来录屏
    2. docker：快速配置环境
    3. conda：配置 python 环境
    4. mkdocs：用来搭网站

## Gnome 美化

1. 装 gnome-tweaks 用于更多的自定义，以及 extensions 用来管理插件
2. 字体：
    1. Interface/document text 用 Noto Sans CJK SC
    2. monospace text/终端/vscode 用 MesloLGS Nerd Font Mono
    3. Chrome 和个人网站 用 LXGW
3. 外观：
    1. Cursor：WhiteSur-cursors
    2. Icons、Shell、Legacy Applications：WhiteSur-Dark
4. 插件：
    1. Blur my shell：用于模糊效果
    2. Caffine：全屏不熄屏
    3. Clipboard Indicator：剪切板
    4. Coverflow-tab：更好的切换页面
    5. Hide items：隐藏 bar 上过多的软件图标
    6. input method panel：给 fcitx5 更好看的输入面板
    7. User themes：自定义主题
    8. Apps menu
    9. Removable drive menu
    10. Ubuntu appindicators
    11. Ubuntu dock：仿 mac 风格
    12. Ubuntu Tilling assistant
5. 壁纸：到处搜集的，隔几天换一下

> [!note]- 点开看壁纸
> ![](https://cdn.jsdelivr.net/gh/KinnariyaMamaTanha/Images@images/20250316203417556.png)
>
> ![](https://cdn.jsdelivr.net/gh/KinnariyaMamaTanha/Images@images/20250316203452502.png)
