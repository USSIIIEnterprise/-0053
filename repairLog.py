import sys
import re
from unicodedata import name
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *


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
        query = QSqlQuery()
        # 创建表
        query.exec("create table test(id int primary key, name vchar, sex vchar, age int, date vchar, reason vchar)")

        # 添加记录
        query.exec("insert into test values(1,'张三','男',20,'计算机','雷电停机')")
        query.exec("insert into test values(2,'李四1','男',19,'经管','雷电停机')")
        query.exec("insert into test values(3,'王五1','男',22,'机械','雷电停机')")
        query.exec("insert into test values(4,'赵六1','男',21,'法律','雷电停机')")
        query.exec("insert into test values(5,'小明1','男',20,'英语','雷电停机')")
        query.exec("insert into test values(6,'小李1','女',19,'计算机','雷电停机')")
        query.exec("insert into test values(7,'小张1','男',20,'机械','雷电停机')")
        query.exec("insert into test values(8,'小刚1','男',19,'经管','雷电停机')")
        query.exec("insert into test values(9,'张三2','男',21,'计算机','雷电停机')")
        query.exec("insert into test values(10,'张三3','女',20,'法律','雷电停机')")
        query.exec("insert into test values(11,'王五2','男',19,'经管','雷电停机')")
        query.exec("insert into test values(12,'张三4','男',20,'计算机','雷电停机')")
        query.exec("insert into test values(13,'小李2','男',20,'机械','雷电停机')")
        query.exec("insert into test values(14,'李四2','女',19,'经管','雷电停机')")
        query.exec("insert into test values(15,'赵六3','男',21,'英语','雷电停机')")
        query.exec("insert into test values(16,'李四2','男',19,'法律','雷电停机')")
        query.exec("insert into test values(17,'小张2','女',22,'经管','雷电停机')")
        query.exec("insert into test values(18,'李四3','男',21,'英语','雷电停机')")
        query.exec("insert into test values(19,'小李3','女',19,'法律','雷电停机')")
        query.exec("insert into test values(20,'王五3','女',20,'机械','雷电停机')")
        query.exec("insert into test values(21,'张三4','男',22,'计算机','雷电停机')")
        query.exec("insert into test values(22,'小李2','男',20,'法律','雷电停机')")
        query.exec("insert into test values(23,'张三5','男',19,'经管','雷电停机')")
        query.exec("insert into test values(24,'小张3','女',20,'计算机','雷电停机')")
        query.exec("insert into test values(25,'李四4','男',22,'英语','雷电停机')")
        query.exec("insert into test values(26,'赵六2','男',20,'机械','雷电停机')")
        query.exec("insert into test values(27,'小李3','女',19,'英语','雷电停机')")
        query.exec("insert into test values(28,'王五4','男',21,'经管','雷电停机')")

        return True

    def __init__(self):
        super().__init__()
        self.setWindowTitle("分页查询例子")
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

    def initUI(self):
        # 创建窗口
        self.createWindow()
        # 设置表格
        self.setTableView()

        # 信号槽连接
        self.prevButton.clicked.connect(self.onPrevButtonClick)
        self.nextButton.clicked.connect(self.onNextButtonClick)
        self.switchPageButton.clicked.connect(self.onSwitchPageButtonClick)

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
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

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

        vbox_editInformation.addStretch(0)
        vbox_editInformation.addWidget(self.refreshButton)
        vbox_editInformation.addWidget(self.addButton)
        vbox_editInformation.addWidget(self.findButton)
        vbox_editInformation.addWidget(self.delButton)
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

        print('totalRecrodCount=' + str(self.totalRecrodCount))
        print('totalPage=' + str(self.totalPage))

        # self.queryModel.setEditStrategy(QSqlQueryModel.OnFieldChange)

        # 设置表格表头
        self.tableModel.setHeaderData(0, Qt.Horizontal, "工号")
        self.tableModel.setHeaderData(1, Qt.Horizontal, "姓名")
        self.tableModel.setHeaderData(2, Qt.Horizontal, "性别")
        self.tableModel.setHeaderData(3, Qt.Horizontal, "故障代码")
        self.tableModel.setHeaderData(4, Qt.Horizontal, "工作日期")
        self.tableModel.setHeaderData(5, Qt.Horizontal, "故障原因")

    # 得到记录数
    def getTotalRecordCount(self):
        self.tableModel.setTable("test")
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
        self.cb.addItems(['点击进行选择','工号', '姓名', '性别', '故障代码', '工作日期', '故障原因'])
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
        message = ['工号', '姓名','故障代码', '故障原因']
        name = self.getname(self.cb.currentText())
        if self.cb.currentText() in message:
            self.lineEdit = QLineEdit()
            self.chooseDialog_formlayout.addRow(informationLabel, self.lineEdit)
            self.OKButton.clicked.connect(lambda: self.queryRecord(name, self.lineEdit.text()))
        elif self.cb.currentText() == '性别':
            self.genderComboBox = QComboBox()
            self.genderComboBox.addItems(['男', '女'])
            self.chooseDialog_formlayout.addRow(informationLabel, self.genderComboBox)
            self.OKButton.clicked.connect(lambda: self.queryRecord(name, self.genderComboBox.currentText()))
        elif self.cb.currentText() == '工作日期':
            dateTimeEdit2 = QDateTimeEdit(QDateTime.currentDateTime())
            dateTimeEdit2.setDisplayFormat('yyyy-MM-dd')
            # dateTimeEdit2.setDisplayFormat('yyyy-MM-dd  HH:mm:ss')
            dateTimeEdit2.setCalendarPopup(True)
            self.chooseDialog_formlayout.addRow(informationLabel, dateTimeEdit2)
            self.OKButton.clicked.connect(lambda: self.queryRecord(name, dateTimeEdit2.text()))
    
    def getname(self, message):
        name = ['id', 'name', 'sex', 'age', 'date', 'reason']
        messages = ['工号', '姓名', '性别', '故障代码', '工作日期', '故障原因']
        index = messages.index(message)
        return name[index]
    
    def queryRecord(self, name, realname):
        print(name)
        print(realname)
        self.tableModel.setFilter(("%s = '%s'" % (name, realname)))
        self.tableModel.select()
        self.screenDialog.close()
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = DataGrid()
    example.show()
    sys.exit(app.exec_())