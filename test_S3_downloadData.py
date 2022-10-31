#!/usr/bin/env python 
# coding:utf-8

import requests
import http.client
import time
import json
import copy
import datetime


def assemble_data_Temp(deviceId, recordTime):
    dict = {}
    dict['profileId'] = 'cyan'
    dict['sensorId'] = deviceId
    dict['deviceBattery'] = 100
    dict['receiveTime'] = 0
    dict['deviceToken'] = 'a934e7c50746a5da8085d6203be024168bcaee14'
    dict['sdkVersion'] = '2.1.0'
    dict['latitude'] = 30.18000030517578
    dict['longtitude'] = 120.22000122070312
    dict['deviceIp'] = '10.10.1.45'
    dict['deviceType'] = 'iPhone'
    dict['deviceOsType'] = 'iOS'
    dict['deviceOsVersion'] = '14.0'
    dict['carrier'] = '中国移动'
    dict['networkType'] = '4G'
    dict['language'] = 'zh-Hans-CN'
    dict['timezone'] = '28800'
    dict['patchMessage'] = 'VV200'
    dict['app_id'] = 'com.vivalnk.mvm'
    # dict['app_id'] = 'Cardiac Scout'

    dict['type'] = 'TemperatureRaw'
    dict["category"] = "not know"
    tag_arr = [{'foo': 'val'}, {'bar': 'val'}]
    dict['tags'] = tag_arr
    context_dic = {'context1': 'context data'}
    dict['context'] = context_dic
    dict['auditTrail'] = tag_arr
    dict['name'] = ''
    dict['customData'] = context_dic
    dict['recordTime'] = recordTime
    dict["collectTime"] = recordTime
    # 数据组装
    data = {}
    data['fw'] = "2.0"
    data['reocrdTime'] = recordTime
    data['displayTemp'] = "36.5"
    data['rawTemp'] = '36.6'
    data['flash'] = 1
    dict['data'] = data
    return dict


def assemble_data_SpO2(deviceId, recordTime):
    dict = {}
    dict['profileId'] = 'cyan'
    dict['sensorId'] = deviceId
    dict['deviceBattery'] = 100
    dict['receiveTime'] = 0
    dict['deviceToken'] = 'a934e7c50746a5da8085d6203be024168bcaee14'
    dict['sdkVersion'] = '2.1.1'
    dict['latitude'] = 30.18000030517578
    dict['longtitude'] = 120.22000122070312
    dict['deviceIp'] = '10.10.1.45'
    dict['deviceType'] = 'iPhone'
    dict['deviceOsType'] = 'iOS'
    dict['deviceOsVersion'] = '14.0'
    dict['carrier'] = '中国移动'
    dict['networkType'] = '4G'
    dict['language'] = 'zh-Hans-CN'
    dict['timezone'] = '28800'
    dict['patchMessage'] = 'VVSpo2'
    dict['app_id'] = 'com.vivalnk.mvm'
    # dict['app_id'] = 'Cardiac Scout'

    dict['type'] = 'SpO2Raw'
    dict["category"] = "not know"
    tag_arr = [{'foo': 'val'}, {'bar': 'val'}]
    dict['tags'] = tag_arr
    context_dic = {'context1': 'context data'}
    dict['context'] = context_dic
    dict['auditTrail'] = tag_arr
    dict['name'] = ''
    dict['customData'] = context_dic
    dict['recordTime'] = recordTime
    dict["collectTime"] = recordTime
    # 数据组装
    data = {}
    data['pr'] = "73"
    data['recordTime'] = recordTime
    data['steps'] = "0"
    data['spo2'] = '99'
    data['flash'] = 1
    data['chargingStatus'] = 0
    data['pi'] = 2
    dict['data'] = data
    return dict


