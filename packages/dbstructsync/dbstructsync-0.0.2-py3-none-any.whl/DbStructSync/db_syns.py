#-*-coding:utf-8-*-

#-*-coding:utf-8-*-

'''
对数据库表结构：表， 字段，索引对同步，将不同更新的sql语句
流程：比较两个目标库的表，如果表有不一致，形成创建表的sql
     表相同后，再比较表与表之间的不一致： 字段不一致， 索引不一致
{'db':
       'source':{'table1':{'update':[update sql1, update sql2],
                 'delete':[delete sql1, delete sql2],
                 'add':[add sql1, add sql2],
                 'index_update':[],
                 'index_delete':[],
                 'index_add':[]
                 },
       'create':[create table 1, create table 2],
       'drop':[drop table 1, drop table 2]
                 }}}
'''

from DbStructSync.common.utils import yaml_loader
from DbStructSync.common.logger import  Logger
from DbStructSync.common.parse import  parse_str, parse_space_split, parse_comma_split, lists2str
import  copy
logger = Logger()
#两个库比较结果
comp_result_dict={}

import  pymysql
import  re
from  DbStructSync.common.mysql_conn import create_connection



def get_db_table_desc(db, table):
    '''
    获取数据库表对描述sql
    :param db: 数据库
    :param table: 具体对表
    :return: 返回一个表对 create 表的sql
    '''
    logger.info('开始获取表{}的描述语句'.format(table))
    tables_desc = []
    with  create_connection(**db) as conn:
        db_table_desc_sql = "show create table  {}".format(str(table).replace("'", ''))
        conn.execute(db_table_desc_sql)
        tables_desc.append(conn.fetchone())

    return tables_desc[0][1]

def get_db_alltables_desc(db:dict , tables:list = None):
    '''
    批次将库里所有表的数据都查出来，减少与数据库之间的交互
    :param db:
    :param tables:
    :return:
    '''
    # TODO 需要进行调试
    if tables is None:
        tables = get_db_tabls(db)
    tables_dict={}
    with create_connection(**db) as conn:
         for table in tables:
           db_table_desc_sql = "show create table {}".format(str(table).replace("'",''))
           conn.execute(db_table_desc_sql)
           tables_dict[table] = conn.fetchone()
    return  tables_dict


def get_db_tabls(db):
    logger.info('开始获取数据库{}的所有表信息'.format(db))
    tables_list = []
    with  create_connection(**db) as conn:
        db_sql = 'show tables'
        conn.execute(db_sql)
        for x in conn.fetchall():
            tables_list.append(x[0])
    return tables_list



def compare_indexs_field(source, target, type=1):
    '''
    比较两个index的区别
    :param source:'KEY `Idx_order_record_invest_account_id` (`invest_account_id`) USING BTREE'
    :param targe: 'KEY `Idx_order_record_invest_account_id` (`invest_account_id`) USING BTREE'
    :param type: type=1 是索引， type=2是字段
    :return: dict

    比较field的时候与比较index有点区别，index可以直接删除了进行重建，不影响表里数据
    但field 需要了解到具体是少字段，还是字段有差异，少字段需要add column， 有差异需要modify column
    '''
    if not isinstance(source, list) or not isinstance(target, list):
          raise  TypeError('传入的field 或者index 类型不是list，请确认')
    result={}
    result['source'] = {}
    result['source']['fields']={}
    result['target'] = {}
    result['target']['fields']={}
    if type ==1:
        logger.info('开始索引的比较，源表索引{}，目标表索引{}'.format(source, target))
        source_diff = set(source) - set(target)
        target_diff = set(target) - set(source)

        result['source']['index'] = source_diff  # source存在，但target不存在的
        result['target']['index'] = target_diff   # target存在，但source不存在的
        logger.info('索引比较的结果{}'.format(result))
    elif type ==2 :
        '''对字段进行比较'''
        logger.info('开始字段的比较，源字段{}目标字段{}'.format(source, target))
        # 第一步解析，拿出具体对字段名
        target_fields_list=[]
        for  tar in target:
            target_fields_list.append(tar.split()[0])
        # 第二步进行比较取出不同对字段
        diff_field  = set(source) - set(target)
        # 比较第二部的结果与第一步的结果，确认这个字段是缺失还是类型差异
        lose_fields=[]
        modify_fields=[]
        for diff in list(diff_field):
            diff_fie = diff.split(' ')[0]
            if diff_fie in target_fields_list:
                modify_fields.append(diff)
            else:
                lose_fields.append(diff)
        if lose_fields:
            result['source']['fields']['lose']= lose_fields
        if  modify_fields:
            result['source']['fields']['modify'] = modify_fields
        logger.info('字段比较的结果为{}'.format(result))


    return  result


