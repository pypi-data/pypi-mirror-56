#-*-coding:utf-8-*-

import  argparse
from DbStructSync import __description__
from DbStructSync.main import run
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

def mains():
    '''
    parse command line options and run commands
    :return:
    '''

    parser = argparse.ArgumentParser(description=__description__)

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


    run(args)

if __name__ == '__main__':
    sys.exit(mains())