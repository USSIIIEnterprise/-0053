'''
  程序名称：GPS定位 v1.1
  函数说明：两个一维数组 存放所有风机坐标:LOCATION_East,LOCATION_North 可以直接import调用
         点击运行后，会提供如下参数  East,East2:东经   North,North2:北纬   Height,Height2:高度   Pressure，Pressure2:气压
  重要返回值：SPOT，SPOT2 代表两个不同位置的GPS传来的最后消失信号最近的点，与数组 LOCATION_East,LOCATION_North 的位置对应
              如果SPOT == -1 代表人员还在风机外面，GPS仍然在正常发送信号，不需要将风机显示红色       如果SPOT != -1 代表信号消失且最后位置离风机很近，其数值就是对应风机的编号，将风机显示红色
           EB,EB2为防误判消抖系数，默认为>1，也就是2次检测不到GPS信号就判断为信号真丢失
           默认自己的端口  B00，字符串在第58行可以更改
           默认接收端口1  F01，字符串在第69行可以更改
           默认接收端口2  F11，字符串在第95行可以更改
  放进mainWindow的方法：  stack1UI中写按键 btn1对应main 点击开始GPS接受和计算       btn2对应main_close 点击关闭GPS通讯(千万记得要关!)
                        import GPS       from GPS import North,East,Height,Pressure,SPOT,North2,East2,Height2,Pressure2,SPOT2

'''
import socket
import threading
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

LOCATION_East = [
                 114.5710000, 114.5500000, 114.5565000, 114.5545000, 114.5526667,  # 1-5
                 114.5566667, 114.5196667, 114.5091667, 114.5050000, 114.5020000,  # 6-10
                 114.5096667, 114.5075000, 114.5036667, 114.5008333, 114.4908333,  # 11-15
                 114.4965000, 114.4920000, 114.4891667, 114.4840000, 114.4838333,  # 16-20
                 114.4793333, 114.4758333, 114.4715000, 114.4880000, 114.4836667,  # 21-25
                 120.4888596, 120.4825816, 120.4788987, 120.4751652, 120.4703928,  # 26-30
                 120.4666892, 120.4629873, 120.4595318, 120.4831499, 120.4761261,  # 31-35
                 120.4707338, 120.4529005, 120.4486530, 120.4443980, 120.4404424,  # 36-40
                 120.4590549, 120.4546929, 120.4584960, 120.4547494, 120.4260136]  # 41-45

LOCATION_North = [
                  33.4583333, 33.4563333, 33.4556667, 33.4550000, 33.4573333,  # 1-5
                  33.4673333, 33.4705000, 33.4670000, 33.4563333, 33.4535000,  # 6-10
                  33.4736667, 33.5036667, 33.4681667, 33.4588333, 33.4558333,  # 11-15
                  33.4541667, 33.4665000, 33.4743333, 33.4695000, 33.4801667,  # 16-20
                  33.4760000, 33.4831667, 33.4788333, 33.4893333, 33.4851667,  # 21-25
                  33.4416415, 33.4361260, 33.4326895, 33.4291831, 33.4248468,  # 26-30
                  33.4213987, 33.4179500, 33.4147437, 33.4469052, 33.4509190,  # 31-35
                  33.4563548, 33.4419428, 33.4381961, 33.4343727, 33.4309654,  # 36-40
                  33.4575613, 33.4536055, 33.4661969, 33.4626774, 33.4460153]  # 41-45
LOCATION_Height = []

def recvlink():
    global Pressure, Height, East, North, EB, Switch ,Pressure2, Height2, East2, North2, EB2, Switch2, SPOT, SPOT2, Flag
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('myfrank-personal.top', 5248))
    sendip = "BAA"             # 自己的编号默认为B00
    client.send(sendip.encode('utf-8'))
    msg = client.recv(1024)
    print(msg.decode('utf-8'))

    while True:
        last_num = 3
        msg = client.recv(1024)
        msgtrans = msg.decode('utf-8')
        strlen = len(msgtrans)
        # print(msgtrans)       # 检测数据传输和解码是否正常
        if (msgtrans[0] == 'F') and (msgtrans[1] == '0') and (msgtrans[2] == '1'):   # 接收来自B01信号
          if (msgtrans[3] == '-') and (msgtrans[4] == '1'):      # 判断是否为-1信号，是就只测气压的值
                EB += 1
                # 从第4位[3]开始检索有用数据，到strlen结束
                for num in range(3, strlen - 1):
                    if msgtrans[num] == 'P':
                        Pressure = float(msgtrans[20: num - 1])
                        last_num = 3
                if EB > 1:
                    if (Switch == 0):
                        compare()
                        Switch = 1























        if (msgtrans[0] == 'F') and (msgtrans[1] == '1') and (msgtrans[2] == '1'):  # 接收来自B11信号
          if (msgtrans[3] == '-') and (msgtrans[4] == '1'):  # 判断是否为-1信号，是就只测气压的值
                EB2 += 1
                # 从第4位[3]开始检索有用数据，到strlen结束
                for num in range(3, strlen - 1):
                    if msgtrans[num] == 'P':
                        Pressure2 = float(msgtrans[20: num - 1])
                        last_num = 3
                if EB2 > 1:
                    if (Switch2 == 0):
                        compare2()
                        Switch2 = 1


          else:  # 是正常信号
            for num in range(3, strlen - 1):
                if msgtrans[num] == 'N':
                    North2 = float(msgtrans[last_num: num - 1])
                    last_num = num + 2
                    EB2 = 0
                    Switch2 = 0
                    SPOT2 = -1
                if msgtrans[num] == 'E':
                    East2 = float(msgtrans[last_num: num - 1])
                    last_num = num + 2
                if msgtrans[num] == 'M':
                    Height2 = float(msgtrans[last_num: num - 1])
                    last_num = num + 2
                if msgtrans[num] == 'P':
                    Pressure = float(msgtrans[last_num: num - 1])
                    last_num = 3


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


def main():
    global  Flag
    Flag = 0

    t = threading.Thread(target = recvlink)
    t.start()


def main_close():
    global Flag
    Flag = 1

if __name__ == '__main__':
    main()
