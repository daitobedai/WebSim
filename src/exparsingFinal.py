# coding: utf-8
from sys import argv as sys_argv
from datetime import datetime
import time
import json
import numpy


class DataContext():
    def __init__(self, data):
        self.openprice = [i['open'] for i in data]
        self.close = [i['close'] for i in data]
        self.high = [i['high'] for i in data]
        self.low = [i['low'] for i in data]
        self.volumn = [i['volumn'] for i in data]


class ExpError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


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
    exp = exp.replace('open', 'openprice')
    if 'import' in exp:
        raise ExpError('Can not import here!')
    if 'os.' in exp:
        raise ExpError('os can not be used here!')
    if 'sys.' in exp:
        raise ExpError('sys can not be used here!')

    res_list = []
    len_data = len(data)
    for date_number in range(1, len_data+1):
        openprice = context.openprice[0:date_number]
        close = context.close[0:date_number]
        high = context.high[0:date_number]
        low = context.low[0:date_number]
        volumn = context.volumn[0:date_number]
        openprice.reverse()
        close.reverse()
        high.reverse()
        low.reverse()
        volumn.reverse()
        res = eval(exp)
        if type(res) is bool:
            res = 1 if res else 0
        res_list.append(res)
    return res_list


def parsing_program(data, program):
    context = DataContext(data)
    if 'import' in program:
        raise ExpError('Can not import here!')
    if 'os.' in program:
        raise ExpError('os can not be used here!')
    if 'sys' in program:
        raise ExpError('sys can not be used here!')
    res = []
    exec(program)
    return res


def neutralization(l):
    abs_list = [abs(i) for i in l]
    max_abs = max(abs_list)
    # all numbers al zeros
    if not max_abs:
        max_abs = 1
    return [i/max_abs for i in l]


if __name__ == '__main__':
    _DEBUG = False
    if _DEBUG:
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

        number = '000403_sz'
    else:
        sim_type = sys_argv[1]
        exp = program = sys_argv[2]
        number = sys_argv[3]

    data = []
    path = 'data/sz/%s'
    filename = "%s.csv" % number

    with open(path % filename) as f:
        lines = f.readlines()

    for line in lines[1:]:
        line_array = line.split(',')
        line_dict = {
            'date': line_array[0],
            'open': float(line_array[1]),
            'high': float(line_array[2]),
            'low': float(line_array[3]),
            'close': float(line_array[4]),
            'volumn': float(line_array[5])
        }
        data.append(line_dict)
        if len(data) > 1000:
            break
    data.reverse()

    if int(sim_type):
        try:
            res = parsing_expr(data, exp)
        except Exception, ex:
            print json.dumps({'isValid': False, 'error': str(ex)})
            exit(0)
    else:
        try:
            res = parsing_program(data, program)
        except Exception, ex:
            print json.dumps({'isValid': False, 'error': str(ex)})
            exit(0)
    res = neutralization(res)

    back_test_data = data
    stratage_res = res

    # 最终结果
    curve_data = []
    stock = []

    # 初始状态
    last_close = data[0]['close']
    # 仓位
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
        total_assets = sell_money
        timestamp = time.mktime(
            datetime.strptime(i[0]['date'], '%Y-%m-%d').timetuple()) * 1000
        curve_data.append([int(timestamp), total_assets])
        stock.append([int(timestamp), today_close])
        last_close = today_close
        last_position = money_position
        # print i[0]['date'], last_position, money_position, total_assets

    json_dump = json.dumps({
            'isValid': True,
            'error': '',
            'data1': curve_data,
            'data2': stock,
            'sharp': 0.0,
            'return': 0.0,
            'dropdown': 0.0
        })
    print json_dump
