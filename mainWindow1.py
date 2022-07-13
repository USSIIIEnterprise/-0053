import sys
import random
import re
import time
import mainvideo
import socket
import qdarkstyle
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from createDialog import createDialog
from createWarning import createWarning
from map import MapWindow
from wy import DataGrid
from mainvideo import MainWindow


gl_count = 0
gl_labelCount = 0
gl_errorPossibility = ['轴承箱剧烈振动', '轴承温升过高', '电机电流过大和温升过高', '雷电停机', '叶片结冰']
gl_informationButton = []
gl_createNum = 0
gl_createDockable = []
gl_point = [
    [158, 516, 210, 449, 279, 449],
    [157, 475, 209, 386, 284, 386],
    [164, 432, 223, 342, 284, 342],
    [154, 391, 219, 308, 286, 308],
    [161, 348, 213, 283, 283, 283],
    [155, 309, 206, 246, 277, 246],
    [158, 229, 216, 315, 289, 315],
    [96, 162, 189, 78, 288, 78],
    [101, 78, 170, 29, 274, 29]
]
gl_height = []
gl_windIndex = []
gl_index = []
gl_labelIndex = []
sec = 0
show_flag = 0
show_flag2 = 0
H_SPOT = 1
H_SPOT2 = 1
Turn = 1
Turn2 = 1
Fall_Flag = 0
Fall_Flag2 = 0
Enter_Pressure = 0
Enter_Pressure2 = 0
LOCATION_East = [
                 120.5710000, 120.5500000, 120.5565000, 120.5545000, 120.5526667,  # 1-5
                 120.5566667, 120.5196667, 120.5091667, 120.5050000, 120.5020000,  # 6-10
                 120.5096667, 120.5075000, 120.5036667, 120.5008333, 120.4908333,  # 11-15
                 120.4965000, 120.4920000, 120.4891667, 120.4840000, 120.4838333,  # 16-20
                 120.4793333, 120.4758333, 120.4715000, 120.4880000, 120.4836667,  # 21-25
                 120.4888596, 120.4825816, 120.4788987, 120.4751652, 120.4703928,  # 26-30
                 120.4666892, 120.4629873, 120.4595318, 120.4831499, 120.4761261,  # 31-35
                 120.4707338, 120.4529005, 120.4486530, 120.4443980, 120.4404424,  # 36-40
                 120.4590549, 120.4546929, 120.4584960, 120.4547494, 120.4260136,  # 41-45
                 120.4590549, 120.4546929, 120.4584960, 120.4547494, 120.4260136,  # 46-50
                 120.4590549, 120.4546929, 120.4584960, 118.9051030, 120.4260136,  # 51-55
                 120.4590549, 120.4546929, 120.4584960, 120.4547494, 120.4260136,  # 56-60
                 120.4590549, 120.4546929, 120.4584960, 120.4547494, 120.4260136,  # 61-65
                 120.4590549, 120.4546929, 118.9043380, 120.905103  # 66-69
]
LOCATION_North = [
                  33.4583333, 33.4563333, 33.4556667, 33.4550000, 33.4573333,  # 1-5
                  33.4673333, 33.4705000, 33.4670000, 33.4563333, 33.4535000,  # 6-10
                  33.4736667, 33.5036667, 33.4681667, 33.4588333, 33.4558333,  # 11-15
                  33.4541667, 33.4665000, 33.4743333, 33.4695000, 33.4801667,  # 16-20
                  33.4760000, 33.4831667, 33.4788333, 33.4893333, 33.4851667,  # 21-25
                  33.4416415, 33.4361260, 33.4326895, 33.4291831, 33.4248468,  # 26-30
                  33.4213987, 33.4179500, 33.4147437, 33.4469052, 33.4509190,  # 31-35
                  33.4563548, 33.4419428, 33.4381961, 33.4343727, 33.4309654,  # 36-40
                  33.4575613, 33.4536055, 33.4661969, 33.4626774, 33.4460153,  # 41-45
                  33.4575613, 33.4536055, 33.4661969, 33.4626774, 33.4460153,  # 46-50
                  33.4575613, 33.4536055, 33.4661969, 32.117987 , 33.4460153,  # 51-55
                  33.4575613, 33.4536055, 33.4661969, 33.4626774, 33.4460153,  # 56-60
                  33.4575613, 33.4536055, 33.4661969, 33.4626774, 33.4460153,  # 61-65
                  33.4575613, 33.4536055, 32.117722, 34.117987  # 66-69
]

class StackedExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 50, 10, 10)
        self.setWindowTitle('实时监控')

        self.list = QListWidget()
        self.list.insertItem(0, '风场监控')
        self.list.insertItem(1, '各风机实时情况')
        self.list.insertItem(2, '检修日志')
        self.list.insertItem(3, '现场视频')
        self.list.insertItem(4, '动作识别')

        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = DataGrid()
        self.stack4 = MainWindow()
        self.stack5 = QWidget()

        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.stack4UI()
        self.stack5UI()
        self.dockableUI()

        self.stack = QStackedWidget()
        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)
        self.stack.addWidget(self.stack4)
        self.stack.addWidget(self.stack5)

        hbox = QHBoxLayout()
        hbox.addWidget(self.list, 1, Qt.AlignLeft)
        hbox.addWidget(self.stack, 5, Qt.AlignLeft)

        self.list.currentRowChanged.connect(self.display)

        mainFrame = QWidget()
        mainFrame.setLayout(hbox)
        self.setCentralWidget(mainFrame)

    def stack1UI(self):
        layout = QVBoxLayout()
        text = QLabel()
        text.setPixmap(QPixmap('Z:\学习\计设和节能\ALL PROGRAMS/3.21\Windows\images/map.png'))
        btn1 = QPushButton()
        btn1.setText("开始定位")
        btn1.setMaximumSize(100, 50)
        btn1.setMinimumSize(100, 50)  # 将按钮的大小定死为100*50
        btn1.clicked.connect(main_open)
        btn2 = QPushButton()
        btn2.setText("结束定位")
        btn2.setMaximumSize(100, 50)
        btn2.setMinimumSize(100, 50)
        btn2.clicked.connect(main_close)

        btn1.clicked.connect(self.GPSInformation)

        hbox = QHBoxLayout()
        hbox.addStretch(0)
        hbox.addWidget(btn1)
        hbox.addWidget(btn2)

        layout.addStretch(0)
        layout.addWidget(text)
        layout.addStretch(1)
        layout.addWidget(QLabel("   "))
        layout.addStretch(0)
        layout.addLayout(hbox)

        self.stack1.setLayout(layout)

        self.workThread = WorkThread()
        self.workThread.timer.connect(self.countTime)
        self.workThread.end.connect(self.end)
        self.workThread.end2.connect(self.end2)
        self.workThread.end3.connect(self.end3)
        self.workThread.end6.connect(self.end6)
        self.workThread.end7.connect(self.end7)
        self.work()
    
    def countTime(self):
        global sec
        sec += 1
        self.GPSInformation()
        print(sec)
    def end(self):
        global flag_thread,show_flag,Enter_Pressure,Pressure
        show_flag = 0
        Enter_Pressure = Pressure
        if flag_thread == 0:
            self.twinkle1(SPOT-1)
        text = self.button[SPOT-1].text()
        self.addInformation1(text, SPOT)
    def end2(self):
        global flag_thread,show_flag2,Enter_Pressure2,Pressure2
        show_flag2 = 0
        Enter_Pressure2 = Pressure2
        if flag_thread == 0:
            self.twinkle2(SPOT2-1)
        text = self.button[SPOT2-1].text()
        self.addInformation2(text, SPOT2)

    def end3(self):
        global close_flag,sec
        if sec % 2 == 0:
            self.twinkle1(SPOT - 1)
        else:
            self.twinkle2(SPOT2 - 1)
        close_flag = 0

    def end6(self):
        global Fall_Flag,Turn
        if (Turn):
            Turn = 0
            mainWin = createWarning("A")
            mainWin.exec_()

    def end7(self):
        global Fall_Flag2, Turn2
        if (Turn2):
            Turn2 = 0
            mainWin = createWarning("B")
            mainWin.exec_()
    # def end4(self):
    #    global show_flag
    #    if show_flag:
    #         self.createDialog()
    # def end5(self):
    #    global show_flag2
    #    if show_flag2:
    #        self.createDialog2()


    def work(self):
        self.workThread.start()


    def stack2UI(self):
        layout = QGridLayout() #创建网络布局
        self.button = []
        self.x = []
        vbox = QVBoxLayout()
        vbox1 = QHBoxLayout()

        for i in range(69):
            self.x.append('#%d' %(i+1))
        # 生成44个风机按钮并将所有按钮类放在列表“self.button”中
        for k in range(len(self.x)):
            i = k // 5
            j = k % 5
            self.button.append(k)
            self.button[k] = QPushButton('''\n#%d\n东经:  %f°\n北纬:  %f°\n''' %((k+1),LOCATION_East[k],LOCATION_North[k]))
            self.button[k].setMaximumSize(220, 100)
            self.button[k].setMinimumSize(220, 100) # 将按钮的大小定死为220*100
            self.button[k].setIcon(QIcon(QPixmap('Z:\学习\计设和节能\ALL PROGRAMS/3.21\Windows/images/pinwheel.png')))
            self.button[k].setIconSize(QSize(67, 80))
            layout.addWidget(self.button[k], i, j, Qt.AlignCenter)

            self.opacity = QGraphicsOpacityEffect()
            self.opacity.setOpacity(1)
            self.button[k].clicked.connect(self.twinkle)
            self.button[k].setProperty('name', 'btn%d' %k)

            self.button[k].clicked.connect(self.addInformation)
        
        vbox.addStretch(0)
        vbox.addLayout(layout)
        vbox.addStretch(1)
        vbox.addWidget(QLabel('   '))

        self.buttonWidget = QWidget()
        self.buttonWidget.setLayout(vbox)
        self.buttonWidget.setMinimumSize(1100, 1500)
        self.buttonscroll = QScrollArea()
        self.buttonscroll.setWidget(self.buttonWidget)
        self.buttonscroll.setMinimumWidth(1200)
        self.buttonscroll.setMaximumWidth(1200)
        
        # self.slideWidget.setMinimumSize(400, 1500)
        # layout.SetMinimumSize(1100,1100)
        # self.buttonscroll = QScrollArea()
        # self.buttonscroll.setLayout(layout)
        vbox1.addStretch(0)
        vbox1.addWidget(self.buttonscroll)
        # vbox1.setGeometry(QtCore.QRect(0, 100, 1100, 900))
        self.stack2.resize(1100, 900)
        self.stack2.setLayout(vbox1)
    
    def stack3UI(self):
        pass

    def stack4UI(self):
        pass

    def stack5UI(self):
        pass

    def display(self, index):
        self.stack.setCurrentIndex(index)


    # 让点击过的按钮闪烁3次并变色
    def twinkle(self):
        global gl_count
        gl_count = 0
        sender = self.sender()
        text = sender.text()
        f1 = re.findall('(\d+)',text)
        self.index = int(f1[0]) - 1
        qssStyle = '''
        QPushButton[name="btn%d"]{
            background-color:rgb(253,150,150)
        }
        ''' % self.index
        self.setStyleSheet(qssStyle)

        self.num = 100
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.timeoutcount)
        self.timer.start()

    def twinkle1(self, index):
        global gl_count
        gl_count = 0
        self.index = index
        qssStyle = '''
        QPushButton[name="btn%d"]{
            background-color:rgb(253,150,150)
        }
        ''' % self.index
        self.setStyleSheet(qssStyle)
        self.num = 100
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.timeoutcount1)
        self.timer.start()

    def twinkle2(self, index):
        global gl_count2
        gl_count2 = 0
        self.index = index
        qssStyle = '''
        QPushButton[name="btn%d"]{
            background-color:rgb(255,165,100)
        }
        ''' % self.index
        self.setStyleSheet(qssStyle)
        self.num = 100
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.timeoutcount2)
        self.timer.start()

    def timeoutcount(self):
        global gl_count
        self.opacity.setOpacity(self.num/100)
        self.button[self.index].setGraphicsEffect(self.opacity)
        if gl_count % 2:
            self.num += 1
            if self.num >= 100:
                gl_count += 1
        else:
            self.num -= 1
            if self.num <= 0:
                gl_count += 1
        if gl_count >= 6:
            gl_count = 0
            self.timer.stop()
            self.timer.deleteLater()

    def timeoutcount1(self):
        global gl_count
        self.opacity.setOpacity(self.num/100)
        self.button[self.index].setGraphicsEffect(self.opacity)
        if gl_count % 2:
            self.num += 1
            if self.num >= 100:
                gl_count += 1
        else:
            self.num -= 1
            if self.num <= 0:
                gl_count += 1
        if gl_count >= 6:
            gl_count = 0
            self.timer.stop()
            self.timer.deleteLater()

    def timeoutcount2(self):
        global gl_count2
        self.opacity.setOpacity(self.num/100)
        self.button[self.index].setGraphicsEffect(self.opacity)
        if gl_count2 % 2:
            self.num += 1
            if self.num >= 100:
                gl_count2 += 1
        else:
            self.num -= 1
            if self.num <= 0:
                gl_count2 += 1
        if gl_count2 >= 6:
            gl_count2 = 0
            self.timer.stop()
            self.timer.deleteLater()

    def dockableUI(self):
        self.items = QDockWidget('故障记录', self)
        vbox_dockableUI = QVBoxLayout()

        self.dockableMainWindow = QMainWindow()

        self.dockableWidget = QWidget()
        self.dockableGridBox = QGridLayout()
        vbox = QVBoxLayout()
        label_empty = QLabel('   ')
        vbox.addStretch(0)
        vbox.addLayout(self.dockableGridBox)
        vbox.addStretch(1)
        vbox.addWidget(label_empty)
        informationLabel = QLabel('出现故障的风机: ')
        informationLabel.setStyleSheet("color:red")
        self.dockableGridBox.addWidget(informationLabel, 0, 0, 1, 5, Qt.AlignLeft | Qt.AlignTop)
        # 添加滚动条
        self.slideWidget = QWidget()
        self.slideWidget.setLayout(vbox)
        self.slideWidget.setMinimumSize(400, 1500)
        self.dockablescroll = QScrollArea()
        self.dockablescroll.setWidget(self.slideWidget)

        self.northLabel = QLabel('北纬A：%f' %North)
        self.eastLabel = QLabel('东经A：%f' %East)
        self.heightLabel = QLabel('高度A：%f' %Height)
        self.pressureLabel = QLabel('气压A：%f' %Pressure)
        self.spotLabel = QLabel('风机编号A：%d' %SPOT)
        self.northLabel2 = QLabel('北纬B：%f' %North2)
        self.eastLabel2 = QLabel('东经B：%f' %East2)
        self.heightLabel2 = QLabel('高度B：%f' %Height2)
        self.pressureLabel2 = QLabel('气压B：%f' %Pressure2)
        self.spotLabel2 = QLabel('风机编号B：%d' %SPOT2)

        self.informationvbox = QVBoxLayout()
        self.informationvbox.addWidget(self.northLabel)
        self.informationvbox.addWidget((self.eastLabel))
        self.informationvbox.addWidget(self.heightLabel)
        self.informationvbox.addWidget(self.pressureLabel)
        self.informationvbox.addWidget(self.spotLabel)
        self.informationvbox.addWidget(self.northLabel2)
        self.informationvbox.addWidget((self.eastLabel2))
        self.informationvbox.addWidget(self.heightLabel2)
        self.informationvbox.addWidget(self.pressureLabel2)
        self.informationvbox.addWidget(self.spotLabel2)

        okButton = QPushButton("确定")
        cancelButton = QPushButton('取消')
        hbox_dockableUI = QHBoxLayout()
        hbox_dockableUI.addStretch(1)
        hbox_dockableUI.addWidget(okButton)
        hbox_dockableUI.addWidget(cancelButton)

        vbox_dockableUI.addStretch(0)
        vbox_dockableUI.addWidget(self.dockablescroll)
        vbox_dockableUI.addLayout((self.informationvbox))
        vbox_dockableUI.addStretch(1)
        vbox_dockableUI.addLayout(hbox_dockableUI)

        self.dockableWidget.setLayout(vbox_dockableUI)
        self.dockableMainWindow.setCentralWidget(self.dockableWidget)
        
        self.items.setWidget(self.dockableMainWindow)
        self.addDockWidget(Qt.RightDockWidgetArea, self.items)

    def addInformation(self):
        global gl_labelCount
        global gl_informationButton
        global gl_labelIndex
        if self.sender().text() not in gl_labelIndex:
            gl_labelIndex.append(self.sender().text())
            gl_informationButton.append(0)
            gl_informationButton[gl_labelCount] = QPushButton('查看高度')
            gl_labelCount += 1
            self.dockableGridBox.addWidget(QLabel('%d.'% gl_labelCount), gl_labelCount, 0, Qt.AlignLeft | Qt.AlignTop)
            self.dockableGridBox.addWidget(gl_informationButton[gl_labelCount-1], gl_labelCount, 1, Qt.AlignLeft | Qt.AlignTop)
            self.dockableGridBox.addWidget(QLabel('A:%d号风机' %(self.index+1)), gl_labelCount, 2, 1, 3, Qt.AlignLeft | Qt.AlignTop)
            gl_informationButton[gl_labelCount-1].clicked.connect(self.createDialog)
            self.createDialog()
            gl_informationButton[gl_labelCount-1].setToolTip('点击查看详情')
    
    def addInformation1(self, text, sec):
        global gl_labelCount
        global gl_informationButton
        global gl_labelIndex
        if text not in gl_labelIndex:
            gl_labelIndex.append(text)
            gl_informationButton.append(0)
            gl_informationButton[gl_labelCount] = QPushButton('查看高度')
            gl_labelCount += 1
            self.dockableGridBox.addWidget(QLabel('%d.'% gl_labelCount), gl_labelCount, 0, Qt.AlignLeft | Qt.AlignTop)
            self.dockableGridBox.addWidget(gl_informationButton[gl_labelCount-1], gl_labelCount, 1, Qt.AlignLeft | Qt.AlignTop)
            self.dockableGridBox.addWidget(QLabel('A:%d号风机' %(sec)), gl_labelCount, 2, 1, 3, Qt.AlignLeft | Qt.AlignTop)
            gl_informationButton[gl_labelCount-1].clicked.connect(self.createDialog)
            gl_informationButton[gl_labelCount-1].setToolTip('点击查看详情')

    def addInformation2(self, text, sec):
        global gl_labelCount
        global gl_informationButton
        global gl_labelIndex
        if text not in gl_labelIndex:
            gl_labelIndex.append(text)
            gl_informationButton.append(0)
            gl_informationButton[gl_labelCount] = QPushButton('查看高度')
            gl_labelCount += 1
            self.dockableGridBox.addWidget(QLabel('%d.'% gl_labelCount), gl_labelCount, 0, Qt.AlignLeft | Qt.AlignTop)
            self.dockableGridBox.addWidget(gl_informationButton[gl_labelCount-1], gl_labelCount, 1, Qt.AlignLeft | Qt.AlignTop)
            self.dockableGridBox.addWidget(QLabel('B:%d号风机' %(sec)), gl_labelCount, 2, 1, 3, Qt.AlignLeft | Qt.AlignTop)
            gl_informationButton[gl_labelCount-1].clicked.connect(self.createDialog2)
            gl_informationButton[gl_labelCount-1].setToolTip('点击查看详情')
    
    def createDockable(self):
        global gl_createDockable
        global gl_createNum
        sender = self.sender()
        text = sender.text()
        # problemNum = random.randint(1,9)
        gl_createDockable.append(0)
        gl_createDockable[gl_createNum] = QDockWidget('%s' %text, self)
        
        vbox = QVBoxLayout()
        label1 = QLabel('%s' %text)
        vbox.addWidget(label1, Qt.AlignHCenter | Qt.AlignTop)

        gl_createDockable[gl_createNum].setLayout(vbox)
        self.addDockWidget(Qt.RightDockWidgetArea, gl_createDockable[gl_createNum])
        gl_createNum += 1

    def createDialog(self):
        global gl_height
        global gl_windIndex
        global gl_index, H_SPOT
        text = self.sender().text()
        if text not in gl_windIndex:
            gl_windIndex.append(text)
            height = random.randint(1,100)
            index = pictureindex(height)
            gl_index.append(index)
            point = gl_point[index-1]
            gl_height.append(height)
            mainWin = createDialog(H_SPOT, "A组", text)
            mainWin.exec_()
        else:
            position = gl_windIndex.index(text)
            index = gl_index[position]
            height = gl_height[position]
            point = gl_point[index-1]
            mainWin = createDialog(H_SPOT, "A组", text)
            mainWin.exec_()

    def createDialog2(self):
        global gl_height
        global gl_windIndex
        global gl_index,H_SPOT2
        global text
        text = self.sender().text()
        if text not in gl_windIndex:
            gl_windIndex.append(text)
            height = random.randint(1,100)
            index = pictureindex(height)
            gl_index.append(index)
            point = gl_point[index-1]
            gl_height.append(height)
            mainWin = createDialog(H_SPOT2, "B组", text)
            mainWin.exec_()
        else:
            position = gl_windIndex.index(text)
            index = gl_index[position]
            height = gl_height[position]
            point = gl_point[index-1]
            mainWin = createDialog(H_SPOT2, "B组", text)
            mainWin.exec_()


    def GPSInformation(self):
        self.northLabel.setText('北纬A：%f' %North)
        self.eastLabel.setText('东经A：%f' %East)
        self.heightLabel.setText("高度A：%f" %Height)
        self.pressureLabel.setText('气压A：%f' %Pressure)
        self.spotLabel.setText('风机编号A：%d' %SPOT)
        self.northLabel2.setText('北纬B：%f' %North2)
        self.eastLabel2.setText('东经B：%f' %East2)
        self.heightLabel2.setText("高度B：%f" %Height2)
        self.pressureLabel2.setText('气压B：%f' %Pressure2)
        self.spotLabel2.setText('风机编号B：%d' %SPOT2)



