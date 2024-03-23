"""
bilibili_api.utils.Credential

凭据类，用于各种请求操作的验证。
"""

import uuid
from typing import Union
import urllib.parse

from ..exceptions import (
    CredentialNoBuvid3Exception,
    CredentialNoBiliJctException,
    CredentialNoSessdataException,
    CredentialNoDedeUserIDException,
    CredentialNoAcTimeValueException,
)


class Credential:
    """
    凭据类，用于各种请求操作的验证。
    """

    def __init__(
        self,
        sessdata: Union[str, None] = None,
        bili_jct: Union[str, None] = None,
        buvid3: Union[str, None] = None,
        dedeuserid: Union[str, None] = None,
        ac_time_value: Union[str, None] = None,
        **kwargs
    ) -> None:
        """
        各字段获取方式查看：https://nemo2011.github.io/bilibili-api/#/get-credential.md

        Args:
            sessdata   (str | None, optional): 浏览器 Cookies 中的 SESSDATA 字段值. Defaults to None.

            bili_jct   (str | None, optional): 浏览器 Cookies 中的 bili_jct 字段值. Defaults to None.

            buvid3     (str | None, optional): 浏览器 Cookies 中的 BUVID3 字段值. Defaults to None.

            dedeuserid (str | None, optional): 浏览器 Cookies 中的 DedeUserID 字段值. Defaults to None.

            ac_time_value (str | None, optional): 浏览器 Cookies 中的 ac_time_value 字段值. Defaults to None.

        
        其他 Cookie 参数可以直接填入，优先级低于上述参数。
        """
        self.sessdata = (
            None
            if sessdata is None
            else (
                sessdata if sessdata.find("%") != -1 else urllib.parse.quote(sessdata)
            )
        )
        self.bili_jct = bili_jct
        self.buvid3 = buvid3
        self.dedeuserid = dedeuserid
        self.ac_time_value = ac_time_value

        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_cookies(self) -> dict:
        """
        获取请求 Cookies 字典

        Returns:
            dict: 请求 Cookies 字典
        """
        cookies = {
            "SESSDATA": self.sessdata,
            "buvid3": self.buvid3,
            "bili_jct": self.bili_jct,
            "ac_time_value": self.ac_time_value,
        }
        if self.dedeuserid:
            cookies.update({"DedeUserID": self.dedeuserid})

        # 填入所有其他参数
        for key, value in self.__dict__.items():
            if key not in cookies and value is not None:
                cookies[key] = value
        return cookies

    def has_dedeuserid(self) -> bool:
        """
        是否提供 dedeuserid。

        Returns:
            bool。
        """
        return self.dedeuserid is not None and self.sessdata != ""

    def has_sessdata(self) -> bool:
        """
        是否提供 sessdata。

        Returns:
            bool。
        """
        return self.sessdata is not None and self.sessdata != ""

    def has_bili_jct(self) -> bool:
        """
        是否提供 bili_jct。

        Returns:
            bool。
        """
        return self.bili_jct is not None and self.sessdata != ""

    def has_buvid3(self) -> bool:
        """
        是否提供 buvid3

        Returns:
            bool.
        """
        return self.buvid3 is not None and self.sessdata != ""

    def has_ac_time_value(self) -> bool:
        """
        是否提供 ac_time_value

        Returns:
            bool.
        """
        return self.ac_time_value is not None and self.sessdata != ""

    def raise_for_no_sessdata(self):
        """
        没有提供 sessdata 则抛出异常。
        """
        if not self.has_sessdata():
            raise CredentialNoSessdataException()

    def raise_for_no_bili_jct(self):
        """
        没有提供 bili_jct 则抛出异常。
        """
        if not self.has_bili_jct():
            raise CredentialNoBiliJctException()

    def raise_for_no_buvid3(self):
        """
        没有提供 buvid3 时抛出异常。
        """
        if not self.has_buvid3():
            raise CredentialNoBuvid3Exception()

    def raise_for_no_dedeuserid(self):
        """
        没有提供 DedeUserID 时抛出异常。
        """
        if not self.has_dedeuserid():
            raise CredentialNoDedeUserIDException()

    def raise_for_no_ac_time_value(self):
        """
        没有提供 ac_time_value 时抛出异常。
        """
        if not self.has_ac_time_value():
            raise CredentialNoAcTimeValueException()

    async def check_valid(self):
        """
        检查 cookies 是否有效

        Returns:
            bool: cookies 是否有效
        """

    # def generate_buvid3(self):
    #     """
    #     生成 buvid3
    #     """
    #     self.buvid3 = str(uuid.uuid1()) + "infoc"
    # 长度都不同了...用 credential.get_spi_buvid
