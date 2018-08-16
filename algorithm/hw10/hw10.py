# -*- coding: utf-8 -*-
'''
@file: network_change.py
@brief: 
    Give a network(graph), return a new network that fulfill the following cond
    -ition.
        1. every node can go through to any other node with only one path
        2. minized the amount of nodes whose degree changed
@Created on Mon Jun  4 16:49:59 2018
@author: Hung-ru Lin
'''

'''
演算法的精神：
　　使用貪婪演算法的精神，每次都選擇最好的選擇，滿足最容易被滿足的點，藉此滿足最多的點
'''

import sys

class Vertex:
    def __init__(self, name):
        self.name = name
        self.degree = 0
        self.neighbor = []
    
    def __repr__(self):
        return str(self.name)
    

def read_files(filename):
    '''
    @brief: for reading input data file.

    @detail: 
        read a network file with the following format:    
            amount_of_node amount_of_edge
            node1 node2
            node1 node2
            ...
    @complexity:
        O(nlogn), n: numbers of node
             reason: sorting use the most of the time
             
    @param param_out: 
        info: a iterable object with amount of node and edge
        data: a sorted list with node_name and its degree
        
    @param param_in: 
        filename: a string that is the name of the file is needed to be read. 
        
    @return: 
        a breif information about the graph
    '''
    with open(filename, 'r') as files:
        data = files.readlines()
        

    for i in range(len(data)):
        data[i] = data[i].rstrip()
        
    info = data[0]
    info = info.split(' ')
    info = list(map(int, info))
    del data[0]
    degree = {}
    
    for i in range(len(data)):
        data[i] = data[i].split(' ')
        for j in range(2):
            if not int(data[i][j]) in degree:
                degree[int(data[i][j])] = 1
            else:
                degree[int(data[i][j])] += 1
               
    data = []
    for i in degree:
        data.append([degree[i], i])
    
    data = sorted(data)
                   
    return info, data
               
def dfs_tree(graph, vertex, traverse):
    traverse[vertex] = True
    tree = {}
    for i in graph:
        tree[i] = []
    
    for i in graph[vertex]:
        if not traverse[i]:
            tree[vertex].append(i)
            tree[i].append(vertex)
            subtree = dfs_tree(graph, i, traverse)
            for i in subtree:
                tree[i] += subtree[i]
                
    return tree

def reconnected(degree):
    '''
    @brief: create a new network by degree information

    @detail: 
        the algorithm try to minize the amount of nodes whose degree changed by
        fulfilling the node with less degree first and fulfilling the node with
        more degree later.
        
        I used a queue to order the node needed to be fulfilled first. An
        -d used a variable to know the node is full or not. 
        
    @complexity:
        O(n), n: the numbers of node.
             reason: loop all of the node once
    
    @param param_out: 
        tree: a adjacent list save the graph information and the nodes' degree 
        diference
        edge: a list of edges
        
    @param param_in: 
        degree: a list save nodes' name and its degree 
        
    @return: 
        a new network fulfill those conditions.    
    '''
    tree = {}
    devide = 0
    
    for i in degree:
        tree[i[1]] = [[],i[0]]
        if i[0] == 1:
            devide += 1
    new_degree = degree[devide : ] + degree[0 : devide] 
    ptr = new_degree.pop(0)[1]
    queue = []
    edges = []
    
    for i in new_degree:
        if tree[ptr][1] == 0:
            ptr = queue.pop(0)[1]
        tree[ptr][0].append(i[1])
        tree[ptr][1] -= 1
        tree[i[1]][0].append(ptr)   
        tree[i[1]][1] -= 1        
        queue.append(i)
        edges.append('%d %d'%(ptr, i[1]))
        
    return tree, edges
        
if __name__ == '__main__':
    filename = sys.argv[1]
    info, degree = read_files(filename)
    tree, edges = reconnected(degree)
    modified = 0
    for i in tree:
        if tree[i][1] != 0:
            modified += 1
            
    filename = filename[:-2] + 'ans'
    with open(filename, 'w') as files:
        files.write('%d\n'%modified)
        files.write('%d %d\n'%(info[0], info[0] - 1))
        for i in edges:
            files.write(i + '\n')

