# -*- coding: utf-8 -*-

from typing import List, Union, Dict

from pip._vendor.requests import Response

from pyesl.aggs import FieldCalculation, QueryCalculation, ResultCalculation, Aggregations, Calculations, \
    Groupby, Step
from pyesl.errors import ParamError
from pyesl.field import ScriptFields, SourceFields, Field, ScriptField
from pyesl.query import Condition, PositiveCondition, NegativeCondition, Terms, ConditionGroup, QuerySorts, Sort, \
    Query, RangeCondition
from pyesl.response import TsdbResponse, Series, DataPoint
from pyesl.search import ElasticsearchQuery


class QueryParser(object):

    @staticmethod
    def single_aggs(
            fields: Dict[str, str], func: str = 'sum', metric: str = 'cpu', expr: Union[None, str] = None,
            filters: Terms = None) -> FieldCalculation:
        """
        生成聚合代码片段

        IN:

            sum(cpu.user + cpu.sys, gameid!='g18') 或者 sum(cpu.user, gameid!='g18')

        OUT:

        名字：
        agg_name

        值：
        {
            'aggs': {
                'agg_name': {
                  "filter": {
                    "term": {
                        "metric": "cpu"
                    },
                    "bool": {
                      "must_not": [
                        {
                          "term": {
                            "tag.gameid": "g18"
                          }
                        }
                      ]
                    }
                  },
                  "aggs": {
                    "sum_fields": {
                      "sum": {
                        "script": {
                          "source": "doc['field.distinctcount'].value + doc['field.count'].value"
                        }
                      }
                    }
                  }
                }
            }
        }
        :param fields: 计算的字段
        :param func: 聚合方法
        :param metric: 聚合的metric
        :param expr: 运算字段的表达式例如：({name1} + {name2}) /2.0
        :param filters: 过滤条件
        :return:
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
        _pc = PositiveCondition(name=metric, value=metric)
        if filters:
            filters.append_condition(_pc, relation='filter')
        else:
            filters = Terms(filter=ConditionGroup([_pc], relation='filter'))
        _qc = QueryCalculation(fields=_fields, expr=expr, func=func, terms=filters)
        return _qc

    @staticmethod
    def aggs_cal(calculations: Dict[str, FieldCalculation], expr: str) -> Calculations:
        """
        聚合算子结果之间四则运算

        IN：
            name1, name2, name3, (name1 + name2) / name3)

        OUT：

            {
            "division_result": {
              "bucket_script": {
                "buckets_path": {
                  "not_g18_sum": "not_g18_sum>sum_fields",
                  "not_360_sum": "not_360_sum>sum_fields"
                },
                "script": "params.not_g18_sum / params.not_360_sum"
              }
            }}

        :param calculations: 聚合算子
        :param expr: 聚合算子四则运算表达式
        :return:
        :rtype: Calculations
        """
        cals = list(calculations.values())
        cals.append(ResultCalculation(calculation=calculations, expr=expr))
        return Calculations(calculations=cals)

    @staticmethod
    def aggs_by_within(
            calculations: Calculations, groupby: List[str] = None, step_s: Union[int, None] = None) -> Aggregations:
        """
        聚合算子加上groupby和within语句

        IN:
            聚合运算的语句块，groupby列表，within列表
        OUT:
            聚合语句块

        :param calculations: 聚合算子
        :param groupby: groupby的字段
        :param step_s: within、step的秒数
        :return:
        :rtype: Aggregations
        """
        glen = len(groupby)
        _groupbys = []
        for idx, _g in enumerate(groupby):
            size = max(1, 1024 / 2 ** (glen - idx - 1))
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
            filter_path: str = 'hits.hits._source,hits.hits.fields,hits.total,took,_shards,aggregations'
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
        :return:
        """
        _metrics = []
        for metric in metrics:
            _metrics.append(Condition(name='metric', value=metric))
        if filters:
            filters.extend_group(ConditionGroup(_metrics))
        else:
            filters = Terms(should=ConditionGroup(_metrics))
        terms = Terms()
        terms.add_terms(filters, relation='filter')
        if aggregations and aggregations.calculations.should_filters:
            for should_filter in aggregations.calculations.should_filters:
                should_filter.add_terms(filters, relation='should')
                terms.add_terms(should_filter, relation='should')
        return ElasticsearchQuery(
            query=Query(terms), query_sorts=QuerySorts([Sort()]),
            source_fields=source_fields, script_fields=script_fields, aggregations=aggregations, offset=0,
            size=0 if aggregations else 5000, routing=','.join(metrics), request_cache=request_cache,
            pre_filter_shard_size=pre_filter_shard_size, track_total_hits=track_total_hits, filter_path=filter_path)

    VALID_OPS = ('=', '!=', '~', '!~', '>', '>=', '<', '<=')

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
            raise ParamError('op: {} is not in {}'.format(op, cls.VALID_OPS))

    VALID_RELS = ('or', 'and')

    @classmethod
    def group_filter(cls, condition: List[Condition], relation='or') -> Terms:
        """
        单个过滤条件之间的组合形成的过滤条件

        and: (a and a='abc')
        or: (a or b)

        :param condition: 单个过滤条件
        :param relation: 过滤条件之间的关系
        :return:
        :rtype: Terms
        """
        if relation == 'or':
            cg = ConditionGroup(condition, relation='should')
        elif relation == 'and':
            cg = ConditionGroup(condition, relation='filter')
        else:
            raise ParamError('rel: {} is not in {}'.format(relation, cls.VALID_RELS))
        return Terms(filter=cg)

    @staticmethod
    def group_filter_block(terms: List[Terms], relation='or') -> Union[Terms, None]:
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
        ret = None
        for _t in terms:
            if ret is None:
                ret = _t
            else:
                ret.add_terms(_t, relation=relation)
        return ret

    def _filter_optimize(self):
        """
        提取过滤条件
        :return:
        """
        pass

    @staticmethod
    def fields_select(fields: List[str]) -> SourceFields:
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

        return SourceFields([Field(_f.split('.', 1)[-1] if '.' in _f else 'value') for _f in fields])

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
                _fields[key] = field_name.split('.', 1)[-1]
            _script_fields.append(ScriptField(_fields, exprs.get(alias_name), alias=alias_name))
        return ScriptFields(_script_fields)


class ResponseParser(object):

    @staticmethod
    def tsfresp(response: Response) -> TsdbResponse:
        print(response.text)
        return TsdbResponse([Series('name', {'tag.key1': 'val1'}, [DataPoint(0, 0)])])
