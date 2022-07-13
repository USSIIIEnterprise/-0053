from operator import index
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QMovie
from PyQt5 import QtWidgets, QtGui, QtCore

class createDialog(QDialog):
    def __init__(self, index, text, SPOT):
        global title, num ,N
        title = text
        num = index
        N = SPOT
        if num == 3:
            N = "位于顶层"
        if num == 2:
            N = "位于中层"
        if num == 1:
            N = "位于底层"
        super().__init__()
        self.setupUi(self)
        self.show()

        movie = QtGui.QMovie('Z:\学习\计设和节能\ALL PROGRAMS/3.21\Windows\images/problem1%d.gif'%num)
        size = QSize(self.label.geometry().size())
        movie.setScaledSize(size);
        print("w=%d, h=%d"% (size.width(),size.height()))
        self.label.setMovie(movie);
        movie.start();

    def setupUi(self,Dialog):
        Dialog.setObjectName("维修人员高度")
        Dialog.resize(400,600)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0,0,400,600))
        self.label.setObjectName("label")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self,Dialog):
        global title,N
        SPOT = N
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", title + SPOT))
        self.label.setText(_translate("Dialog", "TextLabel"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = createDialog(3, "A", 2)
    widget.show()
    sys.exit(app.exec_())