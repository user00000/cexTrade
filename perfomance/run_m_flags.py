# -*- coding: utf-8 -*-

'''Все функции и расчеты !ВЫНОСИТЬ в другой модуль
Здесь идет основной расчет(эмуляция)
Может быть одновременно только один флаг
'''

import time
from datetime import datetime
from datetime import timedelta

from perfomance.data.dataTic import *
from perfomance.TikQueue import TikQueue

from function.calcflag import calcOrder

from algorithms.alg1 import calculation
from algorithms.alg1.logAction import mark_active_orders

from api.cexio import Api

# Константы

DELTA_T = 10  # Запрос каждые десять секунд
START_DATE = '2019-02-03 11:05:17'  # Стартовое время

# Класс с доступом к API
import perfomance.keys as k
api = Api(k.username, k.api_key, k.api_secret)

import db.connection as dbconn

conn = dbconn.getConnect()

n = 0  # Начало итераций. Для тестирования
startCalcPeriodTime = datetime.strptime(START_DATE, '%Y-%m-%d %H:%M:%S')  # Для тестирования
clear_history(conn, 'cex_history_tik')  # Предварительная очистка таблицы. Для тестирования.

tikObj = TikQueue(5)  # Массив размером 5
prev_tik = 0
f_orderIsSet = 0  # флаг (установлен ли ордер)
time_order_place = 0  # время установки флага
tcalc1 = 0  # время до рассчета
tcalc2 = 0  # время после рассчета