class WorkThread(QThread):
    timer = pyqtSignal() # 每隔1秒发送一个信号
    end = pyqtSignal()   # A号闪烁
    end2 = pyqtSignal()  # B号闪烁
    end3 = pyqtSignal()  # 同时闪烁
    end6 = pyqtSignal()  # A高度变化
    end7 = pyqtSignal()  # B高度变化
    def run(self):
        global flag_thread,H_SPOT,H_SPOT2,show_flag,show_flag2
        LAST_H_SPOT = 0
        LAST_H_SPOT2 = 0
        flag_thread = 0  # 轮流闪烁未开启
        while True:
            self.sleep(1)
            # 下面是GPS闪烁界面的信号
            if SPOT != -1:
                self.end.emit()   # 发送end信号
            if SPOT2 != -1:
                self.end2.emit()  # 发送end2信号
            if (SPOT != -1) & (SPOT2 != -1):
                flag_thread = 1   # 多线程开启
                self.end3.emit()  # 发送end3信号
            else:
                if flag_thread == 1:  # 发现轮流闪烁打开状态
                    flag_thread = 0
            # 下面是防跌落安全信息的信号
            if (Fall_Flag):
                self.end6.emit()  # 发送A组跌落信号
            if (Fall_Flag2):
                self.end7.emit()  # 发送B组跌落信号

            self.timer.emit() # 发送timer信号


