from operator import index
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class createWarning(QDialog):
    def __init__(self,index):
        super().__init__()
        global text
        text = index
        self.setWindowTitle(index + "组跌倒！警告！")
        self.resize(350, 350)

    def m_resize(self, w_box, h_box, pil_image):
        w, h = pil_image.width(), pil_image.height()  # 获取图像的原始大小

        f1 = 1.0 * w_box / w
        f2 = 1.0 * h_box / h

        factor = min([f1, f2])

        width = int(w * factor)

        height = int(h * factor)
        # return pil_image.resize(width, height)
        return pil_image.scaled(width, height)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        # 绘制图形
        image= QImage('Z:\学习\计设和节能\ALL PROGRAMS/3.21\Windows\images/fall.png')
        rect = QRect(0, 0, image.width(), image.height())
        painter.drawImage(rect, image)


        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = createWarning()
    mainWindow.show()
    sys.exit(app.exec_())     