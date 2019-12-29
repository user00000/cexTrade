# -*- coding: utf-8 -*-
'''
Элемент Tik  Содержит набор тиков, соответствующий заданной емкости
'''
class TikQueue:

    def __init__(self,capasity):

        #Емкость должна быть переменной, чтобы входные данные не переполняли массив
        #Входные данные должны составлять процент от емкости
        self.capasity = capasity

        self.tikQ = []

        self.l_tid=[]
        self.l_type=[]
        self.l_unixdate=[]
        self.l_amount=[]
        self.l_price=[]


    #набор tik-ов в аргументе подается по уменьшению слева на право
    def add_tail(self,tik):
        len_Que = len(self.tikQ)
        len_tik = len(tik)

        if len_tik >= self.capasity:                #Входящий набор больше емкости
            self.tikQ = tik[:self.capasity]        #заменяем все содержимое на последние(по времени/id) элементи из входных данных
            self.tikQ = self.tikQ[::-1]           #разворот массива

        if len_tik < self.capasity:
            k = self.capasity - len_tik      #Количество элементов, которые необходимо оставить
            self.tikQ = self.tikQ[-k:]
            self.tikQ.extend(tik[::-1])  # Добавление новых элементов





    def remove_leading(self,k):
        self.tikQ = self.tikQ[k:]


    def get_tid(self,type='all'):
        if type == 'sell' or type == 's':
            return [x['tid'] for x in self.tikQ if x['type'] == 'sell']
        if type == 'buy' or type == 'b':
            return [x[0] for x in self.tikQ if x['type'] == 'buy']
        return [x['tid'] for x in self.tikQ]


    def get_type(self,type='all'):
        if type == 'sell' or type == 's':
            return [x['type'] for x in self.tikQ if x['type'] == 'sell']
        if type == 'buy' or type == 'b':
            return [x['type'] for x in self.tikQ if x['type'] == 'buy']
        return [x['type'] for x in self.tikQ]

    def get_unixdate(self,type='all'):
        if type == 'sell' or type == 's':
            return [x['date'] for x in self.tikQ if x['type'] == 'sell']
        if type == 'buy' or type == 'b':
            return [x['date'] for x in self.tikQ if x['type'] == 'buy']
        return [x['date'] for x in self.tikQ]

    def get_amount(self,type='all'):
        if type == 'sell' or type == 's':
            return [x['amount'] for x in self.tikQ if x['type'] == 'sell']
        if type == 'buy' or type == 'b':
            return [x['amount'] for x in self.tikQ if x['type'] == 'buy']
        return [x['amount'] for x in self.tikQ]

    def get_price(self,type='all'):
        if type == 'sell' or type == 's':
            return [x['price'] for x in self.tikQ if x['type'] == 'sell']
        if type == 'buy' or type == 'b':
            return [x['price'] for x in self.tikQ if x['type'] == 'buy']
        return [x['price'] for x in self.tikQ]




