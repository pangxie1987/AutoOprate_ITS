# -*- coding:utf-8 -*-
# https://www.cnblogs.com/Tempted/p/7485629.html

'''
linux windows 远程操作
'''

import wmi,time,os
import paramiko,sys
import re
import time
from oracle_excute import getconfig

class Linux(object):
    '''
    在Linux远程机上执行命令
    '''
    def __init__(self, ip, port, user, passwd, timeout=30):
        self.ip = ip
        self.port = port
        self.user = user
        self.passwd = passwd
        self.timeout = timeout
        self.t = ''
        self.chan = ''
        # 失败后重连次数
        self.try_time = 3

    def connect(self):
        '''
         Linux Remote
        '''
        while True:
            try:
                self.t = paramiko.Transport(self.ip, self.port)
                self.t.connect(username=self.user, password=self.passwd)
                self.chan = self.t.open_session()
                self.chan.settimeout(self.timeout)
                self.chan.get_pty()
                self.chan.invoke_shell()
                print ('%s Connect Sucess!'%self.ip)
                print (self.chan.recv(65535).decode('utf-8'))
                return
            except Exception, e1:
                if self.try_time != 0:
                    print('%sConnect Failed，Try Again'%self.ip)
                    self.try_time -= 1
                else:
                    print('Three Times Tryed, Over')
                    exit(1)

    def close(self):
        'close connect'
        self.chan.close()
        self.t.close()

    def send(self, cmd):
        'send cmd'
        cmd += "\r"
        #通过命令提示符判断命令是否执行完成
        p = re.compile(r':~ #')

        result = ''
        # 发送要执行的命令
        self.chan.send(cmd)
        time.sleep(5)
        # 回显很长的命令可能执行较久，通过循环分批次取回回显
        ret = self.chan.recv(65535)
        
        print(ret)
        # print('指令%s成功'%cmd)
        # while True:
        #      time.sleep(0.5)
        #      ret = self.chan.recv(65535)
        #      # ret = ret.decode('utf-8')
        #      result += ret
        #      if p.search(ret):
        #          print result
        #          return result


def sys_version(ipadress,user,pw):
    '''
    windows 远程操作
    '''
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
            print(u'%s 执行完成'%file)
            print(resback)

    except Exception,e:
        print(e)


def Linux_remote():
    ip = getconfig('linux','host')
    port = getconfig('linux','port')
    username = getconfig('linux','username')
    password = getconfig('linux','passwd')
    cmd = getconfig('linux', 'cmd')
    host = Linux(ip, port, username, password)
    host.connect()
    #host.send("./its/Clearup")
    host.send(cmd)
    host.close()

if __name__ == '__main__':
    Linux_remote()