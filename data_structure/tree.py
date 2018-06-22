# -*- coding: utf-8 -*-
"""
@brief: tree implement  
@time: Created on Fri Jun 22 16:22:06 2018

@author: hrlin
"""

class Node:
    def __init__(self, value):
        self.value = value
        self.child = None
        self.sibiling = None
        
    def __repr__(self):
        string = str(self.value)
        child = 'None'
        sibiling = 'None'
        if self.child != None:
            child = self.child.__repr__()
        if self.sibiling != None:
            sibiling = self.sibiling.__repr__()
        string += '(%s,%s)'%(child, sibiling)
        return string
    
class Binary_search_tree:
    def __init__(self):
        self.root = None
        self.last_ptr = None
        self.ptr = self.root
        self.way = 'root'
    
    def insert(self, node):
        if type(node) in [int, float]:
            node = Node(node)
        
        if self.way == 'root':
            self.root = node
            self.way = 'right'
            
        elif not self.find(node.value):
            if self.way == 'right':
                self.last_ptr.sibiling = node
            elif self.way == 'left':
                self.last_ptr.child = node

    
    def find(self, value):
        self.last_ptr = None
        self.ptr = self.root
        self.way = 'right'
        while self.ptr != None:
            self.last_ptr = self.ptr
            if value > self.ptr.value:
                self.way = 'right'
                self.ptr = self.ptr.sibiling
            elif value < self.ptr.value:
                self.way = 'left'
                self.ptr = self.ptr.child
            else:
                return True
            
        else:
            return False
        
    def __repr__(self):
        return self.root.__repr__()
            
if __name__ == '__main__':
    data = [43,122,4,64,34,1,76,5,76,36,95,23,42,44,86,56,26]
    search_tree = Binary_search_tree()
    for i in data:
        search_tree.insert(i)
        
    find_list = [123,43,46,87,23,34,74,13,32,26]
    for i in find_list:
        print(search_tree.find(i))
    
                
            
