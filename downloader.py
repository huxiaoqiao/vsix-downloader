"""
处理 VSCode 插件下载的核心逻辑
"""

import requests
import tkinter as tk
from tkinter import filedialog
from urllib.parse import urlparse, parse_qs
import os
from utils import validate_version, validate_marketplace_url

def download_vsix(url, version, status_callback, progress_callback=None):
    """
    下载 VSCode 插件的 VSIX 文件。

    Args:
        url (str): VSCode Marketplace 插件页面的 URL。
        version (str): 要下载的插件版本号 ('latest' 或 x.y.z 格式)。
        status_callback (function): 用于更新状态信息的函数，接收一个字符串参数。
        progress_callback (function, optional): 用于更新下载进度的函数，接收一个 0-100 的整数。
                                                Defaults to None.
    """
    status_callback("开始处理...")

    # 1. 验证 URL 和版本号
    if not validate_marketplace_url(url):
        status_callback("错误：无效的 Marketplace URL 格式。")
        return
    if not validate_version(version):
        status_callback(f"错误：无效的版本号格式 '{version}'。请使用 'latest' 或 'x.y.z'。")
        return

    try:
        # 2. 解析 URL 获取 itemName
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        item_name = query_params.get('itemName', [None])[0]

        if not item_name:
            status_callback("错误：无法从 URL 中解析出 itemName。")
            return

        # 3. 提取 fieldA 和 fieldB
        parts = item_name.split('.')
        if len(parts) != 2:
            status_callback(f"错误：无法将 itemName '{item_name}' 分割为两部分。")
            return
        field_a, field_b = parts

        # 4. 构建下载 URL
        # 格式: https://marketplace.visualstudio.com/_apis/public/gallery/publishers/{fieldA}/vsextensions/{fieldB}/{version}/vspackage
        download_url = f"https://marketplace.visualstudio.com/_apis/public/gallery/publishers/{field_a}/vsextensions/{field_b}/{version}/vspackage"
        status_callback(f"准备下载: {item_name} 版本: {version}")

        # 5. 弹出文件保存对话框
        default_filename = f"{field_b}-{version}.vsix"
        save_path = filedialog.asksaveasfilename(
            defaultextension=".vsix",
            initialfile=default_filename,
            title="保存 VSIX 文件",
            filetypes=[("VSIX 文件", "*.vsix"), ("所有文件", "*.*")]
        )

        if not save_path:
            status_callback("用户取消了保存操作。")
            return

        # 6. 下载执行 (流式)
        status_callback(f"正在下载到: {os.path.basename(save_path)}")
        response = requests.get(download_url, stream=True, timeout=30) # 增加超时
        response.raise_for_status()  # 如果状态码不是 2xx，则抛出 HTTPError

        total_size = int(response.headers.get('content-length', 0))
        bytes_downloaded = 0
        chunk_size = 8192 # 8KB

        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    bytes_downloaded += len(chunk)
                    if total_size > 0 and progress_callback:
                        percent = int((bytes_downloaded / total_size) * 100)
                        progress_callback(percent)
                    # 可以在这里加一个小的状态更新，但可能过于频繁
                    # status_callback(f"下载中... {bytes_downloaded / (1024*1024):.2f} MB")

        if progress_callback: # 确保最后是100%
             progress_callback(100)
        status_callback(f"下载完成: {os.path.basename(save_path)}")

    except requests.exceptions.RequestException as e:
        status_callback(f"网络错误: {e}")
    except requests.exceptions.HTTPError as e:
         if e.response.status_code == 404:
             status_callback(f"错误：找不到插件 '{item_name}' 的版本 '{version}'。请检查版本号或使用 'latest'。")
         else:
             status_callback(f"HTTP 错误: {e}")
    except IOError as e:
        status_callback(f"文件保存错误: {e}")
    except Exception as e:
        status_callback(f"发生未知错误: {e}")

if __name__ == '__main__':
    # 这个部分仅用于直接运行 downloader.py 进行测试，需要手动创建 Tkinter root
    # 在实际应用中，这个文件会被 main.py 导入和调用

    def dummy_status(msg):
        print(f"Status: {msg}")

    def dummy_progress(percent):
        print(f"Progress: {percent}%")

    # 需要一个 Tkinter 根窗口来弹出文件对话框
    root = tk.Tk()
    root.withdraw() # 隐藏主窗口

    test_url = "https://marketplace.visualstudio.com/items?itemName=ms-python.python"
    test_version = "latest" # 或者一个具体的版本号 "2023.20.0"

    print(f"测试下载: URL={test_url}, Version={test_version}")
    # 注意：直接运行会弹出文件保存对话框
    # download_vsix(test_url, test_version, dummy_status, dummy_progress)

    print("\n测试无效 URL:")
    download_vsix("invalid-url", "latest", dummy_status, dummy_progress)

    print("\n测试无效版本:")
    download_vsix(test_url, "invalid-version", dummy_status, dummy_progress)

    print("\n测试不存在的版本:")
    download_vsix(test_url, "0.0.0", dummy_status, dummy_progress)


    # root.mainloop() # 如果需要保持窗口以查看对话框，取消注释这行
    # 但是通常测试不需要 mainloop
    root.destroy() # 测试完成后销毁窗口