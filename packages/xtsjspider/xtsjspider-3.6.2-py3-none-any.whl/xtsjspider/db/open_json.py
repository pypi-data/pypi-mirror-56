import json


def timely_json(model, name, ensure_ascii=False):
    '''
    及时保存json格式
    :param model: 数据
    :param name: 名字
    :return: None
    '''
    data = json.dumps(model, ensure_ascii=ensure_ascii)
    with open(name + '.json', 'a', encoding='utf-8') as fp:
        fp.write(data + ',' + '\n')
