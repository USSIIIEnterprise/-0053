from pydoc import text
import sys
from unicodedata import name
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtSql import *
import qdarkstyle
from cProfile import label
import sqlite3 # 导入包
import matplotlib.pyplot as plt
import re
# import xlrd
# import torch

def getIndex(text):
    f1 = re.findall('(\d+)',text)
    if len(f1) > 0:
        return f1[0]
    else:
        return 0

class DataGrid(QWidget):
    def createTableAndInit(self):
        # 添加数据库
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        # 设置数据库名称
        self.db.setDatabaseName('Z:\学习\计设和节能\ALL PROGRAMS/3.21\Windows/db/database.db')
        # 判断是否打开
        if not self.db.open():
            print('False')
            return False

        # 声明数据库查询对象
        self.query = QSqlQuery()
        # 创建表
        self.query.exec("create table fake(id int primary key, date vchar, location vchar, description vchar, answer vchar)")
        # self.query.exec("create table ways(id int primary key, question vchar, wayone vchar, answerone vchar, waytwo vchar, answertwo vchar, waythree vchar, answerthree vchar)")

        # 添加记录
        # self.query.exec("insert into fake values(1,'2021-1-20','aaa','aaa','aaa')")
        # self.query.exec("insert into fake values(2,'2021-1-20','bbb','bbb','bbb')")
        # self.query.exec("insert into fake values(3,'2021-1-20','ccc','ccc','ccc')")

        return True

    def __init__(self):
        super().__init__()
        self.setWindowTitle("故障诊断专家数据库")
        self.resize(750, 300)
        self.createTableAndInit()

        # 当前页
        self.currentPage = 0
        # 总页数
        self.totalPage = 0
        # 总记录数
        self.totalRecrodCount = 0
        # 每页显示记录数
        self.PageRecordCount = 20

        self.initUI()
        self.initDate()

    def initUI(self):
        # 创建窗口
        self.createWindow()
        # 设置表格
        self.setTableView()

        # 信号槽连接
        self.prevButton.clicked.connect(self.onPrevButtonClick)
        self.nextButton.clicked.connect(self.onNextButtonClick)
        self.switchPageButton.clicked.connect(self.onSwitchPageButtonClick)
    
    def initDate(self):
        placeName = ["大丰", "射阳", "金湖", "宝应", "三龙"]
        self.countInformation = {"大丰":0, "射阳":0, "金湖":0, "宝应":0, "三龙":0, "other":0}
        self.Dictionaries = [{}, {}, {}, {}, {}]
        conn = sqlite3.connect('Z:\学习\计设和节能\ALL PROGRAMS/3.21\Windows/db/database.db') # 连接到SQLite数据库
        cursor = conn.cursor() # 创建一个Cursor
        cursor.execute("select fake.description from fake") # 使用SQL语句对数据库进行操作
        for row in cursor.fetchall(): # 从fetchall中读取操作
            name = row[0][0] + row[0][1]
            if name not in placeName:
                self.countInformation["other"] += 1
            else:
                self.countInformation[name] += 1
                index = placeName.index(name)
                num = getIndex(row[0])
                if num == 0:
                    continue
                if num in self.Dictionaries[index]:
                    self.Dictionaries[index][num] += 1
                else:
                    self.Dictionaries[index][num] = 1
        cursor.close()#关闭Cursor
        conn.close()
        plt.rcParams['font.sans-serif']=['Simhei']

    def closeEvent(self, event):
        # 关闭数据库
        self.db.close()

    # 创建窗口
    def createWindow(self):
        # 操作布局
        operatorLayout = QHBoxLayout()
        self.prevButton = QPushButton("前一页")
        self.nextButton = QPushButton("后一页")
        self.switchPageButton = QPushButton("Go")
        self.switchPageLineEdit = QLineEdit()
        self.switchPageLineEdit.setFixedWidth(50)

        switchPage = QLabel("转到第")
        page = QLabel("页")
        operatorLayout.addStretch(0)
        operatorLayout.addWidget(switchPage)
        operatorLayout.addWidget(self.switchPageLineEdit)
        operatorLayout.addWidget(page)
        operatorLayout.addWidget(self.switchPageButton)
        operatorLayout.addStretch(1)
        operatorLayout.addWidget(self.prevButton)
        operatorLayout.addWidget(self.nextButton)
        # 设置边界可拖动
        # operatorLayout.addWidget(QSplitter())

        # 状态布局
        statusLayout = QHBoxLayout()
        self.totalPageLabel = QLabel()
        self.totalPageLabel.setFixedWidth(70)
        self.currentPageLabel = QLabel()
        self.currentPageLabel.setFixedWidth(100)

        self.totalRecordLabel = QLabel()
        self.totalRecordLabel.setFixedWidth(70)

        statusLayout.addStretch(0)
        statusLayout.addWidget(self.totalPageLabel)
        statusLayout.addWidget(self.currentPageLabel)
        # statusLayout.addWidget(QSplitter())
        statusLayout.addStretch(1)
        statusLayout.addWidget(self.totalRecordLabel)

        # 设置表格属性
        self.tableView = QTableView()
        # 表格宽度的自适应调整
        # self.tableView.horizontalHeader().setStretchLastSection(True)
        # self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 创建编辑数据的按钮
        vbox_editInformation = QVBoxLayout()
        self.refreshButton = QPushButton('刷新')
        self.refreshButton.setToolTip('更改数据后按此键重导数据')
        self.refreshButton.clicked.connect(lambda: self.recordQuery((self.currentPage-1) * self.PageRecordCount))

        self.addButton = QPushButton('添加')
        self.addButton.setToolTip('在数据表尾添加全新的一行')
        self.addButton.clicked.connect(self.addrow)

        self.delButton = QPushButton('删除')
        self.delButton.setToolTip('删除所选中的一行')
        self.delButton.clicked.connect(lambda: self.RemoveRow(self.tableView.currentIndex().row(), ((self.currentPage-1)*self.PageRecordCount)))

        self.findButton = QPushButton('查找')
        self.findButton.setToolTip('对数据库中的信息进行筛查')
        self.findButton.clicked.connect(self.chooseDialog)

        self.loadingButton = QPushButton('导入')
        self.loadingButton.setToolTip('导入文本数据')
        self.loadingButton.clicked.connect(self.loadInformation)

        self.analysisButton = QPushButton('数据分析')
        self.analysisButton.setToolTip('查看具体故障数据分析')
        self.analysisButton.clicked.connect(self.drawpic)

        vbox_editInformation.addStretch(0)
        vbox_editInformation.addWidget(self.refreshButton)
        vbox_editInformation.addWidget(self.addButton)
        vbox_editInformation.addWidget(self.findButton)
        vbox_editInformation.addWidget(self.delButton)
        vbox_editInformation.addWidget(self.loadingButton)
        vbox_editInformation.addWidget(self.analysisButton)
        vbox_editInformation.addStretch(1)
        vbox_editInformation.addWidget(QLabel('   '))

        hbox = QHBoxLayout()
        # hbox.addStretch(0)
        hbox.addWidget(self.tableView)
        hbox.addLayout(vbox_editInformation)

        # 创建界面
        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(statusLayout)
        mainLayout.addLayout(hbox)
        mainLayout.addLayout(operatorLayout)
        self.setLayout(mainLayout)

    # 设置表格
    def setTableView(self):
        # 声明查询模型
        self.tableModel = QSqlTableModel(self)
        # 设置当前页
        self.currentPage = 1
        # 得到总记录数
        self.totalRecrodCount = self.getTotalRecordCount()
        # 得到总页数
        self.totalPage = self.getPageCount()
        # 刷新状态
        self.updateStatus()
        # 设置总页数文本
        self.setTotalPageLabel()
        # 设置总记录数
        self.setTotalRecordLabel()

        # 记录查询
        self.recordQuery(0)
        # 设置模型
        self.tableView.setModel(self.tableModel)
        self.tableView.setColumnWidth(0, 80)
        self.tableView.setColumnWidth(1, 150)
        self.tableView.setColumnWidth(2, 200)
        self.tableView.setColumnWidth(3, 500)
        self.tableView.setColumnWidth(4, 800)
        self.tableView.setFont(QFont('Times', 14, QFont.Black))
        self.tableView.verticalHeader().setVisible(False)

        print('totalRecrodCount=' + str(self.totalRecrodCount))
        print('totalPage=' + str(self.totalPage))

        # self.queryModel.setEditStrategy(QSqlQueryModel.OnFieldChange)

        # 设置表格表头
        self.tableModel.setHeaderData(0, Qt.Horizontal, "序号")
        self.tableModel.setHeaderData(1, Qt.Horizontal, "日期")
        self.tableModel.setHeaderData(2, Qt.Horizontal, "计划完成时间")
        self.tableModel.setHeaderData(3, Qt.Horizontal, "故障描述")
        self.tableModel.setHeaderData(4, Qt.Horizontal, "检修方案")

    # 得到记录数
    def getTotalRecordCount(self):
        self.tableModel.setTable("fake")
        self.tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.tableModel.select()
        rowCount = self.tableModel.rowCount()
        print('rowCount=' + str(rowCount))
        return rowCount

    # 得到页数
    def getPageCount(self):
        if self.totalRecrodCount % self.PageRecordCount == 0:
            return (self.totalRecrodCount / self.PageRecordCount)
        else:
            return (self.totalRecrodCount // self.PageRecordCount + 1)

    # 记录查询
    def recordQuery(self, limitIndex):
        szQuery = ("1=1 limit %d offset %d" %(self.PageRecordCount, limitIndex))
        # szQuery = ("select * from test limit %d,%d" % (limitIndex, self.PageRecordCount))
        print('query sql=' + szQuery)
        self.tableModel.setFilter(szQuery)
        # self.queryModel.setTable(szQuery)

    # 刷新状态
    def updateStatus(self):
        szCurrentText = ("当前第%d页" % self.currentPage)
        self.currentPageLabel.setText(szCurrentText)

        # 设置按钮是否可用
        if self.currentPage == 1:
            self.prevButton.setEnabled(False)
            self.nextButton.setEnabled(True)
        elif self.currentPage == self.totalPage:
            self.nextButton.setEnabled(False)
            self.prevButton.setEnabled(True)
        else:
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(True)

    # 设置总数页文本
    def setTotalPageLabel(self):
        szPageCountText = ("总共%d页" % self.totalPage)
        self.totalPageLabel.setText(szPageCountText)

    # 设置总记录数
    def setTotalRecordLabel(self):
        szTotalRecordText = ("共%d条" % self.totalRecrodCount)
        print('*** setTotalRecordLabel szTotalRecordText=' + szTotalRecordText)
        self.totalRecordLabel.setText(szTotalRecordText)

    # 前一页按钮按下
    def onPrevButtonClick(self):
        print('*** onPrevButtonClick ')
        limitIndex = (self.currentPage - 2) * self.PageRecordCount
        self.recordQuery(limitIndex)
        self.currentPage -= 1
        self.updateStatus()

    # 后一页按钮按下
    def onNextButtonClick(self):
        print('*** onNextButtonClick ')
        limitIndex = self.currentPage * self.PageRecordCount
        self.recordQuery(limitIndex)
        self.currentPage += 1
        self.updateStatus()

    # 转到页按钮按下
    def onSwitchPageButtonClick(self):
        # 得到输入字符串
        szText = self.switchPageLineEdit.text()
        # print('********* %s **************'% szText)
        # 得到页数
        if szText != '':
            pageIndex = int(szText)
            # 判断是否有指定页
            if pageIndex > self.totalPage or pageIndex < 1:
                QMessageBox.information(self, "提示", "没有指定的页面，请重新输入")
                return

            # 得到查询起始行号
            limitIndex = (pageIndex - 1) * self.PageRecordCount

            # 记录查询
            self.recordQuery(limitIndex)
            # 设置当前页
            self.currentPage = pageIndex
            # 刷新状态
            self.updateStatus()

    def addrow(self):
        ret = self.tableModel.insertRows(self.tableModel.rowCount(), 1)
        print(self.tableModel.rowCount())
        print('insertRow=%s' % str(ret))

    def RemoveRow(self, row, index):
        reply = QMessageBox.information(self, '消息', '是否确定删除第%d行' % (row+index+1), QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.tableModel.removeRow(row)
        else:
            pass
    
    def chooseDialog(self):
        self.screenDialog = QDialog()
        self.screenDialog.setWindowTitle('选择筛选项')
        self.screenDialog.resize(400, 150)

        vbox = QVBoxLayout()

        hbox = QHBoxLayout()
        self.OKButton = QPushButton('查找')
        self.CancelButton = QPushButton('取消')
        self.CancelButton.clicked.connect(lambda: self.screenDialog.close())
        hbox.addStretch(0)
        hbox.addWidget(self.OKButton)
        hbox.addWidget(self.CancelButton)

        self.chooseDialog_formlayout = QFormLayout()
        chooseLabel = QLabel('请选择具体的筛选项:')
        self.cb = QComboBox()
        self.cb.addItems(['点击进行选择','日期', '计划完成时间', '故障描述', '检修方案'])
        self.chooseDialog_formlayout.addRow(chooseLabel, self.cb)
        self.cb.currentIndexChanged.connect(self.selectionChanged)

        vbox.addStretch(0)
        vbox.addLayout(self.chooseDialog_formlayout)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.screenDialog.setLayout(vbox)
        self.screenDialog.exec_()
    
    def selectionChanged(self, i):
        informationLabel = QLabel()
        informationLabel.setText('请输入具体的%s:' %self.cb.currentText())
        message = ['故障描述', '检修方案']
        name = self.getname(self.cb.currentText())
        if self.cb.currentText() in message:
            self.lineEdit = QLineEdit()
            self.chooseDialog_formlayout.addRow(informationLabel, self.lineEdit)
            self.OKButton.clicked.connect(lambda: self.queryRecord(name, self.lineEdit.text()))
        # elif self.cb.currentText() == '性别':
        #     self.genderComboBox = QComboBox()
        #     self.genderComboBox.addItems(['男', '女'])
        #     self.chooseDialog_formlayout.addRow(informationLabel, self.genderComboBox)
        #     self.OKButton.clicked.connect(lambda: self.queryRecord(name, self.genderComboBox.currentText()))
        elif self.cb.currentText() == '日期' or self.cb.currentText() == '计划完成时间':
            dateTimeEdit2 = QDateTimeEdit(QDateTime.currentDateTime())
            dateTimeEdit2.setDisplayFormat('yyyy-MM-dd')
            # dateTimeEdit2.setDisplayFormat('yyyy-MM-dd  HH:mm:ss')
            dateTimeEdit2.setCalendarPopup(True)
            self.chooseDialog_formlayout.addRow(informationLabel, dateTimeEdit2)
            self.OKButton.clicked.connect(lambda: self.queryRecord(name, dateTimeEdit2.text()))
    
    def getname(self, message):
        name = ['date', 'location', 'description', 'answer']
        messages = ['日期', '计划完成时间', '故障描述', '检修方案']
        index = messages.index(message)
        return name[index]
    
    def queryRecord(self, name, realname):
        print(name)
        print(realname)
        self.tableModel.setFilter(("%s = '%s'" % (name, realname)))
        self.tableModel.select()
        self.screenDialog.close()
    
    def loadInformation(self):
        self.loadingDialog = QDialog()
        self.loadingDialog.setWindowTitle('导入数据')
        self.loadingDialog.resize(700, 500)

        self.hbox = QHBoxLayout()
        self.editor = QTextEdit()

        self.vbox = QVBoxLayout()
        self.openButton = QPushButton('打开文件')
        self.openButton.clicked.connect(self.openFile)
        self.leadButton = QPushButton('导入数据')
        self.leadButton.clicked.connect(self.leadin)
        self.closeButton = QPushButton('取消')
        self.closeButton.clicked.connect(lambda: self.loadingDialog.close())

        self.vbox.addStretch(0)
        self.vbox.addWidget(self.openButton)
        self.vbox.addWidget(self.leadButton)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.closeButton)

        self.hbox.addWidget(self.editor)
        self.hbox.addLayout(self.vbox)

        self.loadingDialog.setLayout(self.hbox)
        self.loadingDialog.exec_()
    
    def openFile(self):
        self.fname = QFileDialog.getOpenFileName(self.loadingDialog, '打开文本文件', './')
        if self.fname[0]:
            with open(self.fname[0], 'r', encoding='utf-8', errors='ignore') as f:
                self.editor.setText(f.read())
    
    def leadin(self):
        startIndex = self.totalRecrodCount + 1
        print(startIndex)
        # workbook = xlrd.open_workbook('C:/Users/19072/Desktop/1.xls')
        # sheet = workbook.sheet_by_index(0)
        # length = sheet.nrows
        # for i in range(2, length):
        #     index = startIndex
        #     rows = sheet.row_values(i)
        #     self.query.exec("insert into fake values("+str(index)+',"'+rows[3]+'","'+rows[4]+'","'+rows[1]+'","'+rows[2]+'")')
        #     startIndex += 1
        #     self.totalRecrodCount += 1
        # self.loadingDialog.close()
        if self.fname[0]:
            with open(self.fname[0], 'r', encoding='utf-8', errors='ignore') as f:
                while True:
                    text = f.readline()
                    if not text:
                        break
                    text = text[:-1]
                    text = text.split()
                    index = startIndex
                    date = text[0]
                    location = text[1]
                    description = text[2]
                    answer = text[3]
                    print(text, end='')
                    self.query.exec("insert into fake values("+str(index)+',"'+date+'","'+location+'","'+description+'","'+answer+'")')
                    startIndex += 1
                    self.totalRecrodCount += 1
                self.loadingDialog.close()

    def drawpic(self):
        self.drawDialog = QDialog()
        self.drawDialog.setWindowTitle('选择筛选项')
        self.drawDialog.resize(400, 150)

        vbox = QVBoxLayout()

        hbox = QHBoxLayout()
        self.YESButton = QPushButton('生成')
        self.NOButton = QPushButton('取消')
        self.NOButton.clicked.connect(lambda: self.drawDialog.close())
        self.YESButton.clicked.connect(self.pictureChanged)
        hbox.addStretch(0)
        hbox.addWidget(self.YESButton)
        hbox.addWidget(self.NOButton)

        self.drawDialog_formlayout = QFormLayout()
        chooseLabel = QLabel('请选择具体的筛选项:')
        self.cb1 = QComboBox()
        self.cb1.addItems(['点击进行选择','各地风机故障', '大丰风机故障', '射阳风机故障', '金湖风机故障', '宝应风机故障', '三龙风机故障'])
        self.drawDialog_formlayout.addRow(chooseLabel, self.cb1)

        vbox.addStretch(0)
        vbox.addLayout(self.drawDialog_formlayout)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.drawDialog.setLayout(vbox)
        self.drawDialog.exec_()
    
    def pictureChanged(self):
        text = self.cb1.currentText()
        modellist = ['点击进行选择','各地风机故障', '大丰风机故障', '射阳风机故障', '金湖风机故障', '宝应风机故障', '三龙风机故障']
        model = modellist.index(text)
        if model == 0:
            pass
        elif model == 1:
            plt.figure(figsize=(6,6))                 # 将画布设定为正方形
            label='大丰','射阳','金湖','宝应','三龙'                 # 各类别标签
            # label = 'a', 'b', 'b', 'b', 'b'
            sizes=[self.countInformation["大丰"],self.countInformation["射阳"],self.countInformation["金湖"],self.countInformation["宝应"],self.countInformation["三龙"]]
                                # 各类别占比
            color='g','r','b','y','c'                 # 各类别颜色
            explode=(0,0,0,0,0.2)                     # 各类别的偏移半径
            patches,text1,text2=plt.pie(sizes,
                                        colors=color,
                                        explode=explode,
                                        labels=label,
                                        shadow=False,       # 无阴影设置       
                                        autopct="%1.1f%%",  # 数值保留固定小数位
                                        startangle=90,      # 逆时针角度设置
                                        pctdistance=0.6)     # 数值距圆心半径倍数距离
            #patches饼图的返回值，text1饼图外label的文本，text2饼图内部的文本
                
            plt.axis('equal')                               # 饼状图呈正圆
            plt.legend()
            plt.title(modellist[model])
            plt.savefig('Z:\学习\计设和节能\ALL PROGRAMS/3.21\Windows\images/%d.png' %model)
            imshowpic(model)
            # plt.show()
        else:
            plt.figure(figsize=(20, 8), dpi=80)
            key = list(self.Dictionaries[model-2].keys())
            for i in range(len(key)):
                key[i] = key[i]+'号'
            value = list(self.Dictionaries[model-2].values())
            y = []
            for i in range(len(key)):
                y.append(value[i])
            x = range(len(y))
            plt.bar(x, y, width=0.2)#修改刻度名称
            plt.xticks(x, key)
            plt.title(modellist[model])
            plt.savefig('Z:\学习\计设和节能\ALL PROGRAMS/3.21\Windows\images/%d.png' %model)
            imshowpic(model)
            # plt.show()

def imshowpic(model):
    picDialog = QDialog()
    layout = QHBoxLayout()
    label = QLabel()
    label.setToolTip("这是一个图片标签")
    label.setPixmap(QPixmap('Z:\学习\计设和节能\ALL PROGRAMS/3.21\Windows\images/%d.png' %model))
    layout.addWidget(label)
    picDialog.setLayout(layout)
    picDialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    example = DataGrid()
    example.show()
    sys.exit(app.exec_())