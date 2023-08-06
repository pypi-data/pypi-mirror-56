"""
***************************
**** @author: Li
**** @date: 2019/11/21
***************************
"""

import random
import string
import time
from datetime import datetime


class RandomString:
    def __init__(self):
        pass

    @staticmethod
    def create_rand_string(num, types='charmix'):
        if types is 'key':
            # 随机生成: str 小写字母 + 数字
            sample = string.ascii_lowercase + string.digits
            rand_str = ''.join(random.choices(sample, k=num))
        elif types is 'int':
            # 随机生成: int num
            sample = string.digits
            rand_str = ''.join(random.choices(sample, k=num))
            rand_str = int(rand_str)
        elif types is 'charmix':
            # 随机生成: str 中文 + 英文 + 数字 + 符号
            e_sample = string.ascii_letters + string.digits + string.punctuation
            e_sample = e_sample.replace('\n', '').replace('\r', '')
            c_num = random.randrange(0, num)
            e_num = num - c_num
            rand_e = ''.join(random.choices(e_sample, k=e_num))
            rand_c = ''
            i = 0
            while i < c_num:
                head = random.randint(0xb0, 0xf7)
                body = random.randint(0xa1, 0xfe)
                str_c = f'{head:x}{body:x}'
                rand_c = rand_c + bytes.fromhex(str_c).decode('gb18030')
                i = i + 1
            str_comb = rand_e + rand_c
            str_list = list(str_comb)
            random.shuffle(str_list)
            rand_str = ''.join([str(i) for i in str_list])
        else:
            raise Exception("The type is invalid.")
        return rand_str


class TimeCalculation:
    def __init__(self):
        pass

    @staticmethod
    def time_elapsed_str_to_now(str_time):
        """ datetime格式字符串str_t1转换成float类型，计算从str_t1到now，所经过的时间

        :param str_time: datetime时间格式的字符串，用于比较
        :return: 从str_t1到函数调用的当前时刻所经过的时间，单位: 秒
        """
        before_time = datetime.timestamp(datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S'))
        now_time = time.time()
        return round(now_time - before_time)

    @staticmethod
    def time_before_now(float_time):
        """ datetime格式字符串str_t1转换成float类型，计算从str_t1到now，所经过的时间

        :param float_time: datetime时间格式的字符串，用于比较
        :return: 从str_t1到函数调用的当前时刻所经过的时间，单位: 秒
        """
        time_e = float(float_time) + 1
        now_time = time.time()
        return round(now_time - time_e)
