# -*- coding: utf-8 -*-
from pyesl.conf import ElasticSearchConfig
from pyesl.response import TsdbResponse
from pyesl.search import ElasticSearchQuery


class SearchClient(object):
    def search(self, query: ElasticSearchQuery, config: ElasticSearchConfig) -> TsdbResponse:
        ElasticSearch()