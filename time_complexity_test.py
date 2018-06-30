# -*- coding: utf-8 -*-
"""
@brief: time complexity testing
@time: Created on Sat Jun 30 13:05:19 2018

@author: hrlin

"""

import time
import random

def explore(void):
    size = 0
    try:
        for i in void:
            if type(i) == str and len(i) == 1:
                size += 1
            else:
                size += explore(i)
    except:
        return 1
    return size


def complexity(function, *arg):
    size = 0
    for i in arg:
        size += explore(i)
    start = time.time()
    function(*arg)
    end = time.time()
    return (size, end - start)
            

if __name__ == '__main__':
    a = []
    b = ''
    d = {}
    for i in range(100000):
        a.append(random.randint(1,100000))
        b += chr(random.randint(1,200))
        d[random.randint(1,10000)] = chr(random.randint(1,222))
    
    