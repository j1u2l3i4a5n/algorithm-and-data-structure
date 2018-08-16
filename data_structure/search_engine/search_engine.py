# -*- coding: utf-8 -*-
'''

'''

import os
import numpy as np

def page_read(path):
    #O(pages_num)
    current = os.getcwd()
    os.chdir(path)
    page_list = os.listdir('.')
    page = []
    for i in page_list:
        with open(i) as files:
            page.append(files.read())
    os.chdir(current)
    return page    

def searching_list():
    #O(list_len)
    with open('list.txt', 'r') as files:
        data = files.read()
    data = data.split('\n')
    data.pop()
    return data

def parsing(raw_page):
    #O(page_num * page_len)
    link_list = []
    content = []
    for i in raw_page:
        data = i.split('\n')
        data.pop()
        length = len(data)
        link_list.append(data[0:length - 2])
        content.append(data[length - 1])
    
    return link_list, content
    
def net_matrix(link_list):
    #O(page_num * page_len)
    size = len(link_list)
    matrix = np.zeros((size,size))
    for i in range(size):
        for j in link_list[i]:
            link = int(j[4:])
            try:
                matrix[i][link] = 1
            except IndexError:
                pass
    return matrix.T
    

def pagerank(net, d, DIFF):
    #O(page_num^3 * 收斂次數)
    size = len(net)
    outdegree = net.sum(0)
    new_net = np.divide(net, outdegree, where = outdegree != 0) * d
              
    pr = np.zeros(size)
    pr += 0.002
    constant = np.zeros(size)
    constant += (1 - d) / size
    
    diff = float('Inf')
    while diff > DIFF:
        pr_new = new_net.dot(pr) + constant
        diff = abs(pr_new - pr).sum()
        pr = pr_new
        
    page = list(range(size))
    change = True
    while change:
        change = False
        for i in range(len(pr) - 1):
            if pr[i] < pr[i + 1]:
                pr[i], pr[i + 1] = pr[i + 1], pr[i] 
                page[i], page[i + 1] = page[i + 1], page[i]
                change = True
                
    return pr, outdegree, page
        
def write_file(pr, outdegree, page, d, DIFF, dictionary, search_list):
    #O()
    d = str(d)[2:]
    DIFF = str(DIFF)[2:]
    with open('%s_%s.txt'%(d, DIFF), 'w') as files:
        for i in range(len(page)):
            files.write('page%d %d %.7f\n'%(page[i], outdegree[page[i]], pr[i]))
            
    with open('reverseindex.txt', 'w') as files:
        sorted_key = sorted(dictionary)
        for i in sorted_key:
            files.write(str(i))
            for j in dictionary[i]:
                files.write(' page%s'%(j))
            files.write('\n')
            
    with open('result_%s_%s.txt'%(d, DIFF), 'w') as files:
        for i in search_list:
            result = searching(i, page, dictionary)
            
            if type(result) == tuple:
                files.write('AND ')
                if len(result[0]) == 0:
                    files.write('none')
                for j in result[0]:
                    files.write('page%d '%(j))
                files.write('\nOR ')
                if result[1] == 0:
                    files.write('none')
                for j in result[1]:
                    files.write('page%d '%(j))
                files.write('\n')

            else:
                if len(result) == 0:
                    files.write('none')
                for j in result:
                    files.write('page%d '%(j))
                files.write('\n')
        
def reverse_index(content):
    dictionary = {}
    for index, value in enumerate(content):
        words = value.split(' ')
        words.pop()
        for j in words:
            if not j in dictionary:
                dictionary[j] = [index]
            else:
                if not index in dictionary[j]:
                    dictionary[j] += [index]
    
    return dictionary

def searching(words, series, dictionary):
    size = len(series)
    words = words.split(' ')
         
    and_pages = []
    or_pages = []
    if words[0] in dictionary:
        for i in dictionary[words[0]]:
            and_pages.append(i)
            or_pages.append(i)

    for i in words[1:]: 
        if i in dictionary:
            tmp = []
            for j in dictionary[i]:
                if not j in or_pages:
                    or_pages.append(j)
                if j in and_pages:
                    tmp.append(j)
            and_pages = tmp

    if len(words) == 1:
        result = []
        i = 0  
        while i < size and len(result) < 10:
            if series[i] in and_pages:            
                result.append(series[i])
            i = i + 1
    
        return result
    
    else:
        and_result = []
        or_result = []
        
        i = 0     
        for i in range(len(series)):
            page = series[i]
            if page in and_pages and len(and_result) < 10:            
                and_result.append(page)
            if page in or_pages and len(or_result) < 10:
                or_result.append(page)
                  
        return and_result, or_result
        
        
if __name__ == '__main__':
    d_list = [0.25, 0.45, 0.65, 0.85]
    DIFF_list = [0.1, 0.01, 0.001]
    search_list = searching_list()
    raw_page = page_read('..\web-search-files2')
    link_list, content = parsing(raw_page)
    net = net_matrix(link_list)
    dictionary = reverse_index(content)
    for d in d_list:
        for DIFF in DIFF_list:
            pr, outdegree, page = pagerank(net, d, DIFF)
            write_file(pr, outdegree, page, d, DIFF, dictionary, search_list)
