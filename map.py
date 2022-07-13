from unicodedata import name
from PyQt5.QtSql import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from GPS import North,East,Height,Pressure,SPOT,main
import sys
import os
import folium
import time
import threading




class MapWindow(QWidget):
   def gps_image(self):
     # while True:
        # 调用高德地图http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}
        Map = folium.Map(location=[North, East],
                         # 大丰风力发电公司的坐标
                         zoom_start=14,
                         control_scale=True,
                         # tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
                         tiles='http://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}',
                         attr='default')

        Map.add_child(folium.LatLngPopup())  # 显示鼠标点击点经纬度
        Map.add_child(folium.ClickForMarker(popup='Waypoint'))  # 将鼠标点击点添加到地图上
        # Map.add_child(folium.ClickForMarker(popup='Waypoint')) 将风力发电机坐标显示到地图上

        # 标记一个实心圆
        folium.CircleMarker(
            location=[North, East],
            radius=10,  # 圈的大小
            popup='popup',
            color='#DC143C',  # 圈的颜色
            fill=True,
            fill_color='#6495E'  # 填充颜色
        ).add_to(Map)

        # 在QWebEngineView中加载网址
        # Map.save("save_map.html")
        # time.sleep(10)  # 十秒刷新一次地图


   def __init__(self):
        super(MapWindow, self).__init__()
        self.setWindowTitle('地图显示')
        self.resize(1200, 800)
        # 新建一个QWebEngineView()对象
        self.qwebengine = QWebEngineView(self)
        # 设置网页在窗口中显示的位置和大小
        # self.qwebengine.setGeometry(20, 20, 960, 600)  #小图
        self.qwebengine.setGeometry(20, 20, 1400, 800)
        # g = threading.Thread(target = self.gps_image)
        # g.start()
        self.gps_image()
        path = "file:\\" + os.getcwd() + "\\index.html"
        path = path.replace('\\', '/')
        self.qwebengine.load(QUrl(path))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MapWindow()
    win.show()
    sys.exit(app.exec_())