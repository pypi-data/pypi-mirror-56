# -*- coding: utf-8 -*-

from abc import ABC
from collections import OrderedDict
from typing import List, Dict, Union

from pyesl.errors import ParamError, QueryBodyError
from pyesl.query import Terms


class AggsBase(ABC):
    def __init__(self, body: dict, name: str):
        self._body = body
        self._name = self._format_name(name)
        self._result_path = []

    @property
    def body(self) -> dict:
        return self._body

    @property
    def name(self) -> str:
        return self._name

    def _format_name(self, value: str) -> str:
        return value.replace('[', '(').replace(']', ')').replace('>', '=')

    @property
    def result_path(self) -> tuple:
        return tuple(self._result_path)


class Groupby(AggsBase):
    """
    Group by condition object of tags eg:

    1. sql like: group by keyA
    2. pql like: by (keyA)
    """

    BODY_TEMPLATE = {
        'agg_name': {
            'terms': {
                'field': 'key',
                'size': 1024,
                'param_name1': 'param_val1'
            }
        }
    }

    def __init__(self, field: str = 'key', name: str = None, size: int = 1024, **params):
        self._field = field
        _name = self._format_name(name or field)
        _body = {
            _name: {
                'terms': params
            }
        }
        _body[_name]['terms']['field'] = field
        _body[_name]['terms']['size'] = size
        super().__init__(_body, _name)

    @property
    def field(self):
        return self._field


class Step(AggsBase):
    """
    Group by condition object of time steps eg:

    1. sql like: group by DATE_FORMAT(ts, '%Y-%d-%h %H')
    2. pql like: step_s = 3600
    """

    BODY_TEMPLATE = {
        'agg_name': {
            'date_histogram': {
                'field': 'key',
                'fixed_interval': '3600s',
                'size': 4096
            }
        }
    }

    def __init__(self, field: str = 'ts', name: str = 'ts', step_s=3600, **params):
        self._field = field
        _name = self._format_name(name or field)
        self._step_s = step_s
        _body = {
            _name: {
                'date_histogram': params
            }
        }
        _body[_name]['date_histogram']['field'] = field
        _body[_name]['date_histogram']['fixed_interval'] = '{}s'.format(step_s)
        super().__init__(_body, _name)

    @property
    def field(self):
        return self._field

    @property
    def step_s(self):
        return self._step_s


class Aggregation(AggsBase):
    """
    Sigle aggregation of group by, step eg:

    1. pql like: by (A, B, C) interval = 3600

    """
    BODY_TEMPLATE = {
        'agg_key': {
            'term': {
                'field': 'key',
                'size': 1024
            },
            'aggs': {
                'agg_ts': {
                    'date_histogram': {
                        'field': 'ts',
                        'fixed_interval': '3600s',
                        'size': 4096
                    }
                }
            }
        }
    }

    def __init__(self, groupby: List[Groupby] = None, step: Step = None):
        self._groupby = OrderedDict()
        self._step = step
        _body = {}
        _cu = _body
        if groupby:
            for _g in groupby:
                self._groupby[_g.name] = _g
                _cu['aggs'] = _g.body
                _cu = _cu['aggs'][_g.name]
        if self._step:
            _cu['aggs'] = self._step.body
            _name = 'agg_{}_{}'.format('#'.join(self._groupby.keys()), step.name)
        else:
            _name = 'agg_{}'.format('#'.join(self._groupby.keys()))
        _name = self._format_name(_name)
        super().__init__(_body['aggs'], _name)
        self._groupby = groupby
        self._step = step

    @property
    def groupby(self) -> List[Groupby]:
        return self._groupby

    @property
    def step(self) -> Step:
        return self._step


