"""
使用 Tkinter 构建 VSCode 插件下载器的用户界面
"""

import tkinter as tk
from tkinter import ttk # 使用 themed widgets 获得更好看的外观
import webbrowser

class DownloaderUI:
    """
    管理下载器 UI 元素的类
    """
    def __init__(self, master, download_callback):
        """
        初始化 UI 界面。

        Args:
            master: Tkinter 的根窗口或父容器。
            download_callback: 当点击下载按钮时调用的函数。
                               此回调函数应接收 URL 和版本作为参数。
        """
        self.master = master
        self.download_callback = download_callback
        master.title("VSCode 插件下载器")
        master.geometry("500x250") # 设置初始窗口大小

        # --- UI 元素 ---
        # 使用 Frame 来组织布局
        main_frame = ttk.Frame(master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # URL 输入
        ttk.Label(main_frame, text="插件市场 URL:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        # 示例 URL 提示
        self.url_entry.insert(0, "") # 清空默认值

        # 版本输入
        ttk.Label(main_frame, text="版本号 (e.g., 1.0.0):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.version_entry = ttk.Entry(main_frame, width=20)
        self.version_entry.grid(row=1, column=1, sticky=tk.W, pady=2)
        self.version_entry.insert(0, "") # 清空默认值

        # 下载按钮
        self.download_button = ttk.Button(main_frame, text="下载 VSIX", command=self._on_download_click)
        self.download_button.grid(row=2, column=1, sticky=tk.E, pady=10)

        # 状态标签
        self.status_label = ttk.Label(main_frame, text="状态：准备就绪", wraplength=480) # wraplength 自动换行
        self.status_label.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)

        # 进度条 (可选，但推荐)
        self.progress_bar = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Marketplace 链接
        link_label = ttk.Label(main_frame, text="访问 VSCode Marketplace", foreground="blue", cursor="hand2")
        link_label.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=10)
        link_label.bind("<Button-1>", lambda e: self._open_marketplace())

        # 配置列权重使输入框可伸缩
        main_frame.columnconfigure(1, weight=1)

    def _on_download_click(self):
        """处理下载按钮点击事件"""
        url = self.get_url()
        version = self.get_version()
        # 禁用按钮防止重复点击
        self.download_button.config(state=tk.DISABLED)
        # 重置进度条
        self.update_progress(0)
        # 调用外部传入的回调函数
        self.download_callback(url, version)
        # 注意：下载完成后需要重新启用按钮，这应该在 download_callback 逻辑中处理
        # 或者通过 status_callback 的特定消息来触发

    def _open_marketplace(self):
        """打开 Marketplace 网站"""
        webbrowser.open_new(r"https://marketplace.visualstudio.com/")

    # --- 公共方法 ---
    def get_url(self):
        """获取 URL 输入框的内容"""
        return self.url_entry.get().strip()

    def get_version(self):
        """获取版本号输入框的内容"""
        return self.version_entry.get().strip()

    def update_status(self, message):
        """更新状态标签的文本"""
        self.status_label.config(text=f"状态：{message}")
        # 如果下载完成或出错，重新启用按钮
        if "完成" in message:
            # 下载成功，重置 UI
            self.url_entry.delete(0, tk.END)
            self.version_entry.delete(0, tk.END)
            self.status_label.config(text="状态：准备就绪") # 直接设置初始状态
            self.update_progress(0) # 重置进度条
            self.download_button.config(state=tk.NORMAL) # 重新启用按钮
        elif "错误" in message or "取消" in message:
             # 下载失败或取消，只重新启用按钮
             self.download_button.config(state=tk.NORMAL)
        self.master.update_idletasks() # 强制更新 UI

    def update_progress(self, percent):
        """更新进度条的值"""
        self.progress_bar['value'] = percent
        self.master.update_idletasks() # 强制更新 UI

# --- 用于独立测试 UI ---
if __name__ == '__main__':
    root = tk.Tk()

    def test_download_callback(url, version):
        print(f"模拟下载请求: URL='{url}', Version='{version}'")
        # 模拟下载过程
        import time
        app.update_status(f"正在处理 {url}...")
        app.update_progress(10)
        time.sleep(1)
        app.update_progress(50)
        app.update_status("正在下载...")
        time.sleep(2)
        app.update_progress(100)
        app.update_status("模拟下载完成!") # 这会重新启用按钮

    app = DownloaderUI(root, test_download_callback)
    root.mainloop()