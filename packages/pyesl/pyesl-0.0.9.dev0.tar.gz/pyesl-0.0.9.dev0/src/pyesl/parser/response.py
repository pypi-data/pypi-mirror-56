# -*- coding: utf-8 -*-
from functools import partial
from typing import Union, Tuple, List, Iterator, Dict

from deprecated import deprecated

from pyesl.errors import SearchFailedError
from pyesl.response import TsdbResponse, Series
from pyesl.search import ElasticsearchQuery


class ResponseParser(object):

    @staticmethod
    def tsfresp(query: ElasticsearchQuery, response: dict) -> TsdbResponse:
        """
            **Get TsdbResponse From Elasticsearch Search API Response**
            This function allows users to get tsdb type response from the Elasticsearch search API return object.
            :param query: 本次查询结果的查询对象
            :param response: Elasticsearch的searchAPI返回结果
            :return: 返回时序格式结构对象
            :rtype: TsdbResponse
            - Example::
                  es_query = TestParser().test_10_where_filters_aggs()
                  cli = SearchClient(**es_conf.es_conf)
                  res = cli.search(es_query)
                  for _s in res.series:
                      print(_s.name) # using name
                      print(_s.legends) # using legends
                      for _dp in _s.data: # using datapoint
                          print(_dp.ts)
                          print(_dp.value)
            - Expected Success Response::
                  self.assertEqual(res.series[0].name, 'agg#gameid=g66#url=/g66/gb/sauth')
                  self.assertEqual(len(res.series[0].data), 7)
                  self.assertEqual(res.series[0].data[0].value, 47022.28388131516)
                  self.assertEqual(res.series[0].data[0].ts, 1573833600000)
                  self.assertEqual(res.series[0].data[6].value, 26883.47335553705)
                  self.assertEqual(res.series[0].data[6].ts, 1573855200000)
                  self.assertEqual(res.series[-1].name, 'agg#gameid=lh2#url=/lh2/gb/sauth')
        """

        if response['_shards']['failed']:
            # failed and handler error
            raise SearchFailedError(u'Search Failed Error: {}'.format(response['_shards']['failures'][0]))
        else:
            # success
            _series = []
            if query.aggregations:
                # 聚合查询
                for series in ResponseParser._walk_through_bucket(
                        response.get('aggregations', {}), query.aggregations.result_path, Series('agg')):
                    _series.append(series)
            else:
                # 一般查询
                _series = ResponseParser._walk_through_hits(response.get('hits', {}).get('hits', []))
        return TsdbResponse(_series)

    @staticmethod
    def _add_tag(tag_name: str, tag_value: str, datapoint: dict):
        datapoint['tag'][tag_name] = tag_value

    @staticmethod
    def _add_ts_metric(tag_name: str, tag_value: Union[str, int], datapoint: dict):
        datapoint[tag_name] = tag_value

    DEFAULT_VALUE = {
        'value': None
    }

    @classmethod
    def _add_datapoint(
            cls, series: Series, ts: Union[int, float, str], field_name: Union[List[str], Tuple[str], str],
            result_bucket: dict):
        """
        将数据节点从es的bucket中抽取放入Series数据结构当中
        :param series:
        :param ts:
        :param field_name:
        :param result_bucket:
        :return:
        """
        if isinstance(field_name, (list, tuple)):
            # 多个运算结果
            for field_path in field_name:
                _cur = result_bucket
                if isinstance(field_path, (list, tuple)):
                    _field_name = field_path[0]
                    for _path in field_path:
                        _cur = _cur.get(_path, cls.DEFAULT_VALUE)
                else:
                    _field_name = field_path
                    _cur = result_bucket.get(field_path, cls.DEFAULT_VALUE)
                series.add_datapoint(_cur['value'], ts)
        else:
            series.add_datapoint(result_bucket[field_name]['value'], ts)

    @staticmethod
    def _walk_through_bucket(
            groupby_result: Dict[str, dict], result_path: Union[tuple, list], series: Series) -> Iterator[Series]:
        """
        返回结构化聚合数据
        :param groupby_result:
        :param result_path:
        :param series:
        :return:
        """
        this_tagname = result_path[0]
        next_layer = result_path[1:]
        if this_tagname == 'ts':
            # 到达了时序数据库的边界
            for bucket in groupby_result.get(this_tagname, {}).get('buckets', []):
                ResponseParser._add_datapoint(series, bucket['key'], next_layer[0], bucket)
            yield series
        elif this_tagname == 'metric':
            # metric
            for bucket in groupby_result.get(this_tagname, {}).get('buckets', []):
                metric_value = bucket['key']
                _s = series.add_copy('metric', metric_value)
                for ret in ResponseParser._walk_through_bucket(bucket, next_layer, _s):
                    yield ret
        else:
            # tagkey
            for bucket in groupby_result.get(this_tagname, {}).get('buckets', []):
                this_tagvalue = bucket['key']
                _s = series.add_copy(this_tagname.split('.', 1)[1], this_tagvalue)
                for ret in ResponseParser._walk_through_bucket(bucket, next_layer, _s):
                    yield ret

    @staticmethod
    def _walk_through_hits(query_result: List[dict]) -> List[Series]:
        """
        返回结构化查询数据
        :param query_result:
        :return:
        """
        s_dict = {}
        for _res in query_result:
            _source = _res['_source']
            _metric = _source['metric']
            _name = 'query#{metric}#{tags}#{field}'
            tags_arr = []
            tags_dict = {
                'metric': _metric
            }
            for key in sorted(_source['tag'].keys()):
                val = _source['tag'][key]
                tags_dict['tag.{}'.format(key)] = val
                tags_arr.append('{}={}'.format(key, val))
            tags = '#'.join(tags_arr)
            script_fields = {
                field_name: field_value[0] for field_name, field_value in _res.get('fields', {}).items()
            }
            fields = _source.get('field', {})
            fields.update(script_fields)
            for field_name, field_value in fields.items():
                s_name = _name.format(metric=_metric, tags=tags, field=field_name)
                tags_dict['field'] = field_name
                series = s_dict.get(s_name, Series(s_name, legends=tags_dict))
                series.add_datapoint(field_value, _source['ts'])
                s_dict[s_name] = series
        return list(s_dict.values())

    @staticmethod
    @deprecated(version='0.0.6', reason="This method is deprecated")
    def _walk_iter_bucket(groupby_result: dict, result_path: Union[tuple, list]) -> dict:
        if len(result_path) == 1:
            # 最底层
            field_name = result_path[0]
            datapoint = None
            if isinstance(field_name, (list, tuple)):
                # 多个运算结果
                for field_path in field_name:
                    _cur = groupby_result
                    if isinstance(field_path, (list, tuple)):
                        _field_name = field_path[0]
                        for _path in field_path:
                            _cur = _cur[_path]
                    else:
                        _field_name = field_path
                        _cur = groupby_result[field_path]
                    if datapoint is None:
                        datapoint = _cur
                        datapoint['field'] = {
                            _field_name: datapoint.pop('value')
                        }
                    else:
                        datapoint['field'][_field_name] = _cur['value']
            else:
                datapoint = groupby_result[field_name]
                datapoint['field'] = {
                    field_name: datapoint.pop('value')
                }
            datapoint['tag'] = {}
            datapoint['ts'] = 0
            yield datapoint
        else:
            this_tagname = result_path[0]
            next_layer = result_path[1:]
            if this_tagname == 'ts':
                add_tag = partial(ResponseParser._add_ts_metric, tag_name=this_tagname)
            elif this_tagname == 'metric':
                add_tag = partial(ResponseParser._add_ts_metric, tag_name=this_tagname)
            else:
                add_tag = partial(ResponseParser._add_tag, tag_name=this_tagname.split('.')[1])
            for bucket in groupby_result[this_tagname]['buckets']:
                this_tagvalue = bucket['key']
                for datapoint in ResponseParser._walk_iter_bucket(bucket, next_layer):
                    add_tag(tag_value=this_tagvalue, datapoint=datapoint)
                    yield datapoint

    @staticmethod
    @deprecated(version='0.0.6', reason="This method is deprecated")
    def _listmydoc(aggr, ignore_keys=('key_as_string',)) -> list:
        """

        :param aggr:
        :param ignore_keys:
        :return:
        """
        rets = []
        for _keyname in aggr.keys():
            for bucket in aggr[_keyname]['buckets']:
                _keyval = bucket.pop('key')
                _fieldval = bucket.pop('doc_count')
                for key in ignore_keys:
                    bucket.pop(key, None)
                if not bucket or ResponseParser._is_value_bucket(bucket):
                    # final bucket
                    if ResponseParser._is_value_bucket(bucket):
                        # bucket like:
                        # {"_fieldname": {"value": "_fieldval"}}
                        _fieldname = list(bucket.keys())[0]
                        _fieldval = bucket.pop(_fieldname)['value']
                        bucket[_fieldname] = _fieldval
                    else:
                        bucket['count'] = _fieldval
                    bucket[_keyname] = _keyval
                    rets.append(bucket)
                else:
                    # maybe son bucket
                    son_aggr = {}
                    _mid = {
                        _keyname: _keyval
                    }
                    for son_k in list(bucket.keys()):
                        if isinstance(bucket[son_k], dict) and 'buckets' in bucket[son_k]:
                            # son bucket
                            son_aggr[son_k] = bucket.pop(son_k)
                        elif isinstance(bucket[son_k], dict) and 'value' in bucket[son_k]:
                            # metric bucket
                            # {"_fieldname": {"value": "_fieldval"}}
                            ret = bucket.pop(son_k)
                            # ret[_keyname] = _keyval
                            _mid[son_k] = ret.pop('value')
                            # rets.append(ret)
                        else:
                            del bucket[son_k]
                    if son_aggr:
                        for son_doc in ResponseParser._listmydoc(son_aggr):
                            son_doc.update(_mid)
                            rets.append(son_doc)
                    else:
                        rets.append(_mid)
        return rets

    @staticmethod
    @deprecated(version='0.0.6', reason="This method is deprecated")
    def _is_value_bucket(bucket):
        """
        Check if bucket is value bucket like:
        {
            "summary": {
                "value": 2323
            }
        }
        :param bucket:
        :return:
        """
        if len(bucket) == 1:
            val_bucket = bucket[list(bucket.keys())[0]]
            if 'value' in val_bucket and len(val_bucket) == 1:
                return True
            else:
                return False
        else:
            return False
