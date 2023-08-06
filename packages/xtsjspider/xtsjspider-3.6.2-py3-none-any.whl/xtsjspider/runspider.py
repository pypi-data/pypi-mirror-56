import os
from xtsjspider.abnormal import abnorm


def run_spider():

    project_name = input("请输入项目名称(英文)")
    path = os.getcwd() + '\\' + project_name

    data = """from xtsjspider.dispatcher.starte import XtSpider, InsetUrls
from xtsjspider.downloader.HTTP import HttpRequest
from xtsjspider.model.modeler import Model


class StartUrl(InsetUrls):
    '''
    在此处添加，爬虫的开始URL可以多个，写入start_url中, 可以多个
    '''
    start_url = []


class %sSpider(XtSpider):

    def parse(self, response):
        '''
        在此处添加爬虫解析代码，最后返回一个可迭代对象。 response为爬虫解析体。
        '''
        pass

    def open_data(self, item):
        '''
        在此处添加爬虫保存代码，无需返回。
        :param item: 数据对象可以使用 item.name，获取name的数据
        :return: None
        '''
        pass
        """ % project_name.capitalize()

    stars = """from %s import StartUrl, %sSpider


if __name__ == '__main__':
    start = StartUrl()

    for i in range(0, 3):  # 更改添加进程数
        spider = %sSpider()
        spider.start()
""" % (project_name, project_name.capitalize(), project_name.capitalize())

    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)
    else:
        raise abnorm.FilesIsTin

    with open(path + '\\' + project_name + '.py', 'w', encoding="utf-8") as fn:
        fn.write(data)

    with open(path + '\\' + 'start.py', 'w', encoding='utf-8') as fn:
        fn.write(stars)

