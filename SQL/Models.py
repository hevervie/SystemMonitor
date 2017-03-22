#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 12/21/16.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, BIGINT, VARCHAR, DATETIME
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


# /*=====================================================*/
# /*     table:  scputimes           CPU信息             */
# /*=====================================================*/

class Scputimes(Base):
    __tablename__ = 'informations_scputimes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(DECIMAL(16, 2), nullable=False)
    nice = Column(DECIMAL(16, 2), nullable=False)
    system = Column(DECIMAL(16, 2), nullable=False)
    idle = Column(DECIMAL(16, 2), nullable=False)
    iowait = Column(DECIMAL(16, 2), nullable=False)
    irq = Column(DECIMAL(16, 2), nullable=False)
    softirq = Column(DECIMAL(16, 2), nullable=False)
    steal = Column(DECIMAL(16, 2), nullable=False)
    guest = Column(DECIMAL(16, 2), nullable=False)
    guest_nice = Column(DECIMAL(16, 2), nullable=False)


# /*=====================================================*/
# /*     table: svmem            物理内存信息             */
# /*=====================================================*/

class Svmem(Base):
    __tablename__ = 'informations_svmem'
    id = Column(Integer, primary_key=True, autoincrement=True)
    total = Column(BIGINT, nullable=False)
    available = Column(BIGINT, nullable=False)
    percent = Column(DECIMAL(16, 2), nullable=False)
    used = Column(BIGINT, nullable=False)
    free = Column(BIGINT, nullable=False)
    active = Column(BIGINT, nullable=False)
    inactive = Column(BIGINT, nullable=False)
    buffers = Column(BIGINT, nullable=False)
    cached = Column(BIGINT, nullable=False)
    shared = Column(BIGINT, nullable=False)

    # 增加


# /*=====================================================*/
# /*     table: sswap            虚拟内存信息             */
# /*=====================================================*/

class Sswap(Base):
    __tablename__ = 'informations_sswap'
    id = Column(Integer, primary_key=True, autoincrement=True)
    total = Column(BIGINT, nullable=False)
    used = Column(BIGINT, nullable=False)
    free = Column(BIGINT, nullable=False)
    percent = Column(DECIMAL(16, 2), nullable=False)
    sin = Column(Integer, nullable=False)
    sout = Column(Integer, nullable=False)


# /*=====================================================*/
# /*     table: sdiskio            磁盘IO                 */
# /*=====================================================*/

class Sdiskio(Base):
    __tablename__ = 'informations_sdiskio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    device = Column(VARCHAR(20), nullable=True)
    read_count = Column(BIGINT, nullable=False)
    write_count = Column(BIGINT, nullable=False)
    read_bytes = Column(BIGINT, nullable=False)
    write_bytes = Column(BIGINT, nullable=False)
    read_time = Column(BIGINT, nullable=False)
    write_time = Column(BIGINT, nullable=False)
    read_merged_count = Column(BIGINT, nullable=False)
    write_merged_count = Column(BIGINT, nullable=False)
    busy_time = Column(BIGINT, nullable=False)


# /*=====================================================*/
# /*     table: sdiskusage            磁盘分区使用率      */
# /*=====================================================*/


class Sdiskusage(Base):
    __tablename__ = 'informations_sdiskusage'
    id = Column(Integer, primary_key=True, autoincrement=True)
    point = Column(VARCHAR(20), nullable=False)
    total = Column(BIGINT, nullable=False)
    used = Column(BIGINT, nullable=False)
    free = Column(BIGINT, nullable=False)
    percent = Column(DECIMAL(16, 2), nullable=False)


# /*=====================================================*/
# /*     table: snetio            网络IO                 */
# /*=====================================================*/


class Snetio(Base):
    __tablename__ = 'informations_snetio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    device = Column(VARCHAR(20), nullable=False)
    type = Column(Integer, nullable=False)
    bytes_sent = Column(BIGINT, nullable=False)
    bytes_recv = Column(BIGINT, nullable=False)
    packets_sent = Column(BIGINT, nullable=False)
    packets_recv = Column(BIGINT, nullable=False)
    errin = Column(BIGINT, nullable=False)
    errout = Column(BIGINT, nullable=False)
    dropin = Column(BIGINT, nullable=False)
    dropout = Column(BIGINT, nullable=False)


# /*=====================================================*/
# /*     table: suser            用户信息                */
# /*=====================================================*/

