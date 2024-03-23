"""
bilibili_api.login_func

登录功能相关
"""

import enum
import threading
from typing import Tuple, Union

from . import login
from .utils.utils import get_api
from .exceptions import LoginError
import urllib.parse
from .utils.picture import Picture
from .utils.credential import Credential

API = get_api("login")


class QrCodeLoginEvents(enum.Enum):
    """
    二维码登录状态枚举

    + SCAN: 未扫描二维码
    + CONF: 未确认登录
    + TIMEOUT: 二维码过期
    + DONE: 成功
    """

    SCAN = "scan"
    CONF = "confirm"
    TIMEOUT = "timeout"
    DONE = "done"


def get_qrcode() -> Tuple[Picture, str]:
    """
    获取二维码及登录密钥（后面有用）

    Returns:
        Tuple[Picture, str]: 第一项是二维码图片地址（本地缓存）和登录密钥。登录密钥需要保存。
    """
    login_data = login.update_qrcode_data()
    login_key = login_data["qrcode_key"]
    img = login.make_qrcode(login_data["url"])
    return (Picture.from_file(img), login_key)


def check_qrcode_events(login_key: str) -> Tuple[QrCodeLoginEvents, Union[str, Credential]]:
    """
    检查登录状态。（建议频率 1s，这个 API 也有风控！）

    Args:
        login_key (str): 登录密钥（get_qrcode 的返回值第二项)

    Returns:
        Tuple[QrCodeLoginEvents, str|Credential]: 状态(第一项）和信息（第二项）（如果成功登录信息为凭据类）
    """
    events = login.login_with_key(login_key)

    if events["code"] == 86101:
        return QrCodeLoginEvents.SCAN, events["message"]
    elif events["code"] == 86090:
        return QrCodeLoginEvents.CONF, events["message"]
    elif events["code"] == 86038:
        return QrCodeLoginEvents.TIMEOUT, events["message"]
    elif events["code"] == 0:
        url: str = events["url"]
        cookies_list = url.split("?")[1].split("&")
        sessdata = ""
        bili_jct = ""
        dede = ""
        for cookie in cookies_list:
            if cookie[:8] == "SESSDATA":
                sessdata = cookie[9:]
            if cookie[:8] == "bili_jct":
                bili_jct = cookie[9:]
            if cookie[:11].upper() == "DEDEUSERID=":
                dede = cookie[11:]
        c = Credential(sessdata, bili_jct, dedeuserid=dede)
        return QrCodeLoginEvents.DONE, c
    else:
        raise LoginError(events["message"])


def get_tv_qrcode() -> Tuple[Picture, str]:
    """
    获取 TV 端登录二维码及登录密钥（后面有用）

    Returns:
        Tuple[Picture, str]: 第一项是二维码图片地址（本地缓存）和登录密钥。登录密钥需要保存。
    """
    qrcode_data = login.update_tv_qrcode_data()
    qrcode_url = qrcode_data["url"]
    auth_code = qrcode_data["auth_code"]
    img = login.make_qrcode(qrcode_url)
    return (Picture.from_file(img), auth_code)


def check_tv_qrcode_events(auth_code: str) -> Tuple[QrCodeLoginEvents, Union[str, Credential]]:
    """
    检查登录状态。

    Args:
        auth_code (str): 登录密钥

    Returns:
        Tuple[QrCodeLoginEvents, str|Credential]: 状态(第一项）和信息（第二项）（如果成功登录信息为凭据类）
    """
    events = login.verify_tv_login_status(auth_code=auth_code)

    if events["code"] == 86039:
        return QrCodeLoginEvents.SCAN, events["message"]
    elif events["code"] == 86038:
        return QrCodeLoginEvents.TIMEOUT, events["message"]
    elif events["code"] == 0:
        c = login.parse_tv_resp(events["data"])
        return QrCodeLoginEvents.DONE, c
    else:
        raise LoginError(events["message"])


def start_geetest_server() -> "ServerThreadModel":
    """
    验证码服务打开服务器

    Returns:
        ServerThread: 服务进程，将自动开启

    返回值内函数及属性:
        (继承：threading.Thread)
        - url   (str)     : 验证码服务地址
        - start (Callable): 开启进程
        - stop  (Callable): 结束进程

    ``` python
    print(start_geetest_server().url)
    ```
    """
    return login.start_server()  # type: ignore


def close_geetest_server() -> None:
    """
    关闭极验验证服务（打开极验验证服务后务必关闭掉它，否则会卡住）
    """
    return login.close_server()


def done_geetest() -> bool:
    """
    检查是否完成了极验验证。

    如果没有完成极验验证码就开始短信登录发送短信，那么可能会让你的项目卡住。

    Returns:
        bool: 是否完成极验验证
    """
    result = login.get_result()
    if result != -1:
        return True
    else:
        return False


def safecenter_start_geetest_server() -> "ServerThreadModel":
    """
    登录验证专用函数：验证码服务打开服务器

    Returns:
        ServerThread: 服务进程，将自动开启

    返回值内函数及属性:
        (继承：threading.Thread)
        - url   (str)     : 验证码服务地址
        - start (Callable): 开启进程
        - stop  (Callable): 结束进程

    ``` python
    print(start_geetest_server().url)
    ```
    """
    return login.safecenter_start_server()  # type: ignore


def safecenter_close_geetest_server() -> None:
    """
    登录验证专用函数：关闭极验验证服务（打开极验验证服务后务必关闭掉它，否则会卡住）
    """
    return login.safecenter_close_server()


def safecenter_done_geetest() -> bool:
    """
    登录验证专用函数：检查是否完成了极验验证。

    如果没有完成极验验证码就开始短信登录发送短信，那么可能会让你的项目卡住。

    Returns:
        bool: 是否完成极验验证
    """
    result = login.safecenter_get_result()
    if result != -1:
        return True
    else:
        return False


COUNTRIES_LIST = login.get_countries_list()
countries_list = COUNTRIES_LIST


class ServerThreadModel(threading.Thread):
    """
    A simple model for bilibili_api.utils.captcha._start_server.ServerThread.
    """

    url: str

    def __init__(self, *args, **kwargs):
        ...

    def stop(self):
        """Stop the server and this thread nicely"""
