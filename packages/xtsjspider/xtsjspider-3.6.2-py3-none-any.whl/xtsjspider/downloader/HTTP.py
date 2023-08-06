import json

import requests

from xtsjspider.parsers.pare import XpathParser


# 静态下载
class HttpRequest(object):
    method = 'get'  # 请求反式
    post_data = None
    params = None

    def __init__(self, url, headers=None, method='get', deliver='parse'):
        '''
        初始化请求类
        :param url: 请求url
        :param headers: 请求头
        '''
        self.method = method
        self.deliver = deliver
        self.url = url
        if not headers:
            self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                              " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
            }
        else:
            self.headers = headers

    def get(self, params=params):
        '''
        发送get请求
        :param params: get的请求参数
        :return: requst对象
        '''
        response = requests.get(self.url, params=params, headers=self.headers)

        return HttpResponse(response, self.deliver)

    def post(self, data=post_data):
        '''
        发送post请求
        :param data: post数据
        :return: request对象
        '''
        if self.post_data:
            if isinstance(self.post_data, dict):
                data = self.post_data

        response = requests.post(self.url, data=data)
        return HttpResponse(response, self.deliver)

    def set_mobile(self):
        '''
        模拟手机
        :return: None
        '''
        self.headers = {
            "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko)'
            ' Version/6.0 Mobile/10A403 Safari/8536.25'
        }


# 动态下载
class AnalogBrowser(object):
    pass


# 返回对象
class HttpResponse(object):

    def __init__(self, response, deliver):
        '''
        创建httpresponse对象
        :param response:
        '''
        self.text = response.text  # 源代码
        self.status_code = response.status_code  # 状态码
        self.url = response.url  # 请求url
        self.headers = response.headers  # 头部信息
        self.content = response.content
        self.cookie = dict(response.cookies)
        self.deliver = deliver

    @property
    def json(self):
        '''
        序列化，格式不支持返回None
        :return: data
        '''
        try:
            data = json.loads(self.text)
        except json.decoder.JSONDecodeError:
            data = None

        return data

    def encoding(self, code):
        text = self.text.encode()
        self.text = text.decode(code)

    def xpath(self, xpath_content):
        '''
        构建xpath对象
        :param xpath_content: xpath语法
        :return: None
        '''
        xpath = XpathParser(self.text, xpath_content)
        xpath = xpath.run()

        return xpath

    def re_path(self, re_content):
        '''
        构建正则法则对象
        :param re_content:  re语法
        :return: None
        '''