def assemble_data_BP(deviceId, recordTime):
    dict = {}
    dict['profileId'] = 'cyan'
    dict['sensorId'] = deviceId
    dict['deviceBattery'] = 100
    dict['receiveTime'] = 0
    dict['deviceToken'] = 'a934e7c50746a5da8085d6203be024168bcaee14'
    dict['sdkVersion'] = '2.1.0'
    dict['latitude'] = 30.18000030517578
    dict['longtitude'] = 120.22000122070312
    dict['deviceIp'] = '10.10.1.45'
    dict['deviceType'] = 'iPhone'
    dict['deviceOsType'] = 'iOS'
    dict['deviceOsVersion'] = '14.0'
    dict['carrier'] = '中国移动'
    dict['networkType'] = '4G'
    dict['language'] = 'zh-Hans-CN'
    dict['timezone'] = '28800'
    dict['patchMessage'] = 'VVBP'
    dict['app_id'] = 'com.vivalnk.mvm'
    # dict['app_id'] = 'Cardiac Scout'

    dict['type'] = 'BPRaw'
    dict["category"] = "not know"
    tag_arr = [{'foo': 'val'}, {'bar': 'val'}]
    dict['tags'] = tag_arr
    context_dic = {'context1': 'context data'}
    dict['context'] = context_dic
    dict['auditTrail'] = tag_arr
    dict['name'] = ''
    dict['customData'] = context_dic
    dict['recordTime'] = recordTime
    dict["collectTime"] = recordTime
    # 数据组装
    data = {}
    data['heartRate'] = "76"
    data['recordTime'] = recordTime
    data['arrhythmia'] = 0
    data['sys'] = 99
    data['dia'] = 70
    data['flash'] = 1
    dict['data'] = data
    return dict


def assemble_data_ECG(deviceId, recordTime):
    dict = {}
    dict['profileId'] = 'cyan'
    dict['sensorId'] = deviceId
    dict['deviceBattery'] = 100
    dict['receiveTime'] = 0
    dict['deviceToken'] = 'a934e7c50746a5da8085d6203be024168bcaee14'
    dict['sdkVersion'] = '2.1.1'
    dict['latitude'] = 30.18000030517578
    dict['longtitude'] = 120.22000122070312
    dict['deviceIp'] = '10.10.1.45'
    dict['deviceType'] = 'iPhone'
    dict['deviceOsType'] = 'iOS'
    dict['deviceOsVersion'] = '14.0'
    dict['carrier'] = '中国移动'
    dict['networkType'] = '4G'
    dict['language'] = 'zh-Hans-CN'
    dict['timezone'] = '28800'
    dict['patchMessage'] = '2.1.0.0017;06;VIVALNK;VV330;128Hz;ENC;100*10;HR;5Hz;2048'
    dict['app_id'] = 'com.vivalnk.mvm'
    # dict['app_id'] = 'Cardiac Scout'

    dict['type'] = 'EcgRaw'
    dict["category"] = "not know"
    tag_arr = [{'foo': 'val'}, {'bar': 'val'}]
    dict['tags'] = tag_arr
    context_dic = {'context1': 'context data'}
    dict['context'] = context_dic
    dict['auditTrail'] = tag_arr
    dict['name'] = ''
    dict['customData'] = context_dic
    dict['recordTime'] = recordTime
    dict["collectTime"] = recordTime
    # 数据组装
    data = {}
    ecg = [-100, -130, -135, -147, -149, -160, -159, -169, -172, -184, -194, -202, -199, -200, -195, -203, -204, -200, -185, -170, -145, -123, -94, -68, -57, -68, -76, -81, -98, -114, -123, -121, -145, -140, -146, -144, -144, -136, -133, -128, -114, -90, -111, -122, -130, -107, -91, -104, -107, -52, -68, -77, -103, -85, -52, -29, -32, -48, -34, -35, -89, -213, -80, 612, 1321, 1228, 553, 207, 48, -41, -48, -57, -88, -84, -97, -104, -105, -121, -128, -141, -133, -145, -145, -190, -191, -183, -188, -177, -171, -165, -135, -110, -103, -102, -82, -82, -113, -122, -121, -133, -114, -110, -96, -93, -105, -130, -119, -108, -87, -89, -69, -68, -74, -79, -85, -78, -78, -85, -52, -67, -24, -2, -14, -19, 1, -1, 7, -19]
    data['ecg'] = ecg
    acc = [{'x': 10, 'y': 100, 'z': 1000}, {'x': 10, 'y': 100, 'z': 1000}, {'x': 10, 'y': 100, 'z': 1000},
           {'x': 10, 'y': 100, 'z': 1000}, {'x': 10, 'y': 100, 'z': 1000}]
    data['acc'] = acc
    rri = [1000, 0, 0, 0, 0]
    data['rri'] = rri
    rwl = [100, -1, -1, -1, -1]
    data['rwl'] = rwl
    data['leadOn'] = 1
    data['recordTime'] = recordTime
    data['HR'] = 0
    data['RR'] = 10
    data['BP'] = ''
    data['accAccuracy'] = 2048
    data['magnification'] = 1000
    data['flash'] = 1
    data['activity'] = 1
    dict['data'] = data
    return dict


def write_log(message):
    recordtime = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("./S3regist.log", "a+") as f:
        f.write(message + ":" + recordtime + "\n")


