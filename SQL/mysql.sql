/*=====================================================*/
/*       Create by zhoupan                             */
/*       Create time: 2016.08.01                       */
/*       Version:  mysql 5.0 and above                 */
/*=====================================================*/
DROP DATABASE IF EXISTS SysMon;
CREATE DATABASE SysMon;
USE SysMon;
DROP TABLE IF EXISTS scputimes;   /*cpu信息表*/
DROP TABLE IF EXISTS svmem;       /*物理内存信息*/
DROP TABLE IF EXISTS sswap;       /*交换分区信息*/
DROP TABLE IF EXISTS sdiskio;     /*磁盘IO信息*/
DROP TABLE IF EXISTS sdiskusage;  /*磁盘使用率信息*/
DROP TABLE IF EXISTS snetio;      /*网络IO信息*/
DROP TABLE IF EXISTS suser;       /*在线用户信息*/
DROP TABLE IF EXISTS sport;       /*端口信息*/
DROP TABLE IF EXISTS client;     /*客户端信息*/
DROP TABLE IF EXISTS receive;     /*接收的数据*/
DROP TABLE IF EXISTS alarm;       /*警告*/
DROP TABLE IF EXISTS strategy;    /*告警策略*/
DROP TABLE IF EXISTS user;        /*合法用户*/
DROP TABLE IF EXISTS port;        /*合法端口*/


/*=====================================================*/
/*     table:  scputimes           CPU信息             */
/*=====================================================*/

CREATE TABLE scputimes (
  id         INT PRIMARY KEY AUTO_INCREMENT,
  user       DOUBLE,
  nice       DOUBLE,
  system     DOUBLE,
  idle       DOUBLE,
  iowait     DOUBLE,
  irq        DOUBLE,
  softirq    DOUBLE,
  steal      DOUBLE,
  guest      DOUBLE,
  guest_nice DOUBLE
);

/*=====================================================*/
/*     table: svmem            物理内存信息             */
/*=====================================================*/

CREATE TABLE svmem (
  id        INT PRIMARY KEY AUTO_INCREMENT,
  total     LONG,
  available LONG,
  precent   DOUBLE,
  used      LONG,
  free      LONG,
  active    LONG,
  inactive  LONG,
  buffers   LONG,
  cached    LONG,
  shared    LONG
);

/*=====================================================*/
/*     table: swap            虚拟内存信息             */
/*=====================================================*/

CREATE TABLE sswap (
  id      INT PRIMARY KEY AUTO_INCREMENT,
  total   LONG,
  used    LONG,
  free    LONG,
  precent DOUBLE,
  sin     INT,
  sout    INT
);

/*=====================================================*/
/*     table: sdiskio            磁盘IO                */
/*=====================================================*/

CREATE TABLE sdiskio (
  id                 INT PRIMARY KEY AUTO_INCREMENT,
  device             VARCHAR(20),                       #预留
  read_count         LONG,
  write_count        LONG,
  read_bytes         LONG,
  write_bytes        LONG,
  read_time          LONG,
  write_time         LONG,
  read_merged_count  LONG,
  write_merged_count LONG,
  busy_time          LONG
);

/*=====================================================*/
/*     table: sdiskusage            磁盘分区使用率      */
/*=====================================================*/

CREATE TABLE sdiskusage (
  id      INT PRIMARY KEY AUTO_INCREMENT,
  point   VARCHAR(20),
  total   LONG,
  used    LONG,
  free    LONG,
  precent DOUBLE
);

/*=====================================================*/
/*     table: snetio            网络IO                 */
/*=====================================================*/

CREATE TABLE snetio (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  device       VARCHAR(20),
  type         INT,
  bytes_sent   LONG,
  bytes_recv   LONG,
  packets_sent LONG,
  packets_recv LONG,
  errin        LONG,
  errout       LONG,
  dropin       LONG,
  dropout      LONG
);

/*=====================================================*/
/*     table: suser            用户信息                */
/*=====================================================*/

