#include <iostream>
#include <boost/thread/thread.hpp>
#include <unistd.h> //close方法
#include <arpa/inet.h>
#include <sys/socket.h>
#include <string>
#include <ros/ros.h>
#include <message_filters/subscriber.h>
#include <message_filters/synchronizer.h>
#include <message_filters/sync_policies/approximate_time.h>

#include <sensor_msgs/FluidPressure.h>
#include <sensor_msgs/NavSatFix.h>
//#include <message_filters/time_synchronizer.h>

std::string sum_string = "";
std::string latitude = "";
std::string latitude_earth = "";
std::string longitude = "";
std::string longitude_earth = "";
std::string altitude = "";
std::string pressure = "";                       //单位P
char *ip[] = {"192.168.1.124", "81.68.195.9"}; //******ip 本地，对方

int sock = socket(PF_INET, SOCK_STREAM, 0); //通信方式SOCK_STREAM一般指tcp/ip编程，第三个参数选择默认0，PF_INET:IPv4协议族也同AF_INET
struct sockaddr_in serv_adr;                //定义ip地址端口,应该只需要对方ip(及)，my_ip可以不用
//绑定代号
char BindNum[3];

//发送文件消息头
char sendNum[3];

//方法2关闭tcp链接，关闭消息头
char closeNum[1];
bool send_flag = false;
void error_handling(char *message) //出现链接错误退出
{
    fputs(message, stderr);
    fputc('\n', stderr);
    exit(1);
}
void multicallback(const sensor_msgs::NavSatFixConstPtr &gnss, const sensor_msgs::FluidPressureConstPtr &press)
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
        altitude=std::to_string(gnss->altitude);
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
    sum_string = sum_string + latitude + "," + latitude_earth + "," + longitude + "," + longitude_earth + "," + altitude + ",M," + pressure + ",P";
    sendto(sock, sum_string.c_str(), sum_string.size(), 0, (struct sockaddr *)&serv_adr, sizeof(serv_adr));
    //sleep(100);

    
        
        sum_string = "";
        //消息头添加
        
        sum_string.push_back(sendNum[0]);
        sum_string.push_back(sendNum[1]);
        sum_string.push_back(sendNum[2]);

    
}
int main(int argc, char **argv)
{
    BindNum[0] = 'B';
    BindNum[1] = 0xfe;
    BindNum[2] = 0xff;
    sendNum[0] = 'S';
    sendNum[1] = 0xff;
    sendNum[2] = 0xff;
    closeNum[0] = 'E';
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

    ros::init(argc, argv, "mti_710_gps_pressure");
    ros::NodeHandle n;

    message_filters::Subscriber<sensor_msgs::NavSatFix> sub_gps(n, "/gnss", 10, ros::TransportHints().tcpNoDelay());
    message_filters::Subscriber<sensor_msgs::FluidPressure> sub_press(n, "/pressure", 10, ros::TransportHints().tcpNoDelay());
    typedef message_filters::sync_policies::ApproximateTime<sensor_msgs::NavSatFix, sensor_msgs::FluidPressure> syncPolicy;
    message_filters::Synchronizer<syncPolicy> synch(syncPolicy(10), sub_gps, sub_press);
    synch.registerCallback(boost::bind(&multicallback, _1, _2));
    ros::spin();
    write(sock, closeNum, strlen(closeNum) + 1); //关闭
    return 0;
}