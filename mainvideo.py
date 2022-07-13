import sys,time
# 导入图形组件库
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
#导入做好的界面库
from untitled import Ui_MainWindow

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        #继承(QMainWindow,Ui_MainWindow)父类的属性
        super(MainWindow,self).__init__()
        #初始化界面组件
        self.setupUi(self)

        #初始化
        self.cap1 = None
        self.cap2 = None
        self.status = 0
        self.time = QTimer()
        self.time.timeout.connect(self.refrsh)
        #拉流
        self.pushButton.clicked.connect(self.loadVideo)
        #结束
        self.pushButton_3.clicked.connect(self.overVideo)
        #录制
        self.pushButton_4.clicked.connect(self.getCamera)
        #结束录制
        self.pushButton_2.clicked.connect(self.overCamera)
        #设置初始地址
        global  Address1,Address2
        Address1 = "NULL"
        Address2 = "NULL"
        self.lineEdit.setPlaceholderText(Address1)
        self.lineEdit_2.setPlaceholderText(Address2)

    def refrsh(self):
        if self.status == 0:
            ref, frame = self.cap1.read()
            if ref:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (752, 337), interpolation=cv2.INTER_AREA)
                self.Qframe = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
                self.label_3.setPixmap(QPixmap.fromImage(self.Qframe))



            ref, frame = self.cap2.read()
            if ref:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (752, 337), interpolation=cv2.INTER_AREA)
                self.Qframe = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
                self.label_4.setPixmap(QPixmap.fromImage(self.Qframe))
        elif self.status == 1:
            ref, frame = self.cap1.read()
            if ref:
                self.out1.write(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (752, 337), interpolation=cv2.INTER_AREA)
                self.Qframe = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
                                     QImage.Format_RGB888)
                self.label_3.setPixmap(QPixmap.fromImage(self.Qframe))

            ref, frame = self.cap2.read()
            if ref:
                self.out2.write(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (752, 337), interpolation=cv2.INTER_AREA)
                self.Qframe = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
                                     QImage.Format_RGB888)
                self.label_4.setPixmap(QPixmap.fromImage(self.Qframe))
    def loadVideo(self):
        path1 = self.lineEdit.text() or Address1
        path2 = self.lineEdit_2.text() or Address2

        if path1 and path2:
            if self.time.isActive():
                self.cap1.release()
                self.cap2.release()
                self.time.stop()
            self.cap1 = cv2.VideoCapture(path1)
            self.cap2 = cv2.VideoCapture(path2)
            self.time.start()
        else:
            QMessageBox.information(self,"提示","存在空地址",QMessageBox.Close)

    def overVideo(self):
        if self.time.isActive():
            self.time.stop()
            self.cap1.release()
            self.cap2.release()
        self.label_3.clear()
        self.label_4.clear()

    def getCamera(self):
        if self.time.isActive():
            date = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
            sz = (int(self.cap1.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(self.cap1.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            fps = self.cap1.get(cv2.CAP_PROP_FPS)
            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            self.out1 = cv2.VideoWriter(f'{date}_1.mp4', fourcc, fps, sz, True)


            sz = (int(self.cap2.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(self.cap2.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            fps = self.cap2.get(cv2.CAP_PROP_FPS)
            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            self.out2 = cv2.VideoWriter(f'{date}_2.mp4', fourcc, fps, sz, True)


            self.status = 1
    def overCamera(self):
        if self.time.isActive():
            self.out1.release()
            self.out2.release()
            self.status = 0
            QMessageBox.information(self,"提示","录制结束",QMessageBox.Close)
if __name__ == "__main__":
    #创建QApplication 固定写法
    app = QApplication(sys.argv)
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    # 实例化界面
    window = MainWindow()
    #显示界面
    window.show()
    #阻塞，固定写法
    sys.exit(app.exec_())