class Suser(Base):
    __tablename__ = 'informations_suser'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Integer, nullable=False)
    name = Column(VARCHAR(20), nullable=False)
    terminal = Column(VARCHAR(20), nullable=False)
    host = Column(VARCHAR(15), nullable=False)
    started = Column(DECIMAL(16, 2), nullable=False)


# /*=====================================================*/
# /*     table: sport            端口信息                 */
# /*=====================================================*/


class Sport(Base):
    __tablename__ = 'informations_sport'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Integer, nullable=False)
    port = Column(Integer, nullable=False)


# /*=====================================================*/
# /*     table:client             客户端列表              */
# /*=====================================================*/


class Client(Base):
    __tablename__ = 'informations_client'
    id = Column(Integer, primary_key=True, autoincrement=True)
    host = Column(VARCHAR(15), unique=True, nullable=False)


# /*=====================================================*/
# /*     table: receive            接收到的信息           */
# /*=====================================================*/


class Receive(Base):
    __tablename__ = 'informations_receive'
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DATETIME, nullable=False)
    client_id = Column(Integer, ForeignKey('informations_client.id'), nullable=False)
    cpu_id = Column(Integer, ForeignKey('informations_scputimes.id'), nullable=False)
    svmem_id = Column(Integer, ForeignKey('informations_svmem.id'), nullable=False)
    sswap_id = Column(Integer, ForeignKey('informations_sswap.id'), nullable=False)
    sdiskio_id = Column(Integer, ForeignKey('informations_sdiskio.id'), nullable=False)
    sdiskusage_id = Column(Integer, ForeignKey('informations_sdiskusage.id'), nullable=False)
    snetio = Column(Integer, nullable=False)
    suser = Column(Integer, nullable=False)
    sport = Column(Integer, nullable=False)


# /*=====================================================*/
# /*     table: alarm            警告信息                 */
# /*=====================================================*/

class Alarm(Base):
    __tablename__ = 'informations_alarm'
    id = Column(Integer, primary_key=True, autoincrement=True)
    receive_id = Column(Integer, ForeignKey('informations_receive.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('informations_client.id'), nullable=False)
    cpu = Column(DECIMAL(16, 2), nullable=False)
    svmem = Column(DECIMAL(16, 2), nullable=False)
    swap = Column(DECIMAL(16, 2), nullable=False)
    diskio = Column(DECIMAL(16, 2), nullable=False)
    diskusage = Column(DECIMAL(16, 2), nullable=False)
    snetio = Column(DECIMAL(16, 2), nullable=False)
    level = Column(Integer, nullable=False)
    message = Column(VARCHAR(200), nullable=False)


# /*=====================================================*/
# /*     table: strategy            告警策略             */
# /*=====================================================*/

class Strategy(Base):
    __tablename__ = 'informations_strategy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(VARCHAR(20), nullable=False)
    argv = Column(Integer, nullable=False)


# /*=====================================================*/
# /*     table: user            合法用户列表              */
# /*=====================================================*/

class User(Base):
    __tablename__ = 'informations_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)


# /*=====================================================*/
# /*     table: port            合法端口列表              */
# /*=====================================================*/

class Port(Base):
    __tablename__ = 'informations_port'
    id = Column(Integer, primary_key=True, autoincrement=True)
    port = Column(Integer, nullable=False)


# /*=====================================================*/
# /*     table: warn            警告保存数据表              */
# /*=====================================================*/
class Warn(Base):
    __tablename__ = 'informations_warn'
    id = Column(Integer, primary_key=True, autoincrement=True)
    alarmid_id = Column(Integer, ForeignKey('informations_alarm.id'), nullable=False)
    datetime = Column(DATETIME, nullable=False)
    status = Column(Integer, default=0, nullable=False)
    type = Column(Integer, nullable=False)


# 定义初始化数据库函数
def init_db(engine):
    Base.metadata.create_all(engine)


# 顶固删除数据库函数
def drop_db(engine):
    Base.metadata.drop_all(engine)


# class Singleton(object):
#     INSTANCE = None
#     lock = threading.RLock()
#
#     def __new__(cls):
#         cls.lock.acquire()
#         if cls.INSTANCE is None:
#
#             cls.INSTANCE =
#         cls.lock.release()
#         return cls.INSTANCE


if __name__ == '__main__':
    engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/test", max_overflow=5)
    # 创建mysql操作对象
    Session = sessionmaker(bind=engine)
    session = Session()
    init_db(engine)
    # user = User(name="zhoupan")
    # session.add(user)
    # session.commit()
