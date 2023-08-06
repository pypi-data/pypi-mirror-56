#-*-coding:utf-8-*-

'''

将解析出来的数据写入到sql文件中
'''
import  sys
import  os

def write_to_files(file_path = None, result_dict = None):

    if result_dict is None:
        return
    if not isinstance( result_dict, dict):
        raise  TypeError('传入的result_dict 不是dict类型，请确认')
    if file_path is None:
        file_path = os.path.dirname(__file__)
    file_path = os.path.join(file_path,'diff.sql')

    with open(file_path,'w+') as f :
        for key , values in result_dict.items():
              f.writelines('use {};\n'.format(key))
              for  key, value in values.get('source').items():
                   #key 为表名，value 里包含 index ， fields
                   if key =='create_table':
                       for item in value:
                          f.writelines(''.join(item)+';\n')
                       continue
                   if value.get('index',None):
                      for item in value['index']:
                         f.writelines(''.join(item)+";\n")
                   if  value.get('fields',None):
                       for item in  value['fields']:
                         f.writelines(''.join(item)+";\n")



