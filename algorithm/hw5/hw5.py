# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 16:04:03 2018

@author: rjlin
"""
import sys

def merge_skyline(A, B):
    '''
    用來整合兩個skyline的函式
    '''
    i = 0
    j = 0
    m = len(A)
    n = len(B)

    A_height = 0  #儲存A_skyline現在的高度
    B_height = 0  #儲存B_skyline現在的高度
    output = []
    '''
    稱呼A陣列裡的元素分別為a1,a2,a3...
    稱呼B陣列裡的元素分別為b1,b2,b3...
    稱呼output陣列裡的元素為c1,c2,c3...
    比較a1和b1，若a1較小，則c1 = a1, c2 = a2
    則可以看成A[a3,a4,a5...]和B[b1,b2,b3...]繼續整合
    反之c1 = b1, c2 = b2
    看成A[a1,a2,a3...]和B[b3,b4,b5...]繼續整合
    如此重複執行直到其中一個skyline讀完
    
    以上是簡單概述，細節上要比較區段內高度(如：b4 > a2)
    以及當高度相同時得處理(如：11,4,13,4,15 = 11,4,15)
    
    '''
    while i < m - 1 and j < n - 1:        
        if A[i] < B[j]:                       
            if A[i + 1] >= B_height:          
                output += A[i : i + 2]        
            else:                             
                if output[len(output) - 1] != B_height:      #(避免出現高度相同卻重複紀錄，e.g. (1,3,2,3,5) = (1,3,5))
                    output += [A[i], B_height]
                    
            A_height = A[i + 1]
            i = i + 2
            
            
        elif B[j] < A[i]:                 #同理A,B互換
            if B[j + 1] >= A_height:
                output += B[j : j + 2]
            else:
                if output[len(output) - 1] != A_height:
                    output += [B[j], A_height]

            B_height = B[j + 1]
            j = j + 2
            
            
        else:                            #當A,B前面的起始點相同時
            if A[i + 1] <= B[j + 1]:     #將高度較小的skyline前面兩個去掉
                A_height = A[i + 1]
                i = i + 2
            else:
                B_height = B[j + 1]
                j = j + 2
         
            
    '''
    當A或B其中一個已經讀到最後一個時
    和上面做類似的事情，但只要比較沒讀完的skyline
    '''
            
    stop = 0                            
    last = []                           
    L_height = 0                        
    compare = 0                         
    if i >= m - 1:
        stop = A[i]    
        last = B[j:]
        compare = A_height
        L_height = B_height
    else:
        stop = B[j]
        last = A[i:]
        compare = B_height
        L_height = A_height
        
    i = 0
    while last[i] <= stop and i < len(last) - 1:        #把last比stop小的skyline畫完
        if last[i + 1] >= compare:                      #方法同
            output += last[i : i + 2]        
        else:
            if output[len(output) - 1] != compare:      
                output += [last[i], compare]
        
        L_height = last[i + 1]
        i = i + 2
        
    '''
    剩下的部分(其中一個skyline比另一個要長的部分)已經不需要逐一比對，直接粘上
    '''
    
    
    if last[i] > stop:
        if L_height == output[len(output) - 1]:
            output += last[i:]
        else:
            output += [stop, L_height] + last[i:]
    else:
        if compare == output[len(output) - 1]:
            output += [stop]
        else:
            output += [last[i], compare, stop]
    
    
    return output

def skyline_problem(data):
    '''
    將資料兩兩整合成新的skyline，重複到剩下一個就是結果輸出
    '''
    m = data[0][0]
    list_of_skyline = data[1:]
    if m == 1:                                         #當只剩一條skyline則輸出結果
        string = '('
        for i in range(len(list_of_skyline[0])):
            string += str(list_of_skyline[0][i]) + ','

        string =  string[0:len(string)-1]
        string += ')'
        print(string)

    else:                                             #剩下兩條以上則兩兩merge起來
        n = int((m + 1) / 2)
        output = [[n]]
        i = 0
        while i < m:
            merge = merge_skyline(list_of_skyline[i], list_of_skyline[i+1])
            output.append(merge)
            i = i + 2
        if m % 2 == 1:
            output.append(list_of_skyline[m-1])
        skyline_problem(output)
        
    
    
def read_file(filename):
    '''
    讀檔用的函數
    資料格式：
    
    building數
    (初始座標, 高度, 結束座標)
    ()
    ...
    ()
    
    '''
    with open(filename, 'r') as files:
        data = files.read()

    data = data.split('\n')
    if data[len(data) - 1] == '':
        data.pop()
    data[0] = [int(data[0])]
    for i in range(1,len(data)):
        data[i] = data[i][1:len(data[i])-1]
        data[i] = data[i].split(',')
        for j in range(len(data[i])):
            data[i][j] = int(data[i][j])
    
    return data

'''
生成測試隨機資料
import random

def data_generate(size):
    data = [str(size)]
    for i in range(size):
        a1 = random.randint(1, 100)
        a2 = random.randint(1, 50)
        a3 = a1 + random.randint(1, 10)
        data.append('(%d,%d,%d)'%(a1,a2,a3))
    with open('data.txt', 'w') as files:
        for i in data:
            files.write(i)
            files.write('\n')

'''         


if __name__ == '__main__':
    filesname = sys.argv[1]
    data = read_file(filesname)
    skyline_problem(data)
    
                

    '''
    時間複雜度：  
    merge_skyline O(m + n)    
        (m：A的長度, n；B的長度)
        由於通常會將A和B讀完一遍，所以是O(m + n)
    skyline_problem O(nlogn)
        (n為building數)
        由於每次merge完後會剩下一半的skyline，所以迴圈跑logn次
        而merge一次的skyline數和skyline長度成反比，一次要花O(n)的時間
        乘上merge所花時間就是O(nlogn)

    應用到何種演算法：
        用了devide and conquer的想法，將building分成小堆小堆的再分別merge起來。
    '''

    