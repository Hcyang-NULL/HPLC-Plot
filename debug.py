# -*- coding: utf-8 -*-
# @Author : Hcyang-NULL
# @Time   : 2020/4/4 7:53 下午
# @Email  : hcyangnull@gmail.com
# - - - - - - - - - - -

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from random import randint
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.ticker
#

def y_format_func(value, tick_number):
    if value == 150:
        return 'mAU'
    return int(value)

def x_format_func(value, tick_number):
    if value == 0:
        return ''
    return int(value)


f = nc.Dataset('SIGNAL01.cdf')

# 获取所有变量名称
all_keys = f.variables.keys()
print(f'key length: {len(all_keys)}')

# 获取所有变量信息
all_data = {}
for key in all_keys:
    all_data[key] = np.array(f[key][:])

# temp_y = all_data['ordinate_values'][:5]
y = [randint(40,140) for i in range(50)]
# y[:1500] = temp_y
# x = np.arange(0, 5, np.float64(1/300))
x = np.arange(1, 51)
plt.rcParams['figure.figsize'] = (12, 3)
dpi = 200
plt.rcParams['savefig.dpi'] = dpi
plt.rcParams['figure.dpi'] = dpi
plt.xlim(0, 50.5)
plt.ylim(-5, 152.5)
ax = plt.gca()
xmajorLocator = MultipleLocator(5)
xminorLocator = MultipleLocator(1)
ax.xaxis.set_major_locator(xmajorLocator)
ax.xaxis.set_major_formatter(plt.FuncFormatter(x_format_func))
ax.xaxis.set_minor_locator(xminorLocator)
ymajorLocator = MultipleLocator(25)
yminorLocator = MultipleLocator(5)
ax.yaxis.set_major_locator(ymajorLocator)
ax.yaxis.set_major_formatter(plt.FuncFormatter(y_format_func))
ax.yaxis.set_minor_locator(yminorLocator)
# ax.tick_params(axis='y', which='major', pad=15)
ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
ax.spines['right'].set_position(('data', 0))
ax.spines['left'].set_position(('outward', 3))
ax.spines['left'].set_visible(False)
ax.tick_params(axis='x', which='major', size=7)
ax.tick_params(axis='x', which='minor', size=4)

plt.plot(x, y, linewidth=0.7)
# plt.savefig('solvent.png')
plt.show()

exit()


# 
# plt.xlim(0, len(x))
# plt.ylim(-2, 30)
# plt.plot(x[939:1065], y[939:1065])
# plt.show()

with open('table.html', 'w', encoding='utf-8') as f:
    for i in range(1, 21):
        line = '<tr id="tr' + str(i) + '" style="{{table_css[' + str(i-1) + ']}}">\n' + '<th scope="row">' + str(i) + '</th>\n' + '<td id="a' + str(i) + '" class="peak-td" contenteditable="true">{{a[' + (str(i-1)) + ']}}</td>\n' + '<input type="hidden" id="input-a' + str(i) + '" name="a' + str(i) + '" value="{{a[' + (str(i-1)) + ']}}" />\n' +'<td id="b' + str(i) + '" class="peak-td" contenteditable="true">{{b[' + (str(i-1)) + ']}}</td>\n' +'<input type="hidden" id="input-b' + str(i) + '" name="b' + str(i) + '" value="{{b[' + (str(i-1)) + ']}}" />\n' +'<td id="c' + str(i) + '" class="peak-td" contenteditable="true">{{c[' + (str(i-1)) + ']}}</td>\n' +'<input type="hidden" id="input-c' + str(i) + '" name="c' + str(i) + '" value="{{c[' + (str(i-1)) + ']}}" />\n' + '<td class="integrate">{{inte_lis[' + str(i-1) + ']}}</td>\n' + '{% if red_lis[' + str(i-1) + '] is True %}\n<td class="red_line"><input name="yy' + str(i) + '" type="checkbox" checked="false"/></td>\n{% end %}\n{% if red_lis[' + str(i-1) + '] is False %}\n<td class="red_line"><input name="yy' + str(i) + '" type="checkbox"/></td>\n{% end %}\n' + '</tr>'

        f.write(line)

# y = np.arange(6, 10, 0.2)
# x = [5 for i in range(len(y))]
# plt.plot(x, y, color='#2000EF', linewidth=0.7)
# plt.show()
# test = 1
