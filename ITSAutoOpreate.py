# -*- coding:utf-8 -*-

'''
运维脚本的主函数,实现一键停止，清理MSSQL，维护ORALCE脚本，一键启动动能
协助自动化环境自动运维
'''
import time
from MonitorClient import AutoStart,logger
from oracle_excute import ora_pro,MsSQL,exceuteScript

def main():
    tostart=AutoStart()
    input = int(raw_input('your command!>0-quit,1-auto,2-start,3-stop\n'))
    while 1:
        if input == 1:

            # 一键停止2003
            tostart.Start(2003)

            # 执行MSSQL和ORALCE清理工作
            exceuteScript()

            # 一键启动2001
            tostart.Start(2001)

            # 进行必要的延时  等待全部上场完成后才能进行开市操作
            time.sleep(20)
            tostart.ExecCoreUpLoadStart()

            # 释放oralce连接
            tostart.closeconnect()
        elif input == 2:
            # 一键启动2001
            tostart.Start(2001)
            # 进行必要的延时  等待全部上场完成后才能进行开市操作
            time.sleep(20)
            tostart.ExecCoreUpLoadStart()
        
        elif input == 3:
            # 一键停止2003
            tostart.Start(2003)
        else:
            logger.info('Quit....!')
            break

if __name__=='__main__':
    main()

