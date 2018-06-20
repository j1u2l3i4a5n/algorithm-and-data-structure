# -*- coding: utf-8 -*-
"""
@brief: heap implement (smaller is more prior)
@time: Created on Thu Jun 14 14:46:49 2018

@author: hrlin
"""

class Node:
    def __init__(self, value):
        self.value = value
        self.ptr = []
        
    def __repr__(self):
        string = str(self.value)
        for i in self.ptr:
            string += ' (%s)'%i.__repr__()
        return string
    
class Binominal_tree:
    def __init__(self, node):
        self.size = 0
        self.root = node
    
    def union(self, other):
        if self.size == other.size:
            if self.root.value > other.root.value:
                other.root.ptr.append(self.root)
                self.root = other.root
                self.size += 1
                
            else:
                self.root.ptr.append(other.root)
                self.size += 1
        
    def __repr__(self):
        return str(self.root.value)

class Binominal_heap:
    def __init__(self):
        self.chain = []
    
    def union(self, other):
        i = 0
        j = 0
        
        while i < len(self.chain) and j < len(other.chain):
            i_digit = self.chain[i].size
            j_digit = other.chain[j].size            
            if i_digit > j_digit:
                self.chain.insert(i, other.chain[j])
                j += 1
                
            elif i_digit < j_digit:
                i += 1
                
            else:
                keep = other.chain[j]
                while i < len(self.chain) and self.chain[i].size == keep.size:
                    self.chain[i].union(keep)
                    keep = self.chain[i]
                    del self.chain[i]
                self.chain.insert(i, keep)
                del keep
                i += 1
                j += 1
                
        self.chain += other.chain[j:]
        
    def insert(self, value):
        other = Binominal_heap()
        node = Node(value)
        binominal_tree = Binominal_tree(node)
        other.chain.append(binominal_tree)
        self.union(other)
        
    def delete_minimum(self):
        index = 0
        for i in range(len(self.chain)):
            if self.chain[i].root.value < self.chain[index].root.value:
                index = i
        rm = self.chain[index].root
        del self.chain[index]
        for i in rm.ptr:
            heap = Binominal_heap()
            heap.chain.append(Binominal_tree(i))
            self.union(heap)
        
        return rm.value
    
    def __repr__(self):
        chain = []
        for i in self.chain:
            chain.append(i.__repr__())
            
        return str(chain)
    
if __name__ == '__main__':
    data = [34,23,76,4,38,5,13,54,75,43,12,84,39,10]
    heap = Binominal_heap()
    for i in data:
        heap.insert(i)
        string = ''
        for j in heap.chain:
            string += ' ' + str(j.size)

    for i in range(len(data)):
        print(heap.delete_minimum())
    