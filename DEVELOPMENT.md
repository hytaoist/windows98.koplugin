# 开发与发布

本文档面向修改、构建和维护项目的人。普通安装请阅读 [README.md](README.md)。

## 项目结构

```text
plugin/                             KOReader 插件入口、部署与 OTA
patches/2-windows98.lua             稳定用户补丁/加载器
plugin/theme/apply.lua              Windows 98 UI 运行时修改
assets/icons/                       KOReader 图标
assets/simpleui-icons/              SimpleUI 图标包
assets/fonts/Windows98UI.ttf        生成的常规 UI 字体
assets/fonts/Windows98UI-Bold.ttf   生成的粗体 UI 字体
assets/fonts/LiberationSans-*.ttf   字体生成源
assets/sponsor/                     微信赞赏码
tools/generate_icons.py             图标生成器
tools/generate_font.py              字体生成器
tools/generate_preview.py           README 预览图生成器
tests/                              自动化测试
dist/                               构建产物
```

安装后，文件分布在：

```text
koreader/plugins/windows98.koplugin/            Storefront 管理的插件
koreader/patches/2-windows98.lua               用户补丁/加载器
koreader/.windows98-theme/runtime/apply.lua    稳定运行时副本
koreader/.windows98-theme/backup/              原文件备份
koreader/icons/                                KOReader 图标
koreader/fonts/Windows98UI.ttf                 常规 UI 字体
koreader/fonts/Windows98UI-Bold.ttf            粗体 UI 字体
koreader/settings/simpleui/sui_icons/packs/Windows 98/
```

插件只使用 KOReader 的公开模块和用户补丁机制。UI 修改均有 `pcall` 保护。
Storefront 可以整体替换插件目录，稳定补丁和部署目录因此独立于插件目录。

## 视觉规则

```text
窗口/按钮主体  #c0c0c0 银色
高光/阴影      #ffffff / #808080
活动标题栏     #000080 深蓝（电子墨水屏上使用深灰）
桌面/屏幕区域  #008080 青色（预览图）
描边/文字      #000000 黑色
按钮圆角       0
窗口阴影       2 px 硬黑阴影
```

运行时使用 KOReader 的 8-bit 灰度颜色常量，因此 Kindle 上不会依赖彩色。
预览图保留 Windows 98 的深蓝标题栏和青色桌面。

## 字体

`tools/generate_font.py` 把 Liberation Sans 在 11 px 下栅格化，再重建为方形
TrueType 轮廓。输出文件：

```text
Windows98UI.ttf       Regular
Windows98UI-Bold.ttf  Bold
```

字体只覆盖 printable ASCII；中文由 KOReader 自动回退到系统中文字体。运行时把
`Windows98UI.ttf` 注册为常规字体，并把 `Windows98UI-Bold.ttf` 注册为其粗体
变体。

```bash
python3 tools/generate_font.py
```

重新生成字体需要 Python 的 `fontTools` 和 `Pillow`。Liberation Sans 源文件及
OFL 许可随仓库保留；生成字体也按 OFL 1.1 分发。

## 图标

图标生成器只使用 SVG 矩形、直线、多边形和路径，不依赖滤镜或渐变。关键视觉元素：

```text
金色文件夹
CRT 电脑 / 文档 / 网络
四色抽象 Windows 徽标
银色凸起和凹陷面板
白色左上高光、深灰右下阴影、黑色硬投影
```

```bash
python3 tools/generate_icons.py
```

生成器会校验 103 个 KOReader 图标和 34 个 SimpleUI 图标的完整文件名集合，避免
升级 KOReader 后漏图标。

## 预览图

```bash
python3 tools/generate_preview.py
```

预览图由 SVG、内置的 `Windows98UI` 字体和本机 Chrome/Chromium 无头模式生成。
如果没有 Chrome，脚本会尝试使用 macOS `sips`。输出位于 `preview/`：

```text
windows98-ui.png
windows98-about.png
icon-sheet.png
simpleui-icon-sheet.png
```

关于页预览内嵌实际微信赞赏码。

## 构建

```bash
./build.sh
```

输出：

```text
dist/windows98-v<version>.koplugin.zip  Storefront Release asset
dist/windows98-v<version>.zip           手动安装包
dist/SHA256SUMS
```

Storefront 要求 ZIP 根目录为 `windows98.koplugin/`，且目录内包含
`_meta.lua`。ZIP 使用固定文件顺序、权限和 `1998-06-25` 时间戳，因此重复构建会
得到相同的 SHA-256。

## 测试

```bash
lua tests/patch_smoke_test.lua plugin/theme/apply.lua
lua tests/main_test.lua plugin/main.lua
lua tests/ota_test.lua plugin/ota.lua
./tests/run_loader_test.sh
./tests/run_deploy_test.sh
./tests/run_installer_test.sh
./tests/run_build_repro_test.sh
```

测试覆盖主题运行时、关于/赞助弹窗、OTA、首次部署、重复安装、双字体部署、
SimpleUI 设置恢复、卸载、AppleDouble 元数据清理、Storefront ZIP 结构和构建
可重复性。

## 发布

1. 修改 `plugin/_meta.lua` 和 `assets/simpleui-icons/pack.lua` 中的版本号。
2. 运行生成器、完整测试和 `./build.sh`。
3. 提交代码并创建 `v<version>` 标签。
4. 推送标签，`.github/workflows/release.yml` 会测试、构建并上传 GitHub Release。

也可以运行 `./publish.sh`，但需要本机 `gh` 已完成 GitHub 登录，并且仓库已存在
或显式设置 `CREATE_GITHUB_REPO=1`。

GitHub Actions：

- `test.yml`：每次 push/PR 跑语法、单元测试、安装测试和可重复构建
- `release.yml`：标签与 `_meta.lua` 版本一致时自动创建 Release

OTA 依赖最新 Release 中的 `.koplugin.zip` 资产，因此仓库和 `v1.0.0` Release
必须先公开发布，在线更新才能工作。

## 赞助入口

微信赞赏码由 `plugin/_meta.lua` 中的 `sponsor_wechat_qr` 配置。当前
`sponsor_url = nil`，关于页只显示 `Show WeChat reward code` 和 `Close`，不会
显示空链接、复制按钮或二维码按钮。

替换赞赏码时，把图片放到 `assets/sponsor/wechat-reward.jpg`，保持文件名即可。
图片会进入 Storefront ZIP，并在设备上离线显示。

## 高级设置

可在 `koreader/settings.reader.lua` 中调整：

```lua
["windows98_enabled"] = true,
["windows98_titlebar"] = false,  -- 关闭深色标题栏与控件面板
["windows98_shadows"] = false,   -- 关闭窗口硬阴影
```

主题不会替换正文字体。SimpleUI 设置会被备份，停用或卸载时恢复安装前的值。
