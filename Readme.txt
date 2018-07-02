1、实现的功能：自动停止->清理MSSQL库->启动MSSQL现货撮合->启动深交所撮合->自动开始->自动开市；
2、脚本介绍：oracle_excute.py实现Oracle和MSSQL的处理；MonitorClient.py实现自动启停工作；
    Script.bat实现深交所模拟撮合的启停工作；ITSAutoOpreate.py主函数文件；
3、模块安装：cx_Oracle，pymssql；
4、运行方式：conf.ini进行相关配置->python ITSAutoOpreate.py;
5、警告：设计文件存放的目录不能有中文；python-Version 2.7.14