# PDFToWordConverter

一个用于将 PDF 按页渲染为图片并写入 Word 文档的 Windows 桌面工具。程序提供 Tkinter 图形界面，支持批量选择 PDF、选择输出目录和调整截图清晰度。

## 功能

- PDF 批量转换为 `.docx`
- 每页 PDF 以图片形式插入 Word
- 支持三档 DPI：`Shot`、`Doc`、`Pic`
- 自动生成不重名的输出文件
- Windows 单文件 exe 发布
- 内置 Poppler，无需业务电脑额外安装 Python 或 Poppler

## 给业务人员使用

从 GitHub Actions 下载最新构建产物：

- Artifact 名称：`PDFToWordConverter-exe`
- 文件名称：`PDFToWordConverter.exe`

下载后直接双击 `PDFToWordConverter.exe` 即可使用。首次启动可能会稍慢，因为单文件 exe 会先解压内置依赖到系统临时目录。

## 界面使用步骤

1. 点击“浏览”选择一个或多个 PDF 文件。
2. 选择输出目录，默认是桌面。
3. 选择 DPI：
   - `Shot`：速度快，清晰度较低
   - `Doc`：默认推荐，清晰度和体积平衡
   - `Pic`：清晰度高，速度较慢，文件较大
4. 点击“开始转换”。
5. 转换完成后，在输出目录中查看生成的 Word 文件。

## 开发环境运行

本项目使用 Python 3.11 开发。

```bash
pip install -r requirements.txt
python main.py
```

macOS 本地开发可以运行源码，但 Windows exe 需要在 Windows 环境构建。当前项目通过 GitHub Actions 在 `windows-latest` runner 上自动打包。

## GitHub Actions 打包

工作流文件：

```text
.github/workflows/build.yml
```

触发方式：

- 手动触发 `workflow_dispatch`
- 推送 `v*` tag

构建产物：

- `PDFToWordConverter-exe`：单文件 Windows exe
- `PDFToWordConverter-exe-sha256`：exe 的 SHA256 校验文件

打包配置文件：

```text
build_spec.spec
```

该配置会将 `poppler/Library` 打进 exe，并在构建时检查以下关键文件是否存在：

- `poppler/Library/bin/pdfinfo.exe`
- `poppler/Library/bin/pdftoppm.exe`

如果 Poppler 缺失，构建会直接失败，避免生成运行时不可用的 exe。

## 项目结构

```text
.
├── .github/workflows/build.yml
├── build_spec.spec
├── main.py
├── poppler/
├── requirements.txt
├── spec/
└── src/
    ├── converter.py
    ├── gui.py
    └── logger.py
```

## 常见问题

### 提示 `Unable to get page count. Is poppler installed and in PATH?`

说明程序运行时没有找到内置 Poppler。请重新从最新 GitHub Actions 构建中下载 `PDFToWordConverter-exe`。

### 单文件 exe 启动比较慢

这是 PyInstaller `onefile` 模式的正常现象。程序启动时会先把依赖解压到临时目录，然后再运行。

### Windows 提示未知发布者或安全提醒

当前 exe 没有做代码签名，Windows SmartScreen 或杀毒软件可能会提示风险。确认来源可信后允许运行即可。

## 依赖

- `pdf2image`
- `Pillow`
- `python-docx`
- `PyInstaller`
- `Poppler for Windows`
