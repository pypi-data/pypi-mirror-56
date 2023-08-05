# coding=utf-8
import hashlib
import random


class StringUtils(object):

    @staticmethod
    def randomStr(length):
        seed = "1234567890abcdefghijklmnopqrstuvwxyz"
        sa = []
        for i in range(length):
            sa.append(random.choice(seed))
        return ''.join(sa)

    @staticmethod
    def randomNum(length):
        seed = "1234567890"
        sa = []
        for i in range(length):
            sa.append(random.choice(seed))
        return ''.join(sa)

    @staticmethod
    def md5(data):
        h = hashlib.md5()
        h.update(data)
        return h.hexdigest()

    @staticmethod
    def phoneToNick(phone):
        if len(phone) > 4:
            return "zzyl_" + phone[-4:]
        else:
            return phone

    @staticmethod
    # 将字典转成字符串
    def dict2str(d):
        s = ''
        for i in d:
            s = s + i + ': ' + d[i] + '\r\n'
        return s
