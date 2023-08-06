from lxml import etree


class XpathParser(object):
    def __init__(self, text, xpath_count):
        self.count = xpath_count
        self.text = text

    def run(self):
        '''
        返回xpath对象
        :return:
        '''
        data = etree.HTML(self.text)
        rest = data.xpath(self.count)
        return rest
