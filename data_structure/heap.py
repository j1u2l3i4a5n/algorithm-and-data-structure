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
    
class Skew_heap:
    def __init__(self):
        self.null_path_len = 0
        self.root = None
        
    def merge(self, other):
        ptr_self = self.root
        ptr_other = other.root
        stack = []
        if ptr_self ==  None:
            last_ptr = True
        else:
            last_ptr = False

        while ptr_self != None and ptr_other != None:
            if ptr_self.value < ptr_other.value:
                tmp = ptr_self.ptr[1]
                ptr_self.ptr[1] = None
                stack.append(ptr_self)
                ptr_self = tmp
                last_ptr = True
                
            else:
                
                tmp = ptr_other.ptr[1]
                ptr_other.ptr[1] = None
                stack.append(ptr_other)
                ptr_other = tmp
                last_ptr = False
               
        if last_ptr:
            current = ptr_other
        else:
            current = ptr_self
        
        for i in range(len(stack)):
            out = stack.pop()
            out.ptr[1] = current
            current = out
            current.ptr[0], current.ptr[1] = current.ptr[1], current.ptr[0]
            
        self.root = current
                
        
    def __repr__(self):
        current = self.root
        right_path = ''
        while current != None:
            right_path += '%d '%current.value
            current = current.ptr[1]
        return right_path
            
    def delete_minimum(self):
        a = self.root.ptr[0]
        b = self.root.ptr[1]
        other = Skew_heap()
        minimum = self.root.value
        if b == None:
            self.root = a
            
        elif a == None or (a.value < b.value):
            self.root = a
            other.root = b
            
        else:
            self.root = b
            other.root = a
            
        self.merge(other)

        return minimum
        
class Binary_heap:
    def __init__(self):
        self.list = []
    
    def balence(self):
        for i in range(len(self.list)-1, -1, -1):
            if self.list[i] < self.list[int(i / 2)]:
                self.list[i], self.list[int(i / 2)] = self.list[int(i / 2)], self.list[i]
        
    def insert(self, value):
        self.list.append(value)
        self.balence()
    
    def delete_minimum(self):
        self.list[0], self.list[-1] = self.list[-1], self.list[0]
        value = self.list.pop()
        self.balence()
        return value
    
    def __repr__(self):
        return str(self.list)
    
class Fibonacii_heap(Binominal_heap):
    def __init__(self):
        self.min = 0
        self.chain = []
        
    def insert(self, value):
        self.chain.append(Binominal_tree(Node(value)))
        if value < self.chain[self.min].root.value:
            self.min = len(self.chain) - 1
        
    def union(self, other):
        if self.chain[self.min] > other.chain[other.min]:
            self.min = len(self.chain) + other.min
        self.chain += other.chain
        
    def delete_minimum(self):
        minimum = self.chain[self.min].root
        
        for i in range(len(minimum.ptr)):
            tmp = Binominal_tree(minimum.ptr[i])
            tmp.size = i
            
            self.chain.append(tmp)
        
        del self.chain[self.min]
        
        bit_list = []
        
        while len(self.chain) != 0:
            j = 0
            tmp = self.chain.pop(0)
            if len(bit_list) == 0:
                bit_list.append(tmp)
            else:
                while j < len(bit_list):
                    if tmp.size == bit_list[j].size:
                        tmp.union(bit_list[j])
                        self.chain.append(tmp)
                        del bit_list[j]
                        break
                
                    elif tmp.size < bit_list[j].size:
                        bit_list.insert(j, tmp)
                        break
                    j += 1
                else:
                    bit_list.append(tmp)
        
        self.min = 0
        self.chain = bit_list    
        for i in range(1, len(self.chain)):
            if self.chain[i].root.value < self.chain[self.min].root.value:
                self.min = i
        return minimum.value
    
    def __repr__(self):
        return str(self.chain)
    
    
if __name__ == '__main__':
    data = [34,23,76,4,38,5,13,54,75,43,12,84,39,10]
    heap = Fibonacii_heap()
    for i in data:
        heap.insert(i)

    
    for i in range(len(data)):
        print(heap.delete_minimum())
    