def replaceSituation(text):
    str_list = text.split('\n')
    str_list[2] = "###故障###"
    string = "\n".join(str_list)
    return string

def pictureindex(height):
    num = height // 10 + 1
    if num > 9:
        return 9
    return num



'''
  程序名称：GPS定位 v2.2
  函数说明：两个一维数组 存放所有风机坐标:LOCATION_East,LOCATION_North 可以直接import调用
         点击运行后，会提供如下参数  East,East2:东经   North,North2:北纬   Height,Height2:高度   Pressure，Pressure2:气压
  重要返回值：SPOT，SPOT2 代表两个不同位置的GPS传来的最后消失信号最近的点，与数组 LOCATION_East,LOCATION_North 的位置对应
              如果SPOT == -1 代表人员还在风机外面，GPS仍然在正常发送信号，不需要将风机显示红色       如果SPOT != -1 代表信号消失且最后位置离风机很近，其数值就是对应风机的编号，将风机显示红色
           EB,EB2为防误判消抖系数，默认为>1，也就是2次检测不到GPS信号就判断为信号真丢失
           默认自己的端口  B01，在第--行可以更改
           默认接收端口1  F10，在第--行可以更改
           默认接收端口2  F12，在第--行可以更改
  放进mainWindow的方法：  stack1UI中写按键 btn1对应main 点击开始GPS接受和计算       btn2对应main_close 点击关闭GPS通讯(千万记得要关!)
                        

'''