CREATE TABLE suser (
  id       INT AUTO_INCREMENT PRIMARY KEY,
  type     INT,                               /*用户类型，用于在receive表中引入*/
  user     VARCHAR(20),
  terminal VARCHAR(20),
  host     CHAR(15),
  started  DOUBLE
);

/*=====================================================*/
/*     table: sport            端口信息                 */
/*=====================================================*/
CREATE TABLE sport (
  id      INT PRIMARY KEY AUTO_INCREMENT,
  type    INT,                               /*端口类型，用于在receive表中引入*/
  port    INT
);


/*=====================================================*/
/*     table:client             客户端列表              */
/*=====================================================*/

CREATE TABLE client (
  id   INT PRIMARY KEY AUTO_INCREMENT,
  host CHAR(15) UNICODE
);



/*=====================================================*/
/*     table: receive            接收到的信息           */
/*=====================================================*/

CREATE TABLE receive (
  id           INT PRIMARY KEY AUTO_INCREMENT,
  client_id    INT,
  cpu_id       INT,
  svmem_id     INT,
  swap_id      INT,
  diskio_id    INT,
  diskusage_id INT,
  netio_type    INT,
  user_type     INT,
  port_type      INT
);

ALTER TABLE receive ADD CONSTRAINT client_fk FOREIGN KEY (client_id) REFERENCES client(id);
ALTER TABLE receive ADD CONSTRAINT cpu_fk FOREIGN KEY (cpu_id) REFERENCES scputimes(id);
ALTER TABLE receive ADD CONSTRAINT svmem_fk FOREIGN KEY (svmem_id) REFERENCES svmem(id);
ALTER TABLE receive ADD CONSTRAINT swap_fk FOREIGN KEY (swap_id) REFERENCES sswap(id);
ALTER TABLE receive ADD CONSTRAINT diskio_fk FOREIGN KEY (diskio_id) REFERENCES sdiskio(id);
ALTER TABLE receive ADD CONSTRAINT diskusage_fk FOREIGN KEY (diskusage_id) REFERENCES sdiskusage(id);

# ALTER TABLE receive ADD CONSTRAINT netio_fk FOREIGN KEY (netio_id) REFERENCES snetio(id);
# ALTER TABLE receive ADD CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES suser(type);
# ALTER TABLE receive ADD CONSTRAINT port_fk FOREIGN KEY (port_id) REFERENCES sport(type);

/*=====================================================*/
/*     table: alarm            警告信息                 */
/*=====================================================*/

CREATE TABLE alarm (
  id        INT PRIMARY KEY AUTO_INCREMENT,
  recv_id   INT,
  client_id INT,
  cpu       DOUBLE,
  svmem     DOUBLE,
  swap      DOUBLE,
  diskio    DOUBLE,
  diskusage DOUBLE,
  snetio    DOUBLE,
  suser     VARCHAR(100),
  port      VARCHAR(100),
  level     INT,
  message   VARCHAR(200)
);

ALTER TABLE alarm ADD CONSTRAINT alarm_client_fk FOREIGN KEY (client_id) REFERENCES client(id);
ALTER TABLE alarm ADD CONSTRAINT alarm_recv_id FOREIGN KEY (recv_id) REFERENCES receive(id);

/*=====================================================*/
/*     table: strategy            告警策略             */
/*=====================================================*/

CREATE TABLE strategy (
  id   INT PRIMARY KEY AUTO_INCREMENT,
  type VARCHAR(20),
  argv INT
);

/*=====================================================*/
/*     table: user            合法用户列表              */
/*=====================================================*/

CREATE TABLE user (
  id   INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255)
);

INSERT INTO user(name) VALUES ('root');

/*=====================================================*/
/*     table: port            合法端口列表              */
/*=====================================================*/

CREATE TABLE port (
  id   INT AUTO_INCREMENT PRIMARY KEY,
  port INT
);

