# -*- coding: utf-8 -*-
'''
Словарь устанвленных ордеров
Последовательность купли/продажи

структура ордера order ={'id':id,'amount':amount,'price':price,'time':ord_time, 'type': r_act, 'x':reserver_sum}
структура словаря order_list  = {id: order}
'''


class ActiveOrders():
    active_orders_list = {}  # активные ордера

    def addOrder(self,key,value):
        ActiveOrders.active_orders_list.update({key:value})


    def removeOrder(self,key):
        return ActiveOrders.active_orders_list.pop(key,{})  #удаляем ордер из списка активных