# -*- coding: utf-8 -*-



#Проверка ордера на заданном интервале
def checkOrder(connect,startPeriod,endPeriod,order_list):



    #На вход подается список ордеров в ожидании order_list
    # структура словаря order_list = {id: order}
    # структура ордера order = {'id': id, 'amount': amount, 'price': price, 'time': ord_time, 'type': r_act}

    #В результате получаем list словарей {'order_id':x,'tik_id':tik_id}
    # order_id - id ордера в списке
    # tik_id - id транзакции, на которой должен был сработать ордер

    orders_done = []
    curr = connect.cursor()
    sql   = 'SELECT tid,unixdate,date,price \n' \
              'FROM cex_history_tik \n' \
              'WHERE tid = \n( ' \
              'SELECT  min(tid) /*самый 1-й id который удовлетворяет условию */ \n' \
              'FROM cex_history_tik \n' \
              'WHERE date > \'{startPeriod}\' AND date <= \'{endPeriod}\'\n' \
              '    and price {select_condition} {order_price}  \n' \
              '    and type = \'{type}\' \n' \
              ')';

    for x in order_list:
        order_price = order_list[x]['price']
        type =  order_list[x]['type']

        #startPeriod = order_list[x]['time']  #Время установки ордера берем из словаря

        select_condition = ''

        if (type == 'sell'):
            select_condition = '>='   # при продаже отбирается все price, которые больше ожидаемой в ордере, т.е. чтобы стработал ордер на продажу'
        if (type == 'buy'):
            select_condition = '<='   # при покупке отбирается все price, которые меньше ожидаемого в ордере, т.е. чтобы стработал ордер на покупку'

        sql_x = sql.format(startPeriod=startPeriod,endPeriod=endPeriod,order_price=order_price,type=type,select_condition=select_condition)
        #print(sql_x)
        res = curr.execute(sql_x)
        try:
            tik_id = res.fetchall()[0][0]
            date_id = res.fetchall()[0][1]
            orders_done.append({'order_id':x,'tik_id':tik_id,'date_id':date_id})
        except:
            pass

    curr.close()

    return orders_done





if __name__ == '__main__':

    import db.connection as dbconn
    conn = dbconn.getConnect()

    order_list = {1:{'id': 1, 'amount': 0.03878, 'price': 100, 'time': '123546', 'type': 'buy'}
                  ,2:{'id': 2, 'amount': 0.03878, 'price': 35050, 'time': '123546', 'type': 'sell'}
                  }


    d = checkOrder(conn,  '2019-02-03 09:07:41','2019-02-04 12:14:56',order_list)

    print(d, len(d))