while 1 == 1:
    n = n + 1
    if (n > 60): break  # Завершение цикла при тестировании

    # time.sleep(DELTA_T)   #Задержка по времени (реализовать в реальном времни) DELTA_T можно менять в зависимости от времени расчета
    startCalcPeriodTime = startCalcPeriodTime + timedelta(
        seconds=DELTA_T)  # В тесте время запроса рассчитывается  !!!! Возможно надо перенести в конец цикла
    # DELTA_T должно быть больше dT1 и dT2, тогда переносить не надо. Но период для проверки флага надо изменить

    # Получение последних 1000 tik на данный момент
    # Данные должны получаться через api
    r = f_data_tic_imitation(conn, startCalcPeriodTime)  # Эмулированный результат

    tcalc1 = datetime.time()  # Время начала рассчетов.  Текущее время. Время,когда начался процесс рассчета

    curr_tik = r[0]['tid']  # максимальный tik_id из полученного запроса

    if (
            curr_tik != prev_tik):  # Только если за промежуток были новые данные. Могут и не быть(если ничего не происходит)

        new_data = [x for x in r if x['tid'] > prev_tik]  # Новые данные из полученных 1000 значений
        tikObj.add_tail(new_data)
        # От tikObj можно отказаться, сохранив новый результат в таблицу  save_tik(conn,new_data)
        # и делать рассчет на основе данных из таблицы
        # save_tik(conn,new_data) Сохраняем, чтобы можно было проверить сработал ли флаг не  через API

        # =====Алгоритм===========
        '''Алгоритм расчитывать только одну позицию
          если делать несколько позиций, то f_orderIsSet надо увеличивать на 1 либо уменьшать на 1 при закрытии
          если выход их всех ордеров то выставлять 0'''

        # Расчет. Анализ данных. Вывод действия: брать/продать/оставить
        res = calculation.calc()  # тогда делаем расчет по полученным данным. Добавить входные переменные.
        isDone = res['flag']  # сработал ли флаг, результат на полученных данных


        if (f_orderIsSet == 0):  # ордер не установлен


            tcalc2 = datetime.time() # время окончания расчетов
            #tcalc2 перевести во время данных
            dCalctime = tcalc2 - tcalc1  # Время работы  расчета

            if dCalctime > timedelta(seconds=DELTA_T):  # расчет был слишком долгий
                print('Too long calc at tik=' + curr_tik + ' startCalcPeriodTime=' + startCalcPeriodTime)
                continue


            # !!!Реализовать  команда на покупку или продажу

            r_act = res['action']  # результат. какое действие делать

            if(r_act==res['stop']):  #остановка
                exit()

            if (r_act == 'buy' or r_act == 'sell'):
                amount = res['amount']  # количество
                price = res['price']    # по какой цене
                market = 'BTC/USD'
                # api set order   # установка ордера через API
                # PRIVATE API place_order = api.buy_limit_order(amount,price,market)  # На выходе получается словарь с данными ордера
                #Попытка

                #Для тестирования генерация id
                id = int(time.time())
                ord_time = int(startCalcPeriodTime.timestamp()) + (datetime.time() - tcalc1)  #Время (по тестовым данным) установки
                #если несколько ордеров, то надо делать словарь (id-время)
                time_order_place = ord_time
                #реализовать Проверка в балансе
                place_order = {'id':id,'amount':amount,'price':price,'time':ord_time, 'type': r_act}

                mark_active_orders(place_order , action='place')  #action передается отдельно, т.к. API не возврвщает тип в случае сброса ордддера
                f_orderIsSet = 1   # f_orderIsSet = f_orderIsSet + 1

                continue


            if (r_act == 'cancel'):

                id = res['id']
                ord_time = int(startCalcPeriodTime.timestamp()) + ( datetime.time() - tcalc1)  # Время (по тестовым данным) установки
                order_reset = {'id': id,'time':ord_time}
                # API return true/false
                #Если false => сработал либо связь
                #Если сработал => Проверка баланса через API
                #Далее обработка баланса и переъход на след шаг

                #Если true, то обработка баланса(возврат к предыдущему)

                #В тесте необходимо проверить вручную на промежутке (time_order_place;tcalc2) либо (startCalcPeriodTime,tcalc2)



                mark_active_orders(order_reset, action='cancel')  # добавить order_buy в словарь id ордера
                f_orderIsSet = 0  #f_orderIsSet = f_orderIsSet - 1

                continue

            if (r_act == 'cancelALL'):
                # res_api = ...
                # list_orders = reas_api['data']

                f_orderIsSet = 0


        else:  # ордер установлен, тогда проверка сработал ли он

            # Доп проверка
            # например calculation2
            # либо в calculation(параметр calc2=true)

            # Проверка только на следующем шаге, посе устанолвки флага, т.к. иначе данные еще не были получены
            r_ord = checkOrder(time_order_place,startCalcPeriodTime) # Проверка флага на промежутке
            # time_order_place < startCalcPeriodTime, т.к. time_order_place - время из предыдущего периода(шага), startCalcPeriodTime - начала текущего шага

            #Проверку перенести в алгоритм -> тогда точно будет на след шаге
            #Тогда в алгоритм будет передаваться флаг
            #Тогда в это условие приходим, если в алгоритме проверка не сработала на промежутке (time_order_place,startCalcPeriodTime)
            #и res['action'] = None т.е. ожидание => time_order_place = startCalcPeriodTime  # т.к. на прошлом промежутке ничего не произошло, то его не надо повторно проверять
            #Тогда проверку





        if (r_ord == 1):  # Сработал

            #Проверка всех ордеров по циклу
            #if p_current in massiv < or > p in order

            #get balace with API  and refresh
            # Test calc balance

            f_orderIsSet = 0
        if(r_ord == 0): # Не сработал
            time_order_place = startCalcPeriodTime # т.к. на прошлом промежутке ничего не произошло, то его не надо повторно проверять







        # За время рассчетов мог сработать ордер

        # Проверять, если был установлен флаг
        tcalc2 = datetime.time()
        dCalctime = tcalc2 - tcalc1  # Время работы  !!! ПРОВЕРИТЬ МОЖНО ЛИ ТАК ВЫЧИТАТЬ ВРЕМЯ

        if dCalctime > timedelta(seconds=DELTA_T):  # расчет был слишком долгий
            print('Too long calc at tik=' + curr_tik + ' startCalcPeriodTime=' + startCalcPeriodTime)
            continue

        # tF=0 - флаг не установлен
        order_complited = calcOrder.check_flag_imulation(conn, tF,
                                                         startCalcPeriodTime + dCalctime)  # от флага до конца рассчета, предыдущий флаг смог сработать
        # order_complited = flag.check_flag в реальности, просто проверить флаг или изменение баланса

        if (order_complited == 1):  # Ордер сработал
            # tF можно приравнять к startCalcPeriodTime, т.к на промежутке [tF;startCalcPeriodTime] ничего не произошло,
            # чтобы в след раз меньше проверять данных

            # Если ордер сработал, то надо расчитать баланс !!!!!!!!!!!
            tf = startCalcPeriodTime
            continue  # переход на след шаг. т.е. рассчет делается на след данных
        else:
            tF = startCalcPeriodTime


            # tF можно приравнять к startCalcPeriodTime, т.к на промежутке tF;startCalcPeriodTime ничего не произошло,
            # чтобы в след раз меньше проверять данных
            pass

        save_tik(conn, new_data)  # Сохранение новых данных в базе таблица истории данных cex_history_tik  dT2>0

        print(tikObj.get_type())

    prev_tik = curr_tik

dbconn.closeConnect(conn)