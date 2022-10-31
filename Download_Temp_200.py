#!/usr/bin/env python 
# coding:utf-8
import threading

import requests
import hashlib
import time
import json
import os
from threading import Thread
all_temp_data = []
class DownloadTemp:
    global all_temp_data
    def __init__(self,write_path):
        self.write_path = write_path

    def download_temp_foreign(self,sn,start_time,end_time,location,type,trigger):
        '''
        下载国外服务器温度数据,缓存设备温度数据
        :param sn: 设备号
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param location: 是否返回定位信息
        :param type: 0是原始温度  1是算法温度  2是两种温度都返回
        :return: json的体温数据
        '''
        host = "http://cadent.us-west-1.elasticbeanstalk.com"
        base_url = host + "/ohin1/api/fever_scout/temperature"
        #一天86,400,000毫秒
        total_time = end_time - start_time
        if total_time / 86400000 <= 1:
            # 未超过一天
            temp_data = self.download_temp_request(base_url, sn, start_time, end_time, location, type, trigger)
            trigger.emit("本次下载已完成")
            with open(self.write_path + '/finall_result.txt', 'a+') as f:
                for data in range(len(temp_data) - 1):
                    end_tick = temp_data[data + 1]["recordTime"]
                    start_tick = temp_data[data]["recordTime"]
                    delta = end_tick - start_tick
                    timeArray = time.localtime(temp_data[data]['recordTime'] / 1000)
                    f_recordTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    f.write("{},{},{},{}".format(str(temp_data[data]['recordTime']), str(temp_data[data]['raw']),
                                                 f_recordTime, str(delta)) + '\n')
                start_tick = temp_data[-1]["recordTime"]
                timeArray2 = time.localtime(start_tick / 1000)
                f_recordTime2 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray2)
                f.write("{},{},{}".format(str(temp_data[-1]['recordTime']), str(temp_data[-1]['raw']), f_recordTime2))
                trigger.emit("文件分析完成")

        else:

            thread_list = []

            # 超过一天，需要算出来具体一共有几天
            int_day = total_time // 86400000
            # 求出不满一天部分共有多少秒
            day = total_time - int_day * 86400000
            for i in range(int_day):
                thread = Mythread(self.download_temp_request,
                                  args=(base_url, sn, start_time, start_time + 86400000, location, type, trigger))
                thread.start()

                e_time = start_time + 86400000
                start_time += 86401000
                thread_list.append(thread)
                thread.join()

            temp_data = self.download_temp_request(base_url, sn, start_time, start_time + day, location, type,
                                                   trigger)
            if temp_data == None:
                pass
            else:
                for data in temp_data:
                    all_temp_data.append(data)
            trigger.emit("本次下载已完成")
            all_temp_data.sort(key=lambda f: f["recordTime"])
            # print(all_temp_data)
            with open(self.write_path + '/finall_result.txt', 'a+') as f:
                for data in range(len(all_temp_data) - 1):
                    end_tick = all_temp_data[data + 1]["recordTime"]
                    start_tick = all_temp_data[data]["recordTime"]
                    delta = end_tick - start_tick
                    timeArray = time.localtime(all_temp_data[data]['recordTime'] / 1000)
                    f_recordTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    f.write(
                        "{},{},{},{}".format(str(all_temp_data[data]['recordTime']), str(all_temp_data[data]['raw']),
                                             f_recordTime, str(delta)) + '\n')
            with open(self.write_path + '/finall_result.txt', 'a+') as file:
                start_tick = all_temp_data[-1]["recordTime"]
                timeArray2 = time.localtime(start_tick / 1000)
                f_recordTime2 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray2)
                file.write("{},{},{}".format(str(all_temp_data[-1]['recordTime']), str(all_temp_data[-1]['raw']),
                                             f_recordTime2))
                trigger.emit("文件分析完成")
            return all_temp_data

    def download_temp_domestic(self,sn,start_time,end_time,location,type,trigger):
        '''
        下载国内服务器温度数据
        :param sn: 设备号
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param location: 是否返回定位信息
        :param type: 0是原始温度  1是算法温度  2是两种温度都返回
        :return:
        '''
        host = "http://ohin1.cn-northwest-1.eb.amazonaws.com.cn"
        base_url = host + "/api/fever_scout/temperature"
        total_time = end_time - start_time
        if total_time / 86400000 <= 1:
            # 未超过一天
            temp_data = self.download_temp_request(base_url, sn, start_time, end_time, location, type, trigger)
            trigger.emit("本次下载已完成")
            with open(self.write_path + '/finall_result.txt', 'a+') as f:
                for data in range(len(temp_data)-1):
                    end_tick = temp_data[data + 1]["recordTime"]
                    start_tick = temp_data[data]["recordTime"]
                    delta = end_tick - start_tick
                    timeArray = time.localtime(temp_data[data]['recordTime']/1000)
                    f_recordTime=time.strftime("%Y-%m-%d %H:%M:%S",timeArray)
                    f.write("{},{},{},{}".format(str(temp_data[data]['recordTime']), str(temp_data[data]['raw']),
                                                 f_recordTime, str(delta)) + '\n')
                start_tick = temp_data[-1]["recordTime"]
                timeArray2 = time.localtime(start_tick/1000)
                f_recordTime2 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray2)
                f.write("{},{},{}".format(str(temp_data[-1]['recordTime']),str(temp_data[-1]['raw']),f_recordTime2))
                trigger.emit("文件分析完成")

        else:

            thread_list = []
            # 超过一天，需要算出来具体一共有几天
            int_day = total_time // 86400000
            # 求出不满一天部分共有多少秒
            day = total_time - int_day * 86400000
            for i in range(int_day):
                thread = Mythread(self.download_temp_request,args=(base_url, sn, start_time, start_time+86400000, location, type, trigger))
                thread.start()


                e_time=start_time+86400000
                start_time += 86401000
                thread_list.append(thread)
                thread.join()

            temp_data = self.download_temp_request(base_url, sn, start_time,start_time+day, location, type,
                                                   trigger)
            if temp_data == None:
                pass
            else:
                for data in temp_data:

                    all_temp_data.append(data)
            trigger.emit("本次下载已完成")
            all_temp_data.sort(key=lambda f: f["recordTime"])
            # print(all_temp_data)
            with open(self.write_path + '/finall_result.txt', 'a+') as f:
                for data in range(len(all_temp_data)-1):
                    end_tick = all_temp_data[data + 1]["recordTime"]
                    start_tick = all_temp_data[data]["recordTime"]
                    delta = end_tick - start_tick
                    timeArray = time.localtime(all_temp_data[data]['recordTime']/1000)
                    f_recordTime=time.strftime("%Y-%m-%d %H:%M:%S",timeArray)
                    f.write("{},{},{},{}".format(str(all_temp_data[data]['recordTime']), str(all_temp_data[data]['raw']),
                                                 f_recordTime, str(delta)) + '\n')
            with open(self.write_path + '/finall_result.txt', 'a+') as file:
                start_tick = all_temp_data[-1]["recordTime"]
                timeArray2 = time.localtime(start_tick/1000)
                f_recordTime2 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray2)
                file.write("{},{},{}".format(str(all_temp_data[-1]['recordTime']),str(all_temp_data[-1]['raw']),f_recordTime2))
                trigger.emit("文件分析完成")
            return all_temp_data

    def download_temp_request(self,url,sn,start_time,end_time,location,type,trigger):
        # snID = sn.replace(".", "_")

        snID = sn
        query_param_dict = {
            "device_sn": sn,
            "start_millis": start_time,
            # start_millis to end_millis is a closed interval
            "end_millis": end_time,
            # 是否上传经纬度
            "location": location,
            "type": type
        }
        # self.Download_Temp_Log(query_param_dict)
        trigger.emit(str(query_param_dict))
        secret_key = "Dr4AYxlucfju1FLuonJNkH1Y+K23Xij3"
        headers_dict = {
            "accessKey": "eyxsPS67mtB7EoTKOcE5tE4Fu"
        }

        query_param_dict = self.generate_query_params(query_param_dict, secret_key)
        start = time.time()
        response = requests.get(url, params=query_param_dict, headers=headers_dict)
        # self.Download_Temp_Log(f"Completed in {round(time.time() - start, 3)} seconds")
        trigger.emit(f"Completed in {round(time.time() - start, 3)} seconds")
        print(response.content)
        json_dict = json.loads(response.content)
        json_data = json_dict["data"]
        json_temp = json_data["temperatures"]

        json_temp.sort(key=lambda f: f["recordTime"])
        if self.write_path != '':
            file_name = os.path.join(self.write_path, f"{snID}_{start_time}_{end_time}.log")
            # self.Download_Temp_Log('温度数据存储在:'+file_name)
            if os.path.exists(file_name):
                print(f"{file_name} exists")
                with open(file_name) as input:
                    return json.load(input)
            else:
                with open(file_name, "w") as output:
                    json.dump(json_temp, output)
        else:
            # self.Download_Temp_Log('没有选择存储的文件夹')
            trigger.emit('没有选择存储的文件夹')
        return json_temp

    def generate_signature(self,query_param_dict, secret_key):
        target_str = ''
        # Concatenate the parameters in ascending order of key
        sorted_key = sorted(query_param_dict.keys())
        for key in sorted_key:
            target_str += f"&{key}={query_param_dict[key]}"
        # Remove the first character '&'
        target_str = target_str[1:]
        # Append secret key
        target_str += secret_key
        md5 = hashlib.md5()
        md5.update(target_str.encode(encoding='utf-8'))
        return md5.hexdigest()

    def generate_query_params(self,query_param_dict, secret_key):
        sign = self.generate_signature(query_param_dict, secret_key)
        query_param_dict["sign"] = sign
        return query_param_dict

class Mythread(threading.Thread):
    global all_temp_data
    def __init__(self,func,args=()):
        super().__init__()
        self.func=func
        self.args=args

    def run(self):
        self.result=self.func(*self.args)
        for data in self.result:
            all_temp_data.append(data)



if __name__ == '__main__':
    print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(1610502393.443)))


