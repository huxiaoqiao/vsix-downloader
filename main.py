"""
VSCode 插件下载器主程序入口
"""

import tkinter as tk
import threading
from ui import DownloaderUI
from downloader import download_vsix

def start_download_thread(url, version, ui_instance):
    """
    在单独的线程中启动下载过程，以避免阻塞 UI。

    Args:
        url (str): 插件市场 URL。
        version (str): 插件版本。
        ui_instance (DownloaderUI): UI 类的实例，用于回调。
    """
    # 使用 lambda 确保在线程中正确调用 download_vsix
    # 并传递 UI 的更新方法作为回调
    download_thread = threading.Thread(
        target=download_vsix,
        args=(url, version, ui_instance.update_status, ui_instance.update_progress),
        daemon=True # 设置为守护线程，这样主程序退出时线程也会结束
    )
    download_thread.start()

def main():
    """
    主函数：创建 UI 并启动 Tkinter 事件循环。
    """
    root = tk.Tk()

    # 创建 UI 实例，并将启动下载线程的函数作为回调传递
    # DownloaderUI 的 download_callback 现在会调用 start_download_thread
    app = DownloaderUI(root, lambda url, ver: start_download_thread(url, ver, app))

    root.mainloop()

if __name__ == "__main__":
    main()