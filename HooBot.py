import requests
import time
import hmac
import hashlib
import random
import json

host = "https://api.hoo.co"

# Change your client_id and client_secret

client_id = "crVmV5ZGLCLmRUXgsWzGH9cDx67EtP"
client_key = "eSwbaBCVqAks4pd3vXHTPoxUALzKf35PmhRD9kuN1YxQtcJmSZ"


def gen_sign(client_id, client_key):
    ts = int(time.time())
    nonce = "abcdefg"
    obj = {"ts": ts, "nonce": nonce, "sign": "", "client_id": client_id}
    s = "client_id=%s&nonce=%s&ts=%s" % (client_id, nonce, ts)
    v = hmac.new(client_key.encode(), s.encode(), digestmod=hashlib.sha256)
    obj["sign"] = v.hexdigest()
    return obj


print("Order Execution Started")

n = 10
# n for while loop infinite condition
while n > 0:

    path = "/open/innovate/v1/kline"
    obj = gen_sign(client_id, client_key)
    obj.update({"symbol": "DOGGY-USDT", "type": "1Min"})
    res = requests.get(host + path, params=obj)
    # print(res.content)

    output = res.content
    datas = json.loads(output)
    # print(datas)

    arrayLength = len(datas['data'])
    openPrice = datas['data'][arrayLength-1]['open']
    closePrice = datas['data'][arrayLength-1]['close']

    print("openPrice: "+openPrice)
    print("closePrice: "+closePrice)

    pathOrder = "/open/innovate/v1/orders/place"
    objOrder = gen_sign(client_id, client_key)
    objOrder.update({"symbol": "DOGGY-USDT", "price": closePrice,
                "quantity": "1000", "side": "1"})

    res2 = requests.post(host + pathOrder, data=objOrder)

    print(res2)

    pathSell = "/open/innovate/v1/orders/place"
    objSell = gen_sign(client_id, client_key)
    objSell.update({"symbol": "DOGGY-USDT", "price": closePrice,
               "quantity": "1000", "side": "-1"})

    res3 = requests.post(host + pathSell, data=objSell)

    print(res3)

    pathTime = "/open/innovate/v1/timestamp"
    res4 = requests.get(host + pathTime)
    resTime = json.loads(res4.content)
    ts=resTime['data']

    time.sleep(3)
    



