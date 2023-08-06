#-*-coding:utf-8-*-

'''
对字符串的各种解析方式
'''

from DbStructSync.common.logger  import Logger
import  re

logger = Logger()

def parse_str(string):
    '''
    解析括号内的内容   aaaaa(adfdfdf)kjkjk，获取（）里面的内容
    :param sql:
    :return:
    '''
    logger.info('需要进行括号内内容提取的数据是{}'.format(string))
    p1 = re.compile(r'[(](.*)[)]', re.S)
    result = re.findall(p1,string)
    logger.info('提取完之后的数据是{}'.format(result))
    return result  # 这里取 1 ： -1 主要是为了将解析完的前后 []去掉


def lists2str(temp_lists):
    '''
    将list的元素逐个进行strip处理，然后返回一个拼接的字符串
    :param temp_lists:
    :return:
    '''
    if not isinstance(temp_lists, list):
        raise  TypeError('类型不是list,请确认{}'.format('lists2str'))
    logger.info('需要转换为str的list是{}'.format(temp_lists))
    for temp_list in temp_lists:
       return  ''.join(temp_list.strip())

def parse_comma_split(temp_str):
    '''
    只对括号外的数据进行指定格式的拆分:按照,分割： cc,d(a,b),ee,解析结果为cc d(a,b) ee
    :param sql:
    :return:
    '''
    #print(sql)
    result = re.split(r",(?![^(]*\))", temp_str)
    return result

def parse_space_split(temp_str):
    '''
    只对括号外的数据进行指定格式的拆分:按照,分割： cc,d(a,b),ee,解析结果为cc d(a,b) ee
    :param sql:
    :return:
    '''
    new_result=[]
    result = re.split(r" (?![^(]*\))", temp_str)
    logger.info('通过空格解析完的数据{}'.format(result))
    for item in result:
        if item.endswith("'") and item.startswith("'"):
             new_result.append(item)
        elif item.endswith("'"):
            new_result.append(item[:-1])
        elif item.startswith("'"):
            new_result.append(item[1:])
        else:
            new_result.append(item)
    logger.info('通过空格解析完的数据{}'.format(new_result))
    return new_result