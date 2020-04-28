# -*- coding: utf-8 -*-
# @Author : Hcyang-NULL
# @Time   : 2020/4/23 3:48 下午
# @Email  : hcyangnull@gmail.com
# - - - - - - - - - - -

import tornado
import tornado.web
import tornado.ioloop
import os
import time
import traceback
import json
from hplc import plot


current_path = os.path.dirname(__file__)


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        args = [0.7, 0, 50, 0, 150, 12, 3, 200]
        table_css = ['']
        table_css.extend(['display: none'] * 19)
        style = [5, 1, 7, 4, 25, 5, 7, 3, 'yes', '#000000', '#000000', '#1B31FA']
        self.render("template.html", hplc_id=-1, args=args, a=['']*20, b=['']*20, c=['']*20, red_lis=[False]*20, inte_lis=['']*20, table_css=table_css, js='', peak_num=2, extra=[0, 0], style=style)


class PlotHandler(tornado.web.RequestHandler):
    def get(self):
        args = [0.7, 0, 50, 0, 150, 12, 3, 200]
        table_css = ['']
        table_css.extend(['display: none'] * 19)
        style = [5, 1, 7, 4, 25, 5, 7, 3, 'yes', '#000000', '#000000', '#1B31FA']
        self.render("template.html", hplc_id=-1, args=args, a=[''] * 20, b=[''] * 20, c=[''] * 20, red_lis=[False]*20, inte_lis=['']*20, table_css=table_css, js='', peak_num=2, extra=[0, 0], style=style)

    def post(self):
        try:
            temp_solvent_start = float(self.get_body_argument('solvent_start'))
            solvent_start = max(int(temp_solvent_start * 300), 0)
            temp_solvent_end = float(self.get_body_argument('solvent_end'))
            solvent_end = min(int(temp_solvent_end * 300), 15000)
            line_width = float(self.get_body_argument('line_width'))
            x_start = float(self.get_body_argument('x_start'))
            x_end = float(self.get_body_argument('x_end'))
            y_start = float(self.get_body_argument('y_start'))
            y_end = float(self.get_body_argument('y_end'))
            width_ratio = float(self.get_body_argument('width_ratio'))
            height_ratio = float(self.get_body_argument('height_ratio'))
            dpi = int(self.get_body_argument('dpi'))
            args = [line_width, x_start, x_end, y_start, y_end, width_ratio, height_ratio, dpi]

            x_major_num = float(self.get_body_argument('x_major_num'))
            x_minor_num = float(self.get_body_argument('x_minor_num'))
            x_major_len = float(self.get_body_argument('x_major_len'))
            x_minor_len = float(self.get_body_argument('x_minor_len'))
            y_major_num = float(self.get_body_argument('y_major_num'))
            y_minor_num = float(self.get_body_argument('y_minor_num'))
            y_major_len = float(self.get_body_argument('y_major_len'))
            y_minor_len = float(self.get_body_argument('y_minor_len'))
            chem_style = self.get_body_argument('chem')
            x_tick_color = self.get_body_argument('x_tick_color')
            y_tick_color = self.get_body_argument('y_tick_color')
            curve_color = self.get_body_argument('curve_color')
            style = [x_major_num, x_minor_num, x_major_len, x_minor_len, y_major_num, y_minor_num, y_major_len, y_minor_len, chem_style, x_tick_color, y_tick_color, curve_color]

            peak_num = int(self.get_body_argument('peak_num'))
            if peak_num <= 2:
                args = [0.7, 0, 50, 0, 150, 12, 3, 500]
                table_css = ['']
                table_css.extend(['display: none'] * 19)
                style = [5, 1, 7, 4, 25, 5, 7, 3, 'yes', '#000000', '#000000', '#1B31FA']
                self.render("template.html", hplc_id=-1, args=args, a=[''] * 20, b=[''] * 20, c=[''] * 20, red_lis=[False]*20, inte_lis=['']*20, table_css=table_css, js='alert("请填写数据！")', peak_num=2, extra=[0, 0], style=style)
                return
            a_lis = []
            b_lis = []
            c_lis = []
            red_lis = []
            count = 0
            for i in range(1, peak_num-1):
                a_lis.append(float(self.get_body_argument('a' + str(i))))
                b_lis.append(float(self.get_body_argument('b' + str(i))))
                c_lis.append(float(self.get_body_argument('c' + str(i))))
                red_lis.append('yy'+str(i) in self.request.body_arguments)
                count += 1

            extra = [solvent_start, solvent_end]
            peak_num = len(a_lis) + 2
            hplc_id, integrate_lis = plot(args, a_lis, b_lis, c_lis, red_lis, extra, style)
            extra = [temp_solvent_start, temp_solvent_end]

            table_css = ['']*(count+1)
            count = 20 - count
            table_css.extend(['display: none']*(count-1))
            a_lis.extend(['']*count)
            b_lis.extend(['']*count)
            c_lis.extend(['']*count)
            red_lis.extend([False]*count)
            integrate_lis.extend(['']*count)
        except Exception as e:
            print(e)
            args = [0.7, 0, 50, 0, 150, 12, 3, 500]
            table_css = ['']
            table_css.extend(['display: none'] * 19)
            style = [5, 1, 7, 4, 25, 5, 7, 3, 'yes', '#000000', '#000000', '#1B31FA']
            self.render("template.html", hplc_id=-1, args=args, a=[''] * 20, b=[''] * 20, c=[''] * 20, red_lis=[False]*20, inte_lis=['']*20, table_css=table_css, js='alert("数据有错误！请重新填写！")', peak_num=2, extra=[0, 0], style=style)
            return

        self.render("template.html", hplc_id=hplc_id, args=args, a=a_lis, b=b_lis, c=c_lis, red_lis=red_lis, inte_lis=integrate_lis, table_css=table_css, js='', peak_num=peak_num, extra=extra, style=style)


def init():
    app = tornado.web.Application(
        handlers = [
            (r'/', HomeHandler),
            (r'/plot', PlotHandler),
            # (r'/pdf_trans/(?P<trans_id>\d*)', TransHandler)
        ],
        template_path='template',
        static_path=os.path.join(os.path.dirname(__file__), "statics"),
        debug=True
    )
    return app


if __name__ == '__main__':
    app = init()
    app.listen(8023)
    tornado.ioloop.IOLoop.current().start()
