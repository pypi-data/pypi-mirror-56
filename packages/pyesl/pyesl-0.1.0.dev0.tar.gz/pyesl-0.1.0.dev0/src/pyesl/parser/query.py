# -*- coding: utf-8 -*-
from collections import OrderedDict
from typing import List, Union, Dict

from pyesl.aggs import FieldCalculation, QueryCalculation, ResultCalculation, Aggregations, Calculations, \
    Groupby, Step
from pyesl.errors import ParamError
from pyesl.field import ScriptFields, SourceFields, Field, ScriptField
from pyesl.query import Condition, PositiveCondition, NegativeCondition, Terms, ConditionGroup, QuerySorts, Sort, \
    Query, RangeCondition
from pyesl.search import ElasticsearchQuery


class QueryParser(object):

    @staticmethod
    def single_aggs(
            fields: Dict[str, str], func: str = 'sum', metric: str = 'cpu', expr: Union[None, str] = None,
            filters: Terms = None) -> FieldCalculation:
        """
        **生成单个metric的N个field之间聚合运算语句块**

        :param fields: 运算所需的字段
        :type fields: Dict[str, str]
        :param func: 聚合方法
        :type func: str
        :param metric: 聚合的metric
        :type metric: str
        :param expr: field之间的运算如:'({name1} + {name2}) /2.0'
        :type expr: Union[None, str]
        :param filters: 过滤条件
        :type filters: Terms
        :return: 聚合运算语句块
        :rtype: FieldCalculation

        - For Case::

            sum(ms_gb_distinct.count + ms_gb_distinct.distinctcount / 2, hostname!~'mgb.*')

        - Example::

            cnd3 = QueryParser.single_filter(tag_name='hostname', value_pattern='mgb.*', op='!~')
            terms = QueryParser.group_filter(cnd3, relation='and')
            aggs = QueryParser.single_aggs(
                fields={'name1': 'ms_gb_distinct.count', 'name2': 'ms_gb_distinct.distinctcount'}, func='sum',
                metric='ms_gb_distinct', expr='{name1} + {name2} / 2', filters=terms)



        - ES Body::

            {
                "filter_sum_{name1} + {name2} / 2": {
                    "aggs": {
                        "sum_{name1} + {name2} / 2": {
                            "sum": {
                                "script": {
                                    "source": "doc['field.count'].value + doc['field.distinctcount'].value / 2"
                                }
                            }
                        }
                    },
                    "filter": {
                        "bool": {
                            "filter": [{
                                "bool": {
                                    "filter": [{
                                        "term": {
                                            "metric": {
                                                "value": "ms_gb_distinct"
                                            }
                                        }
                                    }],
                                    "should": [],
                                    "minimum_should_match": 0
                                }
                            }, {
                                "bool": {
                                    "filter": [{
                                        "bool": {
                                            "must_not": {
                                                "regexp": {
                                                    "tag.hostname": {
                                                        "value": "mgb.*"
                                                    }
                                                }
                                            }
                                        }
                                    }],
                                    "should": [],
                                    "minimum_should_match": 0
                                }
                            }],
                            "should": [],
                            "minimum_should_match": 0
                        }
                    }
                }
            }

        """
        _fields = {}
        for alias_name, metric_field in fields.items():
            if '.' in metric_field:
                metric_name, field_name = metric_field.split('.', 1)
            else:
                metric_name = metric_field
                field_name = 'value'
            if metric != metric_name:
                raise ParamError('field: {} is not field of {}'.format(metric_field, metric))
            else:
                _fields[alias_name] = field_name
        _pc = PositiveCondition(op='term', name='metric', value=metric)
        _filters = Terms(filter=ConditionGroup(_pc, relation='filter'))
        if filters:
            _filters.add_terms(filters, relation='filter')
        _qc = QueryCalculation(fields=_fields, expr=expr, func=func, terms=_filters)
        return _qc

    @staticmethod
    def aggs_cal(expr: str, **calculations: FieldCalculation) -> Calculations:
        """
        **聚合运算结果之间的四则运算**

        :param expr: 聚合运算结果之间的四则运算四则运算表达式
        :type expr: str
        :param calculations: 聚合运算语句块
        :type calculations: FieldCalculation
        :return: 聚合运算和其结果之间的四则运算语句块合集
        :rtype: Calculations

        - Foc Case::

            (
                count(( ms_gb_distinct.count + ms_gb_distinct.distinctcount ) / 2)
                +
                max(logstash_node_pipeline_events_in_total)
            ) * 3

        - Example::

            aggs1 = QueryParser.single_aggs(
                fields={
                    'name1': 'ms_gb_distinct.count', 'name2': 'ms_gb_distinct.distinctcount'
                }, func='value_count', metric='ms_gb_distinct',
                expr='( {name1} + {name2} ) / 2')
            print(json.dumps(aggs1.body))

            aggs2 = QueryParser.single_aggs(
                fields={
                    'name1': 'logstash_node_pipeline_events_in_total'},
                func='max', metric='logstash_node_pipeline_events_in_total'
            )
            print(json.dumps(aggs2.body))

            aggs_cal = QueryParser.aggs_cal(
                '({name1} + {name2}) * 3', name1=aggs1, name2=aggs2)

        - ES Body::

            {
                "aggs": {
                    "bucket_script_({name1} + {name2}) * 3": {
                        "bucket_script": {
                            "buckets_path": {
                                "name1": "filter_value_count_( {name1} + {name2} ) / 2>value_count_( {name1} + {name2} ) / 2",
                                "name2": "filter_max_('name1')>max_('name1')"
                            },
                            "script": {
                                "source": "(params.name1 + params.name2) * 3"
                            }
                        }
                    },
                    "filter_value_count_( {name1} + {name2} ) / 2": {
                        "aggs": {
                            "value_count_( {name1} + {name2} ) / 2": {
                                "value_count": {
                                    "script": {
                                        "source": "( doc['field.count'].value + doc['field.distinctcount'].value ) / 2"
                                    }
                                }
                            }
                        },
                        "filter": {
                            "bool": {
                                "filter": [{
                                    "term": {
                                        "metric": {
                                            "value": "ms_gb_distinct"
                                        }
                                    }
                                }],
                                "should": [],
                                "minimum_should_match": 0
                            }
                        }
                    },
                    "filter_max_('name1')": {
                        "aggs": {
                            "max_('name1')": {
                                "max": {
                                    "field": "field.value"
                                }
                            }
                        },
                        "filter": {
                            "bool": {
                                "filter": [{
                                    "term": {
                                        "metric": {
                                            "value": "logstash_node_pipeline_events_in_total"
                                        }
                                    }
                                }],
                                "should": [],
                                "minimum_should_match": 0
                            }
                        }
                    }
                }
            }

        """
        cals = list(calculations.values())
        result_cal = ResultCalculation(calculation=calculations, expr=expr)
        cals.append(result_cal)
        return Calculations(*cals, return_calculation_name=result_cal.name)

    @staticmethod
    def aggs_by_within(
            calculation: Union[FieldCalculation, Calculations],
            groupby: List[str] = None, step_s: Union[int, None] = None,
            groupby_size: Union[int, None] = None) -> Aggregations:
        """
        **聚合语句块(合集)加上groupby和within语义**

        :param calculation: 聚合运算语句块合集 或者 聚合运算语句块
        :type calculation: Union[FieldCalculation, Calculations]
        :param groupby: 分组的tag字段
        :type groupby: List[str]
        :param step_s: 按时间分组的步长,单位:秒
        :type step_s: Union[int, None]
        :param groupby_size: 分组统计最大分组数量
        :type groupby_size: Union[int, None]
        :return: 完整的聚合统计语句块
        :rtype: Aggregations

        - Foc Case::

            (
                sum(ms_gb_distinct.count + ms_gb_distinct.distinctcount / 2, hostname!~'mga.*')
                +
                avg(ms_gb_distinct.count)
            ) * 3
            group by gameid, url
            within 3600s

        - Example::

            aggs2 = QueryParser.single_aggs(
                fields={'name1': 'ms_gb_distinct.count'}, func='avg', metric='ms_gb_distinct')
            cnd3 = QueryParser.single_filter(tag_name='hostname', value_pattern='mga.*', op='!~')
            terms = QueryParser.group_filter(cnd3, relation='and')
            new_aggs1 = QueryParser.single_aggs(
                fields={'name1': 'ms_gb_distinct.count', 'name2': 'ms_gb_distinct.distinctcount'}, func='sum',
                metric='ms_gb_distinct', filters=terms,
                expr='{name1} + {name2} / 2')
            new_aggs_cal = QueryParser.aggs_cal(
                '({name1} + {name2}) * 3', name1=new_aggs1, name2=aggs2)
            aggs_final4 = QueryParser.aggs_by_within(new_aggs_cal, groupby=['gameid', 'url'], step_s=3600)
            self.assertEqual(
                aggs_final4.body['aggs']['tag.gameid']['aggs']['tag.url']['aggs']['ts']['aggs'],
                new_aggs_cal.body['aggs'])

        - ES Body::

            {
                "aggs": {
                    "tag.gameid": {
                        "terms": {
                            "field": "tag.gameid",
                            "size": 512.0
                        },
                        "aggs": {
                            "tag.url": {
                                "terms": {
                                    "field": "tag.url",
                                    "size": 1024.0
                                },
                                "aggs": {
                                    "ts": {
                                        "date_histogram": {
                                            "field": "ts",
                                            "fixed_interval": "3600s"
                                        },
                                        "aggs": {
                                            "filter_sum_{name1} + {name2} / 2": {
                                                "aggs": {
                                                    "sum_{name1} + {name2} / 2": {
                                                        "sum": {
                                                            "script": {
                                                                "source": "doc['field.count'].value + doc['field.distinctcount'].value / 2"
                                                            }
                                                        }
                                                    }
                                                },
                                                "filter": {
                                                    "bool": {
                                                        "filter": [{
                                                            "bool": {
                                                                "filter": [{
                                                                    "term": {
                                                                        "metric": {
                                                                            "value": "ms_gb_distinct"
                                                                        }
                                                                    }
                                                                }],
                                                                "should": [],
                                                                "minimum_should_match": 0
                                                            }
                                                        }, {
                                                            "bool": {
                                                                "filter": [{
                                                                    "bool": {
                                                                        "must_not": {
                                                                            "regexp": {
                                                                                "tag.hostname": {
                                                                                    "value": "mga.*"
                                                                                }
                                                                            }
                                                                        }
                                                                    }
                                                                }],
                                                                "should": [],
                                                                "minimum_should_match": 0
                                                            }
                                                        }],
                                                        "should": [],
                                                        "minimum_should_match": 0
                                                    }
                                                }
                                            },
                                            "filter_avg_('name1')": {
                                                "aggs": {
                                                    "avg_('name1')": {
                                                        "avg": {
                                                            "field": "field.count"
                                                        }
                                                    }
                                                },
                                                "filter": {
                                                    "bool": {
                                                        "filter": [{
                                                            "term": {
                                                                "metric": {
                                                                    "value": "ms_gb_distinct"
                                                                }
                                                            }
                                                        }],
                                                        "should": [],
                                                        "minimum_should_match": 0
                                                    }
                                                }
                                            },
                                            "bucket_script_({name1} + {name2}) * 3": {
                                                "bucket_script": {
                                                    "buckets_path": {
                                                        "name1": "filter_sum_{name1} + {name2} / 2>sum_{name1} + {name2} / 2",
                                                        "name2": "filter_avg_('name1')>avg_('name1')"
                                                    },
                                                    "script": {
                                                        "source": "(params.name1 + params.name2) * 3"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        """
        if isinstance(calculation, Calculations):
            calculations = calculation
        else:
            calculations = Calculations(calculation)
        _groupbys = []
        if groupby_size:
            groupby_size = max(groupby_size, 1)
        if groupby:
            glen = len(groupby)
            for idx, _g in enumerate(groupby):
                size = groupby_size or max(1, 1024 / 2 ** (glen - idx - 1))
                _groupbys.append(Groupby(field='tag.{}'.format(_g), size=size))
        if step_s:
            _step = Step(step_s=step_s)
        else:
            _step = None
        return Aggregations(calculations=calculations, groupby=_groupbys, step=_step)

    @staticmethod
    def where_filters(
            metrics: List[str], filters: Terms,
            script_fields: Union[ScriptFields, None] = None, source_fields: Union[SourceFields, None] = None,
            aggregations: Union[Aggregations, None] = None,
            request_cache: bool = True, pre_filter_shard_size: int = 1, track_total_hits: bool = False,
            filter_path: str = 'hits.hits._source,hits.hits.fields,hits.total,took,_shards,aggregations',
            offset: int = 0, size: int = 0
    ) -> ElasticsearchQuery:
        """
        **给入指标名字，查询字段，聚合语句块，过滤语句块，指标列表等信息生成ES的查询语句块**

        :param metrics: 指标名字数组
        :type metrics: List[str]
        :param filters: 过滤条件集合
        :type filters: Terms
        :param script_fields: 别名字段
        :type script_fields: Union[ScriptFields, None]
        :param source_fields: 原字段
        :type source_fields: Union[SourceFields, None]
        :param aggregations: 完整的聚合统计语句块
        :type aggregations: Union[Aggregations, None]
        :param request_cache: 请求参数,是否缓存查询结果
        :type request_cache: bool
        :param pre_filter_shard_size: 请求参数,是否预查询shards过滤掉没有相关数据的shards
        :type pre_filter_shard_size: int
        :param track_total_hits: 是否统计并返回查询的有效记录条目数
        :type track_total_hits: bool
        :param filter_path: 返回的必要信息
        :type filter_path: str
        :param offset: 原始查询返回结果的起点位置
        :type offset: int
        :param size: 原始查询返回结果每页的返回数量
        :type size: int
        :return: 完整的Elasticsearch查询结构
        :rtype: ElasticsearchQuery

        - Foc Case::

            (
                sum(ms_gb_distinct.count + ms_gb_distinct.distinctcount / 2, hostname!~'mga.*')
                +
                avg(ms_gb_distinct.count)
            ) * 3
            group by gameid, url
            within 3600s
            where metric='ms_gb_distinct' AND code!='200' AND hostname~'mgb.*' AND ip!~'localhost.*'
                AND ts>'2019-11-15T00:00:00+08:00' AND ts<='2019-11-17T07:00:00+08:00'

        - Example::

            # 生成过滤条件
            # 指标名
            cnd1 = QueryParser.single_filter(tag_name='metric', value_pattern='ms_gb_distinct', op='=')
            # tag名
            cnd2 = QueryParser.single_filter(tag_name='code', value_pattern='200', op='!=')
            cnd3 = QueryParser.single_filter(tag_name='hostname', value_pattern='mgb.*', op='~')
            cnd4 = QueryParser.single_filter(tag_name='ip', value_pattern='localhost.*', op='!~')
            # 时间范围
            cnd5 = QueryParser.single_filter(tag_name='ts', value_pattern='2019-11-15T00:00:00+08:00', op='>')
            cnd8 = QueryParser.single_filter(tag_name='ts', value_pattern='2019-11-17T07:00:00+08:00', op='<=')
            # 条件组合
            terms = QueryParser.group_filter(cnd1, cnd2, cnd3, cnd4, cnd5, cnd6, cnd7, cnd8, relation='and')

            # 生成聚合语句块
            cnd3 = QueryParser.single_filter(tag_name='hostname', value_pattern='mga.*', op='!~')
            terms1 = QueryParser.group_filter(cnd3, relation='and')
            new_aggs1 = QueryParser.single_aggs(
                fields={'name1': 'ms_gb_distinct.count', 'name2': 'ms_gb_distinct.distinctcount'}, func='sum',
                metric='ms_gb_distinct', filters=terms1,
                expr='{name1} + {name2} / 2')
            aggs2 = QueryParser.single_aggs(
                fields={'name1': 'ms_gb_distinct.count'}, func='avg', metric='ms_gb_distinct')
            new_aggs_cal = QueryParser.aggs_cal(
                '({name1} + {name2}) * 3', name1=new_aggs1, name2=aggs2)
            aggs = QueryParser.aggs_by_within(new_aggs_cal, groupby=['gameid', 'url'], step_s=3600)

            # 生成完整的Elasticsearch查询结构
            es_query = QueryParser.where_filters(['ms_gb_distinct', 'cpu'], terms, aggregations=aggs)

        - ES Body::

            {
                "query": {
                    "bool": {
                        "filter": [{
                            "bool": {
                                "filter": [{
                                    "bool": {
                                        "filter": [{
                                            "bool": {
                                                "filter": [{
                                                    "term": {
                                                        "metric": {
                                                            "value": "ms_gb_distinct"
                                                        }
                                                    }
                                                }, {
                                                    "bool": {
                                                        "must_not": {
                                                            "term": {
                                                                "tag.code": {
                                                                    "value": "200"
                                                                }
                                                            }
                                                        }
                                                    }
                                                }, {
                                                    "regexp": {
                                                        "tag.hostname": {
                                                            "value": "mgb.*"
                                                        }
                                                    }
                                                }, {
                                                    "bool": {
                                                        "must_not": {
                                                            "regexp": {
                                                                "tag.ip": {
                                                                    "value": "localhost.*"
                                                                }
                                                            }
                                                        }
                                                    }
                                                }, {
                                                    "range": {
                                                        "ts": {
                                                            "gt": "2019-11-15T00:00:00+08:00"
                                                        }
                                                    }
                                                }, {
                                                    "range": {
                                                        "ts": {
                                                            "gte": "2019-11-16T00:00:00+08:00"
                                                        }
                                                    }
                                                }, {
                                                    "range": {
                                                        "ts": {
                                                            "lt": "2019-11-16T07:00:00+08:00"
                                                        }
                                                    }
                                                }, {
                                                    "range": {
                                                        "ts": {
                                                            "lte": "2019-11-17T07:00:00+08:00"
                                                        }
                                                    }
                                                }],
                                                "should": [],
                                                "minimum_should_match": 0
                                            }
                                        }, {
                                            "bool": {
                                                "filter": [],
                                                "should": [{
                                                    "term": {
                                                        "metric": {
                                                            "value": "ms_gb_distinct"
                                                        }
                                                    }
                                                }, {
                                                    "term": {
                                                        "metric": {
                                                            "value": "cpu"
                                                        }
                                                    }
                                                }],
                                                "minimum_should_match": 1
                                            }
                                        }],
                                        "should": [],
                                        "minimum_should_match": 0
                                    }
                                }],
                                "should": [],
                                "minimum_should_match": 0
                            }
                        }],
                        "should": [{
                            "bool": {
                                "filter": [],
                                "should": [{
                                    "bool": {
                                        "filter": [{
                                            "bool": {
                                                "filter": [{
                                                    "term": {
                                                        "metric": {
                                                            "value": "ms_gb_distinct"
                                                        }
                                                    }
                                                }],
                                                "should": [],
                                                "minimum_should_match": 0
                                            }
                                        }, {
                                            "bool": {
                                                "filter": [{
                                                    "bool": {
                                                        "must_not": {
                                                            "regexp": {
                                                                "tag.hostname": {
                                                                    "value": "mga.*"
                                                                }
                                                            }
                                                        }
                                                    }
                                                }],
                                                "should": [],
                                                "minimum_should_match": 0
                                            }
                                        }],
                                        "should": [],
                                        "minimum_should_match": 0
                                    }
                                }, {
                                    "bool": {
                                        "filter": [{
                                            "term": {
                                                "metric": {
                                                    "value": "ms_gb_distinct"
                                                }
                                            }
                                        }],
                                        "should": [],
                                        "minimum_should_match": 0
                                    }
                                }],
                                "minimum_should_match": 1
                            }
                        }],
                        "minimum_should_match": 1
                    }
                },
                "aggs": {
                    "tag.gameid": {
                        "terms": {
                            "field": "tag.gameid",
                            "size": 512.0
                        },
                        "aggs": {
                            "tag.url": {
                                "terms": {
                                    "field": "tag.url",
                                    "size": 1024.0
                                },
                                "aggs": {
                                    "ts": {
                                        "date_histogram": {
                                            "field": "ts",
                                            "fixed_interval": "3600s"
                                        },
                                        "aggs": {
                                            "filter_sum_{name1} + {name2} / 2": {
                                                "aggs": {
                                                    "sum_{name1} + {name2} / 2": {
                                                        "sum": {
                                                            "script": {
                                                                "source": "doc['field.count'].value + doc['field.distinctcount'].value / 2"
                                                            }
                                                        }
                                                    }
                                                },
                                                "filter": {
                                                    "bool": {
                                                        "filter": [{
                                                            "bool": {
                                                                "filter": [{
                                                                    "term": {
                                                                        "metric": {
                                                                            "value": "ms_gb_distinct"
                                                                        }
                                                                    }
                                                                }],
                                                                "should": [],
                                                                "minimum_should_match": 0
                                                            }
                                                        }, {
                                                            "bool": {
                                                                "filter": [{
                                                                    "bool": {
                                                                        "must_not": {
                                                                            "regexp": {
                                                                                "tag.hostname": {
                                                                                    "value": "mga.*"
                                                                                }
                                                                            }
                                                                        }
                                                                    }
                                                                }],
                                                                "should": [],
                                                                "minimum_should_match": 0
                                                            }
                                                        }],
                                                        "should": [],
                                                        "minimum_should_match": 0
                                                    }
                                                }
                                            },
                                            "filter_avg_('name1')": {
                                                "aggs": {
                                                    "avg_('name1')": {
                                                        "avg": {
                                                            "field": "field.count"
                                                        }
                                                    }
                                                },
                                                "filter": {
                                                    "bool": {
                                                        "filter": [{
                                                            "term": {
                                                                "metric": {
                                                                    "value": "ms_gb_distinct"
                                                                }
                                                            }
                                                        }],
                                                        "should": [],
                                                        "minimum_should_match": 0
                                                    }
                                                }
                                            },
                                            "bucket_script_({name1} + {name2}) * 3": {
                                                "bucket_script": {
                                                    "buckets_path": {
                                                        "name1": "filter_sum_{name1} + {name2} / 2>sum_{name1} + {name2} / 2",
                                                        "name2": "filter_avg_('name1')>avg_('name1')"
                                                    },
                                                    "script": {
                                                        "source": "(params.name1 + params.name2) * 3"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "from": 0,
                "size": 0,
                "sort": [{
                    "ts": {
                        "order": "desc"
                    }
                }]
            }
        """
        request_cache = str(request_cache).lower()
        track_total_hits = str(track_total_hits).lower()
        _metrics = []
        for metric in metrics:
            _metrics.append(PositiveCondition(name='metric', value=metric))
        if filters:
            filters.add_terms(Terms(should=ConditionGroup(*_metrics, relation='should')), relation='filter')
        else:
            filters = Terms(should=ConditionGroup(*_metrics))
        _should_filters = None
        if aggregations and aggregations.calculations.should_filters:
            _should_filters = Terms()
            _should_filters.add_termses(*aggregations.calculations.should_filters, relation='should')
        terms = Terms()
        terms.add_terms(filters, relation='filter')
        if _should_filters:
            terms.add_terms(_should_filters, relation='should')
        return ElasticsearchQuery(
            query=Query(terms), query_sorts=QuerySorts([Sort()]),
            source_fields=source_fields, script_fields=script_fields, aggregations=aggregations,
            offset=0 if aggregations else offset, size=0 if aggregations else min(size, 5000),
            routing=','.join(metrics), request_cache=request_cache,
            pre_filter_shard_size=pre_filter_shard_size, track_total_hits=track_total_hits, filter_path=filter_path)

    _VALID_OPS = ('=', '!=', '~', '!~', '>', '>=', '<', '<=')

    @classmethod
    def single_filter(cls, tag_name: str = 'tag', value_pattern: str = 'val*', op: str = '=') -> Condition:
        """
        **生成单条过滤条件块,支持正则匹配**

        正则:
        https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-regexp-query.html

        :param tag_name: 过滤字段名字
        :type tag_name: str
        :param value_pattern: 字段值,支持正则表达
        :type value_pattern: str
        :param op: 比较运算符号,仅包括: =、!=、~、!~、>、>=、<、<=
        :type op: str
        :return: 过滤条件结构
        :rtype: Condition

        - Foc Case::

            ip='localhost'
            或者
            ip!~'localhost.*'
            或者
            ts>'2019-11-15T00:00:00+08:00'

        - Example::

            # 生成过滤条件
            cnd = QueryParser.single_filter(tag_name='ip', value_pattern='localhost', op='=')
            cnd = QueryParser.single_filter(tag_name='ip', value_pattern='localhost.*', op='!~')
            cnd = QueryParser.single_filter(tag_name='ts', value_pattern='2019-11-15T00:00:00+08:00', op='>')

        - ES Body::

            {
                "term": {
                    "tag.ip": 'localhost'
                }
            }

            或者

            {
                "bool": {
                    "must_not": [
                    {
                        "regexp": {
                            "tag.ip": 'localhost.*'
                        }
                    }]
                }
            }

            或者

            {
                "range": {
                    "ts": {
                        "gt": "2019-11-15T00:00:00+08:00"
                    }
                }
            }
        """
        if tag_name not in ('metric', 'ts'):
            tag_name = 'tag.' + tag_name
        if op == '=':
            return PositiveCondition(op='term', name=tag_name, value=value_pattern)
        elif op == '~':
            return PositiveCondition(op='regexp', name=tag_name, value=value_pattern)
        if op == '!=':
            return NegativeCondition(op='term', name=tag_name, value=value_pattern)
        elif op == '!~':
            return NegativeCondition(op='regexp', name=tag_name, value=value_pattern)
        elif op == '>':
            return RangeCondition(op='gt', name=tag_name, value=value_pattern)
        elif op == '>=':
            return RangeCondition(op='gte', name=tag_name, value=value_pattern)
        elif op == '<':
            return RangeCondition(op='lt', name=tag_name, value=value_pattern)
        elif op == '<=':
            return RangeCondition(op='lte', name=tag_name, value=value_pattern)
        else:
            raise ParamError('op: {} is not in {}'.format(op, cls._VALID_OPS))

    _VALID_RELS = ('or', 'and')

    @classmethod
    def group_filter(cls, *conditions: Condition, relation: str = 'or') -> Terms:
        """
        **组合多个过滤条件形成过滤条件组合**

        注意: 等于是OR的关系，不等于是AND的关系

        :param conditions: 过滤条件结构
        :type conditions: Condition
        :param relation: 过滤条件之间的关系
        :type relation: str
        :return: 过滤条件集合
        :rtype: Terms

        - Foc Case::

            ( ts>'2019-11-15T00:00:00+08:00' AND ts<'2019-11-17T00:00:00+08:00' )

            或者

            ( ip='localhost' OR ip~'mgb.*' OR ip!~'agb.*')

        - Example::

            # 生成过滤条件
            cnd1 = QueryParser.single_filter(tag_name='ts', value_pattern='2019-11-15T00:00:00+08:00', op='>')
            cnd2 = QueryParser.single_filter(tag_name='ts', value_pattern='2019-11-17T00:00:00+08:00', op='<')
            # 生成过滤条件组合
            terms1 = QueryParser.group_filter(cnd1, cnd2, relation='and')

            cnd3 = QueryParser.single_filter(tag_name='ip', value_pattern='localhost', op='=')
            cnd4 = QueryParser.single_filter(tag_name='ip', value_pattern='mgb.*', op='~')
            cnd5 = QueryParser.single_filter(tag_name='ip', value_pattern='agb.*', op='!~')
            terms2 = QueryParser.group_filter(cnd3, cnd4, cnd5, relation='or')

        - ES Body::

            {
                "bool": {
                    "filter": [{
                        "range": {
                            "ts": {
                                "gt": "2019-11-15T00:00:00+08:00"
                            }
                        }
                    }, {
                        "range": {
                            "ts": {
                                "lt": "2019-11-17T00:00:00+08:00"
                            }
                        }
                    }],
                    "should": [],
                    "minimum_should_match": 0
                }
            }

            OR

            {
                "bool": {
                    "filter": [],
                    "should": [{
                        "term": {
                            "tag.ip": {
                                "value": "localhost"
                            }
                        }
                    }, {
                        "regexp": {
                            "tag.ip": {
                                "value": "mgb.*"
                            }
                        }
                    }, {
                        "bool": {
                            "must_not": {
                                "regexp": {
                                    "tag.ip": {
                                        "value": "agb.*"
                                    }
                                }
                            }
                        }
                    }],
                    "minimum_should_match": 1
                }
            }
        """
        if relation == 'or':
            cg = ConditionGroup(*conditions, relation='should')
            return Terms(should=cg)
        elif relation == 'and':
            cg = ConditionGroup(*conditions, relation='filter')
            return Terms(filter=cg)
        else:
            raise ParamError('rel: {} is not in {}'.format(relation, cls._VALID_RELS))

    @classmethod
    def group_filter_block(cls, *terms: Terms, relation: str = 'or') -> Terms:
        """
        **多个过滤条件块之间组合形成更大的条件块**

        :param terms: 过滤条件集合
        :type terms: Terms
        :param relation: 过滤条件集合之间的组合关系
        :type relation: str
        :return: 过滤条件集合
        :rtype: Terms

        - For Case::

            ( ts>'2019-11-15T00:00:00+08:00' AND ts<'2019-11-17T00:00:00+08:00' )
            AND
            ( ip='localhost' OR ip~'mgb.*' OR ip!~'agb.*')

        - Example::

            # 生成过滤条件
            cnd1 = QueryParser.single_filter(tag_name='ts', value_pattern='2019-11-15T00:00:00+08:00', op='>')
            cnd2 = QueryParser.single_filter(tag_name='ts', value_pattern='2019-11-17T00:00:00+08:00', op='<')
            # 生成过滤条件组合
            terms1 = QueryParser.group_filter(cnd1, cnd2, relation='and')

            cnd3 = QueryParser.single_filter(tag_name='ip', value_pattern='localhost', op='=')
            cnd4 = QueryParser.single_filter(tag_name='ip', value_pattern='mgb.*', op='~')
            cnd5 = QueryParser.single_filter(tag_name='ip', value_pattern='agb.*', op='!~')
            terms2 = QueryParser.group_filter(cnd3, cnd4, cnd5, relation='or')

            # 组合过滤条件组合
            terms3 = QueryParser.group_filter_block(terms1, terms2, relation='and')

        - ES Body::

            {
                "bool": {
                    "filter": [{
                        "bool": {
                            "filter": [{
                                "range": {
                                    "ts": {
                                        "gt": "2019-11-15T00:00:00+08:00"
                                    }
                                }
                            }, {
                                "range": {
                                    "ts": {
                                        "lt": "2019-11-17T00:00:00+08:00"
                                    }
                                }
                            }],
                            "should": [],
                            "minimum_should_match": 0
                        }
                    }, {
                        "bool": {
                            "filter": [],
                            "should": [{
                                "term": {
                                    "tag.ip": {
                                        "value": "localhost"
                                    }
                                }
                            }, {
                                "regexp": {
                                    "tag.ip": {
                                        "value": "mgb.*"
                                    }
                                }
                            }, {
                                "bool": {
                                    "must_not": {
                                        "regexp": {
                                            "tag.ip": {
                                                "value": "agb.*"
                                            }
                                        }
                                    }
                                }
                            }],
                            "minimum_should_match": 1
                        }
                    }],
                    "should": [],
                    "minimum_should_match": 0
                }
            }
        """
        ret = Terms()
        if relation == 'and':
            ret.add_termses(*terms, relation='filter')
        elif relation == 'or':
            ret.add_termses(*terms, relation='should')
        else:
            raise ParamError('rel: {} is not one of {}'.format(relation, cls._VALID_RELS))
        return ret

    _REMAIN_FIELDS = ['metric', 'tag', 'ts']

    @classmethod
    def fields_select(cls, fields: List[str]) -> SourceFields:
        """
        **选择同一个metric多个原有field作为返回字段,默认自动带上metric,tag,ts字段**

        :param fields: 原字段名字列表
        :type fields: List[str]
        :return: 原字段名字列表结构
        :rtype: SourceFields

        - For Case::

            ms_gb_distinct.count, ms_gb_distinct.distinctcount, ms_gb_distinct where ( ts>'2019-11-15T00:00:00+08:00' AND ts<'2019-11-17T00:00:00+08:00' ) AND ( ip='localhost' OR ip~'mgb.*' OR ip!~'agb.*')

            中的

            ms_gb_distinct.count, ms_gb_distinct.distinctcount, ms_gb_distinct

        - Example::

            fields_select = QueryParser.fields_select(['ms_gb_distinct.count', 'ms_gb_distinct.distinctcount', 'ms_gb_distinct'])

        - ES Body::

            {'_source': {'includes': ['field.count', 'field.distinctcount', 'field.value', 'metric', 'tag', 'ts']}}

        """
        _fields = OrderedDict()
        for _f in fields + cls._REMAIN_FIELDS:
            _fields[_f] = 1
        return SourceFields(
            [Field('field.' + _f.split('.', 1)[-1] if '.' in _f else _f if _f in cls._REMAIN_FIELDS else 'field.value')
             for _f in _fields])

    @staticmethod
    def fields_cal(fields: Dict[str, Dict[str, str]], exprs: Dict[str, str]) -> ScriptFields:
        """
        **选择使用表达式对同一个metric多个field之间进行四则运算后作为补充的字段**

        :param fields: 每个别名对应的运算表达式需要的运算字段
        :type fields: Dict[str, Dict[str, str]]
        :param exprs: 每个别名对应的运算表达式
        :type exprs: Dict[str, str]
        :return: 计算得到的补充的段名字列表结构
        :rtype: ScriptFields

        - For Case::

            (ms_gb_distinct.count + ms_gb_distinct.distinctcount - 2 / ms_gb_distinct.distinctcount) as alias1,
            (ms_gb_distinct.count + ms_gb_distinct.distinctcount - 3 * ms_gb_distinct.count) as alias2
            where ( ts>'2019-11-15T00:00:00+08:00' AND ts<'2019-11-17T00:00:00+08:00' ) AND ( ip='localhost' OR ip~'mgb.*' OR ip!~'agb.*')

            中的

            (ms_gb_distinct.count + ms_gb_distinct.distinctcount - 2 / ms_gb_distinct.distinctcount) as alias1,
            (ms_gb_distinct.count + ms_gb_distinct.distinctcount - 3 * ms_gb_distinct.count) as alias2

        - Example::

            fields = QueryParser.fields_cal(
                fields={
                    'alias1': {'name1': 'ms_gb_distinct.count', 'name2': 'ms_gb_distinct.distinctcount'},
                    'alias2': {'name1': 'ms_gb_distinct.count', 'name2': 'ms_gb_distinct.count',
                               'name3': 'ms_gb_distinct.distinctcount'}},
                exprs={
                    'alias1': '{name1} + {name2} - 2 / {name2}',
                    'alias2': '{name1} + {name3} - 3 * {name1}'
                }
            )

        - ES Body::

            {
                "script_fields": {
                    "alias1": {
                        "script": {
                            "source": "doc['field.count'].value + doc['field.distinctcount'].value - 2 / doc['field.distinctcount'].value"
                        }
                    },
                    "alias2": {
                        "script": {
                            "source": "doc['field.count'].value + doc['field.distinctcount'].value - 3 * doc['field.count'].value"
                        }
                    }
                }
            }
        """
        _script_fields = []
        for alias_name, field_names in fields.items():
            _fields = {}
            for key, field_name in field_names.items():
                _fields[key] = field_name.split('.', 1)[-1] if '.' in field_name else 'value'
            _script_fields.append(ScriptField(_fields, exprs.get(alias_name), alias=alias_name))
        return ScriptFields(_script_fields)