def  diff_indexs_fields(sourcesql, targetsql, type=1):
    '''
    :param sourcesql: 源数据库表的创建sql
    :param targetsql: 目标数据表的创建sql
    :return: 记录下索引不一致的地方
    '''
    result = {}
    logger.info('解析语句中的索引字段，并进行比较索引')
    sourcesql = parse_str(sourcesql)  # 从括号中提取需要的内容
    #logger.info('从括号中提取出来的信息数据{}'.format(sourcesql))
    sourcesql = lists2str(sourcesql)  #将list转换为str，并对数据的空格数据进行处理
    logger.info('解析完的数据的信息{}'.format(sourcesql))
    sourcesql = sourcesql.split('\n') #将str按照'\\n'进行分割
    logger.info('解析完数据之后的信息{}'.format(sourcesql))
    targetsql = parse_str(targetsql)
    targetsql = lists2str(targetsql)
    targetsql = targetsql.split('\n')
    if type ==1:
        source_index = parse_fields(sourcesql,type)
        target_index = parse_fields(targetsql,type)

        result= compare_indexs_field(source_index, target_index, type)
    elif type ==2:
        source_field_sql = parse_fields(sourcesql, type)
        target_field_sql = parse_fields(targetsql, type)
        result = compare_indexs_field(source_field_sql, target_field_sql, type)
    return  result




def diff_others(sourcesql,targetsql):
     pass


def parse_fields(sql_lists, type=2):
    result_list = []
    if type ==2 : #默认为对字段对处理
        for sql in sql_lists:
            # 先对sql进行空格过滤
            sql = sql.strip()
            if sql.startswith('`'):
                # 只对普通对fields进行处理，将每个字段用 'COMMENT'进行分割，只比较前面对字段，不比较comment 字段
                final = sql.split('COMMENT')
                result_list.append(final[0].strip())
    if type ==1 :  # 对index进行处理
        for sql in sql_lists:
            # 先对sql进行空格过滤
            sql = sql.strip()
            #sql=parse_comma_split(sql)
            if sql.startswith('KEY') or sql.startswith('PRIMARY KEY') or sql.startswith('UNIQUE KEY'):
                # 只对普通对fields进行处理，将每个字段用 'COMMENT'进行分割，只比较前面对字段，不比较comment 字段
                result_list.append(sql)
    return result_list

# def parse_sql(sql):
#     '''
#     解析括号内的内容   aaaaa(adfdfdf)kjkjk，获取（）里面的内容
#     :param sql:
#     :return:
#     '''
#
#     p1 = re.compile(r'[(](.*)[)]', re.S)
#     result = re.findall(p1,sql)
#     return str(result)[6:-4]  # 这里取 1 ： -1 主要是为了将解析完的前后 []去掉

# def parse_split(sql):
#     '''
#     只对括号外的数据进行指定格式的拆分:按照,分割： cc,d(a,b),ee,解析结果为cc d(a,b) ee
#     :param sql:
#     :return:
#     '''
#     #print(sql)
#     result = re.split(r",(?![^(]*\))", sql)
#     return result

# def parse_space_split(sql):
#     '''
#     只对括号外的数据进行指定格式的拆分:按照,分割： cc,d(a,b),ee,解析结果为cc d(a,b) ee
#     :param sql:
#     :return:
#     '''
#     #print(sql)
#     result = re.split(r" (?![^(]*\))", sql)
#     return result


def diff_tables(sourcetable, targettable):
    '''

    :param sourcetable:  源数据库的表名列表
    :param targettable:  目的数据库的表名列表
    :return: 返回dict，包含三种结果，源库多的表，目标库多的表，相同的表
    '''
    logger.info('开始比较两个库中表的差异,源库表{}，目标库表{}'.format(sourcetable, targettable))
    table_result={}
    if not isinstance(sourcetable, list) or not isinstance(targettable, list):
         raise  TypeError('sourcetable , targettable的类型不是list')
    source_diff = set(sourcetable) - set(targettable)
    target_diff = set(targettable) - set(sourcetable)
    same_tables = set(sourcetable)& set(targettable)
    table_result['source'] = source_diff
    table_result['target'] = target_diff
    table_result['same'] = same_tables
    logger.info('两个库中表的差异结果{}'.format(table_result))
    return  table_result


