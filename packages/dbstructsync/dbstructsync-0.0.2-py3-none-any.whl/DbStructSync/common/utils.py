#-*-coding:utf-8-*-

import  yaml
import  os
def yaml_loader(yaml_path=None,yaml_value=None):
    '''
    加载yaml文件，并返回yaml文件中的内容,默认返回全部内容
    :param yaml_path:
    :return:
    '''
    filepath = os.path.dirname(__file__)
    print(filepath)
    filenamepath = os.path.split(os.path.realpath(__file__))[0]
    print(filenamepath)
    yaml_path = os.path.join(filenamepath,'config.yaml')
    if os.path.isdir(yaml_path) or os.path.isfile(yaml_path):
           f = open(yaml_path,'r',encoding='utf-8')
           result = yaml.load(f.read())
    if yaml_value is not None:
           keys = yaml_value.split('.')
           if len(keys)==1:
               result=result.get(keys[0])
           elif len(keys)==2:
               result = result.get(keys[0]).get(keys[1])
    return  result

if __name__ == '__main__':
     x=yaml_loader(yaml_value='dbconfig.source')
     print(x)

