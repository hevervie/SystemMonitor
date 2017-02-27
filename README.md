# 分布式集群运营管理系统
#### 设计说明

> **名称**：分布式集群运营管理系统

> **英文名**：SystemMonitor
> 
> **Logo**：

![这里写图片描述](http://img.blog.csdn.net/20160811161035299)

> **物理架构**：C/S架构，即客户端，服务器型架构

> **开发语言**：Python3.4，Django1.8.x

> **开发平台**：CentOS 7.2

> **最新版本**：v0.1

> **项目源码**：[https://github.com/dreamer2018/SystemMonitor](https://github.com/dreamer2018/SystemMonitor)

> **主要功能简述**：

**客户端：**

获取主机的系统资源，主要包括：

-   内存使用率
-   CPU占用率
-   磁盘I/O
-   磁盘空间使用率
-   网络延迟
-   主机所开端口
-   在线用户信息

客户端收集这些信息，并将这些信息发送至服务器

**服务器端：**

获取到客户端数据后，进行处理计算，策略匹配，对于异常数据通过发送邮件的方式进行告警

> **逻辑架构**：

 **基础逻辑架构图(2.0版)**：
 
![这里写图片描述](http://img.blog.csdn.net/20170227221417303?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvSVRfRFJFQU1fRVI=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

 **模块-类对应图(2.0版)**
 
 ![这里写图片描述](http://img.blog.csdn.net/20170227221449300?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvSVRfRFJFQU1fRVI=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

> **网络架构**：

**网络拓扑架构图(2.0版)：**

![这里写图片描述](http://img.blog.csdn.net/20160811161252003)

> **开发接口(2.0版)**：

![这里写图片描述](http://img.blog.csdn.net/20160811161353473)
![这里写图片描述](http://img.blog.csdn.net/20160811161412067)
![这里写图片描述](http://img.blog.csdn.net/20160811161421739)
![这里写图片描述](http://img.blog.csdn.net/20160811161430005)
![这里写图片描述](http://img.blog.csdn.net/20160811161440193)
![这里写图片描述](http://img.blog.csdn.net/20160811161450800)
![这里写图片描述](http://img.blog.csdn.net/20160811161525944)
![这里写图片描述](http://img.blog.csdn.net/20160811161534832)
![这里写图片描述](http://img.blog.csdn.net/20160811161554582)
![这里写图片描述](http://img.blog.csdn.net/20160811161603711)
![这里写图片描述](http://img.blog.csdn.net/20160811161612633)
![这里写图片描述](http://img.blog.csdn.net/20160811161620332)

更新点：
1. 完成对底层数据库更改，将pymysql变更为pymysql+SQLArchemy
2. 完成将计算转移，将计算从服务器端转义指客户端
3. 对部分代码进行优化，修改json传输格式