Pressure = 0
Height = 0
East = 0
North = 0
SPOT = -1
EB = 0

Pressure2 = 0
Height2 = 0
East2 = 0
North2 = 0
SPOT2 = -1
EB2 = 0

LOCATION_Height = []

def recvlink():
    global Pressure,Height,East,North,EB,Switch,Pressure2,Height2,East2,North2,EB2,Switch2,SPOT,SPOT2,lost_flag,lost_flag2,judge_flag,judge_flag2,Flag,A_x,A_y,A_z,V_x,V_y,V_z,A_x2,A_y2,A_z2,V_x2,V_y2,V_z2
    Switch2 = 0
    Switch = 0
    judge_flag = 1
    judge_flag2 = 1
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('myfrank-personal.top', 5248))
    sendip = "B02"             # 自己的编号默认为B01
    client.send(sendip.encode('utf-8'))
    msg = client.recv(1024)
    # print(msg.decode('utf-8'))

    while True:
        global SPOT,SPOT2
        last_num = 3    #数据初始化
        cont_num = 0
        lost_flag = 0
        lost_flag2 = 0

        msg = client.recv(1024)
        msgtrans = msg.decode('utf-8')
        print(msgtrans)
        strlen = len(msgtrans)
        # print(msgtrans)       # 检测数据传输和解码是否正常
        if (msgtrans[0] == 'F') and (msgtrans[1] == '1') and (msgtrans[2] == '0'):   # 接收来自B01信号
          if (msgtrans[3] == '-') and (msgtrans[4] == '1'):
             lost_flag = 1
             if judge_flag == 1:
                compare()
                judge_flag = 0
          else:
              judge_flag = 1
              SPOT = -1

          # 从第3位[2]开始检索有用数据，到strlen结束
          for num in range(2, strlen-1):
              if  (msgtrans[num] == ','):
                cont_num += 1
                if (cont_num == 1) and (lost_flag == 0): North = float(msgtrans[3: num])
                if (cont_num == 3) and (lost_flag == 0): East = float(msgtrans[last_num+1: num])
                if (cont_num == 5) and (lost_flag == 0): Height = float(msgtrans[last_num+1: num])
                if (cont_num == 7):                      Pressure = float(msgtrans[last_num+1: num])
                if (cont_num == 9):                      A_x = float(msgtrans[last_num+1: num])
                if (cont_num == 10):                     A_y = float(msgtrans[last_num+1: num])
                if (cont_num == 11):                     A_z = float(msgtrans[last_num+1: num])
                if (cont_num == 12):                     V_x = float(msgtrans[last_num+1: num])
                if (cont_num == 13):
                    V_y = float(msgtrans[last_num+1: num])
                    V_z = float(msgtrans[num+1: strlen-1])
                last_num = num
          height_judge()
          fall_judge()
          print(North, ' ', East, ' ', Height, ' ', Pressure, ' ', SPOT, ' ', A_x, ' ', A_y, ' ', A_z, ' ', V_x, ' ', V_y, ' ', V_z, ' ',H_SPOT)






        if (msgtrans[0] == 'F') and (msgtrans[1] == '1') and (msgtrans[2] == '2'):  # 接收来自B12信号
            if (msgtrans[3] == '-') and (msgtrans[4] == '1'):
                lost_flag2 = 1
                if judge_flag2 == 1:
                    compare2()
                    judge_flag2 = 0
            else:
                judge_flag2 = 1
                SPOT2 = -1

            # 从第4位[3]开始检索有用数据，到strlen结束  S0032.117798,N,118.905224,E,45.620000,M,101468.000000,P,1.00,2.00,3.00,1.00,2.00,3.000
            for num in range(2, strlen - 1):
                if (msgtrans[num] == ','):
                    cont_num += 1
                    if (cont_num == 1) and (lost_flag2 == 0): North2 = float(msgtrans[3: num])
                    if (cont_num == 3) and (lost_flag2 == 0): East2 = float(msgtrans[last_num + 1: num])
                    if (cont_num == 5) and (lost_flag2 == 0): Height2 = float(msgtrans[last_num + 1: num])
                    if (cont_num == 7):                        Pressure2 = float(msgtrans[last_num + 1: num])
                    if (cont_num == 9):                        A_x2 = float(msgtrans[last_num + 1: num])
                    if (cont_num == 10):                       A_y2 = float(msgtrans[last_num + 1: num])
                    if (cont_num == 11):                       A_z2 = float(msgtrans[last_num + 1: num])
                    if (cont_num == 12):                       V_x2 = float(msgtrans[last_num + 1: num])
                    if (cont_num == 13):
                        V_y2 = float(msgtrans[last_num + 1: num])
                        V_z2 = float(msgtrans[num + 1: strlen - 1])
                    last_num = num
            height_judge2()
            fall_judge2()
            print(North2, ' ', East2, ' ', Height2, ' ', Pressure2, ' ', SPOT2, ' ', A_x2, ' ', A_y2, ' ', A_z2, ' ', V_x2, ' ', V_y2, ' ', V_z2, ' ',H_SPOT2)


        # 输入要发送的信息 ssendmsg = input()
        # 判断是否取消链接
        if Flag == 1:
            client.send('D'.encode('utf-8'))
            break
            # 向服务器发送消息 tcp_socket.send(sendmsg.encode('utf-8'))
    client.close()  # 结束时关闭客户端

