#!/usr/bin/env python
#-*- coding:utf-8 -*-

#(index)

#全局数据memcached的地址
"""
user_dbconfig_mc_addr = ["127.0.0.1:11211"]
lock_mc_addr = ["127.0.0.1:11211"]
mc_list = ['127.0.0.1:11211']
mb_list = ['127.0.0.1:11211']
"""
user_dbconfig_mc_addr = ["192.168.0.106:11211"]
lock_mc_addr = ["192.168.0.106:11211"]

# 游戏数据, 直接用memcache.Client(mc_list), 让他自己做hash，方便以后rebalance
mc_list = ['192.168.0.106:11211']
mb_list = ['192.168.0.106:11211']

#平台的memcache地址
session_mc = ["192.168.0.106:11211",]

# 存储session用的
session_mc = ['192.168.0.106:11211']

# 公用mc，存储游戏数据，但是是全局的，比如拍卖列表，交易列表
public_mc = ["192.168.0.106:11211",]

