"""
Time : 2021/1/8 15:46 
Author : Rex
File : generate_data_ui.py 
Software: PyCharm
"""
import sys
import time

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QAction, QLineEdit, QPushButton, QTextEdit,QMessageBox
from testToolsKit.UI.startDownload import Ui_MainWindow
from testToolsKit.test_S3_downloadData import registerSubject
from testToolsKit.test_S3_downloadData import registAndsendData
from testToolsKit.test_S3_downloadData import sendData
from PyQt5.QtCore import QThread, pyqtSignal


class Generate_S3_data_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.resize(650, 800)

        self.label1 = QLabel(
            '<html><head/><body><p><span style=" color:#ff0000;">Tenant/Subject ID注册绑定（生成vcloud数据）</span></p></body></html>）',
            self)
        self.label1.setGeometry(20, 30, 291, 16)
        self.setWindowTitle("S3测试一条龙")


        #创建菜单栏并添加vcloud跳转标签
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)
        vcloud = QAction('& vcloud', self)
        self.menubar.addAction(vcloud)
        vcloud.triggered.connect(self.show_vcloud_window)

        temperature=QAction('& Fever Scout/感之度体温',self)
        self.menubar.addAction(temperature)
        temperature.triggered.connect(self.show_temperature)
        #
        #
        #UI部分
        #SN部分
        self.label_sn=QLabel('Patch SN：',self)
        self.label_sn.setGeometry(60,72,81,20)
        self.lineEdit_sn=QLineEdit(self)
        self.lineEdit_sn.setGeometry(160,70,141,20)
        self.label_sn_sueegstion=QLabel('<html><head/><body><p><span style=" color:#ff0000;">填入需要注册设备的SN号</span></p></body></html>）',self)
        self.label_sn_sueegstion.setGeometry(370,70,191,20)
        # Project ID 部分
        self.label_project_id=QLabel('Project ID：',self)
        self.label_project_id.setGeometry(60,120,81,20)
        self.lineEdit_project_id=QLineEdit(self)
        self.lineEdit_project_id.setGeometry(160,120,141,20)
        self.label_project_id_sueegstion=QLabel('<html><head/><body><p><span style=" color:#ff0000;">填入需要绑定的Project ID</span></p></body></html>）',self)
        self.label_project_id_sueegstion.setGeometry(370,120,191,20)
        # Subject ID 部分
        self.label_subject_id=QLabel('Subject ID：',self)
        self.label_subject_id.setGeometry(60,170,81,20)
        self.lineEdit_subject_id=QLineEdit(self)
        self.lineEdit_subject_id.setGeometry(160,170,141,20)
        self.label_subject_id_sueegstion=QLabel('<html><head/><body><p><span style=" color:#ff0000;">填入需要绑定的Subject ID</span></p></body></html>）',self)
        self.label_subject_id_sueegstion.setGeometry(370,170,191,20)

        # data start_time部分：
        self.label_data_start_time = QLabel('Data start_time：', self)
        self.label_data_start_time.setGeometry(60, 220, 111, 20)
        self.lineEdit_data_start_time = QLineEdit(self)
        self.lineEdit_data_start_time.setGeometry(180, 220, 141, 20)
        self.label_data_start_time_sueegstion = QLabel(
            '<html><head/><body><p><span style=" color:#ff0000;">填入需要生成数据的起始时间</span></p></body></html>）', self)
        self.label_data_start_time_sueegstion.setGeometry(370, 220, 191, 20)
        default_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.lineEdit_data_start_time.setText(default_time)

        #data end_time部分
        self.label_data_end_time = QLabel('Data end_time：', self)
        self.label_data_end_time.setGeometry(60, 260, 111, 20)
        self.lineEdit_data_end_time = QLineEdit(self)
        self.lineEdit_data_end_time.setGeometry(180, 260, 141, 20)
        self.label_data_end_time_sueegstion = QLabel(
            '<html><head/><body><p><span style=" color:#ff0000;">填入需要生成数据的结束时间</span></p></body></html>）', self)
        self.label_data_end_time_sueegstion.setGeometry(370, 260, 191, 20)
        self.lineEdit_data_end_time.setText(default_time)
        #注册按钮
        self.registion=QPushButton('注册',self)
        self.registion.setGeometry(10,300,101,31)
        self.registion_suggestion=QLabel('<html><head/><body><p><span style=" color:#ff0000;">只有注册功能</span></p></body></html>）',self)
        self.registion_suggestion.setGeometry(120,310,191,20)
        self.registion.clicked.connect(self.click_registion)
        #发数据按钮
        self.registion3=QPushButton('发数据',self)
        self.registion3.setGeometry(205,300,101,31)
        self.registion3_suggestion=QLabel('<html><head/><body><p><span style=" color:#ff0000;">只发送数据</span></p></body></html>）',self)
        self.registion3_suggestion.setGeometry(310,310,191,20)
        self.registion3.clicked.connect(self.click_registion3)
        #注册+发送数据按钮
        self.registion2 = QPushButton('注册+发数据', self)
        self.registion2.setGeometry(390, 300, 101, 31)
        self.registion2_suggestion = QLabel(
            '<html><head/><body><p><span style=" color:#ff0000;">注册成功之后发送数据</span></p></body></html>）', self)
        self.registion2_suggestion.setGeometry(500,310,191,20)
        self.registion2.clicked.connect(self.click_registion2)

        #提示部分
        self.label_info=QLabel('<html><head/><body><p><span style=" color:#ff0000;">*注意：生成数据的时间需要在注册的时间之后（可以手动改数据库注册时间）否则S3数据会缺失。</span></p></body></html>）',self)
        self.label_info.setGeometry(50,340,571,20)
        #日志部分
        self.log=QTextEdit(self)
        self.log.setGeometry(70,370,500,400)
        # 创建一个消息盒子
        self.message_box=QMessageBox()
        self.setWindowIcon(QIcon('../Pictures/timg.png'))
        self.show()
    def show_temperature(self):
        from testToolsKit.UI.FeverScout_ui import Temperature_MainWindow
        self.close()
        self.temperature_ui=Temperature_MainWindow()
        self.temperature_ui.show()

    def click_registion(self):
        patch_sn=self.lineEdit_sn.text()
        project_id=self.lineEdit_project_id.text()
        subject_id=self.lineEdit_subject_id.text()
        print(patch_sn)
        if patch_sn == '':
            self.message_box.question(self,'Message','Patch SN号不能为空',QMessageBox.Ok)
        elif project_id == '':
            self.message_box.question(self,'Message','Project ID不能为空',QMessageBox.Ok)
        elif subject_id == '':
            self.message_box.question(self,'Message','Subject ID不能为空',QMessageBox.Ok)
        else:

            registerSubject(patch_sn,project_id,subject_id,self.log,QApplication)

    def click_registion2(self):
        patch_sn=self.lineEdit_sn.text()
        project_id=self.lineEdit_project_id.text()
        subject_id=self.lineEdit_subject_id.text()
        start_time=self.lineEdit_data_start_time.text()
        end_time=self.lineEdit_data_end_time.text()
        if patch_sn == '':
            self.message_box.question(self,'Message','Patch SN号不能为空',QMessageBox.Ok)
        elif project_id == '':
            self.message_box.question(self,'Message','Project ID不能为空',QMessageBox.Ok)
        elif subject_id == '':
            self.message_box.question(self,'Message','Subject ID不能为空',QMessageBox.Ok)
        elif start_time == '':
            self.message_box.question(self, 'Message', '开始时间不能为空', QMessageBox.Ok)
        elif end_time == '':
            self.message_box.question(self, 'Message', '结束时间不能为空', QMessageBox.Ok)
        else:
            self.thread=RegistAndsendData(patch_sn,project_id,subject_id,start_time,end_time)
            self.thread.trigger.connect(self.show_log)
            self.thread.start()
    def click_registion3(self):
        patch_sn = self.lineEdit_sn.text()
        start_time=self.lineEdit_data_start_time.text()
        end_time=self.lineEdit_data_end_time.text()
        if patch_sn == '':
            self.message_box.question(self, 'Message', 'Patch SN号不能为空 ', QMessageBox.Ok)
        elif start_time == '':
            self.message_box.question(self, 'Message', '开始时间不能为空', QMessageBox.Ok)
        elif end_time == '':
            self.message_box.question(self, 'Message', '结束时间不能为空', QMessageBox.Ok)
        else:
            start_stamp = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S")) * 1000)
            end_stamp = int(time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S")) * 1000)

            if start_stamp > end_stamp:
                self.message_box.question(self, 'Message', '结束时间不能早于开始时间', QMessageBox.Ok)
            else:
                self.thread=senddata(patch_sn,start_time,end_time)
                self.thread.trigger.connect(self.show_log)
                self.thread.start()



    def show_vcloud_window(self):
        self.close()
        self.vcloud = Ui_MainWindow()
        self.vcloud.show()

    def show_log(self,str):
        self.log.append(str)

class senddata(QThread):
    trigger = pyqtSignal(str)
    def __init__(self, deviceID, startTime, endTime):
        super().__init__()
        self.deviceID=deviceID
        self.startTime=startTime
        self.endTime=endTime


    def run(self):
        sendData(self.deviceID,self.startTime,self.endTime,self.trigger)


class RegistAndsendData(QThread):
    trigger=pyqtSignal(str)
    def __init__(self,patch_sn,project_id,subject_id,start_time,end_time):
        super().__init__()
        self.patch_sn=patch_sn
        self.project_id=project_id
        self.subject_id=subject_id
        self.start_time=start_time
        self.end_time=end_time

    def run(self):
        registAndsendData(self.patch_sn,self.project_id,self.subject_id,self.start_time,self.end_time,self.trigger)

if __name__ == '__main__':

    app = QApplication(sys    .argv)
    ex = Generate_S3_data_MainWindow()
    sys.exit(app.exec_())