def compare():
    global LOCATION_East, LOCATION_North, LOCATION_Height, Distance, SPOT
    Distance = 10000
    print("1-CONNECT FAIL,LAST LOCATION:")
    print("North: ", North, " East: ", East, " Height: ", Height, " Pressure: ", Pressure)
    for num in range(0, len(LOCATION_East)):    # 从表格里比较出最小的距离和编号
        ERROR = (pow((LOCATION_East[num] - East), 2) + pow((LOCATION_North[num] - North), 2))
        if (ERROR < Distance):
            Distance = ERROR
            SSPOT = num
    if Distance < 0.000588:                    # 如果近，说明正常，如果远，防止误判
            SPOT = SSPOT
            print("1-NEAREST SPOT: ", SPOT, "  DISTANCE IS: ", '{:.5f}'.format((Distance)**0.5))

def compare2():
    global LOCATION_East2, LOCATION_North2, LOCATION_Height2, Distance2, SPOT2
    Distance2 = 10000
    print("2-CONNECT FAIL,LAST LOCATION:")
    print("North2: ", North2, " East2: ", East2, " Height2: ", Height2, " Pressure2: ", Pressure2)
    for num in range(0, len(LOCATION_East)):    # 从表格里比较出最小的距离和编号
        ERROR2 = (pow((LOCATION_East[num] - East2), 2) + pow((LOCATION_North[num] - North2), 2))
        if (ERROR2 < Distance2):
            Distance2 = ERROR2
            SSPOT2 = num
    if Distance2 < 0.000588:                    # 如果近，说明正常，如果远，防止误判
            SPOT2 = SSPOT2
            print("2-NEAREST SPOT: ", SPOT2, "  DISTANCE IS: ", '{:.5f}'.format((Distance2)**0.5))


