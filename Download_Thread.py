#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2022/10/30 4:23 下午
# @Author  : Rex
#!/usr/bin/env python
# coding:utf-8
import time
import datetime
import requests
import json
from threading import Thread
import threading
from selenium import webdriver
from queue import Queue


# all_hour_data = []
class download_data():
    exclude_fields=["patchInfo","magnification","rwl","rri","acc","ecg","pi","waveform"]

    def __init__(self, write_path, trigger, tenant,server="Production"):
        self.write_path = write_path
        self.trigger = trigger
        self.tenantId = None
        self.tenantKey = None
        self.tenant=tenant
        # self.draw = draw
        self.server = server
        self.URL = None
        self.get_url()
        self.token = self.get_token()
        self.queue = Queue()
        self.all_hour_data = []
        self.thread_count = 0
        # self.data_type=data_type
        self.lock = threading.Lock()

    # 根据不同的服务器选择接口
    def get_url(self):
        if self.server == "Production":
            self.URL = "https://vcloud2.vivalink.com/"
            self.tenantId="6170706009be6b1f2045cbac77"
            self.tenantKey="Whn_Nla;UtMLt@uUsQL]PDLx^?h46n<ri?v`K[@D"
        elif self.server == "Test":
            self.URL = "https://vcloud-test.vivalink.com/"
            self.tenantId = "617070e40daf63ba334ece90d1"
            self.tenantKey = "@baIevnyO<iqo<r5L5VYK0BH[CFvJXUf0W4Y;WZF"
        else:
            self.URL = "https://vcloud-swe.vivalnk.com/"

    # 获取token
    def get_token(self):
        self.trigger.emit("正在获取token")
        url = self.URL + 'auth'
        params = {'id': self.tenantId, "key": self.tenantKey}
        while True:
            try:
                res = requests.post(url, data=json.dumps(params))
                print(res.json())
                if res.json()['code'] == 200 and res.json()['message'] == 'OK':
                    self.trigger.emit("获取token成功")
                    return res.json()['data']['token']
                else:
                    self.trigger.emit("获取token失败")
                    time.sleep(2)
                    self.trigger.emit("尝试重新获取token")
                    self.get_token()
            except Exception as e:
                print(e)
                self.trigger.emit("获取token失败")
                time.sleep(2)
                self.trigger.emit("尝试重新获取token")
                continue

    def download(self, sn, start, end):
        self.Segmentation_time(start, end)
        self.trigger.emit(f"本次每轮下载启动线程数:{self.thread_count}")
        # 当队列不为空时循环取队列里的内容
        while not self.queue.empty():
            thread_list = []
            for i in range(self.thread_count):
                if not self.queue.empty():
                    data = self.queue.get()
                    request_start = data['start']
                    request_end = data['end']
                    downloadthead=DownloadThead(sn, request_start, request_end,self.server,self.trigger,self.queue,self.write_path,self.token,self.tenant)
                    downloadthead.start()
                    # self.trigger.emit(f"线程{downloadthead.getName()}启动成功")
                    thread_list.append(downloadthead)
                else:
                    break
            for t in thread_list:
                t.join()
                self.lock.acquire()
                # 将所有1小时数据整合到一起
                self.all_hour_data+=t.get_hour_data()
                self.lock.release()

        if len(self.all_hour_data) != 0:
            self.write_file(self.all_hour_data, end, start,sn)

        else:
            print("本次下载时间区间无数据")
            self.trigger.emit("本次下载时间区间无数据")

    def write_file(self, hour_data, end, start,sn):
        all_hour_data = sorted(hour_data, key=lambda r: r['recordTime'])
        with open(self.write_path + '/finall_result.txt', "a+") as f:
            if sn.startswith("ECG"):
                missing = int((end - start) / 1000 - len(all_hour_data))
                print(f"totally {missing} seconds missing")
                self.trigger.emit(f"totally {missing} seconds missing")
            for fields in all_hour_data[0]:
                if fields in self.exclude_fields:
                    pass
                else:
                    f.write(fields+",")
            f.write("format_time,")
            f.write("time_interval")
            f.write('\n')
            # f.write("{},{},{},{},{},{},{}".format("time_stamp", "format_time", "time_interval",
            #                                       "HR", "LeadOn", "flash", "patchBattery" + '\n'))
            for i in range(len(all_hour_data) - 1):
                end_tick = all_hour_data[i + 1]["recordTime"]
                start_tick = all_hour_data[i]["recordTime"]
                # patch_battery = all_hour_data[i]["patchBattery"]
                # hr = all_hour_data[i]['hr']
                # flash = all_hour_data[i]['flash']
                # patchBattery = all_hour_data[i]['patchBattery']
                delta = end_tick - start_tick
                start_str = datetime.datetime.fromtimestamp(start_tick / 1000).strftime('%Y-%m-%d %H:%M:%S')
                end_str = datetime.datetime.fromtimestamp(end_tick / 1000).strftime('%Y-%m-%d %H:%M:%S')
                for key in  all_hour_data[i]:
                    if key in self.exclude_fields:
                        pass
                    else:
                        f.write(str(all_hour_data[i][key])+",")
                f.write(str(start_str)+",")
                f.write(str(delta))
                f.write('\n')
                # leadOn = all_hour_data[i]['leadOn']
                # f.write("{},{},{},{},{},{}".format(str(all_hour_data[i]['recordTime']), start_str, str(delta),
                #                                       str(hr), str(leadOn), str(flash) + '\n'))
                if sn.startswith("ECG"):
                    if abs(delta) < 500:
                        print(f"duplicated from {start_str} to {end_str}")
                        self.trigger.emit(f"duplicated from {start_str} to {end_str}")

                    if delta > 1100 and all_hour_data[i]['leadOn'] == "False":
                        print(f"leadOff part one: missing from {start_str} to {end_str}, count: {delta / 1000 - 1:.0f}")
                        self.trigger.emit(
                            f"leadOff part one: missing from {start_str} to {end_str}, count: {delta / 1000 - 1:.0f}")
                    if delta > 1100 and all_hour_data[i]['leadOn'] == "True":
                        print(f"Missing data part one: missing from {start_str} to {end_str}, count: {delta / 1000 - 1:.0f}")
                        self.trigger.emit(
                            f"Missing data part one: missing from {start_str} to {end_str}, count: {delta / 1000 - 1:.0f}")
        with open(self.write_path + '/finall_result.txt', "a+") as f:
            start_tick = all_hour_data[-1]["recordTime"]
            start_str = datetime.datetime.fromtimestamp(start_tick / 1000).strftime('%Y-%m-%d %H:%M:%S')
            for end_key in all_hour_data[-1]:
                if end_key in self.exclude_fields:
                    pass
                else:
                    f.write(str(all_hour_data[-1][end_key])+",")
            f.write(start_str)
            # f.write(
                    # "{},{},{},{},{},{}".format(str(all_hour_data[-1]['recordTime']), start_str, " ", str(hr),
                    #                               str(leadOn), str(flash)))

            self.trigger.emit("文件分析完成,本次下载结束")

    def Segmentation_time(self, start, end):
        # 1. 将下载的时间按小时进行分割
        # 2. 将分割完后的时间放入队列中
        totalTime = end - start
        # 小于一小时
        if totalTime <= 3600000:
            self.queue.put({"start": start, "end": end})
            self.thread_count = 1
        # 大于一小时
        else:
            import math
            # 判断一共有几个完整的一小时
            totalHour = math.ceil(totalTime / 3600000)
            if totalHour <= 12:
                self.thread_count = 6
            else:
                self.thread_count = 12
            for i in range(totalHour):
                newstart = start + i * 3600000
                newEnd = newstart + 3600000
                if newEnd < end:
                    self.queue.put({"start": newstart, "end": newEnd})
                    continue
                else:
                    self.queue.put({"start": newstart, "end": end})

