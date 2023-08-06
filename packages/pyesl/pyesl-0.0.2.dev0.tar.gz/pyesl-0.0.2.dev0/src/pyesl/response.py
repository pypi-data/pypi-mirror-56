# -*- coding: utf-8 -*-

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


class Series(object):
    def __init__(self, name: str, legends: Dict[str, str], data: List[DataPoint]):
        self._name = name
        self._legends = legends
        self._data = data

    @property
    def name(self) -> str:
        return self._name

    @property
    def legends(self) -> Dict[str, str]:
        return self._legends

    @property
    def data(self) -> List[DataPoint]:
        return self._data


class TsdbResponse(object):
    def __init__(self, series: List[Series]):
        self._series = series

    @property
    def series(self) -> List[Series]:
        return self._series
