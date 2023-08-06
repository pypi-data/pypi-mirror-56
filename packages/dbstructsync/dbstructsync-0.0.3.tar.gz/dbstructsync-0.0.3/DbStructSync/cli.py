#-*-coding:utf-8-*-

import  argparse
#from DbStructSync import __description__
from DbStructSync.main_entrance import  run
import  sys
class  StoreDictKeyPair(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
         my_dict={}
         for kv in values.split(","):
             k,v = kv.split("=")
             if k =='port':
                 my_dict[k] = int(v)
             else:
                 my_dict[k] = v
         setattr(namespace, self.dest, my_dict)


def db_sync(sourcedb, targetdb):
    '''
    需要传入两个参数，分别为soure数据库 和 target数据库
    :param args:{'host':'','port':123,'user':'','passwd':'','db':''}
    :return:
    '''

    if not isinstance(sourcedb, dict) or not isinstance(targetdb,dict):
        raise TypeError('传入的参数类型错误')
    if sourcedb.get('host',None) is None or sourcedb.get('port',None) is None or sourcedb.get('user',None) is None or sourcedb.get('passwd',None) is None or sourcedb.get('db',None) is None :
        raise  KeyError('缺少参数host, port,user, passwd,db 中的一个参数')
    if targetdb.get('host',None) is None or targetdb.get('port',None) is None or targetdb.get('user',None) is None or targetdb.get('passwd',None) is None or targetdb.get('db',None) is None :
        raise  KeyError('缺少参数host, port,user, passwd,db 中的一个参数')
    return run(sourcedb=sourcedb, targetdb=targetdb)



def db_sync_commandline():
    '''
    parse command line options and run commands,给用户提供的命令行的操作
    :return:
    '''

    parser = argparse.ArgumentParser(description='')

    parser.add_argument(
        '-V','--version', dest='version', action='store_true', help='show version'
    )
    parser.add_argument(
        '--only-file', action='store_true', default=True,
        help='only generate the sql file include difference '
    )

    parser.add_argument(
        '--only-index', action='store_true', default=False,
        help='only generate the sql file include index difference'
    )

    parser.add_argument(
        '--only-fields', action='store_true', default=False,
        help='only generate the sql file include table fields difference'
    )

    parser.add_argument(
        '--source', dest='source_db', action=StoreDictKeyPair, metavar='host=xx,port=xx,user=xx,passwd=xx,db=xx', required=True
    )

    parser.add_argument(
        '--target', dest='target_db',action=StoreDictKeyPair, metavar='host=xx,port=xx,user=xx,passwd=xx,db=xx',required=True
    )
    args = parser.parse_args()


    return run(args)


if __name__ == '__main__':
    # x=db_sync({'host':'10.1.1.32','port':33306,'user':'root','passwd':'root','db':'investment'},
    #         {'host': '10.1.1.37', 'port': 33306, 'user': 'root', 'passwd': 'root', 'db': 'investment'}
    #         )
    # print(x)
    pass