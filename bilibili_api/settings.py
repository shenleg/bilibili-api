"""
bilibili_api.settings

这里是配置模块的地方
"""

import logging
from enum import Enum

class HTTPClient(Enum):
    """
    - AioHttp: aiohttp
    - Httpx: httpx
    """

    AIOHTTP = "aiohttp"
    HTTPX = "httpx"

http_client: HTTPClient = HTTPClient.AIOHTTP
"""
用于设置使用的 HTTP 客户端，默认为 Httpx

e.x.:
``` python
from bilibili_api import settings
settings.http_client = settings.HTTPClient.AIOHTTP
```

**Note: 当前模块所有 `Web Socket` 操作强制使用 `aiohttp`**
"""

proxy: str = ""
"""
代理设置

e.x.:
``` python
from bilibili_api import settings
settings.proxy = "https://www.example.com"
```
"""

timeout: float = 5.0
"""
web 请求超时时间设置
"""

geetest_auto_open: bool = True
"""
是否自动打开 geetest 验证窗口
"""

request_log: bool = False
"""
请求 Api 时是否打印 Api 信息
"""

wbi_retry_times: int = 3
"""
WBI请求重试次数上限设置, 默认为3次
"""

logger = logging.getLogger("request")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[Request][%(asctime)s] %(message)s"))
    logger.addHandler(handler)