def dict2sql(dict_str):
    '''
    将解析完成的数据转换为对应的可执行sql
    :param dict_str:
    :return:
    '''

    dict_str = copy.deepcopy(dict_str) # 做一个深度copy，可以放心的进行相关数据处理

    if not isinstance(dict_str, dict):
        raise  TypeError('调用方法{}参数不是dict类型，请确认'.format('dict2sql'))

    #dict_str={'investment': {'source': {'create_table': ['CREATE TABLE `test_async` (\n  `test_async` varchar(30) NOT NULL,\n  `aa` varchar(400) DEFAULT NULL,\n  PRIMARY KEY (`test_async`)\n) ENGINE=InnoDB DEFAULT CHARSET=utf8'], 'order_record': {'index': {'KEY `idx_aa` (`fee`)', 'KEY `Idx_order_record_asset_type` (`asset_type`,`bbbb`),'}}, 'channel_auto_publish_conf': {'index': {'KEY `index_channel` (`channel_num`,`channel_product`) USING BTREE'}}, 'order_depository': {'index': {'KEY `idx_order_depository_order_id` (`order_id`) USING BTREE'}}, 'order_transfer_auditing_limit': {'fields': {'modify': ["`type` int(11) NOT NULL DEFAULT '100'"]}}}, 'target': {}}}

    #获取db名字
    for key ,value in dict_str.items():
        dbname = key
        logger.info('数据库名{}'.format(dbname))

        for table, table_desc  in  value.get('source').items():
               if table =='create_table':
                   #create_table_sql = lists2str(table_desc)
                   dict_str[dbname]['source'][table] = table_desc
                   #其他的都是table的名字
                   logger.info('数据库的修改语句:{}'.format(table_desc))
               else:
                  logger.info('对于索引和字段的解析原始数据{}'.format(table_desc))
                  if table_desc.get('index'):
                      create_index_sql_lists=[]
                      #create_index_sql_lists.append('use {};'.format(dbname))
                      index_lists= (table_desc.get('index'))

                      result_index= parse_comma_split(str(index_lists)[1:-1])
                      for i in result_index:
                           if i.strip().startswith('\'KEY'):
                               #print(i.strip())
                               index_values = parse_space_split(i.strip())
                               drop_index_sql= 'drop index {} on {}'.format(index_values[1],table )
                               if len(index_values)<=3:
                                  create_index_sql='create index {} on {}{} '.format(index_values[1], table, index_values[2])
                               else:
                                  create_index_sql='create index {} on {}{} {}'.format(index_values[1], table, index_values[2], ' '.join(index_values[3:]))
                               create_index_sql_lists.append(drop_index_sql)
                               create_index_sql_lists.append(create_index_sql)

                           if i.strip().startswith('\'UNIQUE KEY'):
                                 index_values = parse_space_split(i.strip())
                                 drop_index_sql = 'drop index {} on {}'.format(index_values[2], table)
                                 if len(index_values) <= 4:
                                     create_index_sql = 'create unique index {} on {}{} '.format(index_values[2], table,
                                                                                          index_values[3])
                                 else:
                                     create_index_sql = 'create unique index {} on {}{} {}'.format(index_values[2], table,
                                                                                               index_values[3],
                                                                                               ' '.join(index_values[4:]),
                                                                                               )

                                 create_index_sql_lists.append(drop_index_sql)
                                 create_index_sql_lists.append(create_index_sql)
                      logger.info('表{}解析出来的索引的修改sql{}'.format(table, create_index_sql_lists))

                      dict_str[dbname]['source'][table]['index'] = create_index_sql_lists

                  if table_desc.get('fields'):
                      create_fields_sql_lists=[]
                      #create_fields_sql_lists.append('use {};'.format(dbname))
                      modify_field_sqls = table_desc.get('fields').get('modify',None)
                      create_field_sqls=table_desc.get('fields').get('lose',None)

                      if modify_field_sqls:
                           for modify_field_sql in modify_field_sqls:

                               sql_indexs = parse_space_split(str(modify_field_sql)[0:-1])
                               #print(sql_indexs)
                               alter_fields_sql='alter table {} modify column {} {} {}'.format(table, sql_indexs[0],sql_indexs[1],' '.join(sql_indexs[2:]))

                               create_fields_sql_lists.append(alter_fields_sql)
                      if create_field_sqls:
                           for  create_field_sql in create_field_sqls:
                                sql_indexs = parse_space_split(str(create_field_sql)[0:-1])

                                create_fields_sql='alter table {} add column {} {}'.format(table, sql_indexs[0],' '.join(sql_indexs[2:]))
                                create_fields_sql_lists.append(create_fields_sql)
                      logger.info('表{}解析出来的字段的修改sql{}'.format(table,create_fields_sql_lists))
                      dict_str[dbname]['source'][table]['fields'] = create_fields_sql_lists

    return  dict_str  # 返回给一个全部是可执行sql的dict