def sendDataToVCloud(payload):
    # print(payload)
    try:
        url = "https://ohez5b65zj.execute-api.ap-south-1.amazonaws.com/production/ingestion"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZW5zb3Jfc24iOiJ0ZXN0NSIsInJlZ19hdHRyaWJ1dGUiOiJhdHRyaWJ1dGUiLCJhcHBfaWQiOiJ2aXZhLXRlc3QiLCJhcHBfa2V5IjoidGVzdF9hcHBfa2V5IiwiZXBvY2hfdHMiOjEwMDAwLCJleHAiOjE2NTY5ODM5ODUsInByaW5jaXBhbCI6InZpdmEtdGVzdCJ9.EbmF4zsZ3TXwq1zZ-2Qha5Q9bdOP3aoanln2R02K1AI'
        }
        print()
        response = requests.post(url, json=payload, headers=headers)
        # print(response.text)
        if json.loads(response.content)['code'] == 200 and json.loads(response.content)[
            'message'] == 'Batch ingestion done':
            print("数据发送成功")
            return True
        else:
            print('发送失败')
            return False
    except Exception as e:
        print("数据发送出错")
        print(e)
        return False


def bind_deviceId_projectId(deviceId, projectId, subjectID,trigger):
    # print(f'设备号:{deviceId}绑定在{projectId}项目上')
    trigger.emit(f'设备号:{deviceId}绑定在{projectId}项目上')
    url = 'https://h0l9dox0g0.execute-api.ap-south-1.amazonaws.com/production/bind-device-tenant'
    data = {
        'tenantName': projectId,
        'deviceId': deviceId,
        'userId': subjectID
    }

    try:
        response = requests.request("POST", url, json=data)
        if response.status_code == 200 and json.loads(response.content)['message'] == 'Bind success':
            # print(json.loads(response.content))
            # success = assemble_json_data(deviceId=deviceId)
            trigger.emit("绑定成功")

            return True
        else:
            # write_log(f"{projectId}绑定失败")

            trigger.emit(f"{projectId}绑定失败")
            return False
    except Exception as e:

        trigger.emit(f"{projectId}绑定失败 {e}")
        return False


def registerSubject(deviceId, projectId, subjectID,trigger):
    url = 'https://8mni95qtb4.execute-api.ap-south-1.amazonaws.com/production/tenant-mode'

    data = {
        'tenantName': projectId,
        'userId': subjectID
    }
    print(f'账号{projectId}注册用户名为{subjectID}')
    trigger.emit(f'账号{projectId}注册用户名为{subjectID}')
    try:
        response = requests.request("POST", url, json=data)
        if response.status_code == 200 and json.loads(response.content)['message'] == 'Validate success':
            print(json.loads(response.content))
            trigger.emit("绑定成功")
            success = bind_deviceId_projectId(deviceId, projectId, subjectID,trigger)
            return success
        else:
            # write_log(f"{projectId}注册失败")
            trigger.emit(f"{projectId}注册失败")
            return False
    except Exception as e:
        # write_log(f"{projectId}绑定失败")
        trigger.emit(f"{projectId}绑定失败")
        return False


def registAndsendData(deviceID, projectId, subjectID,startTime, endTime,trigger ):
    registerSubject(deviceID, projectId, subjectID,trigger)
    sendData(deviceID, startTime, endTime,trigger)


