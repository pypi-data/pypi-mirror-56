# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import List, Tuple, Union, Dict

from elasticsearch import Elasticsearch

from pyesl.conf import ElasticsearchConfig
from pyesl.parser.response import ResponseParser
from pyesl.response import TsdbResponse
from pyesl.search import ElasticsearchQuery


class SearchClient(object):
    pool: Dict[str, SearchClient] = {}

    def __init__(self, hosts: List[str], http_auth: Union[None, Tuple[str, str]] = None, **params):
        self._config = ElasticsearchConfig(hosts, http_auth=http_auth, **params)
        self._es = Elasticsearch(**self._config)

    def search(self, query: ElasticsearchQuery) -> TsdbResponse:
        response = self._es.search(index=query.index, body=query.body, params=query.params)
        return ResponseParser.tsfresp(query, response)

    @classmethod
    def from_pool(cls, hosts: List[str], http_auth: Union[None, Tuple[str, str]] = None, **params) -> SearchClient:
        _config = ElasticsearchConfig(hosts, http_auth=http_auth, **params)
        if _config.name in cls.pool:
            return cls.pool[_config.name]
        else:
            ret = SearchClient(**_config)
            cls.pool[_config.name] = ret
            return ret

    @classmethod
    def reset_pool(cls, hosts: List[str], http_auth: Union[None, Tuple[str, str]] = None, **params):
        _config = ElasticsearchConfig(hosts, http_auth=http_auth, **params)
        cls.pool[_config.name] = SearchClient(**_config)

    @property
    def name(self):
        return self._config.name
