import queue

from xtsjspider.abnormal import abnorm
from xtsjspider.downloader.HTTP import HttpRequest
from xtsjspider.model.modeler import Model
import threading

URL_MANAGER = queue.Queue(999999)


# 普通调度器
class RunSpider(object):
    start_url = None

    def __init__(self):
        if self.start_url is not None:
            URL_MANAGER.put(self.start_url)
            urls = self.insert_url()  # 添加爬虫url
            if not isinstance(urls, list):
                raise abnorm.InsertUrlNotList

            for url in urls:
                URL_MANAGER.put(url)

            self.scheduling()  # 开始调度
        else:
            raise abnorm.StartUrlNotNone  # 抛出异常

    def scheduling(self):
        while not URL_MANAGER.empty():  # URL没有空间了结束
            response = HttpRequest(URL_MANAGER.get()).get()
            data = self.start(response)  # 调用用户方法

            # 根据用户方法进行调用,并且释放空间

            if isinstance(data, Model):  # 调用保存方法
                self.open_data(data.__dict__)
                del data

            elif isinstance(data, HttpRequest):  # 下载器方法
                URL_MANAGER.put(data.url)
                print(data)
                del data

    def open_data(self, data, *args):
        '''

        :param args: 用户自定义保留爬虫方法。
        :return: None
        '''
        pass

    def insert_url(self):
        '''
        用户定义
        :return: 返回一个list , 用于添加url
        '''
        return []

    def start(self, response):
        '''
        该方法给用户重定义
        :param response: HttpResponse对象
        :return: 返回模型类， 或者HttpRequest类
        '''
        pass


# 加强版，推服调度器
class XtSpider(threading.Thread):
    # start_url = []  # 定义开始爬虫方法，可以多个

    def __init__(self):
        '''
        初始化多线程
        '''
        threading.Thread.__init__(self)

    def run(self):
        self.scheduling()  # 开始调度

    def scheduling(self):
        # 调用开始

        while not URL_MANAGER.empty():  # 队列不为空
            request = URL_MANAGER.get()  # 获取数据

            if request.method == 'get':
                response = request.get()
                response.encoding("utf-8")   # 确定编码
            else:
                response = request.post()
                response.encoding("utf-8")  # 确定编码

            try:
                res = getattr(self, response.deliver)(response)  # 获取parse返回
            except AttributeError:
                raise abnorm.NotParse

            for rs in res:  # 判断返回类型，重复调度
                if isinstance(rs, HttpRequest):
                    URL_MANAGER.put(rs)

                elif isinstance(rs, Model):
                    self.open_data(rs)

    def parse(self, response):
        return []

    def open_data(self, item):
        pass


class InsetUrls(object):
    start_url = []

    def __init__(self):
        '''
        开始URL，添加get的HttpResponse对象入库
        '''
        for url in self.start_url:
            response = HttpRequest(url)

            self.install_url(response)

    def install_url(self, list_data):
        '''
        :param list_data: HttpResponse类
        :return: None
        '''

        if isinstance(list_data, str):
            raise abnorm.NotDataStr

        URL_MANAGER.put(list_data)


def install_url(list_data):
    '''
    根据用户提供列表添加爬虫队列
    :param list_data: 用户添加URL列表
    :return: None
    '''
    if isinstance(list_data, list):
        raise abnorm.InsertUrlNotList

    for url in list_data:
        if isinstance(url, HttpRequest):
            raise abnorm.NotInsertHttpRequest

        URL_MANAGER.put(url)