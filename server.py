__author__ = 'user'

import os
import pathlib
import calendar
import datetime
from bottle import route, run, static_file, template

PORT = int(os.environ.get("PORT", 5000))
BASE_PATH = pathlib.Path(__file__).parent

yy = datetime.datetime.now().year
mm = datetime.datetime.now().month


@route('/')
@route('/<req_year>/<req_month>')
def cal_for_month(req_year=yy, req_month=mm):
    global yy
    global mm
    yy = int(req_year)
    mm = int(req_month)
    cal_html = get_cal(yy, mm)
    return template('cal_template', cal_html=cal_html)


@route('/next')
def nxt():
    global yy
    global mm
    if mm == 12:
        mm = 1
        yy += 1
    else:
        mm += 1
    cal_html = get_cal(yy, mm)
    return template('cal_template', cal_html=cal_html)

@route('/prev')
def prev():
    global yy
    global mm
    if mm == 1:
        mm = 12
        yy -= 1
    else:
        mm -= 1
    cal_html = get_cal(yy, mm)
    return template('cal_template', cal_html=cal_html)


@route('/year')
def get_year ():
    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    cal_html = cal.formatyear(datetime.datetime.now().year)
    return template('year_template', cal_html=cal_html)


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=str(BASE_PATH / 'static'))


def get_cal(yy, mm):
    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    return cal.formatmonth(yy, mm)

run(host='0.0.0.0', port=PORT)
