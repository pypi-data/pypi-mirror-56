#-*-coding:utf-8-*-

# a_list=["\n  `order_journal_id` bigint(20) NOT NULL COMMENT '定投订单流水id',\n  `order_id` bigint(20) NOT NULL COMMENT '订单id',\n  `account_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '投资人账户id',\n  `journal_type` int(11) NOT NULL DEFAULT '0' COMMENT '流水类型',\n  `in_out` int(11) NOT NULL DEFAULT '0' COMMENT '1 进账  0出账',\n  `amount` decimal(14,2) NOT NULL DEFAULT '0.00' COMMENT '金额',\n  `order_balance` decimal(14,2) NOT NULL DEFAULT '0.00' COMMENT '订单可用余额',\n  `credit_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '债权id',\n  `business_time` bigint(20) NOT NULL DEFAULT '0' COMMENT '业务发生时间',\n  `create_time` bigint(20) NOT NULL DEFAULT '0' COMMENT '创建时间',\n  `modify_time` bigint(20) NOT NULL DEFAULT '0' COMMENT '修改时间',\n  `journal_desc` varchar(1024) NOT NULL COMMENT '摘要',\n  `remark` varchar(1024) NOT NULL COMMENT '备注',\n  `is_delete` int(11) NOT NULL DEFAULT '0' COMMENT '逻辑删除',\n  PRIMARY KEY (`order_journal_id`),\n  KEY `Idx_investment_account_id` (`account_id`) USING BTREE,\n  KEY `Idx_investment_order_id` (`order_id`) USING BTREE,\n  KEY `Idx_investment_credit_id` (`credit_id`) USING BTREE\n"]
#
#
# x=str(a_list).split('\\n')
# for i in x:
#     print(i)

string='''
CREATE TABLE `order_journal_20` (
  `order_journal_id` bigint(20) NOT NULL COMMENT '定投订单流水id',
  `order_id` bigint(20) NOT NULL COMMENT '订单id',
  `account_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '投资人账户id',
  `journal_type` int(11) NOT NULL DEFAULT '0' COMMENT '流水类型',
  `in_out` int(11) NOT NULL DEFAULT '0' COMMENT '1 进账  0出账',
  `amount` decimal(14,2) NOT NULL DEFAULT '0.00' COMMENT '金额',
  `order_balance` decimal(14,2) NOT NULL DEFAULT '0.00' COMMENT '订单可用余额',
  `credit_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '债权id',
  `business_time` bigint(20) NOT NULL DEFAULT '0' COMMENT '业务发生时间',
  `create_time` bigint(20) NOT NULL DEFAULT '0' COMMENT '创建时间',
  `modify_time` bigint(20) NOT NULL DEFAULT '0' COMMENT '修改时间',
  `journal_desc` varchar(1024) NOT NULL COMMENT '摘要',
  `remark` varchar(1024) NOT NULL COMMENT '备注',
  `is_delete` int(11) NOT NULL DEFAULT '0' COMMENT '逻辑删除',
  PRIMARY KEY (`order_journal_id`),
  KEY `Idx_investment_account_id` (`account_id`) USING BTREE,
  KEY `Idx_investment_order_id` (`order_id`) USING BTREE,
  KEY `Idx_investment_credit_id` (`credit_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
import  re
import  argparse
import  sys
def main():
    '''
    parse command line options and run commands
    :return:
    '''

    parser = argparse.ArgumentParser(description='description')

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

    # parser.add_argument(
    #     "--source", dest="source_dict" , action= StoreDictKeyPair,
    #     metavar="KEY1=VAL1,KEY2=VAL2,KEY3=VAL3...", required=True
    # )

    args = parser.parse_args()

    print(args.only_index)
    print(args.only_file)
    print(args.source_dict)
    #print(args.sourcedb)
    print(type(args.source_dict))

class  StoreDictKeyPair(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
         my_dict={}
         for kv in values.split(","):
             k,v = kv.split("=")
             my_dict[k] = v
         setattr(namespace, self.dest, my_dict)
test_dict={}
test_dict['a']=1

if test_dict.get('b',None):
    print('error')
import  site
print(site.getsitepackages())
# if __name__ == '__main__':
#      sys.exit(main())