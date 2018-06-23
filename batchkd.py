#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

#批量通过Excel导入快递订单

import xlrd
from pprint import pprint
import pymysql


file = '1.xlsx'

def open_excel(file='1'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(e)
    
def excel_by_index(file = "1.xlsx", colindex = 0, by_index = 0):
    data = open_excel(file)
    tab = data.sheets()[by_index]
    nrows = tab.nrows
    ncols = tab.ncols
    colName = tab.row_values(colindex)
    list = []
    for x in range(0, nrows):
        row = tab.row_values(x)
        if row:
            app = {}
            for y in range(0, ncols):
                app[colName[y]] = row[y]
            list.append(app)
    return list

#直接读取Excel表中的各个值
def read_excel(file = '1.xlsx', by_index = 0):
    data = open_excel(file)
    tab = data.sheets()[by_index]
    nrows = tab.nrows
    ncols = tab.ncols
    for x in range(0, nrows):
        for y in range(0, ncols):
            value = tab.cell(x, y).value
            print(value)
    

     


#每次批处理需要计算的数量
size = 5000
#测试
temp_test = "insert into temp values(%s,%s)";
#对账信息表
fms_account_sql_insert = 'INSERT INTO t_fin_fms_account (ORDER_CODE, COST_PRICE, TOTAL_PRICE, ACCOUNT_USER, REMARK) VALUES (%s,%s,%s,%s,%s)'
#快递订单表
fms_order_info_insert = 'INSERT INTO fms_order_info (ORDER_CODE, BUSINESS_ID, ORDER_TYPE, FMS_COMPANY, FMS_TYPE, SEND_ADDRESS, DELIVERY_ADDRESS, TOTAL_PRICE, COST_PRICE, PRICE_RATO, ORDER_STATUS) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'


def batch_import_excel(file = '1.xlsx', by_index = 0, insert_sql = temp_test):
    data = open_excel(file)
    tab = data.sheets()[by_index]
    nrows = tab.nrows
    ncols = tab.ncols
    print('当前[%s]Excel中当前存在 %d 行, %d 列.' %(file, nrows, ncols))
    num = nrows / size
    num_y = nrows % size
    print('按照 %d 进行划分组装,可以有 %d个整批, 余下 %d个.' %(size, num, num_y))
   
    curr = 0
    for c in range(int(num)):
        list = []
        crows = c * size
        curr = curr + crows + size
        for y in range(crows, crows + size):
            every = []
            for x in range(0, ncols):
                every.append(tab.cell(y, x).value)
            list.append(tuple(every))
        print("当前第 %d 次批处理对应的请求参数组装对象 %s."%(c, list))
        mysql_batch_insert_kx(insert_sql, list)
        mysql_batch_insert_fin(insert_sql, list)
        print("当前第 %d 次批处理MySql插入结束." %(c))
    
    print("最后处理剩余的数量,当前已到 %d 条, 剩余 %d 条." %( curr, num_y))
    last = []
    for y in range(int(curr), int(num_y)):
        every = []
        for x in range(0, ncols):
            every.append(tab.cell(y, x).value)
        last.append(tuple(every))
    print("最后一次批处理对应的请求参数组装对象 %s."%(last))
    mysql_batch_insert_kx(insert_sql, last)
    mysql_batch_insert_fin(insert_sql, last)
    print("最后一次批处理MySql插入结束.")


# 财务库批量插入
def mysql_batch_insert_fin(sql, values):
    conn = pymysql.connect( host = 'rm-2zelk5rjf0qm1b40bo.mysql.rds.aliyuncs.com',  user = 'mecv', password = 'mecvDB99', use_unicode=True, charset="utf8" )
    cur = conn.cursor()
    conn.select_db('mecv_fin')
    cur.execute('SET NAMES utf8;') 
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')    
    try:  
        cur.executemany(sql, values)  
        conn.commit()  
    except Exception as err:  
        print(err)  
    finally:  
        cur.close()  
        conn.close() 
        
# 快线库批量插入        
def mysql_batch_insert_kx(sql, values):
    conn = pymysql.connect( host = 'rdsi354lc7pt48kzsry2o.mysql.rds.aliyuncs.com',  user = 'mecv', password = 's_eQmdYe93R4', use_unicode=True, charset="utf8" )
    cur = conn.cursor()
    conn.select_db('mecv')
    cur.execute('SET NAMES utf8;') 
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')    
    try:  
        cur.executemany(sql, values)  
        conn.commit()  
    except Exception as err:  
        print(err)  
    finally:  
        cur.close()  
        conn.close()         
        


def main():
    # t_fin_fms_account
    # batch_import_excel('1.xlsx', 1, fms_account_sql_insert)
    # fms_order_info
    batch_import_excel('1.xlsx', 2, fms_order_info_insert)

if __name__ == '__main__':
    main()