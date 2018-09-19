# -*- coding:utf-8 -*-
'''
仿造监控客户端，实现系统的一键启停
'''
import cx_Oracle,time
import pkgutil
import logging,time
from oracle_excute import getconfig

# def getconfig(section,key):
#     #print ('cwd:',os.getcwd())#获得当前工作目录
#     config = ConfigParser()
#     try:
#         config.read('conf.ini')
#         return config.get(section, key)
#     except Exception,e:
#         print (e)
#         #print(u'找不到配置文件conf.ini')


logname=time.strftime('%H-%M-%S')
print(logname)
def loginit():
    '''
    #定义日志格式，并将日志同时向屏幕输出并写入文件
    '''
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    #datefmt='%a, %d %b %Y %H:%M:%S',
                    datefmt= '%Y-%m-%d %H:%M:%S',
                    filename=logname+'.log',
                    filemode='w')
    #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


loginit()
logger=logging.getLogger(__name__)

class AutoStart(object):
    def __init__(self):
        try:
            logger.info('Oracle connecting>>>>>>>>>')
            self.conn=cx_Oracle.connect(getconfig('oracle','host'))
            
        except Exception,e:
            logger.info(e)
            raise e
        else:
            self.curs=self.conn.cursor()
            logger.info('Operating ORACLE :%s'%(getconfig('oracle','host')))

            self.group_ids=[]

    def Start(self,type):
        '''
        启动/停止函数
        '''
        # 从its_monitor_modules查询所有的设备信息
        logger.info('Strating Server.....')
        sql_modules='select start_index, group_id, device_id, device_name from its_monitor_modules where monitor_enabled = 1 order by start_index'
        self.curs.execute(sql_modules)
        rows=self.curs.fetchall()
        logger.info(rows)
        for row in rows:
            logger.info('group_id:%s'%row[1])
            self.group_ids.append(row[1])
            logger.info('device_id:%s'%row[2])
            # print(codetype)
            # print('device_name------》正在启动:%s'%(row[3].decode(codetype['encoding'])))
            if type==2001:

                logger.info('Staring------>>:%s'%(row[3]))
            else:
                logger.info('Stoping------>>:%s'%(row[3]))
            # print('group_id:%s'%row[1])
            # print('device_id:%s'%row[2])
            group_id=row[1]
            device_id=row[2]
            time.sleep(0.5)

            # 根据group_id，device_id查询设备详细信息
            # group_id=27
            # device_id=1

            sql_one="SELECT GROUP_ID, DEVICE_ID, MONITORS_ERVER_IP, MODULE_START_PATH, MODULE_START_NAME, MODULE_START_PARAMETER, AUTO_RESTART_ENABLED,DEVICE_TYPE,DEVICE_NAME FROM ITS_MONITOR_MODULES WHERE GROUP_ID = %s AND DEVICE_ID = %s AND MONITOR_ENABLED>0 "%(group_id,device_id)

            self.curs.execute(sql_one)
            deivices=self.curs.fetchall()
            for device in deivices:
                # print(device)
                monitors_erver_ip=device[2]
                module_start_path=str(device[3])
                module_start_name=str(device[4])
                if str(device[5])=='None':
                    module_start_parameter=''
                else:
                    module_start_parameter=str(device[5])
                    
                auto_restart_enabled = str(device[6])

                delete_all_enable='1'  #清流操作的定义
                device_type=str(device[7])
                time.sleep(0.5)


                # 查询最大的msg_index，后续插入使用
                sql_index="select p.msg_index from its_monitor_message p order by p.msg_index desc"
                self.curs.execute(sql_index)
                index=self.curs.fetchone()

                max_index=int(index[0]+1)
                # print('max_index=',max_index)

                # 构造启动/停止时插入its_monitor_message的sql串
                #type=2001   #启动2001  停止2003
                text=str(str(group_id)+'|'+str(device_id)+'|'+module_start_path+'|'+module_start_name+'|'+module_start_parameter+'|'+auto_restart_enabled+'|'+delete_all_enable+'|'+device_type)
                logger.info('text:%s'%text)
                status=0  #默认状态为0
                strtime=time.strftime('%Y%m%d%H%M%S')
                # print(time)
                sql_insert="insert into its_monitor_message values(:msg_index,:monitors_erver_ip,:type,:text,:status,:strtime)"
    
                value={'msg_index':max_index,
                        'monitors_erver_ip':monitors_erver_ip,
                        'type':type,
                        'text':text,
                        'status':status,
                        'strtime':strtime}
                # print('insert value:%s'%value)
                # print('sql_insert:',sql_insert)


                resback=self.curs.execute(sql_insert,value)
                logger.debug(sql_insert)
                logger.debug(value)
                # print('resback:%s'%resback)
                self.conn.commit()

                # 报盘启动时，默认延时40S
                if group_id==51 and type==2001:
                    logger.info('OrderCentral Delay 30S To Start')
                    time.sleep(40)
                else:
                    time.sleep(1)
        if type==2001:
            logger.info('<<------->>ALL Start Sucess<<------->>')
        else:
            logger.info('<<------->>ALL Stop Sucess<<------->>')
            time.sleep(10)



    def ExecCoreUpLoad(self,condition,businissno):
        '''
        开市操作,向cmn_sync_msg_upload写入约定的开市类型
        此方法为获取这些数据
        '''
        # 获取最大的msgno
        sql_msgno=" select core.fc_nb('cmn_sync_msg_upload_id') from dual"
        self.curs.execute(sql_msgno)
        msgnos=self.curs.fetchone()
        msgno_max=msgnos[0]

        # 将开市操作插入上场表
        sql_upload="insert into cmn_sync_msg_upload values(:msgno, :tablename, :condition, :status, :createtime,:finishtime, :errmsg, :sessionid, :businissno, :operation_type)"


        createtime=time.strftime('%Y%m%d%H%M%S')
        values_ip={'msgno':msgno_max,
                    'tablename':'null',
                    'condition':condition,
                    'status':'0',
                    'createtime':createtime,
                    'finishtime':createtime,
                    'errmsg':'null',
                    'sessionid':msgno_max,
                    'businissno':businissno,
                    'operation_type':0}

        # 期货/期权核心开市
        self.curs.execute(sql_upload,values_ip)
        logger.debug(sql_upload,values_ip)
        self.conn.commit()

    # 主键串
    condition='0','3'
    #证券 上场/初始化
    businissno_S='74114','8230' 
    #个股期权 上场/初始化
    businissno_O='74117','143106'
    #期货/商品期权 上场/初始化
    businissno_F='74115','143105'
    #黄金核心 上场/初始化
    businissno_G='74118','208641'


    def ExecCoreUpLoadStart(self):
        '''
        进行初始化和开市的操作
        '''
        print('group_ids',self.group_ids)

        # 期货核心  根据设备配置中是否有50组
        if 50 in self.group_ids:
            self.ExecCoreUpLoad(0,74115)
            self.ExecCoreUpLoad(3,143105)
            logger.info('futures_trade_server Upload Sucess')
        else:
            logger.info('NO futures_trade_server')

        # 现货
        if 25 in self.group_ids:
            self.ExecCoreUpLoad(0,74114)
            self.ExecCoreUpLoad(3,8230)
            logger.info('securities_trade_server Upload Sucess')
        else:
            logger.info('NO securities_trade_server')

        # 个股期权
        if 52 in self.group_ids:
            self.ExecCoreUpLoad(0,74117)
            self.ExecCoreUpLoad(3,143106)
            logger.info('stock_options_trade_server Upload Sucess')
        else:
            logger.info('NO stock_options_trade_server')

        # 黄金
        if 70 in self.group_ids:
            self.ExecCoreUpLoad(0,74115)
            self.ExecCoreUpLoad(3,143105)
            logger.info('gold_trade_server Upload Sucess')
        else:
            logger.info('NO gold_trade_server')
    
    def closeconnect(self):
        '''
        关闭ORALCE建立的连接，释放资源
        '''
        self.conn.close()

# tostart=AutoStart()

# # 一键停止
# tostart.Start(2003)

# # 一键启动
# tostart.Start(2001)

# # 进行必要的延时  等待全部上场完成后才能进行开市操作
# time.sleep(20)
# tostart.ExecCoreUpLoadStart()



