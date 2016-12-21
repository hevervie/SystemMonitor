#!/usr/env python
# -*- coding: UTF-8 -*-
"""
    Created by zhoupan on 12/11/16.
"""
from SQL.SQLAlchemy import Scputimes
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/test", max_overflow=5)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()
scputimes = Scputimes()
scputimes.add(session, user=1, nice=1, system=1, idle=1, iowait=1, irq=1, softirq=1, steal=1, guest=1, guest_nice=1)
test = 2
