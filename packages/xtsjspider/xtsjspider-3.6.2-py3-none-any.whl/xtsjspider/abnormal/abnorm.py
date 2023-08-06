class NotDataStr(Exception):
    '''
    data异常
    '''
    def __str__(self):
        return "输入的数据应该是str类型"


class StartUrlNotNone(Exception):
    '''
    start_url异常
    '''

    def __str__(self):
        return "开始Url不可以为空"


class InsertUrlNotList(Exception):
    '''
    添加url错误
    '''

    def __str__(self):
        return "不是list"


class NotInsertHttpRequest(Exception):
    '''
    添加url时，添加的不是HttpRequest对象
    '''

    def __str__(self):
        return "添加URL应该是一个HttpRequest对象"


class FilesIsTin(Exception):
    '''
    文件已经存在
    '''

    def __str__(self):
        return "项目文件以及存在"


class NotParse(Exception):
    '''
    没有这个解析方法错误
    '''

    def __str__(self):
        return "没有这个解析方法,请检查解析名是否有问题"
