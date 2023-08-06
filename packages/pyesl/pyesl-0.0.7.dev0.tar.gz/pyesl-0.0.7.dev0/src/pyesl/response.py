# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Union, List, Dict


class DataPoint(object):
    def __init__(self, ts: Union[float, int, str], value: float):
        self._ts = ts
        self._val = value

    @property
    def ts(self) -> Union[float, int, str]:
        return self._ts

    @property
    def value(self) -> float:
        return self._val


class Legend(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Series(object):
    def __init__(self, name: str, legends: Dict[str, str] = None, data: List[DataPoint] = None):
        self._name = name
        self._legends = Legend(**legends) if legends else Legend()
        self._data = data or []

    @property
    def name(self) -> str:
        return self._name

    @property
    def legends(self) -> Dict[str, str]:
        return self._legends

    @property
    def data(self) -> List[DataPoint]:
        return self._data

    def add_legend(self, tagname: str, tagvalue: str):
        self._legends[tagname] = tagvalue
    
    def add_datapoint(self, value: float, ts: Union[int, float, str]):
        self._data.append(DataPoint(ts, value))

    def add_copy(self, tagname: str, tagvalue: str) -> Series:
        new_s = Series(self._name + '#' + tagname + '=' + tagvalue, self._legends.copy())
        new_s.add_legend(tagname, tagvalue)
        return new_s


class TsdbResponse(object):
    def __init__(self, series: List[Series]):
        self._series = series

    @property
    def series(self) -> List[Series]:
        return self._series