if __name__ == '__main__':
    pass
    # sourcedb = yaml_loader(yaml_value='dbconfig.source')
    # targetdb = yaml_loader(yaml_value='dbconfig.target')
    #
    # print(targetdb)
    # sourcetables  = get_db_tabls(sourcedb)
    # targettables = get_db_tabls(targetdb)
    # print('拿到的源表：{}'.format(sourcetables))
    # print('拿到的目标表{}'.format(targettables))
    #
    # diff_tables_dict = diff_tables(sourcetables, targettables)
    # print('不同的表{}'.format(diff_tables_dict))
    # print('获取不同表的的创建sql')
    # comp_result_dict[sourcedb['db']]={}
    # comp_result_dict[sourcedb['db']]['source']={}
    # comp_result_dict[sourcedb['db']]['target']={}
    # for key , values   in diff_tables_dict.items():
    #     source_sql=[]
    #     target_sql=[]
    #     if key =='source' and values :
    #          for value in values:
    #            db_desc_sql = get_db_table_desc(sourcedb, value)
    #          source_sql.append(db_desc_sql)
    #          print('源表造表的sql{}'.format(source_sql))
    #          comp_result_dict[sourcedb['db']]['source'].update({'create_table':source_sql})
    #     if key=='target' and values:
    #          for value in values:
    #             db_desc_sql = get_db_table_desc(targetdb, value)
    #          target_sql.append(db_desc_sql)
    #          print('目标表造表的sql{}'.format(target_sql))
    #          #comp_result_dict[targetdb['db']].update({'target':{'table_create':target_sql}})
    #          comp_result_dict[targetdb['db']]['target'].update({'create_table':target_sql})
    # print(comp_result_dict)
    # #其他相同的表，需要进行近一步的字段、索引的比较  TODO
    # #diff_tables_dict['same']=('order_depository',)
    # for  table in list(diff_tables_dict['same']):
    #     #comp_result_dict[sourcedb['db']]['source'][table]={}
    #
    #     source_table_sql = get_db_table_desc(sourcedb, table)
    #     target_table_sql = get_db_table_desc(targetdb, table)
    #     diff_ind = diff_indexs(source_table_sql, target_table_sql)
    #     diff_fid = diff_fields(source_table_sql, target_table_sql)
    #
    #
    #     index_dict_source={}
    #     index_dict_source[table]={}
    #     index_dict_target={}
    #     index_dict_target[table]={}
    #
    #
    #     for key ,values in diff_ind.items():
    #
    #         if key =='source' and values['index']:
    #              #index_dict_source[table].update({'add_index':values['index']})
    #              comp_result_dict[sourcedb['db']]['source'][table] ={}
    #              comp_result_dict[sourcedb['db']]['source'][table]['index'] = values['index']
    #         # if key =='target' and values:
    #         #      index_dict_target[table].update({'add_index':values['index']})
    #         #      comp_result_dict[targetdb['db']]['target'].update(index_dict_target[table])
    #
    #     fields_dict_source={}
    #     fields_dict_source[table]={}
    #     #fields_dict_source[table]['fields']={}
    #
    #     for key ,values in diff_fid.items():
    #         print('values ---{}'.format(values))
    #         if key =='source' and values['fields']:
    #              comp_result_dict[sourcedb['db']]['source'][table]={}
    #              comp_result_dict[sourcedb['db']]['source'][table]['fields']={}
    #              # fields_dict_source[table]['fields']['add']= values['fields']['lose']
    #              # fields_dict_source[table]['fields']['modify'] = values['fields']['modify']
    #
    #              #fields_dict_source[table]['fields'] ={}
    #              if values['fields'].get('lose',None):
    #                 comp_result_dict[sourcedb['db']]['source'][table]['fields']['lose'] = values['fields']['lose']
    #              if values['fields'].get('modify',None):
    #                 comp_result_dict[sourcedb['db']]['source'][table]['fields']['modify'] = values['fields']['modify']
    #         # if key =='target' and values:
    #         #      fields_dict_target[table].update({'add_field':list(values)})
    #         #      comp_result_dict[targetdb['db']]['target'].update(fields_dict_target[table])
    # print(comp_result_dict)
    #
    # dict2sql(comp_result_dict)