class FieldCalculation(AggsBase):
    """
    Calculation of field eg:

    1. sql like: sum(a)
    2. pql like: sum_over_time(abc.value)
    3. aql like: sum(abc.field1 + abc.field2 / 2)

    """

    BODY_TEMPLATE = {
        'cal_name': {
            'func': {
                'field': 'field_name',
                'param_name1': 'param_val1'
            }
        }
    }

    VALID_FUNC = ('sum', 'avg', 'max', 'min', 'value_count')

    def __init__(
            self, fields: dict, expr: str = None, func: str = 'sum',
            field_format: str = "doc['field.{field}'].value", **params):
        if func not in self.VALID_FUNC:
            raise ParamError('func: {} is not in {}'.format(func, self.VALID_FUNC))
        self._func = func
        self._fields = fields
        self._is_script = True if expr else False
        self._expr = expr
        if len(fields) > 1 and not self._is_script:
            raise ParamError('To use script when more than one field: {}'.format(fields))
        self._expr_formatted = None
        self._fields_formatted = {}
        for key, field in self._fields.items():
            self._fields_formatted[key] = field_format.format(field=field)
        if not self._is_script:
            _name = self._format_name('{}_{}'.format(func, sorted(fields.keys())))
            _body = {
                _name: {
                    self._func: params
                }
            }
            _body[_name][self._func]['field'] = list(self._fields_formatted.values())[0]
        else:
            self._expr_formatted = self._expr.format(**self._fields_formatted)
            _name = self._format_name('{}_{}'.format(func, expr))
            _body = {
                _name: {
                    self._func: params
                }
            }
            _body[_name][self._func]['script'] = {
                'source': self._expr_formatted
            }
        super().__init__(_body, _name)
        self._result_path.append(_name)

    @property
    def is_script(self) -> bool:
        return self._is_script


