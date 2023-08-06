import json
import requests
import hashlib
import random
import time

def get_random():
    return random.randint(100000, 999999),


def get_cur_time():
    return int(time.time())

def calculate_sig(appkey, rnd, cur_time, phone_numbers):
    if type(phone_numbers) in (str, int):
        phone_numbers = [phone_numbers]


    mobile = ",".join([str(num) for num in phone_numbers])
    hash_str = "appkey={appkey}&random={rnd}&time={cur_time}&mobile={mobile}".format(
            appkey=appkey,
            rnd=rnd,
            cur_time=cur_time,
            mobile=mobile)

    return hashlib.sha256(hash_str.encode()).hexdigest()

def phone_numbers_to_list(nation_code, phone_numbers):
    tel = []
    for phone_number in phone_numbers:
        tel.append({"nationcode": nation_code, "mobile":phone_number})
    return tel

def send_request(url, data):
    rsp = requests.post(url, data=json.dumps(data))
    return rsp
