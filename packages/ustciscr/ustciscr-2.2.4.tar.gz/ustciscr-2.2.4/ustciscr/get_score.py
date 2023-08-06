import pandas as pd
import numpy as np
import datetime
import requests
from pyDes import des, CBC, PAD_PKCS5
import binascii

user_id = ''
start_time = ''
end_time = ''
KEY = 'ustciscr'

def get_user_id(id):
    global user_id
    global start_time
    user_id = id
    start_time = datetime.datetime.now()


def logscore(y_true, y_pred, l):
    eps = 1e-15
    y_true = np.array(y_true).astype(np.float)
    y_pred = np.array(y_pred).astype(np.float)
    assert (len(y_true) and len(y_true) == len(y_pred))

    p = np.clip(y_pred, eps, 1 - eps)
    a = float(np.sum(- y_true * np.log(p) * 0.7 - (1 - y_true) * np.log(1 - p) * 0.3))
    score = (1 - (a / l)) * 100

    return score


def unitest(y_true, y_pred, l):
    score = logscore(y_true, y_pred, l)

    return score


def des_encrypt(s):
    secret_key = KEY
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en)


def des_descrypt(s):
    secret_key = KEY
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return de


def get_score_by_yunanbao(train, test):
    if train.shape[0] != test.shape[0]:
        print("The train_length and test_length is different!")
        return None
    y_true = []
    y_pred = []
    length = 0
    df_merge = pd.merge(train, test, on='zjnsrsbh')
    for index, row in df_merge.iterrows():
        y_true.append(row['pc'])
        y_pred.append(row['Probability'])
        length = length + 1
    score = unitest(y_true, y_pred, length)
    return score


def getscore(train, test):
    global end_time, start_time
    score_log = get_score_by_yunanbao(train=train, test=test)
    accurate = round(score_log, 8)
    end_time = datetime.datetime.now()
    run_time = (end_time - start_time).total_seconds()
    if run_time < 60:
        score_time = score_log * 0.9 + 1
        score = round(score_time, 8)
    elif run_time >= 60 and run_time < 120:
        score_time = score_log * 0.9 + 0.7
        score = round(score_time, 8)
    elif run_time >= 120 and run_time < 360:
        score_time = score_log * 0.9 + 0.5
        score = round(score_time, 8)
    elif run_time >= 360 and run_time < 600:
        score_time = score_log * 0.9 + 0.3
        score = round(score_time, 8)
    else:
        score_time = score_log * 0.9 + 0.1
        score = round(score_time, 8)
    return start_time, end_time, run_time, accurate, score


def post_data(train,test):
    global user_id
    url = 'http://60.167.58.71:88/match/submit'
    if user_id != '':
        start_time, end_time, run_time, accurate, score = getscore(train, test)
        print('%s,%s,%s,%s,%s,%s' % (user_id, start_time, end_time, run_time, accurate, score))
        text = '{},{},{},{},{},{}'.format(user_id, start_time, end_time, run_time, accurate, score)
        params_encrypt = str(des_encrypt(text), 'utf-8')
        params = {
            "scoreDetail": params_encrypt
        }
        page = requests.get(url, params=params)
        print(page.text)
    else:
        print("Please input your id")

