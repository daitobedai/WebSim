# coding: utf-8
import sys
import json
import numpy
from datetime import datetime
import time

class DataContext():
    def __init__(self, data):
        self.close = [i['close'] for i in data]
        self.high = [i['high'] for i in data]
        self.low = [i['low'] for i in data]


def max_list(l, n):
    if n > len(l):
        n = len(l)
    return max(l[0:n])


def min_list(l, n):
    if n > len(l):
        n = len(l)
    return min(l[0:n])


def average(l, n):
    if n > len(l):
        n = len(l)
    return sum(l[0:n])/n


def std_dev(l, n):
    if n > len(l):
        n = len(l)
    avg = sum(l[0:n])/n
    return sum([(i-avg)**0.5 for i in l[0:n]])


def parsing_expr(data, exp):
    context = DataContext(data)

    exp = exp.replace('max', 'max_list')
    exp = exp.replace('min', 'max_list')
    exp = exp.replace('avg', 'average')
    exp = exp.replace('stdDev', 'std_dev')
    # print exp
    res_list = []
    len_data = len(data)
    for date_number in range(1, len_data+1):
        close = context.close[0:date_number]
        high = context.high[0:date_number]
        low = context.low[0:date_number]
        close.reverse()
        high.reverse()
        low.reverse()
        res = eval(exp)
        if type(res) is bool:
            res = 1 if res else 0
        res_list.append(res)
    return res_list


def parsing_program(data, program):
    context = DataContext(data)
    res = []
    exec(program)
    return res


def neutralization(l):
    abs_list = [abs(i) for i in l]
    max_abs = max(abs_list)
    return [i/max_abs for i in l]


if __name__ == '__main__':
    sim_type = 1
    exp = "max(close, 5) > max(close, 3)"
    program = "def f(context):\n" \
        "   res_list = []\n"  \
        "   for i in context.close:\n" \
        "       if i > 13:\n" \
        "           res_list.append(1)\n"\
        "       else:\n"\
        "           res_list.append(0)\n"\
        "   return res_list\n"\
        "res = f(context)\n"
    data = []
    with open('data/table.csv', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line_array = line.split(',')
            line_dict = {
                'date': line_array[0],
                'open': float(line_array[1]),
                'high': float(line_array[2]),
                'low': float(line_array[3]),
                'close': float(line_array[4])
            }
            data.append(line_dict)
            if len(data) > 100:
                break
    data.reverse()
    #  00000000
    # 11111111
    if sim_type:
        res = parsing_expr(data, exp)
    else:
        res = parsing_program(data, program)
    res = neutralization(res)

    # from the second day to start
    back_test_data = data[1:]
    stratage_res = res[0:-1:1]
    # final result
    curve_data = []

    # initial status
    last_close = data[0]['close']
    last_position = 0.0
    # 盈亏
    sell_money = 0.0
    # 持有
    hold = 0.0
    # 总资金，交易过程中维持不变
    total_money = 100000.0
    for i in zip(back_test_data, stratage_res):
        today_close = i[0]['close']
        money_position = i[1]
        # sell
        sell_money += hold * (today_close-last_close)
        # buy
        hold = total_money * money_position / today_close
        # total assets
        total_assets = total_money + sell_money
        timestamp = time.mktime(
            datetime.strptime(i[0]['date'], '%Y/%m/%d').timetuple())*1000
        curve_data.append([int(timestamp), total_assets])
    print curve_data
    # return curve_data