def sendData(deviceID, startTime, endTime,trigger):
    start_timearray = time.strptime(startTime, "%Y-%m-%d %H:%M:%S")
    startTime = int(time.mktime(start_timearray)) * 1000

    end_timearray = time.strptime(endTime, "%Y-%m-%d %H:%M:%S")
    endTime = int(time.mktime(end_timearray)) * 1000
    total_s = endTime - startTime  # 总毫秒数
    tenMin = int(total_s // 300000)  # 总共有几个5分钟
    otherMin = int(total_s % 300000)  # 不足5分钟部分转换成秒
    count = 0
    if deviceID.startswith("ECG"):
        while (tenMin * 1200 - 1200 * count > 0):
            send_array = []
            for i in range(0, 300):
                data_dict = assemble_data_ECG(deviceID, startTime)
                startTime += 1000
                send_array.append(data_dict)
            success = sendDataToVCloud(send_array)
            if success:
                count += 1
                trigger.emit(f'第{count}组数据发送成功')
            else:
                startTime -= 1000 * 300
                count += 1
                trigger.emit(f'第{count}组数据发送失败')

                count -= 1
                continue
        if otherMin !=0:
            send_array2 = []
            for i in range(int(otherMin / 1000)):
                data_dict = assemble_data_ECG(deviceID, startTime)
                startTime += 1000

                send_array2.append(data_dict)

            success = sendDataToVCloud(send_array2)
            if success:
                count += 1
                trigger.emit(f'第{count}组数据发送成功')
                trigger.emit("所有数据发送完毕")

            else:
                startTime -= 1000 * int(otherMin / 1000)
                trigger.emit(f'第{count}组数据发送失败')

        else:
            pass
    elif deviceID.startswith("BP"):
        while (tenMin * 1200 - 1200 * count > 0):
            send_array = []
            for i in range(0, 300):
                data_dict = assemble_data_BP(deviceID, startTime)
                startTime += 1000
                send_array.append(data_dict)
            success = sendDataToVCloud(send_array)
            if success:
                count += 1
                # print(f'第{count}组数据发送成功')

                trigger.emit(f'第{count}组数据发送成功')


            else:
                startTime -= 1000 * 300
                # print(f'第{count}组数据发送失败')
                count += 1
                trigger.emit(f'第{count}组数据发送失败')

                count -= 1
                continue
        if otherMin !=0:


            send_array2 = []
            for i in range(int(otherMin / 1000)):
                data_dict = assemble_data_BP(deviceID, startTime)
                # log.append(str(startTime))
                # app.processEvents()
                startTime += 1000

                send_array2.append(data_dict)

            # print(send_array)

            success = sendDataToVCloud(send_array2)
            if success:
                count += 1
                trigger.emit(f'第{count}组数据发送成功')
                trigger.emit("所有数据发送完毕")

            else:
                startTime -= 1000 * int(otherMin / 1000)
                trigger.emit(f'第{count}组数据发送失败')

    elif deviceID.startswith("O2"):
        while (tenMin * 1200 - 1200 * count > 0):
            send_array = []
            for i in range(0, 300):
                data_dict = assemble_data_SpO2(deviceID, startTime)
                startTime += 1000
                send_array.append(data_dict)
            success = sendDataToVCloud(send_array)
            if success:
                count += 1
                # print(f'第{count}组数据发送成功')
                trigger.emit(f'第{count}组数据发送成功')


            else:
                startTime -= 1000 * 300
                # print(f'第{count}组数据发送失败')
                count += 1
                trigger.emit(f'第{count}组数据发送失败')

                count -= 1
                continue
        if otherMin !=0:

            send_array2 = []
            for i in range(int(otherMin / 1000)):
                data_dict = assemble_data_SpO2(deviceID, startTime)
                # log.append(str(startTime))
                # app.processEvents()
                startTime += 1000

                send_array2.append(data_dict)

            # print(send_array)

            success = sendDataToVCloud(send_array2)
            if success:
                count += 1
                trigger.emit(f'第{count}组数据发送成功')
                trigger.emit("所有数据发送完毕")

            else:
                startTime -= 1000 * int(otherMin / 1000)
                trigger.emit(f'第{count}组数据发送失败')

    else:
        while (tenMin * 1200 - 1200 * count > 0):
            send_array = []
            for i in range(0, 300):
                data_dict = assemble_data_Temp(deviceID, startTime)
                startTime += 1000
                send_array.append(data_dict)
            success = sendDataToVCloud(send_array)
            if success:
                count += 1
                # print(f'第{count}组数据发送成功')
                trigger.emit(f'第{count}组数据发送成功')


            else:
                startTime -= 1000 * 300
                # print(f'第{count}组数据发送失败')
                count += 1
                trigger.emit(f'第{count}组数据发送失败')

                count -= 1
                continue
        if otherMin !=0:
            send_array2 = []
            for i in range(int(otherMin / 1000)):
                data_dict = assemble_data_Temp(deviceID, startTime)
                # log.append(str(startTime))
                # app.processEvents()
                startTime += 1000

                send_array2.append(data_dict)

            # print(send_array)

            success = sendDataToVCloud(send_array2)
            if success:
                count += 1
                trigger.emit(f'第{count}组数据发送成功')
                trigger.emit("所有数据发送完毕")

            else:
                startTime -= 1000 * int(otherMin / 1000)
                trigger.emit(f'第{count}组数据发送失败')


if __name__ == "__main__":
    sn = 'ECGRec_123456/C123456'

    startTime = '2021-01-19 11:10:01'
    endTime = '2021-01-19 11:20:00'
    sendData(sn, startTime, endTime)
