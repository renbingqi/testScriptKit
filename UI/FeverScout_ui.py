"""
Time : 2021/1/13 16:13 
Author : Rex
File : FeverScout_ui.py 
Software: PyCharm
"""
import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QAction, QLineEdit, QPushButton, QTextEdit, QMessageBox, \
    QRadioButton, QFileDialog

from testToolsKit.Download_Temp_200 import DownloadTemp
from testToolsKit.UI.startDownload import Ui_MainWindow

class Temperature_MainWindow(QMainWindow):
    platform = None
    def __init__(self):
        super().__init__()
        self.initUI()



    def initUI(self):
        self.resize(650, 800)

        self.label1 = QLabel(
            '<html><head/><body><p><span style=" color:#ff0000;">Fever Scout/感之度体温云端数据下载</span></p></body></html>）',
            self)
        self.label1.setGeometry(20, 30, 291, 16)
        self.setWindowTitle("Fever Scout&感之度体温")

        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)
        platform = QAction('& vcloud', self)
        self.menubar.addAction(platform)
        platform.triggered.connect(self.show_vcloud_window)

        S3 = QAction('& S3', self)
        self.menubar.addAction(S3)
        S3.triggered.connect(self.show_s3_window)
        #
        #
        # UI部分
        # SN部分
        self.label_sn = QLabel('Patch SN：', self)
        self.label_sn.setGeometry(60, 112, 101, 20)
        self.lineEdit_sn = QLineEdit(self)
        self.lineEdit_sn.setGeometry(160, 112, 151, 20)
        self.label_sn_sueegstion = QLabel(
            '<html><head/><body><p><span style=" color:#ff0000;">请填入设备SN eg: F33.00150424</span></p></body></html>）', self)
        self.label_sn_sueegstion.setGeometry(370, 112, 221, 20)
        # 开始时间 部分
        self.label_project_id = QLabel('Start_time：', self)
        self.label_project_id.setGeometry(60, 160, 81, 20)
        self.lineEdit_project_id = QLineEdit(self)
        self.lineEdit_project_id.setGeometry(160, 160, 151, 20)
        self.label_project_id_sueegstion = QLabel(
            '<html><head/><body><p><span style=" color:#ff0000;">请输入下载数据开始时间</span></p></body></html>）', self)
        self.label_project_id_sueegstion.setGeometry(370, 160, 191, 20)
        # 结束时间 部分
        self.label_subject_id = QLabel('End_time：', self)
        self.label_subject_id.setGeometry(60, 210, 81, 20)
        self.lineEdit_subject_id = QLineEdit(self)
        self.lineEdit_subject_id.setGeometry(160, 210, 151, 20)
        self.label_subject_id_sueegstion = QLabel(
            '<html><head/><body><p><span style=" color:#ff0000;">请输入下载数据结束时间</span></p></body></html>）', self)
        self.label_subject_id_sueegstion.setGeometry(370, 210, 191, 20)
        default_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.lineEdit_project_id.setText(default_time)
        self.lineEdit_subject_id.setText(default_time)
        #选择下载路径部分
        self.label_file_patch = QLabel('File path：', self)
        self.label_file_patch.setGeometry(60, 260, 81, 20)
        self.lineEdit_file_patch = QLineEdit(self)
        self.lineEdit_file_patch.setGeometry(160, 260, 201, 20)
        self.label_file_patch_sueegstion = QPushButton('下载路径',self)
        self.label_file_patch_sueegstion.setGeometry(370, 260, 90, 30)
        self.label_file_patch_sueegstion.clicked.connect(self.selectFilepath)

        #Fever Scout和感之度体温部分
        self.F=QRadioButton('Fever Scout',self)
        self.G=QRadioButton('感之度体温',self)
        self.F.setGeometry(160, 70, 291, 16)
        self.F.setChecked(True)
        self.G.setGeometry(340, 70, 291, 16)

        self.registion = QPushButton('开始下载', self)
        self.registion.setGeometry(240, 350, 131, 31)
        self.registion.clicked.connect(self.download)

        #日志部分
        self.log_textEdit=QTextEdit(self)
        self.log_textEdit.setGeometry(100,400,450,350)
        self.setWindowIcon(QIcon('../Pictures/timg.png'))

        self.show()
        self.message_box=QMessageBox()
    def selectFilepath(self):
        dname = QFileDialog.getExistingDirectory(self, 'Open file', 'C:\\Users\\test\\Desktop\\数据')
        self.file_path = dname
        self.lineEdit_file_patch.setText(self.file_path)
    def show_vcloud_window(self):
        self.close()
        self.vcloud = Ui_MainWindow()
        self.vcloud.show()

    def show_s3_window(self):
        from testToolsKit.UI.generate_data_ui import Generate_S3_data_MainWindow
        self.close()
        self.s3_ui=Generate_S3_data_MainWindow()
        self.s3_ui.show()

    def download(self):
        start_time = self.lineEdit_project_id.text()
        end_time = self.lineEdit_subject_id.text()
        start_stamp = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S")) * 1000)
        end_stamp = int(time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S")) * 1000)
        file_path=self.lineEdit_file_patch.text()
        sn=self.lineEdit_sn.text()
        if self.F.isChecked():
            self.platform='Fever Scout'
        else:
            self.platform='Ganzhidu'
        if sn == '':
            self.message_box.question(self, 'Message', 'SN号不能为空', QMessageBox.Ok)

        elif start_time =='':
            self.message_box.question(self, 'Message', '开始时间不能为空', QMessageBox.Ok)

        elif end_time =='':
            self.message_box.question(self, 'Message', '结束时间不能为空', QMessageBox.Ok)

        elif start_stamp > end_stamp:
            self.messagebox.question(self, 'Message', '结束时间不能早于开始时间', QMessageBox.Ok)

        elif file_path=='':
            self.message_box.question(self,"Message","下载路径不能为空",QMessageBox.Ok)

        else:
            self.thread=Mythread(file_path,sn,start_stamp,end_stamp,self.platform)
            self.thread.trigger.connect(self.showMessage)
            self.thread.start()

    def showMessage(self,str):
        self.log_textEdit.append(str)

class Mythread(QThread):
    trigger=pyqtSignal(str)
    def __init__(self,file_path,sn,start_time,end_time,platform):
        super().__init__()
        self.file_path=file_path
        self.sn=sn
        self.start_time=start_time
        self.end_time=end_time
        self.platform=platform


    def run(self):
        runner = DownloadTemp(self.file_path)
        if self.platform == 'Fever Scout':
            print("开始下载国外的")
            #下载国外的
            runner.download_temp_foreign(self.sn,self.start_time,self.end_time,location=True,type=2,trigger=self.trigger)
        else:
            print("开始下载国内的")
            runner.download_temp_domestic(self.sn, self.start_time, self.end_time, location=True,type=2,trigger=self.trigger)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Temperature_MainWindow()
    sys.exit(app.exec_())