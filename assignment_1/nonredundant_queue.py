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



class QueueItem:
    def __init__(self, node, parent_node, depth):
        self.node = node
        self.depth = depth
        self.parent_node = parent_node


class GraphVisitQueue:
    def __init__(self):
        self.queue = deque()
        self.dict = {}

    def append(self, queue_item):
        self.queue.append(queue_item)
        self.dict[queue_item.node.number] = queue_item
        

    def popleft(self):
        queue_item = self.queue.popleft()
        del self.dict[queue_item.node.number]
        
        return queue_item

    def get_item_by_key(self, number):
        if number in self.dict:
            queue_item = self.dict[number]
        return queue_item


    def has_key(self, number):
        return number in self.dict

    def length(self):
        return len(self.queue)

    def top_item(self):
        return self.queue[0]

    def print_me(self):
        for queue_item in self.queue:
            print('({0},{1})'.format(queue_item.node.number, queue_item.depth), end=' ')
        print('')


    def extend(self, queue):
        for i in range(len(queue.queue)):
            self.append(queue.queue[i])

    def remove(self, queue_item):
        self.queue.remove(queue_item)
        del self.dict[queue_item.node.number]



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
            #create all upstream nodes
            self.all_nodes[b].up[a] = self.all_nodes[a]

        #All nodes without upstream
        for (number, node) in self.all_nodes.items():
            if(len(node.up) == 0):
                self.top_nodes[node.number] = node



    #Visit next node
    def VisitNextNode(self, queue, junk_queue):

        #queue.print_me()
        
        if queue.length() > 0:
            current_queue_item = queue.popleft()
            current_node = current_queue_item.node
            junk_queue.append(current_queue_item)


            for (number, node) in current_node.down.items():
                if queue.has_key(number):
                    existing_item = queue.get_item_by_key(number)
                    if existing_item.depth == 1 and current_queue_item.depth >= 1:
                        redundant_offspring = existing_item.node
                        #print('Redundant edge: R({0},{1})'.format(existing_item.parent_node.number, redundant_offspring.number))
                        del existing_item.parent_node.down[redundant_offspring.number]
                        del redundant_offspring.up[existing_item.parent_node.number]

                    queue.remove(existing_item)
            
                elif junk_queue.has_key(number):
                    existing_item = junk_queue.get_item_by_key(number)
                    if existing_item.depth == 1 and current_queue_item.depth >= 1:
                        redundant_offspring = existing_item.node
                        #print('Redundant edge: R({0},{1})'.format(existing_item.parent_node.number, redundant_offspring.number))
                        del existing_item.parent_node.down[redundant_offspring.number]
                        del redundant_offspring.up[existing_item.parent_node.number]
                
                    junk_queue.remove(existing_item)
           
                queue.append(QueueItem(node, current_node, current_queue_item.depth + 1))
            return current_queue_item
        else:
            return 0             




    def CleanUpRedundancy(self, root):

        junk_queue = GraphVisitQueue()
        queue = GraphVisitQueue()
        queue.append(QueueItem(root, 0, 0))

        while queue.length() > 0:
            self.VisitNextNode(queue, junk_queue)



    def CleanUpAllRedundancy(self):

        for (number, node) in self.all_nodes.items():
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
    input('')


        
