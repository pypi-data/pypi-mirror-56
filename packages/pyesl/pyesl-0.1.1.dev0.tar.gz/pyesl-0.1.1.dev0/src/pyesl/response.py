# -*- coding: utf-8 -*-
from __future__ import annotations

from copy import deepcopy
from typing import Union, List, Dict, Tuple

from dateutil.parser import parse


class DataPoint(object):
    def __init__(self, ts: Union[float, int, str], value: float):
        if isinstance(ts, str):
            self._ts = parse(ts).timestamp() * 1000
        elif isinstance(ts, float):
            point_size = len(str(ts).split('.')[1])
            self._ts = int(ts * (10 ** point_size))
        else:
            self._ts = ts
        # 1574925204228
        ts_str = str(self._ts)
        if len(ts_str) > 13:
            self._ts = int(str(ts_str)[:13])
        elif len(ts_str) < 13:
            self._ts = int(ts_str.ljust(13, '0'))
        self._val = value
        self._datapoint = (self._val, self._ts)

    @property
    def ts(self) -> int:
        """
        **Millseconds since 1970**
        :return: Millseconds
        :rtype: int
        """
        return self._ts

    @property
    def value(self) -> float:
        return self._val

    @property
    def datapoint(self) -> Tuple[float, int]:
        return self._datapoint


class Legend(dict):
    def __init__(self, **kwargs):
        kwargs['tag'] = kwargs.get("tag", {})
        super().__init__(**kwargs)


class Series(object):
    def __init__(self, name: str, legends: Dict[str, Union[Dict[str, str], str]] = None, data: List[DataPoint] = None):
        self._name = name
        self._legends = Legend(**legends) if legends else Legend()
        self._data = data or []

    @property
    def name(self) -> str:
        return self._name

    @property
    def legends(self) -> Dict[str, Union[Dict[str, str], str]]:
        return self._legends

    @property
    def data(self) -> List[Tuple[float, int]]:
        """
        **Return list of data point with data type as a tuple of (value, ts)**
        :return:
        :rtype List[Tuple[float, int]]
        """
        return [_data.datapoint for _data in self._data]

    def add_legend(self, tagname: str, tagvalue: str):
        """
        **Add legend tag name and tag value**
        if '.' in tagname, like 'tag.field.name', legend will be {'tag': {'field': {'name': 'value'}}}

        :param tagname: tag name
        :type tagname: str
        :param tagvalue: tag value
        :type tagvalue: str
        :return:
        """
        if "." not in tagname:
            self._legends[tagname] = tagvalue
        else:
            cur = self._legends
            tag_arr = tagname.split('.')
            for _tag in tag_arr[:-1]:
                if _tag in cur:
                    cur = cur[_tag]
                else:
                    cur[_tag] = {}
                    cur = cur[_tag]
            cur[tag_arr[-1]] = tagvalue

    def add_datapoint(self, value: float, ts: Union[int, float, str]):
        self._data.append(DataPoint(ts, value))

    def add_copy(self, tagname: str, tagvalue: str) -> Series:
        new_s = Series(self._name + '#' + tagname + '=' + tagvalue, deepcopy(self._legends))
        new_s.add_legend(tagname, tagvalue)
        return new_s


class TsdbResponse(object):
    def __init__(self, series: List[Series], response: dict):
        self._series = series
        self._response = response

    @property
    def series(self) -> List[Series]:
        return self._series

    @property
    def response(self) -> dict:
        return self._response
