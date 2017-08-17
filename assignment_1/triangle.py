import sys

from array import *
from math import *


class TriangleItem:
    def __init__(self, value):
        self.value = value
        self.left_route = []
        self.all_routes = 0
        self.max_sum = 0



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

                i = 0
                for str_number in str_numbers:

                    # data in file should be triangle
                    if i > depth:
                        raise ValueError

                    try:
                        item = TriangleItem(int(str_number))
                        triangle[(depth * (depth + 1) // 2) + i] = item
                    except ValueError:
                        print('Incorrect data in file, giving up.')
                        sys.exit()
                    i += 1

                # data in file should be triangle
                if i <= depth:
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
        print(triangle[i].value, end = "")
        print(' ', end = "")

    print('')



def ScanRow(depth, triangle):
    
    for i in range(depth + 1):
        index = (depth * (depth + 1) // 2) + i 

        if depth < Index2Depth(len(triangle) - 1):

            sub_left_index = ((depth + 1) * (depth + 2) // 2) + i
            sub_right_index = ((depth + 1) * (depth + 2) // 2) + i + 1
            
            left_sub_max_sum = triangle[sub_left_index].max_sum
            right_sub_max_sum = triangle[sub_right_index].max_sum

            if left_sub_max_sum > right_sub_max_sum:
                triangle[index].max_sum = triangle[index].value + left_sub_max_sum
                triangle[index].left_route.append(triangle[index].value)
                triangle[index].left_route.extend(triangle[sub_left_index].left_route)
                triangle[index].all_routes = triangle[sub_left_index].all_routes

            elif left_sub_max_sum < right_sub_max_sum:
                triangle[index].max_sum = triangle[index].value + right_sub_max_sum
                triangle[index].left_route.append(triangle[index].value)
                triangle[index].left_route.extend(triangle[sub_right_index].left_route)
                triangle[index].all_routes = triangle[sub_right_index].all_routes    
                                
            else:
                triangle[index].max_sum = triangle[index].value + left_sub_max_sum
                triangle[index].left_route.append(triangle[index].value)
                triangle[index].left_route.extend(triangle[sub_left_index].left_route)
                triangle[index].all_routes = triangle[sub_left_index].all_routes + triangle[sub_right_index].all_routes

            #print(triangle[index].left_route)
        else:
            triangle[index].max_sum = triangle[index].value

            triangle[index].left_route.append(triangle[index].value)
            triangle[index].all_routes += 1
            
            #print(triangle[index].left_route)



def SearchLeftMaxPath(triangle):

    depth = Index2Depth(len(triangle) - 1)
    
    while depth >= 0:
        ScanRow(depth, triangle)
        depth -= 1

    left_max_path = triangle[0].left_route
    amount_of_max_paths = triangle[0].all_routes

    return (triangle[0].max_sum, amount_of_max_paths, left_max_path)
        
            

if __name__ == '__main__':


    file_name = input('Which data file do you want to use? ')
    
    the_triangle = ReadTriangleFromFile(file_name)

    #PrintTriangle(the_triangle)

    (max_sum, amount_of_max_paths, left_max_path) = SearchLeftMaxPath(the_triangle)

    print('The largest sum is: {0}'.format(max_sum))

    
    print('The number of paths yielding this sum is: {0}'.format(amount_of_max_paths))


    print('The leftmost path yielding this sum is: {0}'.format(left_max_path))

    #for path in all_paths:
    #    print(path)

    






