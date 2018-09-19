rem 调用远程机器上的系统任务，执行深交所模拟撮合程序

echo:正在开启深交所模拟撮合
schtasks /run /s 10.243.140.218 /u its /p Passw0rd@218 /tn ShenZhen_script

exit