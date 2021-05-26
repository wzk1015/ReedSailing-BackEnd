import random
import os
import json
import jieba.analyse
import math

MAX_ACCEPT = 100
ACCEPT_THRESH = 0
WEIGHT_TYPE = 1
WEIGHT_KEYWORD = 10

portrait_dir = '/root/portraits/'

if not os.path.exists(portrait_dir):
    os.mkdir(portrait_dir)


def get_portrait_path(id_):
    path = portrait_dir+str(id_)+".json"
    if not os.path.exists(path):
        with open(path, "w") as f:
            init = {
                'type': {},
                'keyword': {}
            }
            json.dump(init, f)
    return path


def load_portrait(id_):
    with open(get_portrait_path(id_), 'r') as f:
        port = json.load(f)
    return port


def save_portrait(id_, port):
    with open(get_portrait_path(id_), 'r') as f:
        json.dump(port, f)


def portrait_add_keyword(port, kwds):
    d = port['keyword']
    kwds = kwds.split(' ')
    for kwd in kwds:
        if not d.get(kwd):
            d[kwd] = 1
        else:
            d[kwd] += 1


def portrait_del_keyword(port, kwds):
    d = port['keyword']
    kwds = kwds.split(' ')
    for kwd in kwds:
        if d.get(kwd, 0) > 0:
            d[kwd] -= 1


def update_keyword(id_, old_kwds, new_kwds):
    port = load_portrait(id_)
    portrait_del_keyword(port, old_kwds)
    portrait_add_keyword(port, new_kwds)
    save_portrait(id_, port)


def delete_keyword(id_, kwds):
    port = load_portrait(id_)
    portrait_del_keyword(port, kwds)
    save_portrait(id_, port)


def add_keyword(id_, kwds):
    port = load_portrait(id_)
    portrait_add_keyword(port, kwds)
    save_portrait(id_, port)


def get_keyword(text):
    K = min(5, math.floor(len(text)/20))
    kwds = jieba.analyse.extract_tags(text, topK=K)
    return ' '.join(kwds)


def cal_suitability(act, user_pic):
    suit = 0
    kwds = act.keywords
    kwds = kwds.split()
    kwd_dict = user_pic['keyword']
    for kwd in kwds:
        suit += kwd_dict.get(kwd, 0)
    return suit


def take_suit(elem):
    # this function is for sort method to take key from a element
    return elem['suitability']


def get_accept_list(act_list, user_id):
    if not user_id:
        # user not verified yet
        return act_list
    user_pic = load_portrait(user_id)
    accept_list = []
    accept_cnt = 0
    for act in act_list:
        suitability = cal_suitability(act, user_pic)
        if suitability >= ACCEPT_THRESH:
            act['suitability'] = suitability
            accept_cnt += 1
            accept_list.append(act)
            if accept_cnt > MAX_ACCEPT:
                break
    accept_list.sort(key=take_suit, reverse=True)
    return accept_list


def getgroup(accept_list):
    raise NotImplementedError
