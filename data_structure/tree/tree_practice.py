# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 10:30:00 2018

@author: rjlin
"""
import sys

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        

class Binary_tree:
    def __init__(self):
        self.tree = None
        
    def insert(self, value):
        if self.tree == None:
            self.tree = Node(value)
        else:
            ptr = self.tree
            last = None
            while ptr != None:
                last = ptr
                if value > ptr.value:
                    ptr = ptr.right
                else:
                    ptr = ptr.left
                    
            if value > last.value:
                last.right = Node(value) 
            else:
                last.left = Node(value)
    
    def inorder(self, tree):
        data = []
        if tree != None:
            data += self.inorder(tree.left)
            data.append(tree.value)
            data += self.inorder(tree.right)

        return data

    def preorder(self, tree):
        data = []
        if tree != None:
            data.append(tree.value)
            data += self.preorder(tree.left)
            data += self.preorder(tree.right)
        else:
            data.append('-')
        return data
        
    def levelorder(self, tree):
        data = []
        queue = [tree]
        while len(queue) != 0:
            node = queue.pop(0)
            data.append(node.value)
            if node.left != None:    
                queue.append(node.left)
            if node.right != None:
                queue.append(node.right)
        return data

    def level(self, tree):
        data = []
        depth = []
        queue1 = [tree]
        queue2 = []
        while len(queue1) != 0:
            node = queue1.pop()
            depth.append(node.value)
            if node.left != None:
                queue2.append(node.left)
            if node.right != None:
                queue2.append(node.right)
            if len(queue1) == 0:
                queue1, queue2 = queue2, queue1
                data.append(depth)
                depth = []
        return data
    
    def __repr__(self):
        stack = []
        order = self.preorder(self.tree)
        for i in order:
            stack.append(i)
            while len(stack) >= 2 and type(stack[-1]) == str and type(stack[-2]) == str:
                right = stack.pop()
                left = stack.pop()
                parent = stack.pop()
                if right == '-' and left == '-':
                    stack.append(str(parent)) 
                elif left[-1] == ')' and right != '-':
                    stack.append('%d(%s%s)'%(parent, left, right))
                else:
                    stack.append('%d(%s %s)'%(parent, left, right))
                    
        return stack[0]
    
    def graph(self):
        coordinate = {}
        inorder = self.inorder(self.tree)
        level = self.level(self.tree)
        for i in range(len(inorder)):     
            if inorder[i] in coordinate:
                coordinate[inorder[i]][1] = i
            else:
                coordinate[inorder[i]] = [None, i]
            
        for i in range(len(level)):
            for j in level[i]:
                coordinate[j][0] = i
                          
            
        data = []
        for i in coordinate:
            data.append((coordinate[i][0], coordinate[i][1],i))
        data = sorted(data)
        
        return data
                
def read_file(filename):
    with open(filename, 'r') as files:
        data = files.read()
        data = data.split('\n')
        if data[-1] == '':
            data.pop()
        for i in range(len(data)):
            data[i] = data[i].split(' ')
            if data[i][-1] == '':
                data[i].pop()
            for j in range(len(data[i])):
                data[i][j] = int(data[i][j])
        return data
    
def write_file(data):
    parenthesis = ''
    textual = ''
    left = ''
    for i in data:
        parenthesis += '%s\n'%(i.__repr__())
    
        graph = i.graph()
        
        current = -1
        last = 0
        for i in graph:
            if i[0] == current:
                textual += '  '*(i[1] - last - 1) + str(i[2])
            else:
                current = i[0]
                textual += '\n%s%d'%('  '*i[1], i[2])
                left += '%d '%i[2]
                
            last = i[1]
        left += '\n'
        textual += '\n'
    textual = textual[1:]
    
    with open('parenthesis_representation.txt', 'w') as files:
        files.write(parenthesis)
    
    with open('textual_printing.txt', 'w') as files:
        files.write(textual)
    
    with open('left_boundary.txt', 'w') as files:
        files.write(left)
                
if __name__ == '__main__':
    filename = 'tree.txt'#sys.argv[1]
    data = read_file(filename)
    test = []
    for i in data:
        tree = Binary_tree()
        for j in i:
            tree.insert(j)
        test.append(tree)
    write_file(test)
    