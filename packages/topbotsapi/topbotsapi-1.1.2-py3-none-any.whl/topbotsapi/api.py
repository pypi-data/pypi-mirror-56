import json
import urllib3
from .classes import *
from .exceptions import *


def getType(data):
    decoder = json.decoder.JSONDecoder()
    dic = decoder.decode(data)
    if dic['code'] != 200:
        if dic['code'] == 205:
            raise TokenExeption(dic['message'])
        else:
            raise IdExeption(dic['message'])
    else:
        return dic["message"]


def getBot(botid, token):
    http = urllib3.PoolManager()
    dic = dict(token=token, botID=f'{botid}')
    r = http.request("GET", "https://topdiscordbots.tk/api/bots/get/", body=json.dumps(dic).encode('utf-8'),
                     headers={'Content-Type': 'application/json'})
    data = r.data.decode()
    dta = getType(data)
    if type(dta) == type(""):
        return dta
    else:
        return Bot(**dta)


def getUser(userid, token):
    http = urllib3.PoolManager()
    dic = dict(token=token, userID=f'{userid}')
    r = http.request("GET", "https://topdiscordbots.tk/api/users/get/", body=json.dumps(dic).encode('utf-8'),
                     headers={'Content-Type': 'application/json'})
    data = r.data.decode()
    dta = getType(data)
    if type(dta) == type(""):
        return dta
    else:
        return User(**dta)


def getUserBots(userid, token):
    http = urllib3.PoolManager()
    dic = dict(token=token, userID=f'{userid}')
    r = http.request("GET", "https://topdiscordbots.tk/api/users/get/bots", body=json.dumps(dic).encode('utf-8'),
                     headers={'Content-Type': 'application/json'})
    data = r.data.decode()
    dta = getType(data)
    if type(dta) == type(""):
        return dta
    else:
        bots = []
        for i in dta:
            bots.append(Bot(**i))
        return bots


def isVoted(botid,userid,token):
    http = urllib3.PoolManager()
    dic = dict(token=token, userID=f'{userid}',botID=f'{botid}')
    r = http.request("GET", "https://topdiscordbots.tk/api/users/get/voted", body=json.dumps(dic).encode('utf-8'),
                     headers={'Content-Type': 'application/json'})
    data = r.data.decode()
    dta = getType(data)
    if type(dta) == type(""):
        return dta
    else:
        return dta
