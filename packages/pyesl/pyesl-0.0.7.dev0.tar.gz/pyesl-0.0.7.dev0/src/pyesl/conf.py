# -*- coding: utf-8 -*-
from typing import List, Tuple, Union


class ElasticsearchConfig(dict):
    def __init__(
            self, hosts: List[str], maxsize: int = 20, max_retries: int = 2,
            http_auth: Union[Tuple[str, str], None] = None, timeout: int = 60, use_ssl: bool = False,
            verify_certs: bool = False, ca_certs: Union[bytes, str, None] = None, **kwargs):
        """

        :param hosts:
        :param maxsize:
        :param max_retries:
        :param http_auth:
        :param timeout:
        :param use_ssl:
        :param verify_certs:
        :param ca_certs:
        :param kwargs:
        """
        hosts = sorted(set(hosts))
        self._name = '#'.join(hosts)
        super().__init__(
            hosts=hosts, maxsize=maxsize, max_retries=max_retries, http_auth=http_auth, timeout=timeout,
            use_ssl=use_ssl, verify_certs=verify_certs, ca_certs=ca_certs, **kwargs)

    @property
    def name(self) -> str:
        return self._name
