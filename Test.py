# # '''
# # Testfile 
# # '''
# # print('hello')
# # import time

# # msecond=time.time()
# # print(int(round(msecond * 1000)))
# # print(len((round(msecond * 1000))))

# print('input please>\n')
# data=raw_input()
# print(type(data))
# if data=='a':
#     print('a')
# else:
#     print('b')
import json

with open ('conf.json') as fileconf:
    data=json.load(fileconf)

print(data['host'])