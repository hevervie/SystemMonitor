# SystemMonitor
### 分布式集群监控系统
> python开发的一个基于分布式的集群监控系统，C/S架构

主要监控的系统属性有：
   - 内存使用率
   - CPU占用率
   - 磁盘I/O
   - 磁盘使用率
   - 外网延迟
   - 主机启动的端口信息
   - 在线用户
   
## 网络拓扑结构图(1.0)：
![网络拓扑图](https://github.com/dreamer2018/SystemMonitor/blob/master/Document/%E7%BD%91%E7%BB%9C%E6%8B%93%E6%89%91%E6%9E%B6%E6%9E%84-1.0%E7%89%88.png)

## 逻辑架构图(1.0)：
![逻辑架构图](https://github.com/dreamer2018/SystemMonitor/blob/master/Document/%E9%80%BB%E8%BE%91%E6%9E%B6%E6%9E%84%E5%9B%BE-1.0.png)

## 模块与类关系图(1.0)
![模块与类关系](https://github.com/dreamer2018/SystemMonitor/blob/master/Document/%E6%A8%A1%E5%9D%97%E4%B8%8E%E7%B1%BB%E5%85%B3%E7%B3%BB-1.0.png)

SystemResource类
类名： SystemResource
属性：无
描述：获取系统资源类，包括cpu,内存，网络，磁盘，端口，在线用户等信息。
方法：
|方法名	| 形参	| 返回值类型	| 功能描述|
|:--------|:-------:|:---------------:|:-----------:|
| get_cpu_info  |   无	|  scputimes	获取cpu信息
| get_mem_info  |	  无	|  tuple	获取内存信息
| get_disk_info |	mount_point(string)	tuple	获取磁盘信息
| get_net_info  |	  无	|  tuple	获取网络信息
| get_port_info |	  无	|  tuple	获取端口信息
| get_user_info |	  无	|  suser	获取在线用户信息

Information类
类名：Information
属性：info(string)
描述：对收集到的信息进行处理，转换成为可以通过网络传送的内容
方法：
方法名	形参	返回值类型	功能描述
trans_cpu_info	无	tuple	对cup信息进行转换
trans_mem_info	无	tuple	对内存信息进行转换
trans_disk_info	无	tuple	对磁盘信息进行转换
trans_net_info	无	dict	对网络信息进行转换
trans_user_info	无	tuple	对用户信息进行转换
trans_port_info	无	tuple	对端口信息进行转换
collect_all_info	无	tuple	对所有信息进行集成

Client类
类名：Client
属性：threadID(int),threadName(string)
描述：信息传送类，将信息发送至客户端
方法：
方法名	形参	返回值类型	功能描述
run	无	无	连接服务器，并将数据发送至服务器

Configure类
类名：Configure
属性：无
描述：读取配置文件
方法：
方法名	形参	返回值类型	功能描述
read_config	conf_name(string,配置文件名)
section(string)
option(string)	
int,string	
读取指定配置文件的指定内容
write_config	config_name(string,配置文件名)
section(string)
option(string)	
无	
写入测试文件


MainThread类
类名：MainThread
属性：threadID(int ,线程ID)
 name(string,线程名)
描述：服务器端主线程类，主要用来循环接受客户端的连接
方法：
方法名	形参	返回值类型	功能描述
run	无	无	循环接受客户端连接

ResponseThread类
类名：ResponseThread
属性：addr(string,客户端地址)
 	 tcpClient(socket,与客户端建立连接的套接字)
描述：接受客户端发来的数据，并交给下一模块继续处理
方法：
方法名	形参	返回值类型	功能描述
run	无	无	接受客户端发来的数据，并交给下一模块继续处理

Information类
类名：Information
属性：addr(string,客户端地址，或者说是信息所有者)
 data(string,客户端接收到的信息)
描述：将接收到的信息进行处理，解析
方法：
方法名	形参	返回值类型	功能描述
get_cpu_info	无	tuple	对cup信息进行转换
get_mem_info	无	tuple	对内存信息进行转换
get_disk_info	无	tuple	对磁盘信息进行转换
get_net_info	无	dict	对网络信息进行转换
get_user_info	无	tuple	对用户信息进行转换
get_port_info	无	tuple	对端口信息进行转换
get_all_info	无	tuple	对所有信息进行集成


InfoCompute类
类名：InfoCompute
属性：new_data(string,刚获取到的新数据)
 	 old_data(string,上一次的旧数据) 
描述：对获取到的信息进行计算，方便下一模块进行处理
方法：
方法名	形参	返回值类型	功能描述
get_cpu_precent	无	double	获取cpu使用率
get_svmem_precent	无	double	获取物理内存使用率
get_swap_precent	无	double	获取交换分区使用率
get_diskio_precent	无	double	获取磁盘IO使用率
get_disk_usage	无	double	获取磁盘分区使用率
get_netio_precent	无	double	获取网络IO使用率
get_user	无	tuple	获取用户列表
get_port	无	tuple	获取端口列表

Persistent类
类名：Persistent	
属性：无
描述：数据持久化操作
方法：
方法名	形参	返回值类型	功能描述
save_all_data	data(string,需要保存的数据)	无	保存所有数据
get_cpu_data	id(int ,数据ID,允许为空，空就选出全部)	tuple	获取数据库中cpu信息
get_svmem_data	id(int ,数据ID,允许为空，空就选出全部)	tuple	获取数据库中物理内存信息
get_swap_data	id(int ,数据ID,允许为空，空就选出全部)		tuple	获取数据库中虚拟内存信息
get_diskio_data	id(int ,数据ID,允许为空，选出空就全部)	   tuple	获取数据库中磁盘IO信息
get_disk_usage	id(int ,数据ID,允许为空，空就选出全部)	   tuple	获取磁盘使用率信息
get_netio_data	id(int ,数据ID,允许为空，空就选出全部)	tuple	获取网络IO信息
get_user_data	id(int ,数据ID,允许为空，空就选出全部)	tuple	获取用户数据
get_port_data	id(int ,数据ID,允许为空，空就选出全部)	tuple	获取端口信息

Alam类
类名：Alam
属性：mail(tuple,告警信息列表)
描述：警告类，主要是发送警告
方法：
方法名	形参	返回值类型	功能描述
get_send_lsit	level(int,告警等级)	tuple	通过告警等级，获取需要发送的邮箱列表

send_mail	message(string,告警信息)
level(int,告警等级)
	
无	
通过传入的邮箱列表，遍历发送信息
 
 Strategies类
类名：Strategies
属性：cpu_precent(double,cpu使用率阈值)
 svmem_precent(double,内存使用阈值)
 swap_precent(double,虚拟内存使用率阈值)
 	 diskio_precent(double,磁盘IO阈值)
 diskusage_precent(double,磁盘使用率阈值)
 netio_precent(double,网络使用率阈值)
 user(tuple,合法用户列表)
 port(tuple,合法端口列表)
描述：警告检测类，对数据进行过滤，按规定的策略
方法：
方法名	形参	返回值类型	功能描述
check_cpu_data	cpu_percent(double,当前)	tuple(level,message)	根据策略匹配
check_svmem_data	svmem_precent	tuple(level,message)	根据策略匹配
cheak_swap_data	swap_precent	tuple(level,message)	根据策略匹配
check_diskio_data	diskio_precent	tuple(level,message)	根据策略匹配
check_diskusage_data	diskusage_precent	tuple(level,message)	根据策略匹配
check_netio_data	netio_precent	tuple(level,message)	根据策略匹配
check_user_data	user	tuple(level,message)	根据策略匹配
check_port_data	port	tuple(level,message)	根据策略匹配

Configure类
类名：Configure
属性：无
描述：读取配置文件类
方法：
方法名	形参	返回值类型	功能描述
read_config	conf_name(string,配置文件名)
section(string)
option(string)	
int,string	
读取指定配置文件的指定内容
write_config	config_name(string,配置文件名)
section(string)
option(string)	
无	
写入测试文件





