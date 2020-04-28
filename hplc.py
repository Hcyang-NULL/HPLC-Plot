# -*- coding: utf-8 -*-
# @Author : Hcyang-NULL
# @Time   : 2020/4/4 10:30 下午
# @Email  : hcyangnull@gmail.com
# - - - - - - - - - - -

import netCDF4
from numpy import exp
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from os.path import join
from random import randint
from matplotlib.ticker import MultipleLocator

"""输出参数设置"""
out_dir = '/root/hplc/statics/hplc_imgs'

"""HPLC参数设置"""
# 采样频率：x分/次
sample_frequency = np.float64(1/300)
# 采样时间：x分
sample_time_minute = 50

"""Plot参数设置"""
# 线条粗细度
# line_width = 0.7
# # x轴范围
# x_lim = [-2, 52]
# # y轴范围
# y_lim = [-2, 20]
# # 宽高比
# wh_ratio = [12.0, 3.0]
# # 分辨率
# dpi = 200


def gaussian(a, b, c):
    """
    :param a: 最高峰Y值
    :param b: 中心坐标
    :param c: 方差
    :return: 返回对应y值列表
    """
    # 类型转换
    a, b, c = np.float64(a), np.float64(b), np.float64(c)

    # Gaussian函数值
    def func(x):
        return np.float64(a*exp(-((x-b)**2)/(2*c)))

    # 计算Gaussian函数值
    value_y = np.array([func(i) for i in np.arange(0, sample_time_minute, sample_frequency)])

    return value_y


def loc_left_point(x, y, start, max_value):
    gap = 1e-3
    fix_index = -1
    for index, ix in enumerate(x):
        if ix >= start:
            fix_index = index - 1
            break

    if y[fix_index-1] > y[fix_index]:
        past_y_gap = max_value - y[fix_index]
        new_y_gap = past_y_gap
        while new_y_gap <= past_y_gap:
            fix_index -= 1
            past_y_gap = new_y_gap
            new_y_gap = max_value - y[fix_index]

    while fix_index >= 0:
        if y[fix_index] < gap:
            return fix_index, 0
        elif y[fix_index-1] >= y[fix_index]:
            return fix_index, 1
        fix_index -= 1


def loc_right_point(x, y, start, max_value):
    gap = 1e-2
    fix_index = -1
    for index in range(len(x)-1, -1, -1):
        ix = x[index]
        if ix <= start:
            fix_index = index + 1
            break

    if y[fix_index+1] > y[fix_index]:
        past_y_gap = max_value - y[fix_index]
        new_y_gap = past_y_gap
        while new_y_gap <= past_y_gap:
            fix_index += 1
            past_y_gap = new_y_gap
            new_y_gap = max_value - y[fix_index]

    while fix_index < len(x):
        if y[fix_index] < gap:
            return fix_index, 0
        elif y[fix_index+1] >= y[fix_index]:
            return fix_index, 1
        fix_index += 1


def plot_point_line(x, y, start=True):
    if start:
        line_y = np.arange(y, y+2, 0.01)
    else:
        line_y = np.arange(y-2, y, 0.01)
    line_x = [x for i in range(len(line_y))]
    plt.plot(line_x, line_y, color='#000000', linewidth=0.7)


def plot_connect_line(x1, y1, x2, y2):
    line_x = np.arange(x1, x2, 0.01)

    def line_func(x):
        return np.float64((y1-y2)/(x1-x2)*(x-x1)+y1)

    line_y = [line_func(i) for i in line_x]
    plt.plot(line_x, line_y, color='#EF5963', linewidth=0.7)