class DownloadThead(threading.Thread):
    def __init__(self,sn, dl_start, dl_end,server,trigger,queue,write_path,token,tenant):
        super(DownloadThead, self).__init__()
        self.hour_data = []
        self.sn=sn
        self.dl_start=dl_start
        self.dl_end=dl_end
        self.server=server
        self.trigger=trigger
        self.queue=queue
        self.write_path=write_path
        self.token=token
        self.lock=threading.Lock()
        self.tenant=tenant

    def run(self):
        if self.server == "Production":
            self.payload = {
                "patchSn": self.sn,
                "startTime": self.dl_start,
                "endTime": self.dl_end,
                "version":"v3",
                # "denoise": "true"
            }
            self.base_url = f"https://vcloud2.vivalink.com/tenants/{self.tenant}/data"
        elif self.server == "Test":
            self.payload = {
                "patchSn": self.sn,
                "startTime": self.dl_start,
                "endTime": self.dl_end,
                "version": "v3",
                # "denoise": "true"
            }
            self.base_url = f"https://vcloud-test.vivalink.com/tenants/{self.tenant}/data"
        else:
            self.payload = {
                "patchSn": self.sn,
                "startTime": self.dl_start,
                "endTime": self.dl_end,
                "denoise": "true",
                "version": "v2"}
            self.base_url = f"https://vcloud-test.vivalink.com/tenants/{self.tenant}/data"
        self.headers = {
            "Authorization": self.token
        }
        # base_url = self.URL + "data"

        while True:
            try:
                self.response = requests.get(self.base_url, headers=self.headers, params=self.payload, timeout=60)
                if self.response.json()['code'] != 200:
                    print(self.response.json())
                    continue
                else:
                    self.res_data = self.response.json()["data"]["list"]
                    if "nextStart" in self.response.json()['data']:
                        self.queue.put(
                            {"start": self.response.json()['data']['nextStart'], "end": self.response.json()['data']['nextEnd']})
                    break
            except Exception as e:
                print(str(e))
                print("请求超时")
                print("正在重试")
                continue
        if len(self.res_data) == 0:
            print(f'{self.dl_start}--{self.dl_end}:此区间无下载数据')
            self.trigger.emit(f'{self.dl_start}--{self.dl_end}:此区间无下载数据')
        else:
            print(f'{self.dl_start}--{self.dl_end}:此区间共{len(self.res_data)}条数据')
            self.trigger.emit(f'{self.dl_start}--{self.dl_end}:此区间共{len(self.res_data)}条数据')
            # data拿到每一秒的数据
            # 如果后一个recordTime与前一个之间大于1500说明有数据丢失
            # 有数据丢失时判断是不是因为leadoff导致的丢失
            # 过滤数据，拿到想要的字段
            # 拼接每秒有效的数据
            for self.data in self.res_data:
                valid_data = {}
                for key in self.data:
                    if key == "vitals":
                        for vitals_key in self.data['vitals']:
                            valid_data[vitals_key] = self.data['vitals'][vitals_key]
                    else:
                        valid_data[key] = self.data[key]
                self.Valid_data =valid_data
                self.hour_data.append(self.Valid_data)
            self.v_sn = self.sn.replace("/", "_")
            self.file_name = f'{self.v_sn}_{self.dl_start}--{self.dl_end}.json'
            self.file_path = self.write_path + "/" + self.file_name
            self.write_hour_data(self.file_path, self.hour_data)

    def write_hour_data(self, file_path, data):
        with open(file_path, "w") as f:
            json.dump(data, f)

    def get_hour_data(self):
        return self.hour_data

    # if __name__ == '__main__':

    # # runner=download_ecg_data()
    # # runner.download('ECGRec_202051/C740018',1617242400372,1617247800000)
    # for i in range(1):
    #     print(i)

