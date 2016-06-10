import math
import hashlib


def md5(data):
    h = hashlib.md5()
    h.update(bytes(data, 'utf8'))
    return h.hexdigest()


def cantor(k1,k2):
    return math.floor((0.5*(k1+k2)*(k1+k2+1))+k2)


def uncantor(z):
    i = math.floor((math.sqrt(1+(8*z))-1)/2)
    return int(((i*(i+3))/2)-z), int(z-((i*(i+1))/2))


shortset = "0123456789abcdef"
def id2shorturl(id):
    url = ""
    while True:
        url += shortset[(id % 16)]
        id //= 16
        if id <= 0: break
    return url[::-1]


def shorturl2id(shorturl):
    id = 0
    for i in range(0,len(shorturl)):
        id += shortset.index(shorturl[i]) * 16**((len(shorturl)-1)-i)
    return id