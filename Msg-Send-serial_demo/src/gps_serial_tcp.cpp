/*蘑菇头GPS（绿色）*/
#include <ros/ros.h>

#include <actionlib/client/simple_action_client.h>

#include <nav_msgs/Odometry.h>
#include <geometry_msgs/Quaternion.h>
#include <geometry_msgs/PoseStamped.h>
#include <tf/transform_broadcaster.h>
#include <tf/tf.h>

#include <fstream>
#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>
#include <algorithm>
#include <cstdlib>
#include <inttypes.h>
#include <serial/serial.h>
#include <std_msgs/String.h>
#include <std_msgs/Empty.h>
#include <string.h>
#include <math.h>
#include <unistd.h> //close方法
#include <arpa/inet.h>
#include <sys/socket.h>
//serial init
serial::Serial ser0;
std::string command;
std::string rcv;
uint8_t buffer[256] = {0};
uint8_t write_x[] = {'l', 'o', 'g', ' ', 'g', 'p', 'g', 'g', 'a', ' ', 'o', 'n', 't', 'i', 'm', 'e', ' ', '1', '\n'}; //'\0'
uint8_t stop_x[] = {'u', 'n', 'l', 'o', 'g', 'a', 'l', 'l', '\n'};
//uint8_t write_x[] = {'l', 'o', 'g', ' ', 'g', 'p', 'g', 'g', 'a', ' ', 'o', 'n', 't', 'i', 'm', 'e', ' ', '1','\r','\n'};    //'\0'
//uint8_t write_x[] = {'l', 'o', 'g', ' ', 'c', 'o', 'm', 'c', 'o', 'n', 'f', 'i', 'g'};
char *ip[] = {"192.168.1.124", "81.68.195.9"}; //******ip,本地对方
int position = 0;
int height_position = 0;
double weidu;
double jingdu;
std::string weidu_earth;
std::string jingdu_earth;
double height;
std::string sum_str = "";		//处理的，也是最终要发送的
std::string sum_baidu_str = ""; //
std::string temp;				//字符串临时处理变量
int find_gpgga = 0;
bool send_flag = false;
void error_handling(char *message) //出现链接错误退出
{
	fputs(message, stderr);
	fputc('\n', stderr);
	exit(1);
}
int main(int argc, char *argv[]) //如果有参数，则运行命令是rosrun serial_demo gps_serial serv_adr my_ip   ;在次情况下serv_adr=windows显示地图IP,my_ip=192.168.1.120,只能是在小车局域网下
{								 //ser0.write(buffer[20],20);//my_ip接到GPS的IP
	std::cout << argc << std::endl;
	if (argc == 3)
	{
		ip[0] = argv[1];
		ip[1] = argv[2];
		std::cout << ip[0] << std::endl;
		std::cout << ip[1] << std::endl;
		std::cout << argc << std::endl;
	}
	//创建通信套接字
	int sock = socket(PF_INET, SOCK_STREAM, 0); //通信方式SOCK_STREAM一般指tcp/ip编程，第三个参数选择默认0，PF_INET:IPv4协议族也同AF_INET

	if (sock == -1)
		error_handling("tcp socket() create failed.");
	struct sockaddr_in serv_adr; //定义ip地址端口,应该只需要对方ip(及)，my_ip可以不用

	memset(&serv_adr, 0, sizeof(serv_adr)); //用来清空数组
	serv_adr.sin_family = AF_INET;
	//IP地址
	serv_adr.sin_addr.s_addr = inet_addr(ip[1]); // inet_pton(AF_INET, "192.168.237.131", &addr.sin_addr.s_addr);
	//PORT，大端端口
	serv_adr.sin_port = htons(5248);

	//链接
	int ret = connect(sock, (struct sockaddr *)&serv_adr, sizeof(serv_adr));
	if (ret == -1)
	{
		error_handling("tcp connect failed");
	}
	//绑定代号
	char BindNum[3];
	BindNum[0] = 'B';
	BindNum[1] = '1'; //change
	BindNum[2] = '0'; //change
	//发送绑定代号
	write(sock, BindNum, strlen(BindNum) + 1); //+1将结束符'\0'带上

	char sendNum[3];
	sendNum[0] = 'S';
	sendNum[1] = '0'; //change maybe here
	sendNum[2] = '1'; //change

	/*向网页端百度地图*/
	int sock_baidu = socket(PF_INET, SOCK_STREAM, 0);
	if (sock_baidu == -1)
		error_handling("tcp socket_baidu create failed.");
	struct sockaddr_in serv_adr_baidu;
	memset(&serv_adr_baidu, 0, sizeof(serv_adr_baidu));
	serv_adr_baidu.sin_family = AF_INET;
	serv_adr_baidu.sin_addr.s_addr = inet_addr(ip[1]);
	serv_adr_baidu.sin_port = htons(5249);
	int ret_baidu = connect(sock_baidu, (struct sockaddr *)&serv_adr_baidu, sizeof(serv_adr_baidu));
	if (ret_baidu == -1)
		error_handling("tcp connect failed");
	char send_baidNum[3];
	send_baidNum[0] = 'S';
	send_baidNum[1] = '1';
	send_baidNum[2] = '1';
	/*向网页端百度地图取消了绑定和断开链接环节*/
	sum_str.push_back(sendNum[0]);
	sum_str.push_back(sendNum[1]);
	sum_str.push_back(sendNum[2]);
	sum_baidu_str.push_back(send_baidNum[0]);
	sum_baidu_str.push_back(send_baidNum[1]);
	sum_baidu_str.push_back(send_baidNum[2]);
	ros::init(argc, argv, "send_goal");
	ros::NodeHandle nh;
	int i = 0, k = -1;
	//串口0
	try
	{
		//设置串口属性，并打开串口
		ser0.setPort("/dev/ttyUSB0");
		ser0.setBaudrate(115200); //115200
		serial::Timeout to = serial::Timeout::simpleTimeout(1000);
		ser0.setTimeout(to);
		ser0.open();
	}
	catch (serial::IOException &e)
	{
		ROS_ERROR_STREAM("Unable to open port 0");
		return -1;
	}
	//串口0
	ROS_INFO("port 0 opened. ");

	//main loop
	//std::cout << sizeof(write_x) << std::endl;
	ser0.write(write_x, sizeof(write_x));
	//std::cout << sizeof(write_x) << std::endl;
	while (ros::ok())
	{
		if (ser0.available())
		{
			rcv = ser0.readline();

			//std::cout << " buffer = ";
			//std::cout << "size of rcv=" << rcv.size() << std::endl;
			//std::cout << "rcv =" << rcv << std::endl;
			/*
			for (i = 0; i < rcv.size(); i++)
			{
				buffer[i] = rcv[i];
				//buffer[i] = 0xff&(buffer[i]);
				//std::cout << buffer[i];
			}
			*/
			//这个40不确定
			if (rcv.size() > 70)
			{
				find_gpgga = rcv.find("$GPGGA");
				if (find_gpgga != -1)
				{
					/******处理数据*******/
					/*定义消息头*/
					/*定义消息头*/
					position = rcv.find(',');
					rcv.erase(0, position + 1); //左开右边闭  ,所以加个1：   第二个是number,,,,,,$GPGGA

					position = rcv.find(',');
					rcv.erase(0, position + 1); //utc时间

					position = rcv.find(',');
					temp = rcv.substr(0, position);																		  //纬度未处理
					weidu = atof(temp.substr(0, 2).c_str()) + atof(temp.substr(2, temp.length()).c_str()) / double(60.0); //处理
					//printf("weidu=%.7f\n", weidu);
					rcv.erase(0, position + 1);
					sum_str.append(std::to_string(weidu));
					sum_str.append(",");

					position = rcv.find(',');
					weidu_earth = rcv.substr(0, position); //纬度半球
					//std::cout << "纬度半球=";
					//std::cout << weidu_earth << std::endl;
					rcv.erase(0, position + 1);
					sum_str.append(weidu_earth);
					sum_str.append(",");

					position = rcv.find(',');
					temp = rcv.substr(0, position); //经度未处理
					jingdu = atof(temp.substr(0, 3).c_str()) + atof(temp.substr(3, temp.length()).c_str()) / double(60.0);
					//printf("jingdu=%.7f\n", jingdu);
					rcv.erase(0, position + 1);
					sum_str.append(std::to_string(jingdu));
					sum_str.append(",");

					position = rcv.find(',');
					jingdu_earth = rcv.substr(0, position);
					//std::cout << "经度半球=";
					//std::cout << jingdu_earth << std::endl;
					rcv.erase(0, position + 1);
					sum_str.append(jingdu_earth);
					sum_str.append(",");

					position = rcv.find('M');						//第一个M，是高
					height_position = rcv.rfind(',', position - 2); //这种找发不适应找经纬度，因为最后的十六进制表示中有E    //但可以先找第一个M,将后面给删掉
					height = atof(rcv.substr(height_position + 1, position - height_position - 2).c_str());
					//printf("height=%fM\n", height);

					sum_str.append(std::to_string(height));
					sum_str.append(",M,-1,P");
					//std::cout << "sum_str=";
					//std::cout << sum_str << std::endl;
					/*******处理数据,是将数据发送出去，maybe change,sendto一般UDP协议中,但是如果在TCP中connect函数调用后也可以用.*********/
					//write(sock, sum_str.c_str(), sum_str.size());//strlen()+1-->字符数组
					sum_baidu_str = sum_str;
					sum_str.append(",1,1,1,1,1,1");
					sum_baidu_str[1] = send_baidNum[1];
					sum_baidu_str[2] = send_baidNum[2];
				}
			}
			else
			{
				sum_str.append("-1,-1,-1,-1,-1,M,-1,P,1,1,1,1,1,1");
				sum_baidu_str.append("-1,-1,-1,-1,-1,M,-1,P");
			}
			std::cout << sum_str << std::endl;
			sendto(sock, sum_str.c_str(), sum_str.size(), 0, (struct sockaddr *)&serv_adr, sizeof(serv_adr));
			sendto(sock_baidu, sum_baidu_str.c_str(), sum_baidu_str.size(), 0, (struct sockaddr *)&serv_adr_baidu, sizeof(serv_adr_baidu));
			//std::cout << std::endl;
			//std::cout << "serial has been received. " << std::endl;
		}

		//decode info from serial

		sum_str = "";
		sum_baidu_str = "";
		//消息头添加
		sum_str.push_back(sendNum[0]);
		sum_str.push_back(sendNum[1]);
		sum_str.push_back(sendNum[2]);
		sum_baidu_str.push_back(send_baidNum[0]);
		sum_baidu_str.push_back(send_baidNum[1]);
		sum_baidu_str.push_back(send_baidNum[2]);

	} //main loop end

	ser0.write(stop_x, sizeof(stop_x));	  //结束命令
	std::cout << "stop gps" << std::endl; //结束命令
	//方法2关闭tcp链接
	char closeNum[1];
	closeNum[0] = 'E';
	write(sock, closeNum, strlen(closeNum) + 1);
	//关闭tcp链接
	return 0;
}
//uint8_t//用char,string-->char[]
/*可能改掉serial flag*/
/*
if(rcv.size()>numX)
{
	处理数据，find("$GPGGA")
}else
{
	sum_str.append("-1,-1,-1,-1,-1,M")；
}


*/
