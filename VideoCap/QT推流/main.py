import cv2, time
import myfrank
import numpy as np
from PyQt5.QtGui import *

def mat2Qimage(colorimg):
    #colorimg = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    imgshow = cv2.cvtColor(colorimg, cv2.COLOR_BGR2RGB)#彩色
    height, width, bytesPerComponent = imgshow.shape
    bytesPerLine = bytesPerComponent * width #表示彩色图像每个像素占用3个（ndarray图像数组的第三维长度）字节的空间
    QImg = QImage(imgshow.data, width, height, bytesPerLine, QImage.Format_RGB888)
    return QImg
    

# Frame process function
def proc(frame):
    cv2.imshow("frame",frame) # Show the frame in OpenCV dialog
    if cv2.waitKey(1) & 0xFF == ord('q'): # Press 'Q' to exit
        ffp.stop()
    '''
    label.setPixmap(QPixmap.fromImage(mat2Qimage(frame)))
    '''

#Error process function
def errhnd(exception):
    print(exception)
    raise exception

#Demo
ffp = myfrank.FFPlayer('rtsp://myfrank-personal.top:554/live/35558', proc, errhnd)
ffp.start()
while ffp.is_alive():
    time.sleep(1)

cv2.destroyAllWindows()