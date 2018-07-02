# -*- coding:utf-8 -*-
# https://www.cnblogs.com/Tempted/p/7485629.html

'''
linux windows 远程操作处理，测试用
'''

import wmi,time,os
import paramiko,sys

def ssh_cmd(ip,port,cmd,user,passwd):
    '''
    Linux远程
    '''
    result = ""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,port,user,passwd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        print result
        ssh.close()
    except:
        print "ssh_cmd err."
    return result

# ssh_cmd('10.243.140.218','2000','start','its',"Passw0rd@218")

def sys_version(ipadress,user,pw):
    conn=wmi.WMI(computer=ipadress,user=user,password=pw)
    for sys in conn.Win32_OperatingSystem():
        print('Version:%s'%sys.Caption.encode('utf-8'),'Vernum:%s'%sys.BuildNumber)  #系统信息
        # print('系统位数：%s'%sys.OSArchitecture)   #系统的位数
        # print('系统进程：%s'%sys.NumberofProcesses)    #系统的进程

    try:
        filename=['C:\its\深模拟撮合\3_start.bat','C:\its\深模拟撮合\Test.bat']
        # cmd_callbat=['cd C:\its\深模拟撮合','start bpdemo.prg /B']
        for file in filename:
            
            cmd_callbat=r'cmd /c call %s'%file
            # cmd_callbat=r'start '+file
            print(cmd_callbat)
            process_id,resback=conn.Win32_Process.Create(cmd_callbat)  #执行bat
            time.sleep(1)
            print('%s 执行完成'%file)
            print(resback)

    except Exception,e:
        print(e)

# sys_version ("10.243.140.218","ksadmin",'Kayak2018!')