class ResultCalculation(FieldCalculation):
    """
    Calculation of FieldCalculation or QueryCalculation eg:

    1. sql like: sum(abc.field1 + abc.field2, a='b', b='c')
    2. pql like: sum_over_time(abc.value) + sum_over_time(abc.value)
    3. aql like: sum(abc.field1 + abc.field2 / 2, a='b', b='c') / sum(abc.field1 + abc.field2 / 2, a='b', b='c')
        group by a, b, c within

    """

    BODY_TEMPLATE = {
        "cal_name": {
            "bucket_script": {
                "buckets_path": {
                    "name1": "_ignore_agg_name1>cal_name",
                    "name2": "_ignore_agg_name2"
                },
                "script": "params.name1 / params.name2 + 2 /10"
            }
        },
        '_ignore_agg_name1': {
            "filter": {
                "bool": {
                    "filter": [
                        {
                            "term": {
                                "metric": "cpu"
                            }
                        }
                    ],
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
                'cal_name': {
                    'func': {
                        'field': 'field_name',
                        'param_name1': 'param_val1'
                    }
                }
            }
        },
        '_ignore_agg_name2': {
            'func': {
                'field': 'field_name',
                'param_name1': 'param_val1'
            }
        }
    }

    VALID_FUNC = ('bucket_script',)

    def __init__(self, calculation: Dict[str, FieldCalculation], expr: str, **params):
        self._buckets_path = {}
        self._calname_formatted = {}
        for name, _cal in calculation.items():
            self._buckets_path[name] = '>'.join(_cal.result_path)
            self._calname_formatted[name] = 'params.{}'.format(name)
        self._expr = expr
        super().__init__(
            fields=self._calname_formatted, expr=expr, func='bucket_script', field_format='{field}',
            buckets_path=self._buckets_path, **params)


class QueryCalculation(FieldCalculation):
    """
    Calculation with query terms eg:

    1. pql like: sum_over_time(abc.value, a='b', c='d', e='a') by (a, b, c)
    2. aql like: sum(abc.field1 + abc.field2 / 2, a='bc', c='a', fas='fs') groupby (c, d, e, f)

    """
    BODY_TEMPLATE = {
        'agg_name': {
            "filter": {
                "bool": {
                    "filter": [
                        {
                            "term": {
                                "metric": "cpu"
                            }
                        }
                    ],
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
                'cal_name': {
                    'func': {
                        'field': 'field_name',
                        'param_name1': 'param_val1'
                    }
                }
            }
        }
    }

    def __init__(
            self, terms: Terms, fields: dict, expr: str = None, func: str = 'sum',
            field_format: str = "doc['field.{field}'].value", **params):
        if not expr:
            field_format = 'field.{field}'
        super().__init__(fields, expr, func, field_format, **params)
        self._name = 'filter_{}'.format(self._name)
        self._result_path.insert(0, self._name)
        _body = {
            self._name: {
                'aggs': self._body
            }

        }
        _body[self._name]['filter'] = terms.body
        self._body = _body
        self._terms = terms

    @property
    def terms(self) -> Terms:
        return self._terms


class Calculations(AggsBase):
    """
    Calculations combination of all kind of calculations
    """
    BODY_TEMPLATE = {
        'aggs': {
            'agg_name1': {
                "filter": {
                    "bool": {
                        "filter": [
                            {
                                "term": {
                                    "metric": "cpu"
                                }
                            }
                        ],
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
                    'cal_name': {
                        'func': {
                            'field': 'field_name',
                            'param_name1': 'param_val1'
                        }
                    }
                }
            },
            'agg_name2': {
                "filter": {
                    "bool": {
                        "filter": [
                            {
                                "term": {
                                    "metric": "cpu"
                                }
                            }
                        ],
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
                    'cal_name': {
                        'func': {
                            'field': 'field_name',
                            'param_name1': 'param_val1'
                        }
                    }
                }
            }
        }
    }

    def __init__(self, *calculations: FieldCalculation, return_calculation_name: Union[str, None] = None):
        self._should_filters = []
        self._calculations = {}
        _body = {
            'aggs': {

            }
        }
        _cal_paths = []
        _names = []
        if len(calculations) == 1:
            return_calculation_name = calculations[0].name
        elif return_calculation_name is None:
            raise QueryBodyError('Choose One of Calculation Result to Return: {}'.format(
                [_cal.name for _cal in calculations]))
        for _cal in calculations:
            if isinstance(_cal, QueryCalculation):
                if _cal.terms:
                    self._should_filters.append(_cal.terms)
            _body['aggs'][_cal.name] = _cal.body[_cal.name]
            _names.append(_cal.name)
            self._result_calculation = None
            if return_calculation_name is None:
                _cal_paths.append(_cal.result_path)
            elif _cal.name == return_calculation_name:
                _cal_paths.append(_cal.result_path)
                self._result_calculation = _cal
            else:
                continue
            self._calculations[_cal.name] = _cal
        if self._result_calculation is None:
            raise QueryBodyError('Choose One of Calculation Result to Return: {}'.format(
                [_cal.name for _cal in calculations]))
        super().__init__(_body, 'cal_{}'.format('#'.join(_names)))
        self._result_path = [_cal_paths]

    @property
    def should_filters(self) -> List[Terms]:
        return self._should_filters

    def calculation_names(self) -> List[str]:
        return list(self._calculations.keys())

    def get_calculation(self, name: str) -> FieldCalculation:
        return self._calculations[name]

    @property
    def result_calculation(self) -> Union[FieldCalculation, None]:
        return self._result_calculation


class Aggregations(AggsBase):
    """
    Aggregation combination of calculation(with filter), group by, step eg:

    1. pql like: sum(a, b, c) by (A, B, C) interval = 3600
    2. aql like: sum(cpu.a + cpu.b, kk=1 and bb=1) group by 3600 within 10s
    """

    BODY_TEMPLATE = {
        'aggs': {
            'agg_key': {
                'term': {
                    'field': 'key',
                    'size': 1024
                },
                'aggs': {
                    'agg_ts': {
                        'date_histogram': {
                            'field': 'ts',
                            'fixed_interval': '3600s',
                            'size': 4096
                        },
                        "aggs": {
                            'agg_name': {
                                "filter": {
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
                                'aggs': {
                                    'cal_field': {
                                        'sum': 'field.field_name'
                                    }
                                }
                            }

                        }
                    }
                }
            }
        }
    }

    def __init__(self, calculations: Calculations, groupby: List[Groupby] = None, step: Step = None):
        _groupby = OrderedDict()
        self._step = step
        _body = {}
        _cu = _body
        _result_path = []
        if groupby:
            self._groupby = groupby
            for _g in groupby:
                _groupby[_g.name] = _g
                _result_path.append(_g.name)
                _cu['aggs'] = _g.body
                _cu = _cu['aggs'][_g.name]
        else:
            self._groupby = []
        if self._step:
            _cu['aggs'] = self._step.body
            _result_path.append(self._step.name)
            _cu = _cu['aggs'][self._step.name]
            _name = 'agg_{}_{}'.format('#'.join(_groupby.keys()), step.name)
        else:
            _name = 'agg_{}'.format('#'.join(_groupby.keys()))
        super().__init__(_body, _name)
        _cu['aggs'] = calculations.body['aggs']
        _result_path.extend(calculations.result_path)

        self._step = step
        self._calculations = calculations
        self._result_path = _result_path

    @property
    def groupby(self) -> List[Groupby]:
        return self._groupby

    @property
    def step(self) -> Union[Step, None]:
        return self._step

    @property
    def calculations(self) -> Calculations:
        return self._calculations
