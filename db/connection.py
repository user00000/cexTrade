# -*- coding: utf-8 -*-

import sqlite3
import config



'''
connect_global = None
def createConnect():
    db_path = config.getPathDB()
    conn = sqlite3.connect(db_path)
    connect_global = conn
    return connect_global

def getConnect():
    if (connect_global == None):
        return createConnect()
    else:
        return connect_global

'''

def getConnect():
    db_path = config.getPathDB()
    conn = sqlite3.connect(db_path)
    return conn


def closeConnect(connect):
    connect.close()





if __name__ == '__main__':
    ins_query = 'INSERT INTO transaction_log ( id,order_time,real_time) ' \
                'VALUES(3,123,1234);'


    con1 = getConnect()
    print(con1)
    cursor = con1.cursor()
    r = cursor.execute('SELECT max(ID) ID FROM transaction_log')
    r1 = r.fetchall()
    r2 = r1[0][0]
    print(r2)
    #con1.commit()


    con2 = getConnect()
    print(con2)
    ins_query2 = 'INSERT INTO transaction_log ( ID,order_time,real_time) ' \
                 'VALUES('+str(r2+1)+',123,1234);'
    cursor = con2.cursor()
    cursor.execute(ins_query2)
    #con2.commit()

    con3 = getConnect()
    print(con3)
    ins_query3 = 'INSERT INTO transaction_log ( ID,order_time,real_time) ' \
                 'VALUES(' + str(r2 + 2) + ',123,1234);'
    cursor = con3.cursor()
    cursor.execute(ins_query3)
    con3.commit()

    #con1.close()
    #con2.close()