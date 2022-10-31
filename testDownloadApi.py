"""
Time : 2021/1/13 11:33 
Author : Rex
File : testDownloadApi.py 
Software: PyCharm
"""
import requests
from threading import Thread
import time
import json


def print_time():
    count = 1
    while 1:
        print(f'程序正在运行，已等待{count}s')
        time.sleep(1)
        count+=1

def sendRequest(file_name):
    url = "https://cardiac.vivalnk.com/api/data/full_ecg?sensorId=ECGRec_201942/C830021&start=1609893837772&end=1609980237000"
    payload={}
    headers = {"accessKey": "sejefpnsddsn","secretKey": "psttZOf3UwBr3jdH"}
    thread=Thread(target=print_time)
    thread.setDaemon(True)
    thread.start()
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response)
    with open(f'./ECG{file_name}.txt','w',encoding='utf-8')as f:
        f.write(response.text)
t_list=[]
for i in range(1):
    t=Thread(target=sendRequest,args=(i,))
    t.start()
    print(t.getName()+"已启动")
    t_list.append(t)
for k in t_list:
    k.join()

# if __name__ == '__main__':
#     # with open()
#     pass