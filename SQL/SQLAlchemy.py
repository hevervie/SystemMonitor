#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 12/10/16.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index, DECIMAL, BIGINT, VARCHAR, CHAR, \
    DATETIME
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/test", max_overflow=5)

Base = declarative_base()


class Scputimes(Base):
    __tablename__ = 'scputimes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(DECIMAL(16, 2))
    nice = Column(DECIMAL(16, 2))
    system = Column(DECIMAL(16, 2))
    idle = Column(DECIMAL(16, 2))
    iowait = Column(DECIMAL(16, 2))
    irq = Column(DECIMAL(16, 2))
    softirq = Column(DECIMAL(16, 2))
    steal = Column(DECIMAL(16, 2))
    guest = Column(DECIMAL(16, 2))
    guest_nice = Column(DECIMAL(16, 2))


class Svmem(Base):
    __tablename__ = 'svmem'
    id = Column(Integer, primary_key=True, autoincrement=True)
    total = Column(BIGINT)
    available = Column(BIGINT)
    percent = Column(DECIMAL(16, 2))
    used = Column(BIGINT)
    free = Column(BIGINT)
    active = Column(BIGINT)
    inactive = Column(BIGINT)
    buffers = Column(BIGINT)
    cached = Column(BIGINT)
    shared = Column(BIGINT)


class Sswap(Base):
    __tablename__ = 'sswap'
    id = Column(Integer, primary_key=True, autoincrement=True)
    total = Column(BIGINT)
    used = Column(BIGINT)
    free = Column(BIGINT)
    percent = Column(DECIMAL(16, 2))
    sin = Column(Integer)
    sout = Column(Integer)


class Sdiskio(Base):
    __tablename__ = 'sdiskio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    device = Column(VARCHAR(20))
    read_count = Column(BIGINT)
    write_count = Column(BIGINT)
    read_bytes = Column(BIGINT)
    write_bytes = Column(BIGINT)
    read_time = Column(BIGINT)
    write_time = Column(BIGINT)
    read_merged_count = Column(BIGINT)
    write_merged_count = Column(BIGINT)
    busy_time = Column(BIGINT)


class Sdiskusage(Base):
    __tablename__ = 'sdiskusage'
    id = Column(Integer, primary_key=True, autoincrement=True)
    point = Column(VARCHAR(20))
    total = Column(BIGINT)
    used = Column(BIGINT)
    free = Column(BIGINT)
    percent = Column(DECIMAL(16, 2))


class Snetio(Base):
    __tablename__ = 'snetio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    device = Column(VARCHAR(20))
    type = Column(Integer)
    bytes_sent = Column(BIGINT)
    bytes_recv = Column(BIGINT)
    packets_sent = Column(BIGINT)
    packets_recv = Column(BIGINT)
    errin = Column(BIGINT)
    errout = Column(BIGINT)
    dropin = Column(BIGINT)
    dropout = Column(BIGINT)


class Suser(Base):
    __tablename__ = 'suser'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Integer)
    name = Column(VARCHAR(20))
    terminal = Column(VARCHAR(20))
    host = Column(CHAR(15))
    started = Column(DECIMAL(16, 2))


class Sport(Base):
    __tablename__ = 'sport'
    id = Column(Integer)
    type = Column(Integer)
    port = Column(Integer)


class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, autoincrement=True)
    host = Column(CHAR(15), unique=True)


class Receive(Base):
    __tablename__ = 'receive'
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DATETIME)
    client = Column(Integer, ForeignKey('client.id'))
    cpu = Column(Integer, ForeignKey('scputimes.id'))
    svmem = Column(Integer, ForeignKey('svmem.id'))
    sswap = Column(Integer, ForeignKey('sswap.id'))
    diskio = Column(Integer, ForeignKey('diskio.id'))
    diskusage = Column(Integer, ForeignKey('diskusage'))
    netio = Column(Integer)
    user = Column(Integer)
    port = Column(Integer)

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
  level     INT,
  message   VARCHAR(200)
);

class Alarm(Base):
    __tablename__ = 'alarm'
    id = Column(Integer, primary_key=True, autoincrement=True)
    receive = Column(Integer, )



# 一对多
class Favor(Base):
    __tablename__ = 'favor'
    nid = Column(Integer, primary_key=True)
    caption = Column(String(50), default='red', unique=True)


# 多对多
class ServerToGroup(Base):
    __tablename__ = 'servertogroup'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(Integer, ForeignKey('server.id'))
    group_id = Column(Integer, ForeignKey('group.id'))


# 定义初始化数据库函数
def init_db():
    Base.metadata.create_all(engine)


# 顶固删除数据库函数
def drop_db():
    Base.metadata.drop_all(engine)


# drop_db()
init_db()

# 创建mysql操作对象
Session = sessionmaker(bind=engine)
session = Session()
