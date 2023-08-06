# -*- coding: utf-8 -*-
from typing import List, Tuple, Union

from elasticsearch import Elasticsearch

from pyesl.conf import ElasticsearchConfig
from pyesl.parser.response import ResponseParser
from pyesl.response import TsdbResponse
from pyesl.search import ElasticsearchQuery


class SearchClient(object):
    def __init__(self, hosts: List[str], http_auth: Union[None, Tuple[str, str]] = None, **params):
        self._config = ElasticsearchConfig(hosts, http_auth=http_auth, **params)

    def search(self, query: ElasticsearchQuery) -> TsdbResponse:
        es = Elasticsearch(**self._config)
        response = es.search(index=query.index, body=query.body, params=query.params)
        return ResponseParser.tsfresp(query, response)

    @property
    def name(self):
        return self._config.name
