"""
辅助工具函数模块
"""

# 可以在此添加如 URL 验证、版本号验证等辅助函数
# 目前保持为空

def validate_version(version):
  """
  简单的版本号验证 (示例)
  实际可能需要更复杂的正则或逻辑
  """
  # 允许 'latest' 或类似 x.y.z 的格式
  if version.lower() == 'latest':
    return True
  parts = version.split('.')
  if len(parts) == 3 and all(part.isdigit() for part in parts):
    return True
  return False

def validate_marketplace_url(url):
    """
    简单的 VSCode Marketplace URL 验证 (示例)
    """
    from urllib.parse import urlparse
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'],
                    result.netloc == 'marketplace.visualstudio.com',
                    '/items' in result.path,
                    'itemName=' in result.query])
    except ValueError:
        return False

if __name__ == '__main__':
    # 简单测试
    print(validate_version("1.2.3"))
    print(validate_version("latest"))
    print(validate_version("1.a.3"))
    print(validate_marketplace_url("https://marketplace.visualstudio.com/items?itemName=ms-python.python"))
    print(validate_marketplace_url("invalid-url"))
    print(validate_marketplace_url("https://example.com/items?itemName=ms-python.python"))