__all__ = (
    'ServerChanNotifier',
)

import time
from typing import Optional

import requests

from .base import *
from ..constant import *


class ServerChanNotifier(INotifier):
    PLATFORM_NAME = 'Server 酱'

    def __init__(self, *, sckey: str, sess: requests.Session):
        """
        :param sckey: Server 酱的 API Token
        :param sess: requests 的 Session 实例
        """
        self._sckey = sckey
        self._sess = sess

    def notify(self, *, success: bool, msg: Optional[str]) -> None:
        """发送消息。"""

        # Server 不允许短时间重复发送相同内容，故加上时间
        time_str = str(int(time.time()))[-3:]

        if success:
            title = '成功'
            if msg is not None:
                body = f'**成功：**服务器的返回是：\n\n```\n{msg}\n```'
            else:
                body = '**成功**'
        else:
            title = '失败'
            if msg is not None:
                body = f'**失败：**产生如下异常：\n\n```\n{msg}\n```'
            else:
                body = '**失败**'

        # 调用 Server 酱接口发送消息
        sc_res_raw = self._sess.post(
            f'https://sctapi.ftqq.com/{self._sckey}.send',
            data={
                'text': f'bupt_ncov_report运行{title}',
                'desp': f'({time_str}) {body}',
            },
            timeout=TIMEOUT_SECOND,
        )

        # 处理可能出现的异常情况
        try:
            sc_res = sc_res_raw.json()
        except:
            raise RuntimeError(
                f'Server 酱的返回值不能解析为 JSON，可能您的 SCKEY 配置有误。'
                f'API 的返回是：\n{sc_res_raw.text}\n您输入的 SCKEY 为\n{self._sckey}'
            )

        errno = sc_res.get('data')['errno']
        if errno != 0:
            raise RuntimeError(
                f'Server 酱调用失败，可能您的 SCKEY 配置有误。API 的返回是：\n{sc_res}\n'
                f'您输入的 SCKEY 为\n{self._sckey}')
