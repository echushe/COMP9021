import sys

from array import *
from math import *


class StackItem:
    def __init__(self, index, value, depth, the_sum):
        self.index = index
        self.value = value
        self.depth = depth
        self.the_sum = the_sum



class MyGlobals:
    max_sum = 0
    first_max_path = []
    amount_of_max_paths = 0


def ReadTriangleFromFile (file_name):

    try:
        with open(file_name, 'r') as myfile:
            str_list = myfile.readlines()

            amount_of_rows = len(str_list)
            array_length = (1 + amount_of_rows) * amount_of_rows // 2
            triangle = {}

            #read string data into triangle of integers
            depth = 0
            for str_item in str_list:
                str_numbers = str_item.split()

                index = 0
                for str_number in str_numbers:

                    # data in file should be triangle
                    if index > depth:
                        raise ValueError

                    try:
                        triangle[(depth * (depth + 1) // 2) + index] = int(str_number)
                    except ValueError:
                        print('Incorrect data in file, giving up.')
                        sys.exit()
                    index += 1

                # data in file should be triangle
                if index <= depth:
                    raise ValueError

                depth += 1

    except IOError:
        print('Incorrect file name or file not found, giving up.')
        sys.exit()

    return triangle

def isqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def Index2Depth(index):
    return int((isqrt(1 + 8 * index) - 1) // 2)


def PrintTriangle(triangle):

    depth = 0
    for i in range(0, len(triangle)):
        if  Index2Depth(i) > depth:
            depth += 1
            print('')
        print(triangle[i], end = "")
        print(' ', end = "")

    print('')



# Simpler implementation of recursion, probable stack overflow if the triangle is too large
def Paths(triangle, index, depth, entire_depth, the_sum, path):

    #if index == 0:
    #    max_sum = 0
    #    max_paths = []

    the_sum += triangle[index]
    path.append(triangle[index])
    
    if depth < entire_depth:
        #go to left
        Paths(triangle, index + depth + 1, depth + 1, entire_depth, the_sum, path)

        #go to right
        Paths(triangle, index + depth + 2, depth + 1, entire_depth, the_sum, path)
    else:
        
        if the_sum > MyGlobals.max_sum:
            path_copy = list(path)
            MyGlobals.max_sum = the_sum          
            MyGlobals.first_max_path = path_copy
            MyGlobals.amount_of_max_paths = 1
            
        elif the_sum == MyGlobals.max_sum:
            MyGlobals.amount_of_max_paths += 1
            
        else:
            pass

    path.pop()


# The logic of how to go to the next node of triangle is implemented here
def VisitNextElement(triangle, triangle_visit_mark, stack, entire_depth):

    if len(stack) > 0:
        current = stack[-1]

        left_index = current.index + current.depth + 1
        right_index = current.index + current.depth + 2

        # if this node was already visited
        if triangle_visit_mark[current.index] == 1:
            # if left sub node is not visited
            if triangle_visit_mark[left_index] == 0:
                stack.append(StackItem(left_index, triangle[left_index], current.depth + 1, current.the_sum + triangle[left_index]))

            # if left sub node was visited but right node is not visited
            elif triangle_visit_mark[right_index] == 0:
                stack.append(StackItem(right_index, triangle[right_index], current.depth + 1, current.the_sum + triangle[right_index]))

            # if both sub nodes were visited
            else:
                triangle_visit_mark[left_index] = 0
                triangle_visit_mark[right_index] = 0
                stack.pop()

        # if this node is not visited
        else:
            triangle_visit_mark[current.index] = 1

            # if this node is at bottom row  
            if len(stack) == entire_depth + 1:
            
                if current.the_sum > MyGlobals.max_sum:
                    path_copy = []
                    for stack_item in stack:
                        path_copy.append(stack_item.value)
                        
                    MyGlobals.max_sum = current.the_sum 
                    MyGlobals.first_max_path = path_copy
                    MyGlobals.amount_of_max_paths = 1
                    
                elif current.the_sum == MyGlobals.max_sum:
                    MyGlobals.amount_of_max_paths += 1
                    
                else:
                    pass
                
                stack.pop()

    
        
    
# using loop to implement recurion to get rid of stack overflow
##
def Paths_Loop(triangle):

    triangle_visit_mark = {}

    for key, value in triangle.items():
        triangle_visit_mark[key] = 0
    
    stack = []
    stack.append(StackItem(0, triangle[0], 0, triangle[0]))
    
    entire_depth = Index2Depth(len(triangle) - 1)
    
    while len(stack) > 0:
        VisitNextElement(triangle, triangle_visit_mark, stack, entire_depth )      




if __name__ == '__main__':

    file_name = input('Which data file do you want to use? ')
    
    the_triangle = ReadTriangleFromFile(file_name)

    #PrintTriangle(the_triangle)

    #start_path = []
    #Paths(the_triangle, 0, 0, Index2Depth(len(the_triangle) - 1), 0, start_path)

    Paths_Loop(the_triangle)

    print('The largest sum is: {0}'.format(MyGlobals.max_sum))

    
    print('The number of paths yielding this sum is: {0}'.format(MyGlobals.amount_of_max_paths))


    print('The leftmost path yielding this sum is: {0}'.format(MyGlobals.first_max_path))

    #for path in all_paths:
    #    print(path)


        