def main_open():
    global  Flag
    Flag = 0

    t = threading.Thread(target = recvlink)
    t.start()


def main_close():
    global Flag
    Flag = 1

# 高度层数判断函数，方法是测量进入目标建筑后的气压插值，如果差值大于1000，判断为顶楼，500-1000，为中层，500以下，判断为底层
def height_judge():
    global Pressure, SPOT, H_SPOT, Enter_Pressure
    if (SPOT !=-1) and (Enter_Pressure != 0):
        error = abs(Enter_Pressure - Pressure)
        if error > 1000:
            H_SPOT = 3          #最高层
        else:
            if (error <= 1000) & (error > 500):
                H_SPOT = 2      #中间层
            else: H_SPOT = 1    #最底层

def height_judge2():
    global Pressure2, SPOT2, H_SPOT2, Enter_Pressure2
    if (SPOT2 !=-1) and (Enter_Pressure2 != 0):
        error = abs(Enter_Pressure2 - Pressure2)
        if error > 1000:
            H_SPOT2 = 3         #最高层
        else:
            if (error <= 1000) & (error > 500):
                H_SPOT2 = 2     #中间层
            else: H_SPOT2 = 1   #最底层

def fall_judge():
    global A_x, A_y, A_z, V_x, V_y, V_z, Fall_Flag
    if (A_x + A_y + A_z) < 3 and (A_x + A_y + A_z) > 0:
        Fall_Flag = 1

def fall_judge2():
    global A_x2, A_y2, A_z2, V_x2, V_y2, V_z2, Fall_Flag2
    if (A_x2 + A_y2 + A_z2) < 3 and (A_x2 + A_y2 + A_z2) > 0:
        Fall_Flag2 = 1
'''
   上面属于GPS模块搬运！！！！
'''



if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = StackedExample()
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    demo.show()
    sys.exit(app.exec_())