# encoding:utf-8

import urllib3, json
from urllib.parse import urlencode
from urllib3.response import HTTPResponse


class HttpError(Exception):
  def __init__(self, msg):
    super().__init__(self)
    self.msg = msg

  def __str__(self) -> str:
    return self.msg


class Request(object):
  """
  进一步封装urllib3的接口, 直接提供GET, POST, PUT, DELETE接口, body全部使用json格式
  """

  def __init__(self):
    self.http = urllib3.PoolManager()
    self.UTF8 = 'utf-8'

  def get(self, url: str, **params: dict) -> HTTPResponse:
    """
    http GET method
    :param url: URL
    :param params: http request params. should be class's dict. e.g., url.Request.get('https://example.com', **object.__dict__)
                   if your define a dict variable, you just use it like, url.Request.get('https://example.com', **dict)
    :return:
    """
    if params is not None:
      return self.http.request('GET', url, fields = params)
    else:
      return self.http.request('GET', url)

  def put(self, url: str, body: object = None, **params: dict) -> HTTPResponse:
    """
    http PUT method
    :param url: URL
    :param body: put body. one object
    :param params: http request params
    :return:
    """
    if params is not None:
      url += '?' + urlencode(params)
    if body is not None:
      return self.http.request('PUT', url, body = json.dumps(body.__dict__),
                               headers = {'Content-Type': 'application/json'})
    else:
      return self.http.request('PUT', url)

  def post(self, url: str, body: object, **params: dict) -> HTTPResponse:
    """
    http POST method
    :param url: URL
    :param body: post body. one object
    :param params: http request params
    :return:
    """
    if body is None:
      raise HttpError('POST request\'s body can not be None')
    if params is not None:
      url += '?' + urlencode(params)

    return self.http.request('POST', url, body = json.dumps(body.__dict__),
                             headers = {'Content-Type': 'application/json'})

  def delete(self, url: str, **params: dict) -> HTTPResponse:
    """
    http DELETE method
    :param url: URL
    :param params: http request params
    :return:
    """
    if params is not None:
      return self.http.request('DELETE', url, fields = params)
    else:
      return self.http.request('DELETE', url)
