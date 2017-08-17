import re
import sys
from collections import *
from math import *
import datetime
import time


class Node:
    def __init__(self, number):
        self.number = number
        self.down = {}
        self.up = {}
        self.down_not_visited = {}
        self.being_visited = False


##class Destination:
##    def __init__(self, end, distance):
##        self.end = end
##        self.distance = distance


class StackItem:
    def __init__(self, node):
        self.node = node
        self.index = 0


class GraphVisitStack:
    def __init__(self):
        self.stack = []
        self.dict = {}

    def append(self, stack_item):
        stack_item.index = len(self.stack)
        self.stack.append(stack_item)
        self.dict[stack_item.node.number] = stack_item
        

    def pop(self):
        stack_item = self.stack.pop()
        del self.dict[stack_item.node.number]
        
        return stack_item

    def at(i):
        return self.stack[i]

    def get_node_by_key(self, number):
        if number in self.dict:
            stack_item = self.dict[number]
        return stack_item.node

    def has_key(self, number):
        return number in self.dict

    def length(self):
        return len(self.stack)

    def top_item(self):
        return self.stack[-1]

    def print_me(self):
        for stack_item in self.stack:
            print(stack_item.node.number, end=' ')
        print('')

    def get_sub_stack_from_key(self, number):
        sub_stack = GraphVisitStack()
        if number in self.dict:
            stack_item = self.dict[number]
            for i in range(stack_item.index, len(self.stack)):
                sub_stack.append(self.stack[i])

        return sub_stack

    def extend(self, stack):
        for i in range(len(stack.stack)):
            self.append(stack.stack[i])



def ReadOrdersFromFile (file_name):

    orders = []

    try:
        with open(file_name, 'r') as myfile:
            str_list = myfile.readlines()

            for str_item in str_list:

                try:
                    match = re.search('[\s]*R[\s]*\([\s]*([^\s]*)[\s]*,[\s]*([^\s]*)[\s]*\)[\s]*', str_item)
                    if match:
                        left = int(match.group(1))
                        right = int(match.group(2))

                        orders.append((left, right))
                    else:
                        raise ValueError
                except ValueError:
                    print('Incorrect data in file, giving up.')
                    sys.exit()

    except IOError:
        print('Incorrect file name or file not found, giving up.')
        sys.exit()

    return orders

class Graph:
    
    #generate graph from partial pairs
    def __init__(self, orders):

        self.all_nodes = {}
        self.top_nodes = {}
        self.stack = GraphVisitStack()

        #Create all graph nodes
        for (a, b) in orders:
            if not a in self.all_nodes:
                self.all_nodes[a] = Node(a)
            if not b in self.all_nodes:
                self.all_nodes[b] = Node(b)

        #Create connections of all graph nodes
        for (a, b) in orders:
            #create all downstream nodes
            self.all_nodes[a].down[b] = self.all_nodes[b]
            self.all_nodes[a].down_not_visited[b] = self.all_nodes[b]
            #create all upstream nodes
            self.all_nodes[b].up[a] = self.all_nodes[a]

        #All nodes without upstream
        for (number, node) in self.all_nodes.items():
            if(len(node.up) == 0):
                self.top_nodes[node.number] = node



    #Visit next node
    def VisitNextNode(self):

        stack = self.stack
        
        if stack.length() > 0:
            current_node = stack.top_item().node
        else:
            return

        #stack.print_me()

        if not current_node.being_visited:
            top_stack_item = stack.pop()
            if stack.length() > 0:
                up_to_del = []
                for (number, up_node) in current_node.up.items():
                    # print('Checking R({0},{1})'.format(number, current_node.number))
                    # this direct parent node is not previous parent node visited
                    # but was visited long long ago
                    if (stack.top_item().node.number != number and stack.has_key(number)):
                        #print('R({0},{1}) is redundant.'.format(number, current_node.number))
                        del up_node.down[current_node.number]
                        if current_node.number in up_node.down_not_visited:
                            del up_node.down_not_visited[current_node.number]
                        up_to_del.append(number)

                for number in up_to_del:
                    del current_node.up[number]

            stack.append(top_stack_item)

            current_node.being_visited = True

        else:            
            #there is no sub nodes here
            if len(current_node.down) == 0:
                current_node.being_visited = False
                stack.pop()
            #there are sub nodes here
            else:
                if len(current_node.down_not_visited) == 0:
                    for (number, sub_node) in current_node.down.items():
                        current_node.down_not_visited[number] = sub_node

                    current_node.being_visited = False
                    stack.pop()
                    
                #there is(are) unvisited subnode(s)
                else:
                    (number, sub_node) = current_node.down_not_visited.popitem()
                    stack.append(StackItem(sub_node))
                        




    def CleanUpRedundancy(self, root):

        self.stack.append(StackItem(root))

        while self.stack.length() > 0:
            self.VisitNextNode()


    def CleanUpAllRedundancy(self):
        for (number, node) in self.top_nodes.items():
            #print('From: {0}'.format(number))
            self.CleanUpRedundancy(node)


##    def PrintAllDestinations(dest):
##        for (number, dest_item) in dest.items():
##            print('Destination: {0}  Distance: {1}'.format(dest_item.end, dest_item.distance))


    def PrintAllEdges(self):
        for (a, node) in self.all_nodes.items():
            for (b, sub_node) in node.down.items():
                print('R({0},{1})'.format(a, b))

    def PrintAllEdgesAsInputSequence(self, orders):
        for (a, b) in orders:
            if a in self.all_nodes:
                node = self.all_nodes[a]
                if b in node.down:
                    print('R({0},{1})'.format(a, b))
                

if __name__ == '__main__':

    file_name = input('Which data file do you want to use? ')
        
    orders = ReadOrdersFromFile(file_name)

    #for (a, b) in orders:
    ##   print('R({0},{1})'.format(a, b))
       
    print('The nonredundant facts are: ')

    the_graph = Graph(orders)

    #t1 = datetime.datetime.now()

    the_graph.CleanUpAllRedundancy()

    #t2 = datetime.datetime.now()
    
    #PrintAllEdges(all_nodes)
    the_graph.PrintAllEdgesAsInputSequence(orders)

    #print(t2 - t1)


        
