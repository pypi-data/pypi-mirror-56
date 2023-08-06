#-*-coding:utf-8-*-


from DbStructSync.common.utils import  yaml_loader
from DbStructSync.common.logger import  Logger
from DbStructSync.db_syns import  get_db_tabls, get_db_alltables_desc, diff_tables, get_db_table_desc, diff_indexs_fields,dict2sql
from   DbStructSync.save_tofiles import  write_to_files
comp_result_dict={}
logger = Logger()

def  run(args=None):

    if args is not None and  args.source_db and args.target_db:
         sourcedb = args.source_db
         targetdb = args.target_db
    else:
        sourcedb = yaml_loader(yaml_value='dbconfig.source')
        targetdb = yaml_loader(yaml_value='dbconfig.target')

    logger.info('从yaml中加载的源库配置{}，目标库配置{}'.format(sourcedb, targetdb))

    sourcetables = get_db_tabls(sourcedb)
    targettables = get_db_tabls(targetdb)
    logger.info('获取到的源库表数据{}， 目标库表数据{}'.format(sourcetables, targettables))

    diff_tables_dict = diff_tables(sourcetables, targettables)


    comp_result_dict[sourcedb['db']] = {}
    comp_result_dict[sourcedb['db']]['source'] = {}
    comp_result_dict[sourcedb['db']]['target'] = {}
    for key, values in diff_tables_dict.items():
        source_sql = []
        target_sql = []
        if key == 'source' and values:
            for value in values:
                db_desc_sql = get_db_table_desc(sourcedb, value)
            source_sql.append(db_desc_sql)
            logger.info('源库新建表的sql {}'.format(source_sql))
            comp_result_dict[sourcedb['db']]['source'].update({'create_table': source_sql})
        if key == 'target' and values:
            for value in values:
                db_desc_sql = get_db_table_desc(targetdb, value)
            target_sql.append(db_desc_sql)
            logger.info('目标库新建表的sql{}'.format(target_sql))
            # comp_result_dict[targetdb['db']].update({'target':{'table_create':target_sql}})
            comp_result_dict[targetdb['db']]['target'].update({'create_table': target_sql})
    # 其他相同的表，需要进行近一步的字段、索引的比较

    logger.info('剩余相同的表，进行字段和索引的比较')
    same_table_source_dict = get_db_alltables_desc(sourcedb, list(diff_tables_dict['same']))
    same_table_target_dict = get_db_alltables_desc(targetdb, list(diff_tables_dict['same']))
    for table , table_desc_sql in same_table_source_dict.items():
        # comp_result_dict[sourcedb['db']]['source'][table]={}

        source_table_sql = table_desc_sql[1]
        target_table_sql = same_table_target_dict[table][1]
        logger.info('source_table_sql 的类型{} 内容{}'.format(type(source_table_sql), source_table_sql))
        logger.info('same_table_target_dict 内容{}'.format(same_table_target_dict[table][1]))
        if   args is not None  and  not args.only_fields:
            diff_ind = diff_indexs_fields(source_table_sql, target_table_sql,type=1)

            index_dict_source = {}
            index_dict_source[table] = {}
            index_dict_target = {}
            index_dict_target[table] = {}

            for key, values in diff_ind.items():

                if key == 'source' and values['index']:
                    # index_dict_source[table].update({'add_index':values['index']})
                    comp_result_dict[sourcedb['db']]['source'][table] = {}
                    comp_result_dict[sourcedb['db']]['source'][table]['index'] = values['index']
                # if key =='target' and values:
                #      index_dict_target[table].update({'add_index':values['index']})
                #      comp_result_dict[targetdb['db']]['target'].update(index_dict_target[table])
        if args is not None and not  args.only_index :
            diff_fid = diff_indexs_fields(source_table_sql, target_table_sql, type=2)
            fields_dict_source = {}
            fields_dict_source[table] = {}
            # fields_dict_source[table]['fields']={}

            for key, values in diff_fid.items():
                #print('values ---{}'.format(values))
                if key == 'source' and values['fields']:
                    comp_result_dict[sourcedb['db']]['source'][table] = {}
                    comp_result_dict[sourcedb['db']]['source'][table]['fields'] = {}
                    # fields_dict_source[table]['fields']['add']= values['fields']['lose']
                    # fields_dict_source[table]['fields']['modify'] = values['fields']['modify']

                    # fields_dict_source[table]['fields'] ={}
                    if values['fields'].get('lose', None):
                        comp_result_dict[sourcedb['db']]['source'][table]['fields']['lose'] = values['fields']['lose']
                    if values['fields'].get('modify', None):
                        comp_result_dict[sourcedb['db']]['source'][table]['fields']['modify'] = values['fields']['modify']
                # if key =='target' and values:
                #      fields_dict_target[table].update({'add_field':list(values)})
                #      comp_result_dict[targetdb['db']]['target'].update(fields_dict_target[table])

    result = dict2sql(comp_result_dict)
    logger.info('最终比对结果为{}'.format(result))
    #将具体的数据，写入sql文件中
    write_to_files(result_dict=result)


if __name__ == '__main__':
     run()