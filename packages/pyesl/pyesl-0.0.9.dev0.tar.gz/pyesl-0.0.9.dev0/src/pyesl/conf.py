# -*- coding: utf-8 -*-
from typing import List, Tuple, Union


class ElasticsearchConfig(dict):
    def __init__(
            self, hosts: List[str], maxsize: int = 20, max_retries: int = 2,
            http_auth: Union[Tuple[str, str], None] = None, timeout: int = 60, use_ssl: bool = False,
            verify_certs: bool = False, ca_certs: Union[bytes, str, None] = None, http_compress=True, **kwargs):
        """

        :param hosts: ES的访问地址
        :param maxsize: 连接池大小
        :param max_retries: 重试次数
        :param http_auth: 用户名:密码，either ‘:’ separated string or a tuple
        :param timeout: 访问超时时间，默认default timeout in seconds (float, default: 10) 这里设置 60
        :param use_ssl: use ssl for the connection if True
        :param verify_certs: whether to verify SSL certificates
        :param ca_certs: optional path to CA bundle
        :param http_compress: When using capacity-constrained networks (low throughput), This is especially useful when
            doing bulk loads or inserting large documents. This will configure compression on the request
        :param kwargs: 其他更多的参数
        """
        hosts = sorted(set(hosts))
        self._name = '#'.join(hosts)
        super().__init__(
            hosts=hosts, maxsize=maxsize, max_retries=max_retries, http_auth=http_auth, timeout=timeout,
            use_ssl=use_ssl, verify_certs=verify_certs, ca_certs=ca_certs, http_compress=http_compress, **kwargs)

    @property
    def name(self) -> str:
        return self._name
