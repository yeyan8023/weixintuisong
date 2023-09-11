# python学习
# 日期 2023/3/7 11:25
from datetime import date, datetime
import json
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

rb = requests.get('http://t.weather.sojson.com/api/weather/city/1001161301')
data = json.loads(rb.text)
# 访问今天的天气情况
dat=data['data']['forecast'][0]

def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_birthday_me():
    return get_birthday() + 279


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
'''

今天是:{{ymd.DATA}}  {{week.DATA}} 
今天:{{type.DATA}}
最{{high.DATA}}  最{{low.DATA}} 
{{sunrise.DATA}} 日出 {{sunset.DATA}}日落
今天 {{fx.DATA}}  {{fl.DATA}} 
{{notice.DATA}} 
今天是我们在一起的第{{love_days.DATA}}天 
距离你的生日还有{{birthday_left.DATA}}天
距离我的生日还有{{birthday_left_me.DATA}}天
今天你的宝贝也很爱你哦

{{words.DATA}}'''
# wea, temperature = get_weather()
data = {"love_days": {"value": get_count()},"ymd": {"value": dat.get('ymd')},"type": {"value": dat.get('type')},
        "birthday_left_me": {"value": get_birthday_me()},"high": {"value": dat.get('high')},
        "low": {"value": dat.get('low')}, "sunrise": {"value": dat.get('sunrise')},"week": {"value": dat.get('week')},
        "sunset": {"value": dat.get('sunset')}, "fx": {"value": dat.get('fx')}, "fl": {"value": dat.get('fl')},
        "notice": {"value": dat.get('notice')},
        "birthday_left": {"value": get_birthday()}, "words": {"value": get_words(), "color": get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
