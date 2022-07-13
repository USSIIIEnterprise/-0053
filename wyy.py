# import sqlite3
# conn = sqlite3.connect("E:/Python39/poor_personal_code/PyQt5/db/database.db")

# cursor = conn.cursor()
# sql = """pragma table_info(fake)"""
# cursor.execute(sql)
# result = cursor.fetchall()
# print(result)
# print(type(result))
# conn.close()

# 创建游标
# cursor = conn.cursor()
# # 查询数据
# sql = "select * from fake"
# values = cursor.execute(sql)
# for i in values:
#     print(i)
# # 查询数据 2
# sql = "select * from fake where id=?"
# values = cursor.execute(sql, (1,))
# for i in values:
#     # print('id:', i[0])
#     # print('name:', i[1])
#     # print('age:', i[2])
#     print("***************************************")
# # 提交事物
# conn.close()

from cProfile import label
import sqlite3 # 导入包
import matplotlib.pyplot as plt
import re
from numpy import number

def getIndex(text):
    f1 = re.findall('(\d+)',text)
    if len(f1) > 0:
        return f1[0]
    else:
        return 0

placeName = ["大丰", "射阳", "金湖", "宝应", "三龙"]
countInformation = {"大丰":0, "射阳":0, "金湖":0, "宝应":0, "三龙":0, "other":0}
Dictionaries = [{}, {}, {}, {}, {}]
conn = sqlite3.connect('Z:\学习\计设和节能\ALL PROGRAMS/3.20\Windows/db/database.db') # 连接到SQLite数据库
cursor = conn.cursor() # 创建一个Cursor
cursor.execute("select fake.description from fake") # 使用SQL语句对数据库进行操作
for row in cursor.fetchall(): # 从fetchall中读取操作
    name = row[0][0] + row[0][1]
    if name not in placeName:
        countInformation["other"] += 1
    else:
        countInformation[name] += 1
        index = placeName.index(name)
        num = getIndex(row[0])
        if num == 0:
            continue
        if num in Dictionaries[index]:
            Dictionaries[index][num] += 1
        else:
            Dictionaries[index][num] = 1

# print(placeName)
print(countInformation)
print(Dictionaries)
cursor.close()#关闭Cursor
conn.close()

plt.figure(figsize=(6,6))                 # 将画布设定为正方形
plt.rcParams['font.sans-serif']=['Simhei']
label='大丰','射阳','金湖','宝应','三龙'                 # 各类别标签
# label = 'a', 'b', 'b', 'b', 'b'
sizes=[countInformation["大丰"],countInformation["射阳"],countInformation["金湖"],countInformation["宝应"],countInformation["三龙"]]
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
plt.show()