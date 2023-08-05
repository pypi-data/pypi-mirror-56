import json
import requests
import hashlib
import random
import time



def get_random():
    return random.randint(100000, 999999)

def get_cur_time():
    return int(time.time())

def calculate_sig(appkey, rnd, cur_time, phone_numbers):
    phone_numbers_string = phone_numbers[0]
    for i in range(1, len(phone_numbers)):
        phone_numbers_string += "," + phone_numbers[i]
    return hashlib.sha256(("appkey=" + appkey + "&random=" + str(rnd) + "&time=" + str(cur_time)
                          + "&mobile=" + phone_numbers_string).encode()).hexdigest()

def calculate_sig_for_templ_phone_numbers(appkey, rnd, cur_time, phone_numbers):
    """ 计算带模板和手机号列表的 sig """
    phone_numbers_string = phone_numbers[0]
    for i in range(1, len(phone_numbers)):
        phone_numbers_string += "," + phone_numbers[i]
    return hashlib.sha256(("appkey=" + appkey + "&random=" + str(rnd) + "&time="
                          + str(cur_time) + "&mobile=" + phone_numbers_string).encode()).hexdigest()

def calculate_sig_for_templ(appkey, rnd, cur_time, phone_number):
    phone_numbers = [phone_number]
    return calculate_sig_for_templ_phone_numbers(appkey, rnd, cur_time, phone_numbers)

def phone_numbers_to_list(nation_code, phone_numbers):
    tel = []
    for phone_number in phone_numbers:
        tel.append({"nationcode": nation_code, "mobile":phone_number})
    return tel

def send_request(url, data):
    rsp = requests.post(url, data=json.dumps(data))
    return rsp
