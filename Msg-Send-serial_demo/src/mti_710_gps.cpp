/*mti-710橙色（红色）*/
#include <ros/ros.h>
#include <string>
#include <geometry_msgs/Vector3Stamped.h>

#include <sensor_msgs/FluidPressure.h>
#include <sensor_msgs/NavSatFix.h>
#include <message_filters/subscriber.h>
#include <message_filters/synchronizer.h>
#include <message_filters/sync_policies/approximate_time.h>
#include <message_filters/time_synchronizer.h>
#include <boost/thread/thread.hpp>
#include <unistd.h> //close方法
#include <arpa/inet.h>
#include <sys/socket.h>
#include <iostream>
std::string sum_string = "";
std::string sum_baidu_str = "";
std::string latitude = "";
std::string latitude_earth = "";
std::string longitude = "";
std::string longitude_earth = "";
std::string altitude = "";
std::string pressure = ""; //单位P
std::string acc_x = "";    //三轴加速度
std::string acc_y = "";
std::string acc_z = "";
std::string angle_x = "";
std::string angle_y = "";
std::string angle_z = "";
char *ip[] = {"192.168.1.124", "81.68.195.9"}; //******ip 本地，对方
//创建通信套接字
int sock = socket(PF_INET, SOCK_STREAM, 0); //通信方式SOCK_STREAM一般指tcp/ip编程，第三个参数选择默认0，PF_INET:IPv4协议族也同AF_INET
struct sockaddr_in serv_adr;                //定义ip地址端口,应该只需要对方ip(及)，my_ip可以不用
//绑定代号
char BindNum[3];

//发送文件消息头
char sendNum[3];
char send_baidNum[3];
//方法2关闭tcp链接，关闭消息头
char closeNum[1];

