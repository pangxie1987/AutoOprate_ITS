# -*- coding:utf-8 -*-

import os, pymssql,threading,time
from configparser import ConfigParser

def getconfig(section,key):
    #print ('cwd:',os.getcwd())#获得当前工作目录
    config = ConfigParser()
    try:
        config.read('conf.ini')
        return config.get(section, key)
    except Exception,e:
        print (e)
        #print(u'找不到配置文件conf.ini')

class ora_pro(object):
    if os.path.exists('update_log'):
        print(u'update_log已存在')
    else:
        os.mkdir('update_log')
        print(u'update_log创建成功')

    def oracle_process(self):
        '''
        将数据库脚本导入数据库中；
        sqlfile中不能出现中文
        '''

        print('Processing ORACLE_CORE.sql')
        host = getconfig('oracle','host')
        sqlfile = getconfig('oracle','sqlfile')
        isfile=os.path.exists(sqlfile)
        if isfile:

            cmd = 'sqlplus '+host+' @'+sqlfile+'>update_log/core.log'
            print (cmd)
            os.system(cmd)
            print('ORACLE_CORE.sql EXECUTE Sucess')
            time.sleep(1)
        else:
            print('Not Found--->%s'%sqlfile)
            os._exit()

class MsSQL(object):
    '''
    MSSQL操作
    '''
    def __init__(self,host,user,pwd,db):
        self.host=host
        self.user=user
        self.pwd=pwd
        self.db=db

    def _GetConnect(self):
        if not self.db:
            raise(NameError,"Can't Get %s Message!"%self.db)
        self.conn=pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset='utf8')
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,u'Fail to connet %s'%self.host)
        else:
            return cur

    def ExecQuery(self,sql):
        '''
        构造数据库查询函数
        '''
        print('ExecQuery')
        cur=self._GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        print('Sucessd：%s'%sql)

        # 执行完成后关闭连接
        self.conn.close()
        return resList

    def ExecUpdateQuery(self,sql):
        '''
        构造数据库修改函数
        '''
        cur=self._GetConnect()
        cur.execute(sql)
        self.conn.commit()
        print('Sucessd：%s'%sql)
        self.conn.close()

def Oracle_exe():
    '执行Oracle脚本'
    
    ora=ora_pro()
    ora.oracle_process()

def exceuteScript():
    '清理MSSQL数据库，并启动撮合'

    # 调用Script.bat脚本执行深交所模拟撮合
    info=os.system('Script.bat')
    print('Shenzhen Stock Exchange married deal start sucess !')

    ms_oiw = MsSQL(host=getconfig('MsSQL','host'),user=getconfig('MsSQL','user'),pwd=getconfig('MsSQL','password'),db=getconfig('MsSQL','database_oiw'))

    # 查询oiw库
    sel_oiw = 'select * from dbo.ordwth'
    data=ms_oiw.ExecQuery(sel_oiw)
    for i in data:
        print('data:',i)

    # 清理oiw库
    del_oiw = ['delete from dbo.CJHB','delete from dbo.ordwth','delete from dbo.ordwth2']
    for sql in del_oiw:
        ms_oiw.ExecUpdateQuery(sql)
    print('OIW CLearUp Sucess')

    ms_ezstep = MsSQL(host=getconfig('MsSQL','host'),user=getconfig('MsSQL','user'),pwd=getconfig('MsSQL','password'),db=getconfig('MsSQL','database_ezstep'))
    # 查询ezstep库
    sel_ezstep = 'select * from dbo.reqresp'
    data=ms_ezstep.ExecQuery(sel_ezstep)
    for i in data:
        print('data:',i)

    # 清理ezstep库
    del_ezstep= ['delete from dbo.execreport','delete from dbo.pubdata','delete from dbo.reqresp']
    for sql in del_ezstep:
        ms_ezstep.ExecUpdateQuery(sql)
    print('ezstep_dz CLearUp Sucess')


    ms_ezstep_dz = MsSQL(host=getconfig('MsSQL','host'),user=getconfig('MsSQL','user'),pwd=getconfig('MsSQL','password'),db=getconfig('MsSQL','database_dz'))
    # 查询DZ库
    sel_ezstep_dz = 'select * from dbo.reqresp'
    data=ms_ezstep.ExecQuery(sel_ezstep_dz)
    for i in data:
        print('data:',i)

    # 清理DZ库
    del_ezstep_dz= ['delete from dbo.execreport','delete from dbo.pubdata','delete from dbo.reqresp']
    for sql in del_ezstep_dz:
        ms_ezstep.ExecUpdateQuery(sql)
    print('ezstep CLearUp Sucess')

    # 执行竞价库-OIW
    script_exe='''
                declare @i int
                set nocount on
                select @i=1
                while (@i=1)
                begin
                exec ado4alltest
                exec ado4alltest_cd
                end
            '''
       
    t1=threading.Thread(target=ms_oiw.ExecUpdateQuery,args=(script_exe,))
    t1.start()
    print(' OIW is Rinning !')

    # 执行个股期权库-EZSTEP
    script_option='''
                declare @i int
                set nocount on
                select @i=1
                while (@i=1)
                begin
                exec ezstep_myret
                end
                
                '''
    # ms_ezstep.ExecUpdateQuery(script_option)
    t2=threading.Thread(target=ms_ezstep.ExecUpdateQuery,args=(script_option,))
    print('EZSTEP is Rinning !')
    t2.start()
    

# if __name__=='__main__':
#     main()
