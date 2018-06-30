# -*- coding: utf-8 -*-
"""
@brief: tree implement  
@time: Created on Fri Jun 22 16:22:06 2018

@author: hrlin
"""

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 0
        
    def __repr__(self):
        string = str(self.value)
        left = 'None'
        right = 'None'
        if self.left != None:
            left = self.left.__repr__()
        if self.right != None:
            right = self.right.__repr__()
        string += '(%s,%s)'%(left, right)
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
                self.last_ptr.right = node
            elif self.way == 'left':
                self.last_ptr.left = node

    
    def find(self, value):
        self.last_ptr = None
        self.ptr = self.root
        self.way = 'right'
        while self.ptr != None:
            self.last_ptr = self.ptr
            if value > self.ptr.value:
                self.way = 'right'
                self.ptr = self.ptr.right
            elif value < self.ptr.value:
                self.way = 'left'
                self.ptr = self.ptr.left
            else:
                return True
            
        else:
            return False
        
    def __repr__(self):
        return self.root.__repr__()
        
    
class AVL_tree(Binary_search_tree):
    def __init__(self):
        pass
        
    def insert(self, node):
        pass
        
        
class Splay_tree(Binary_search_tree):
    def __init__(self):
        Binary_search_tree.__init__(self)      
        
          
            
    def R_rotate(self):
        self.left_ptr.right = self.path[0]
        self.left_ptr = self.left_ptr.right
        
    def L_rotate(self):
        self.right_ptr.left = self.path[0]
        self.right_ptr = self.right_ptr.left
        
    def LL_rotate(self):
        self.path[0].left = self.path[1].right
        self.path[1].right = self.path[0]
        self.path[1].left = None
        self.right_ptr.left = self.path[1]
        self.right_ptr = self.right_ptr.left
        print('LL')
        
    def RR_rotate(self):
        self.path[0].right = self.path[1].left
        self.path[1].left = self.path[0]
        self.path[1].right = None
        self.left_ptr.right = self.path[1]
        self.left_ptr = self.left_ptr.right
        print('RR')
        
    def LR_rotate(self):
        self.left_ptr.right = self.path[1]                  
        self.right_ptr.left = self.path[0]
        self.path[0].left = None
        self.path[1].right = None
        self.left_ptr = self.left_ptr.right
        self.right_ptr = self.right_ptr.left
        print('LR')
        
    def RL_rotate(self):
        self.right_ptr.left = self.path[1]   
        self.left_ptr.right = self.path[0]
        self.path[1].left = None
        self.path[0].right = None
        self.left_ptr = self.left_ptr.right
        self.right_ptr = self.right_ptr.left                
        print('RL')

    def splay(self, value, insert = False):
        self.last_ptr = None
        self.ptr = self.root
        self.splay_left = Node(None)
        self.splay_right = Node(None)
        self.way = 'right'
        self.double_way = None
        self.left_ptr = self.splay_left
        self.right_ptr = self.splay_right
        self.path = []
        
        while self.ptr != None:
            self.last_ptr = self.ptr
            
            if value == self.ptr.value:
                if len(self.path) == 1:
                    if self.way == 'right':
                        self.R_rotate()
                    else:
                        self.L_rotate()                    
                        
                self.path = []
                
                self.left_ptr.right = self.ptr.left
                self.right_ptr.left = self.ptr.right
                self.ptr.left = self.splay_left.right
                self.ptr.right = self.splay_right.left
                self.root = self.ptr

                return True
            
            elif value > self.ptr.value:
                self.double_way = self.way
                self.way = 'right'
                self.ptr = self.ptr.right
                
            elif value < self.ptr.value:
                self.double_way = self.way
                self.way = 'left'
                self.ptr = self.ptr.left
            self.path.append(self.last_ptr)
            
            if len(self.path) == 2:
                if self.double_way == 'left' and self.way == 'right':
                    self.LR_rotate()
                    
                elif self.double_way == 'right' and self.way == 'left':
                    self.RL_rotate()

                elif self.double_way == 'left' and self.way == 'left':
                    self.LL_rotate()
                    
                elif self.double_way == 'right' and self.way == 'right':
                    self.RR_rotate()

                self.path = []
                

                
        else:
            if len(self.path) == 1:
                if self.way == 'right':
                    self.R_rotate()
                else:
                    self.L_rotate()
            
            try:
                self.left_ptr.right = self.ptr.left
                self.right_ptr.left = self.ptr.right
            except:
                pass
            if insert:
                node = Node(value)
            else:
                node = Node(self.last_ptr.value)
                del self.last_ptr
            self.root = node
            self.root.left = self.splay_left.right
            self.root.right = self.splay_right.left                
            print(self.root)  
            return False
              
    def __repr__(self):
        return self.root.__repr__()
        
        
if __name__ == '__main__':
    data = [43,122,4,64,34,1,76,5,76,36,95,23,42,44,86,56,26]
    search_tree = Splay_tree()
    
    for i in data:
        search_tree.insert(i)
        
    
    a = [1,3,4,5,6,7,923,43]
    for i in a:
        print(search_tree.find(i))
    