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


class Svmem(Base):
    __tablename__ = 'svmem'
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


class Sswap(Base):
    __tablename__ = 'sswap'
    id = Column(Integer, primary_key=True, autoincrement=True)
    total = Column(BIGINT, nullable=False)
    used = Column(BIGINT, nullable=False)
    free = Column(BIGINT, nullable=False)
    percent = Column(DECIMAL(16, 2), nullable=False)
    sin = Column(Integer, nullable=False)
    sout = Column(Integer, nullable=False)


class Sdiskio(Base):
    __tablename__ = 'sdiskio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    device = Column(VARCHAR(20), nullable=False)
    read_count = Column(BIGINT, nullable=False)
    write_count = Column(BIGINT, nullable=False)
    read_bytes = Column(BIGINT, nullable=False)
    write_bytes = Column(BIGINT, nullable=False)
    read_time = Column(BIGINT, nullable=False)
    write_time = Column(BIGINT, nullable=False)
    read_merged_count = Column(BIGINT, nullable=False)
    write_merged_count = Column(BIGINT, nullable=False)
    busy_time = Column(BIGINT, nullable=False)


class Sdiskusage(Base):
    __tablename__ = 'sdiskusage'
    id = Column(Integer, primary_key=True, autoincrement=True)
    point = Column(VARCHAR(20), nullable=False)
    total = Column(BIGINT, nullable=False)
    used = Column(BIGINT, nullable=False)
    free = Column(BIGINT, nullable=False)
    percent = Column(DECIMAL(16, 2), nullable=False)


class Snetio(Base):
    __tablename__ = 'snetio'
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


class Suser(Base):
    __tablename__ = 'suser'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Integer, nullable=False)
    name = Column(VARCHAR(20), nullable=False)
    terminal = Column(VARCHAR(20), nullable=False)
    host = Column(CHAR(15), nullable=False)
    started = Column(DECIMAL(16, 2), nullable=False)


class Sport(Base):
    __tablename__ = 'sport'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Integer, nullable=False)
    port = Column(Integer, nullable=False)


class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, autoincrement=True)
    host = Column(CHAR(15), unique=True, nullable=False)


class Receive(Base):
    __tablename__ = 'receive'
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DATETIME, nullable=False)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    cpu_id = Column(Integer, ForeignKey('scputimes.id'), nullable=False)
    svmem_id = Column(Integer, ForeignKey('svmem.id'), nullable=False)
    sswap_id = Column(Integer, ForeignKey('sswap.id'), nullable=False)
    diskio_id = Column(Integer, ForeignKey('sdiskio.id'), nullable=False)
    diskusage_id = Column(Integer, ForeignKey('sdiskusage.id'), nullable=False)
    netio = Column(Integer, nullable=False)
    user = Column(Integer, nullable=False)
    port = Column(Integer, nullable=False)


class Alarm(Base):
    __tablename__ = 'alarm'
    id = Column(Integer, primary_key=True, autoincrement=True)
    receive = Column(Integer, ForeignKey('receive.id'), nullable=False)
    client = Column(Integer, ForeignKey('client.id'), nullable=False)
    cpu = Column(DECIMAL(16, 2), nullable=False)
    svmem = Column(DECIMAL(16, 2), nullable=False)
    swap = Column(DECIMAL(16, 2), nullable=False)
    diskio = Column(DECIMAL(16, 2), nullable=False)
    diskusage = Column(DECIMAL(16, 2), nullable=False)
    snetio = Column(DECIMAL(16, 2), nullable=False)
    level = Column(Integer, nullable=False)
    message = Column(VARCHAR(200), nullable=False)


class Strategy(Base):
    __tablename__ = 'strategy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(VARCHAR(20), nullable=False)
    argv = Column(Integer, nullable=False)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)


class Port(Base):
    __tablename__ = 'port'
    id = Column(Integer, primary_key=True, autoincrement=True)
    port = Column(Integer, nullable=False)


# 定义初始化数据库函数
def init_db():
    Base.metadata.create_all(engine)


# 顶固删除数据库函数
def drop_db():
    Base.metadata.drop_all(engine)


#drop_db()
init_db()

# 创建mysql操作对象
Session = sessionmaker(bind=engine)
session = Session()
