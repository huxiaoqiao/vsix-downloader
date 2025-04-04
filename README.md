# VSIX Downloader

一个用于下载 Visual Studio Code 扩展 (VSIX 文件) 的 Python 脚本。

## 用法

1.  确保你已安装 Python。
2.  运行主脚本：

    ```bash
    python main.py
    ```

    (请根据你的实际入口文件和运行方式调整此命令)

## 依赖

在运行此项目前，请先安装所需的依赖：

## 打包为 EXE

你可以使用 PyInstaller 将此脚本打包成一个独立的 Windows 可执行文件 (.exe)。

1.  **安装 PyInstaller:**
    如果尚未安装 PyInstaller，请在终端或命令提示符中运行以下命令：
    ```bash
    pip install pyinstaller
    ```

2.  **执行打包:**
    在项目的根目录下运行以下命令 (确保 `main.py` 是你的主入口文件)：
    ```bash
    pyinstaller --onefile main.py
    ```
    *   `--onefile` 参数会将所有依赖项打包到一个单独的 `.exe` 文件中。
    *   如果你的应用包含图形界面 (如 Tkinter, PyQt 等)，或者需要包含额外的数据文件，可能需要查阅 PyInstaller 的文档以了解更高级的打包选项。

3.  **查找 EXE 文件:**
    打包成功后，你可以在项目根目录下新生成的 `dist` 文件夹中找到 `.exe` 文件。

## 贡献

欢迎提出问题或贡献代码。