bool send_flag = false;
/*向网页端百度地图*/
int sock_baidu = socket(PF_INET, SOCK_STREAM, 0);
struct sockaddr_in serv_adr_baidu; //ip
/*向网页端百度地图取消了绑定和断开链接环节*/
/*
latitude  纬度
longitude 经度
altitude  海拔高度
*/
void error_handling(char *message) //出现链接错误退出
{
    fputs(message, stderr);
    fputc('\n', stderr);
    exit(1);
}
void multi_callback(const geometry_msgs::Vector3StampedConstPtr &acc, const geometry_msgs::Vector3StampedConstPtr &angle, const sensor_msgs::FluidPressureConstPtr &press, const sensor_msgs::NavSatFixConstPtr &gnss)
{
    if (gnss->status.status == 0) //检测到gps
    {
        if (gnss->latitude >= 0) //>0 为北纬
        {
            latitude_earth = "N";
        }
        else
        {
            latitude_earth = "S";
        }

        if (gnss->longitude >= 0) //>0 为东经
        {
            longitude_earth = "E";
        }
        else
        {
            longitude_earth = "W";
        }
        latitude = std::to_string(gnss->latitude); //float64->std::string
        longitude = std::to_string(gnss->longitude);
        altitude = std::to_string(gnss->altitude);
    }
    else //未检测到
    {
        latitude = "-1";
        latitude_earth = "-1";
        longitude = "-1";
        longitude_earth = "-1";
        altitude = "-1";
    }
    pressure = std::to_string(press->fluid_pressure); //float64->std::string
    //跟一个气压高度(算出)
    //三轴加速度
    acc_x = std::to_string(acc->vector.x); //float64->std::string
    acc_y = std::to_string(acc->vector.y);
    acc_z = std::to_string(acc->vector.z);
    //三轴角速度
    angle_x = std::to_string(angle->vector.x); //float64->std::string
    angle_y = std::to_string(angle->vector.y);
    angle_z = std::to_string(angle->vector.z);
    sum_string = sum_string + latitude + "," + latitude_earth + "," + longitude + "," + longitude_earth + "," + altitude + ",M," + pressure + ",P," + acc_x + "," + acc_y + "," + acc_z + "," + angle_x + "," + angle_y + "," + angle_z;
    sum_baidu_str = sum_string;
    sum_baidu_str[1] = send_baidNum[1];
    sum_baidu_str[2] = send_baidNum[2];
    sendto(sock, sum_string.c_str(), sum_string.size(), 0, (struct sockaddr *)&serv_adr, sizeof(serv_adr));
    sendto(sock_baidu, sum_baidu_str.c_str(), sum_baidu_str.size(), 0, (struct sockaddr *)&serv_adr_baidu, sizeof(serv_adr_baidu));

    sum_string = "";
    sum_baidu_str = "";
    //消息头添加
    sum_string.push_back(sendNum[0]);
    sum_string.push_back(sendNum[1]);
    sum_string.push_back(sendNum[2]);
    sum_baidu_str.push_back(send_baidNum[0]);
    sum_baidu_str.push_back(send_baidNum[1]);
    sum_baidu_str.push_back(send_baidNum[2]);
}
int main(int argc, char **argv)
{
    BindNum[0] = 'B';
    BindNum[1] = '1';
    BindNum[2] = '2';
    sendNum[0] = 'S';
    sendNum[1] = '0';
    sendNum[2] = '1';
    closeNum[0] = 'E';
    send_baidNum[0] = 'S';
    send_baidNum[1] = '0';
    send_baidNum[2] = '0';
    std::cout << argc << std::endl;
    if (argc == 3)
    {
        ip[0] = argv[1];
        ip[1] = argv[2];
        std::cout << ip[0] << std::endl;
        std::cout << ip[1] << std::endl;
        std::cout << argc << std::endl;
    }
    //创建通信套接字，全局
    if (sock == -1)
        error_handling("tcp socket() create failed.");
    //定义ip地址端口,应该只需要对方ip(及)----->全局
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
    //发送绑定代号
    write(sock, BindNum, strlen(BindNum) + 1); //+1将结束符'\0'带上
    //消息头添加
    sum_string.push_back(sendNum[0]);
    sum_string.push_back(sendNum[1]);
    sum_string.push_back(sendNum[2]);

    /*向网页端百度地图*/
    if (sock_baidu == -1)
        error_handling("tcp socket_baidu create failed.");
    memset(&serv_adr_baidu, 0, sizeof(serv_adr_baidu));
    serv_adr_baidu.sin_family = AF_INET;
    serv_adr_baidu.sin_addr.s_addr = inet_addr(ip[1]);
    serv_adr_baidu.sin_port = htons(5249);
    int ret_baidu = connect(sock_baidu, (struct sockaddr *)&serv_adr_baidu, sizeof(serv_adr_baidu));
    if (ret_baidu == -1)
        error_handling("tcp connect failed");
    sum_baidu_str.push_back(send_baidNum[0]);
    sum_baidu_str.push_back(send_baidNum[1]);
    sum_baidu_str.push_back(send_baidNum[2]);
    /*向网页端百度地图取消了绑定和断开链接环节*/

    ros::init(argc, argv, "mti_710_gps_data_process"); //创建节点
    ros::NodeHandle n;

    //数据同步
    typedef message_filters::sync_policies::ApproximateTime<geometry_msgs::Vector3Stamped, geometry_msgs::Vector3Stamped,
                                                            sensor_msgs::FluidPressure, sensor_msgs::NavSatFix>
        syncPolicy;
    message_filters::Subscriber<geometry_msgs::Vector3Stamped> sub_acc(n, "/imu/acceleration", 10, ros::TransportHints().tcpNoDelay());
    message_filters::Subscriber<geometry_msgs::Vector3Stamped> sub_angle(n, "/imu/angular_velocity", 10, ros::TransportHints().tcpNoDelay());
    message_filters::Subscriber<sensor_msgs::FluidPressure> sub_press(n, "/pressure", 10, ros::TransportHints().tcpNoDelay());
    message_filters::Subscriber<sensor_msgs::NavSatFix> sub_gps(n, "/gnss", 10, ros::TransportHints().tcpNoDelay());
    message_filters::Synchronizer<syncPolicy> synch(syncPolicy(10), sub_acc, sub_angle, sub_press, sub_gps);

    synch.registerCallback(boost::bind(&multi_callback, _1, _2, _3, _4));
    ros::spin();                                 //等待回调函数
    write(sock, closeNum, strlen(closeNum) + 1); //关闭
    return 0;
}
