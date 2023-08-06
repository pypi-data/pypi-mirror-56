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
        **聚合算子加上groupby和within语句**

        - Example::

            aggs1 = QueryParser.single_aggs(
                fields={'name1': 'ms_gb_distinct.count', 'name2': 'ms_gb_distinct.distinctcount'}, func='sum',
                metric='ms_gb_distinct',
                expr='{name1} + {name2} / 2')
            aggs2 = QueryParser.single_aggs(
                fields={'name1': 'ms_gb_distinct.count'}, func='avg', metric='ms_gb_distinct')
            aggs_cal = QueryParser.aggs_cal(
                '({name1} + {name2}) * 3', name1=aggs1, name2=aggs2)

        IN:
            聚合运算的语句块，groupby列表，within列表
        OUT:
            聚合语句块

        :param calculation: 聚合运算语句块合集 或者 聚合运算语句块
        :type calculation: Union[FieldCalculation, Calculations]
        :param groupby: 分组的tag字段
        :type groupby: List[str]
        :param step_s: 按时间分组的步长,单位:秒
        :type step_s: Union[int, None]
        :return:
        :rtype: Aggregations
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
            metrics: List[str], filters: Terms, script_fields: ScriptFields = None, source_fields: SourceFields = None,
            aggregations: Aggregations = None,
            request_cache: bool = True, pre_filter_shard_size: int = 1, track_total_hits: bool = False,
            filter_path: str = 'hits.hits._source,hits.hits.fields,hits.total,took,_shards,aggregations',
            offset: int = 0, size: int = 0
    ) -> ElasticsearchQuery:
        """
        整合一整个语句块

        IN:
            指标名字，查询字段，聚合语句块，过滤语句块，指标列表

        OUT:
            整个query语句块

        :param metrics: 指标名字
        :param filters: 过滤条件
        :param script_fields: 别名字段
        :param source_fields: 原字段
        :param aggregations: 聚合语句块
        :param request_cache: 是否使用缓存
        :param pre_filter_shard_size: 是否预查询shards
        :param track_total_hits: 是否跟踪所有记录条目数
        :param filter_path: 返回的必要信息
        :param offset: 原始查询起点
        :param size: 原始查询页大小
        :return:
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
        生成过滤条件块，等于是OR的关系，不等于是AND的关系

        IN:
            A = '123' 或者 A != '123' 或者 A ～ 'g*'

        OUT:
            过滤条件块
            {
                "term": {
                    "tag.A": '123'
                }
            }

            {
                "bool": {
                    "must_not": [
                    {
                        "term": {
                            "tag.B": '123'
                        }
                    }]
                }
            }

            {
                "regexp": {
                    "tag.A": 'g*'
                }
            }

            {
                "range": {
                    "tag.A": {
                        "gte": 1
                    }
                }
            }

        :param tag_name: 字段名字
        :param value_pattern: 字段值（支持正则过滤）
        :param op: =、!=、~、!~、>、>=、<、<=
        :return:
        :rtype: Condition
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
    def group_filter(cls, *conditions: Condition, relation='or') -> Terms:
        """
        单个过滤条件之间的组合形成的过滤条件

        and: (a and a='abc')
        or: (a or b)

        :param conditions: 单个过滤条件
        :param relation: 过滤条件之间的关系
        :return:
        :rtype: Terms
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
    def group_filter_block(cls, *terms: Terms, relation='or') -> Union[Terms, None]:
        """
        多个过滤条件块之间组合形成更大的条件块

        IN:
            过滤条件块: (A_terms or B_terms) 或者 (A and B)

        OUT:

            {
                'bool': {
                    'should': [
                         {
                            "term": {
                                "tag.A": '123'
                            }
                        },
                        {
                            "term": {
                                "tag.A": '123'
                            }
                        },
                        {
                            "term": {
                                "tag.A": '123'
                            }
                        }
                    ]
                }
            }

        :param terms: 过滤条件块
        :param relation: 过滤条件块之间的关系
        :return:
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
        选择同一个metric多个原有field
        IN:
            sql: select a, b, c
            aql: cpu.a, cpu.b, cpu.c
        OUT:
            多个原字段的表示对象

        :param fields: 原字段名字
        :return:
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
        选择使用表达式对同一个metric多个field之间进行四则运算后得到的结果

        IN:
            sql: select a + b as a, b + c as c
            aql: cpu.a + cpu.b, cpu.c + cpu.d

        OUT:
            多个表达式的表示对象

        :param fields: 每个别名对应的运算表达式需要的运算字段，例如{ 'alias_name1': {'name1': 'field1', 'name2': 'field2'}}
        :param exprs: 每个别名对应的运算表达式
        :return:
        """
        _script_fields = []
        for alias_name, field_names in fields.items():
            _fields = {}
            for key, field_name in field_names.items():
                _fields[key] = field_name.split('.', 1)[-1] if '.' in field_name else 'value'
            _script_fields.append(ScriptField(_fields, exprs.get(alias_name), alias=alias_name))
        return ScriptFields(_script_fields)
