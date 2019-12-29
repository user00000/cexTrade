# -*- coding: utf-8 -*-



import algorithms.alg1.algParams as prmt

def calc():

    #Добавление параметров

    #Проверка баланса

    #return {'action': 'sell', 'X': 'BTC','amount': 1000, 'price': 10000}
    #return {'action': 'reset','id':id_for_reset}
    #return {'action': 'N'}

    # x сколько необходимо на резерве
    return {'type': 'buy', 'crypt':'BTC', 'amount': 0.001, 'price': 10000, 'x': 100 }

def calc_reset():
    #если сбросить флат, то возможно нужно на след шаге сделать продащу
    #этот флаг поместить в класс значимых флагов

    #test
    import time
    from algorithms.alg1.orders import  ActiveOrders
    actOrd = ActiveOrders()

    #Проверяем все ордера на условие
    #сбросить или нет
    #для теста берем 1-й id

    id_x=-1
    for x in actOrd.active_orders_list:
        #if...
        id_x=x

    x = time.time()
    if(int(x)%2==1):
        return {'type': 'cancel','id':id_x}
    else:
        return {'type':'wait'}


if __name__ == '__main__':
    calc_reset()