def calc_integrate(x, y, a_lis, b_lis, c_lis, red_lis):
    integrate_lis = []
    for a, b, c, red in zip(a_lis, b_lis, c_lis, red_lis):
        left_index = loc_left_point(x, y, b, a)[0]
        right_index = loc_right_point(x, y, b, a)[0]
        x1, y1 = x[left_index], y[left_index]
        x2, y2 = x[right_index], y[right_index]
        if red:
            plot_point_line(x1, y1, start=True)
            plot_point_line(x2, y2, start=False)
            plot_connect_line(x1, y1, x2, y2)
        integrate_value, err_value = quad(lambda m: a*exp(-((m-b)**2)/(2*c)), x1, x2)
        integrate_lis.append(round(integrate_value, 4))
    return integrate_lis


def plot_solvent(y, info):
    start = info[0]
    end = info[1]
    f = netCDF4.Dataset('SIGNAL01.cdf')
    all_keys = f.variables.keys()
    all_data = {}
    for key in all_keys:
        if key != 'ordinate_values':
            continue
        all_data[key] = np.array(f[key][:])
    solvent_y = all_data['ordinate_values'][start:end]
    y[start:end] = solvent_y
    return y


def set_display(args, style):
    line_width = args[0]
    x_start, x_end = args[1], args[2]
    y_start, y_end = args[3], args[4]
    width_ratio, height_ratio = args[5], args[6]
    dpi = args[7]
    plt.rcParams['figure.figsize'] = (width_ratio, height_ratio)
    plt.rcParams['savefig.dpi'] = dpi
    plt.rcParams['figure.dpi'] = dpi

    ax = plt.axes()
    ax.spines['top'].set_visible(False)
    x_major_num, x_minor_num = style[0], style[1]
    ax.xaxis.set_major_locator(MultipleLocator(x_major_num))
    ax.xaxis.set_minor_locator(MultipleLocator(x_minor_num))

    x_major_len, x_minor_len = style[2], style[3]
    x_tick_color = style[9]
    ax.tick_params(axis='x', which='major', size=x_major_len, pad=2, color=x_tick_color)
    ax.spines['bottom'].set_color(x_tick_color)
    ax.tick_params(axis='x', which='minor', size=x_minor_len, color=x_tick_color)

    y_major_num, y_minor_num = style[4], style[5]
    ax.yaxis.set_major_locator(MultipleLocator(y_major_num))
    ax.yaxis.set_minor_locator(MultipleLocator(y_minor_num))

    y_major_len, y_minor_len = style[6], style[7]
    y_tick_color = style[10]
    ax.tick_params(axis='y', which='major', size=y_major_len, pad=0, color=y_tick_color)
    ax.spines['right'].set_color(y_tick_color)
    ax.tick_params(axis='y', which='minor', size=y_minor_len, color=y_tick_color)

    use_chem = style[8].lower() in ['yes', 'y']
    if use_chem:
        ax.spines['left'].set_position(('outward', 3))
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_position(('data', 0))

        def y_format(value, tick_number):
            if value == y_end:
                return 'mAU'
            return int(value)

        ax.yaxis.set_major_formatter(plt.FuncFormatter(y_format))
        plt.xlim(x_start + sample_frequency, x_end + (x_minor_num / 2.0))
        plt.ylim(y_start - y_minor_num, y_end + y_minor_num)

    else:
        plt.xlim(x_start, x_end)
        plt.ylim(y_start, y_end)
        ax.spines['right'].set_visible(False)

    curve_color = style[11]

    return line_width, curve_color


def plot(args, a_lis, b_lis, c_lis, red_lis, extra, style):
    x = np.arange(0, sample_time_minute, sample_frequency)

    y = None
    for a, b, c in zip(a_lis, b_lis, c_lis):
        temp_y = gaussian(a, b, c)
        if y is None:
            y = temp_y
        else:
            y = y+temp_y

    y = plot_solvent(y, extra)

    line_width, curve_color = set_display(args, style)
    plt.plot(x, y, color=curve_color, linewidth=line_width)

    integrate_lis = calc_integrate(x, y, a_lis, b_lis, c_lis, red_lis)

    seed = randint(1, 50)
    png_name = str(seed) + '.png'
    print(png_name)
    plt.savefig(join(out_dir, png_name))
    plt.close()
    return seed, integrate_lis





