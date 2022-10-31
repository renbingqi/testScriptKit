"""
Time : 2020/12/14 14:12 
Author : Rex
File : startDownload.py
Software: PyCharm
"""
import json
import os
import time

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QLineEdit, QMessageBox, \
    QRadioButton, QButtonGroup, QTextEdit, QInputDialog, QAction, QTabWidget, QCheckBox, QComboBox
import sys
from PyQt5.QtGui import QIcon
# from dataDownload.Download_ECG import download_ecg_data
from testToolsKit.Download_ECG_Thread import download_ecg_data
# from dataDownload.Download_Universal import DownloadDataFromVCloud
from testToolsKit.Download_SpO2_Thread import download_SpO2_data
from PyQt5.QtCore import QThread

from testToolsKit.Download_Temp_Thread import download_Temp_data
from testToolsKit.Download_BP_Thread import download_BP_data
from testToolsKit.Download_Thread import download_data


class Ui_MainWindow(QMainWindow, QTabWidget):
    # checkBoxstate1=0
    # checkBoxstate2=0
    file_path = None
    app_id = None
    # data_type = None
    # draw = None

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(650, 800)
        self.label1 = QLabel(
            '<html><head/><body><p><span style=" color:#ff0000;">从云端下载数据输入条件如下（ECG/Temp/SpO2/BP):</span></p></body></html>）',
            self)
        self.label1.setGeometry(20, 25, 350, 16)
        # 选择数据服务器所在位置
        self.cblabel = QLabel("请选择数据服务器:", self)
        self.cblabel.setGeometry(50, 43, 179, 22)
        # self.cb = QComboBox(self)
        # self.cb.setGeometry(180, 43, 179, 22)
        # self.cb.addItems(['Bombay', 'Sweden'])
        # 选择数据服务器部分
        # 创建按钮组件
        self.qbg1 = QButtonGroup(self)
        self.checkBox1 = QRadioButton('Production', self)
        self.checkBox1.setGeometry(180, 43, 179, 22)
        self.checkBox1.setChecked(True)

        self.checkBox2 = QRadioButton('Test', self)
        self.checkBox2.setGeometry(280, 43, 179, 22)

        self.checkBox3 = QRadioButton('Sweden', self)
        self.checkBox3.setGeometry(380, 43, 179, 22)

        self.qbg1.addButton(self.checkBox1)
        self.qbg1.addButton(self.checkBox2)
        self.qbg1.addButton(self.checkBox3)
        # self.checkBox1.toggled.connect(lambda isChecked: self.tenantLineEdit.setText("mvm-app"))
        # self.checkBox2.toggled.connect(lambda isChecked: self.tenantLineEdit.setText(""))
        # self.checkBox3.toggled.connect(lambda isChecked: self.tenantLineEdit.setText("Vivalnk-Swe"))
        # 创建Label标签
        self.app_idlabel = QLabel('请输入tenant:', self)
        # 放置位置
        self.app_idlabel.setGeometry(50, 70, 179, 22)
        # 创建一个输入框
        self.tenantLineEdit = QLineEdit(self)
        # 放置位置
        self.tenantLineEdit.setGeometry(150, 70, 200, 22)
        # 设置默认值
        self.tenantLineEdit.setText("Vivalnk")
        #
        # 创建修改tenant按钮
        # self.changeTenant = QPushButton('修改Tenant', self)
        # self.changeTenant.setGeometry(350, 65, 90, 30)
        # self.changeTenant.clicked.connect(self.modifyTenant)

        self.snLabel = QLabel('设备号：', self)
        self.snLabel.setGeometry(61, 111, 54, 16)
        self.snLineEdit = QLineEdit(self)
        self.snLineEdit.setGeometry(150, 110, 200, 22)
        self.snLineEdit.setText("ECGRec_201917/C600053")
        self.snEglabel = QLabel('eg:ECGRec_202003/C800001', self)
        self.snEglabel.setGeometry(440, 110, 171, 16)
        self.snbutton = QPushButton("修改设备号", self)
        self.snbutton.clicked.connect(self.modifySn)
        self.snbutton.setGeometry(350, 105, 90, 30)
        # 起始时间部分
        default_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.startLabel = QLabel('起始时间:', self)
        self.startLabel.setGeometry(61, 151, 54, 16)
        self.startLineEdit = QLineEdit(self)
        self.startLineEdit.setGeometry(150, 150, 200, 22)
        self.startLineEdit.setText(default_time)
        self.startEglabel = QLabel('eg:2020-12-14 09:00:00', self)
        self.startEglabel.setGeometry(440, 150, 171, 16)
        # 结束时间部分
        self.endLabel = QLabel('结束时间:', self)
        self.endLabel.setGeometry(61, 181, 54, 16)
        self.endLineEdit = QLineEdit(self)
        self.endLineEdit.setGeometry(150, 180, 200, 22)
        self.endLineEdit.setText(default_time)

        # 下载数据存储位置部分
        self.dlpLabel = QLabel('下载数据存储位置:', self)
        self.dlpLabel.setGeometry(61, 220, 111, 16)
        self.dlLineEdit = QLineEdit(self)
        self.dlLineEdit.setGeometry(189, 219, 200, 22)
        self.dlbtn = QPushButton("选择下载位置", self)
        self.dlbtn.setGeometry(420, 215, 131, 33)
        self.dlbtn.clicked.connect(self.clickdlbtn)
        self.dlLineEdit.setText("/Users/rexren/vcloud数据")
        if self.dlLineEdit.text() != None:
            self.file_path=self.dlLineEdit.text()


        # 实时数据&历史数据部分
        # self.qbg3 = QButtonGroup(self)
        # self.app_idlabel4 = QLabel('选择数据类型：', self)
        # self.app_idlabel4.setGeometry(50, 290, 179, 22)
        # self.qlabel = QLabel(
        #     '<html><head/><body><p><span style=" color:#ff0000;">注：此项对ECG数据不生效</span></p></body></html>）', self)
        # self.qlabel.setGeometry(440, 297, 200, 16)
        # self.checkBox5 = QRadioButton('实时数据', self)
        # self.checkBox5.setGeometry(170, 295, 272, 16)
        # self.checkBox5.setChecked(True)
        # # self.checkBox3.setChecked(True)
        # self.checkBox7 = QRadioButton('实时+历史', self)
        # self.checkBox7.setGeometry(260, 295, 272, 16)
        # self.checkBox6 = QRadioButton('历史数据', self)
        # self.checkBox6.setGeometry(350, 295, 549, 16)
        # self.qbg3.addButton(self.checkBox5)
        # self.qbg3.addButton(self.checkBox6)
        # self.qbg3.addButton(self.checkBox7)

        # #是否绘制波形部分
        # self.draw_ecg_label = QLabel('是否绘制波形', self)
        # self.draw_ecg_label.setGeometry(60, 255, 111, 16)
        # self.checkBox3 = QRadioButton('是', self)
        # self.checkBox3.setGeometry(180, 255, 179, 16)
        # self.checkBox4 = QRadioButton('否', self)
        # self.checkBox4.setChecked(True)
        # self.checkBox4.setGeometry(340, 255, 179, 16)

        # 开始下载按钮
        self.start_download_btn = QPushButton('开始下载并分析', self)
        self.start_download_btn.setGeometry(230, 370, 170, 33)
        self.start_download_btn.clicked.connect(self.start_download)

        # #日志部分
        self.loglabel = QLabel('日志', self)
        self.loglabel.setGeometry(50, 410, 131, 16)
        self.log_textEdit = QTextEdit(self)
        self.log_textEdit.setGeometry(90, 410, 520, 341)

        # 创建一个状态栏
        self.statusbar = self.statusBar()
        # self.setLayout(hlayout)
        # 创建一个消息盒子
        self.messagebox = QMessageBox()
        self.setWindowTitle("vcloud data download")
        self.setWindowIcon(QIcon('../Pictures/ImageReady.png'))
        self.show()

        # 创建一个菜单栏
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)
        S3 = QAction('S3', self)
        self.menubar.addAction(S3)
        S3.triggered.connect(self.show_s3_window)

        Temperature = QAction('Fever Scout/感之度体温', self)
        self.menubar.addAction(Temperature)
        Temperature.triggered.connect(self.show_temperature)

    def show_temperature(self):
        from testToolsKit.UI.FeverScout_ui import Temperature_MainWindow
        self.close()
        self.temperature_ui = Temperature_MainWindow()
        self.temperature_ui.show()

    def show_s3_window(self):
        from testToolsKit.UI.generate_data_ui import Generate_S3_data_MainWindow
        self.close()
        self.s3_ui = Generate_S3_data_MainWindow()
        self.s3_ui.show()

    def modifySn(self):
        sn_list = []
        if not os.path.exists("../SN.json"):
            self.messagebox.question(self, "Message", "文件不存在，请手动输入SN后创建新文件", QMessageBox.Ok)
        else:
            with open("../SN.json", 'r') as f:
                try:
                    sn_message = json.loads(f.read())
                    ECG_list = sn_message["ECG"]
                    sn_list += ECG_list
                    Temp_list = sn_message["Temp"]
                    sn_list += Temp_list
                    SpO2_list = sn_message["SpO2"]
                    sn_list += SpO2_list
                    BP_list = sn_message["BP"]
                    sn_list += BP_list
                    text, ok = QInputDialog.getItem(self, "修改SN", "请选择SN号", sn_list)
                    if ok:
                        self.snLineEdit.setText(text)
                except:
                    self.log_textEdit.append("文件内容为空")

    # def modifyTenant(self):
    #     if self.checkBox1.isChecked():
    #         with open("../tenant.json", 'r') as f:
    #             try:
    #                 tenant_message = json.loads(f.read())
    #                 tenant_list = tenant_message['tenantName']
    #                 text, ok = QInputDialog.getItem(self, "修改Tenant", "请选择Tenant", tenant_list)
    #                 if ok:
    #                     self.tenantLineEdit.setText(text)
    #             except:
    #                 self.log_textEdit.append("文件内容为空")
    #     elif self.checkBox2.isChecked():
    #         with open("../tenant_swe.json", 'r') as f:
    #             try:
    #                 tenant_message = json.loads(f.read())
    #                 tenant_list = tenant_message['tenantName']
    #                 text, ok = QInputDialog.getItem(self, "修改SN", "请选择SN号", tenant_list)
    #                 if ok:
    #                     self.tenantLineEdit.setText(text)
    #             except:
    #                 self.log_textEdit.append("文件内容为空")

    def show_testEdit(self, str):
        self.log_textEdit.append(str)

    def clickdlbtn(self):
        dname = QFileDialog.getExistingDirectory(self, 'Open file', 'C:\\Users\\test\\Desktop\\数据')
        self.file_path = dname
        self.dlLineEdit.setText(self.file_path)

    def start_download(self):

        # if self.checkBox5.isChecked():
        #     self.data_type = "realtime"
        # elif self.checkBox6.isChecked():
        #     self.data_type = "history"
        # else:
        #     self.data_type = "real+his"
        sn = self.snLineEdit.text()

        # if self.checkBox3.isChecked():
        #     self.draw = "1"
        # elif self.checkBox4.isChecked():
        #     self.draw = "0"

        if not os.path.exists("../SN.json"):
            ECG_list = []
            Temp_list = []
            SpO2_list = []
            BP_list = []
            self.log_textEdit.append(f'添加新设备{sn}')
            if sn.startswith("ECG"):
                ECG_list.append(sn)
            elif "." in sn:
                Temp_list.append(sn)
            elif sn.startswith("O2"):
                SpO2_list.append(sn)
            elif sn.startswith("BP"):
                BP_list.append(sn)
            data = {"ECG": ECG_list, "Temp": Temp_list, "SpO2": SpO2_list,
                    "BP": BP_list}
            with open('../SN.json', 'w') as f:
                json.dump(data, f)
                self.log_textEdit.append('新设备添加成功')

        else:
            sn_list = []
            with open("../SN.json", 'r') as f:
                try:
                    sn_message = json.loads(f.read())
                    ECG_list = sn_message["ECG"]
                    sn_list += ECG_list
                    Temp_list = sn_message["Temp"]
                    sn_list += Temp_list
                    SpO2_list = sn_message["SpO2"]
                    sn_list += SpO2_list
                    BP_list = sn_message["BP"]
                    sn_list += BP_list
                    if sn in sn_list:
                        pass
                    else:
                        # print("添加新设备")
                        self.log_textEdit.append(f'添加新设备{sn}')
                        if sn.startswith("ECG"):
                            ECG_list.append(sn)
                            print(ECG_list)
                            data = {"ECG": ECG_list, "Temp": Temp_list, "SpO2": SpO2_list,
                                    "BP": BP_list}
                            with open('../SN.json', 'w') as f:
                                json.dump(data, f)
                                self.log_textEdit.append('新设备添加成功')
                        elif "." in sn:
                            Temp_list.append(sn)
                            print(Temp_list)
                            data = {"ECG": ECG_list, "Temp": Temp_list, "SpO2": SpO2_list,
                                    "BP": BP_list}
                            with open('../SN.json', 'w') as f:
                                json.dump(data, f)
                                self.log_textEdit.append('新设备添加成功')
                        elif sn.startswith("O2") or sn.startswith("BabyO2") or sn.startswith("C208S"):
                            SpO2_list.append(sn)
                            print(SpO2_list)
                            data = {"ECG": ECG_list, "Temp": Temp_list, "SpO2": SpO2_list,
                                    "BP": BP_list}
                            with open('../SN.json', 'w') as f:
                                json.dump(data, f)
                                self.log_textEdit.append('新设备添加成功')
                        elif sn.startswith("BP"):
                            BP_list.append(sn)
                            print(BP_list)
                            data = {"ECG": ECG_list, "Temp": Temp_list, "SpO2": SpO2_list,
                                    "BP": BP_list}
                            with open('../SN.json', 'w') as f:
                                json.dump(data, f)
                                self.log_textEdit.append('新设备添加成功')
                        else:
                            self.messagebox.question(self, 'Message', '没有这样的SN号，请确认后重新输入', QMessageBox.Ok)



                except:
                    pass
        start_time = self.startLineEdit.text()
        end_time = self.endLineEdit.text()
        try:
            start_stamp = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S")) * 1000)
            end_stamp = int(time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S")) * 1000)
            tenant = self.tenantLineEdit.text()
        except:
            self.messagebox.question(self, 'Message', '输入的时间有误，请确认后重新输入', QMessageBox.Ok)
            return
        if self.checkBox1.isChecked():
            server = "Production"

        elif self.checkBox2.isChecked():
            server = "Test"

        else:
            server = 'Sweden'

        if start_stamp > end_stamp:
            self.messagebox.question(self, 'Message', '结束时间不能早于开始时间', QMessageBox.Ok)

        elif sn == None:
            self.messagebox.question(self, 'Message', '设备号不能为空', QMessageBox.Ok)
        elif self.file_path == None:
            self.messagebox.question(self, 'Message', '数据存储位置不能为空', QMessageBox.Ok)
        else:
            self.log_textEdit.clear()
            if sn.startswith("ECG"):
                self.log_textEdit.append("心电数据开始下载")
            elif sn.startswith("O2") or sn.startswith("BabyO2") or sn.startswith("C208S"):
                self.log_textEdit.append("血氧数据开始下载")
            elif "." in sn:
                self.log_textEdit.append("体温数据开始下载")
            elif "BP" in sn:
                self.log_textEdit.append("血压数据开始下载")
            self.thread = StartDownload(self.file_path, self.app_id, self.log_textEdit, sn, start_stamp,
                                           end_stamp,tenant,server)
            self.thread.trigger.connect(self.show_testEdit)
            self.thread.start()

            # if sn.startswith("ECG"):
            #     self.log_textEdit.clear()
            #     self.log_textEdit.append("ECG数据开始下载")
            #     self.thread = StartDownloadECG(self.file_path, self.app_id, self.log_textEdit, sn, start_stamp,
            #                                    end_stamp, self.draw,tenant, server)
            #     self.thread.trigger.connect(self.show_testEdit)
            #     self.thread.start()
            # elif sn.startswith("O2") or sn.startswith("BabyO2") or sn.startswith("C208S"):
            #     self.log_textEdit.clear()
            #     self.log_textEdit.append("SpO2数据开始下载")
            #     self.thread = StartDownloadSpO2(self.file_path, self.app_id, self.log_textEdit, sn, start_stamp,
            #                                     end_stamp, self.draw,tenant, self.data_type, server)
            #     self.thread.trigger.connect(self.show_testEdit)
            #     self.thread.start()
            # elif "." in sn:
            #     self.log_textEdit.clear()
            #     self.log_textEdit.append("体温数据开始下载")
            #     self.thread = StartDownloadTEMP(self.file_path, self.app_id, self.log_textEdit, sn, start_stamp,
            #                                     end_stamp, self.draw,tenant, self.data_type, server)
            #     self.thread.trigger.connect(self.show_testEdit)
            #     self.thread.start()
            # elif "BP" in sn:
            #     self.log_textEdit.clear()
            #     self.log_textEdit.append("血压数据开始下载")
            #     self.thread = StartDownloadBP(self.file_path, self.app_id, self.log_textEdit, sn, start_stamp,
            #                                     end_stamp, self.draw, self.data_type, server)
            #     self.thread.trigger.connect(self.show_testEdit)
            #     self.thread.start()
            #
            # else:
            #     self.messagebox.question(self, 'Message', '请输入正确的设备号', QMessageBox.Ok)

class StartDownload(QThread):
    trigger = pyqtSignal(str)
    def __init__(self, file_path, app_id, log_textEdit, sn, start_stamp, end_stamp,tenant,
                 server="Production"):
        super(StartDownload, self).__init__()
        self.file_path = file_path
        self.app_id = app_id
        self.log_textEdit = log_textEdit
        self.sn = sn
        self.start_stamp = start_stamp
        self.end_stamp = end_stamp
        # self.draw = draw
        self.server = server
        self.tenant=tenant
        # self.data_type=data_type

    def run(self):
        downloader = download_data(self.file_path, self.trigger,self.tenant,
                                          self.server)
        downloader.download(self.sn, self.start_stamp, self.end_stamp)
# 下载ECG数据
class StartDownloadECG(QThread):
    trigger = pyqtSignal(str)

    def __init__(self, file_path, app_id, log_textEdit, sn, start_stamp, end_stamp, draw,tenant,
                 server="Production"):
        super(StartDownloadECG, self).__init__()
        self.file_path = file_path
        self.app_id = app_id
        self.log_textEdit = log_textEdit
        self.sn = sn
        self.start_stamp = start_stamp
        self.end_stamp = end_stamp
        self.draw = draw
        self.server = server
        self.tenant=tenant

    def run(self):
        download_data = download_ecg_data(self.file_path, self.trigger,self.tenant, self.draw,
                                          self.server)
        download_data.download(self.sn, self.start_stamp, self.end_stamp)


class StartDownloadTEMP(QThread):
    trigger = pyqtSignal(str)

    def __init__(self, file_path, app_id, log_textEdit, sn, start_stamp, end_stamp, draw,tenant,data_type,server="Production"):
        super(StartDownloadTEMP, self).__init__()
        self.file_path = file_path
        self.app_id = app_id
        self.log_textEdit = log_textEdit
        self.sn = sn
        self.start_stamp = start_stamp
        self.end_stamp = end_stamp
        self.draw = draw
        self.server = server
        self.data_type=data_type
        self.tenant=tenant

    def run(self):
        download_data = download_Temp_data(self.file_path, self.trigger, self.draw,self.tenant,self.data_type,
                                          self.server)
        download_data.download(self.sn, self.start_stamp, self.end_stamp)


class StartDownloadSpO2(QThread):
    trigger = pyqtSignal(str)

    def __init__(self, file_path, app_id, log_textEdit, sn, start_stamp, end_stamp, draw,tenant,
                 data_type,
                 server="Production"):
        super(StartDownloadSpO2, self).__init__()
        self.file_path = file_path
        self.app_id = app_id
        self.log_textEdit = log_textEdit
        self.sn = sn
        self.start_stamp = start_stamp
        self.end_stamp = end_stamp
        self.draw = draw
        self.server = server
        self.data_type = data_type
        self.tenant=tenant

    def run(self):
        download_data = download_SpO2_data(self.file_path, self.trigger, self.draw,self.tenant,
                                           self.data_type, self.server)
        download_data.download(self.sn, self.start_stamp, self.end_stamp)


class StartDownloadBP(QThread):
    trigger = pyqtSignal(str)

    def __init__(self, file_path, app_id, log_textEdit, sn, start_stamp, end_stamp, draw,data_type,
                 server="Production"):
        super(StartDownloadBP, self).__init__()
        self.file_path = file_path
        self.app_id = app_id
        self.log_textEdit = log_textEdit
        self.sn = sn
        self.start_stamp = start_stamp
        self.end_stamp = end_stamp
        self.draw = draw
        self.server = server
        self.data_type=data_type

    def run(self):
        download_data = download_BP_data(self.file_path, self.trigger, self.draw,self.data_type,
                                          self.server)
        download_data.download(self.sn, self.start_stamp, self.end_stamp)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("../Pictures/ImageReady.png"))
    ex = Ui_MainWindow()
    sys.exit(app.exec_())
