# -*- coding: utf-8 -*-
import api.data as cexdata
import db.connection as dbconn
import parameters.comission_db as prmt

'''Параметры и комиссии, которые вытаскиваются из базы'''


if __name__ == '__main__':

    conn = dbconn.getConnect()

    #Параметры
    p_alfa = prmt.alfa_curr(conn, 'USD', 'RUB')
    p_mt = prmt.maker_taker(conn, 5)
    p_dep = prmt.deposit_fee(conn, 'USD', 'VISA')
    p_dep_r = prmt.deposit_fee(conn, 'RUB', 'VISA')

    usd_b = p_alfa[0]  # Покупка
    usd_s = p_alfa[1]  # Продажа
    mk = p_mt[0]

    # Комиссия на депозит
    u_dep_prc = p_dep[0]  # USD INPUT ON DEPOSIT PERCENT
    u_dep_fix = p_dep[1]  # USD INPUT ON DEPOSIT FIX
    u_wthrw_prc = p_dep[2]  # USD OUT  DEPOSIT
    u_wthrw_fix = p_dep[3]  # USD OUT  DEPOSIT

    r_dep_prc = p_dep_r[0]  # RUB INPUT ON DEPOSIT PERCENT
    r_dep_fix = p_dep_r[1]  # RUB INPUT ON DEPOSIT FIX

    dbconn.closeConnect(conn)

    price_btcusd = float(cexdata.lastprice('BTC', 'USD')['lprice'])
    price_btcrub = float(cexdata.lastprice('BTC', 'RUB')['lprice'])
