##############################################################
#
#            COMP9021 Assignment 2
#            Written by Chunnan Sheng
#            Student Code: z5100764
#
#-------------------------------------------------------- 
#    Examples of how to run this program:
#    python3 maze.py --file filename.txt 
#    python3 maze.py -print --file filename.txt
#
#    Examples of how to generate a maze:
#    python3 maze.py --generate 20:30:0
#    python3 maze.py -print --generate 20:30:0
#--------------------------------------------------------
##############################################################


import sys
import re
import datetime
from random import *


#----------------------------------------------
#       A cell of this maze
#----------------------------------------------
class MazeNode:
    def __init__(self):
        self.dir = {(-1, 0):1, (0, 1):1, (1, 0):1, (0, -1):1}
        self.visited = False
        #These directions will be depleted by visit
        self.uv_dir = {(-1, 0):1, (0, 1):1, (1, 0):1, (0, -1):1}
        self.belongs_to_cul_de_sacs = False
        
        self.rand_dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
    def unvisit(self):
        self.visited = False
        self.uv_dir = {(-1, 0):1, (0, 1):1, (1, 0):1, (0, -1):1}
        
    def get_num_of_walls(self):
        count = 0
        for ((i, j), k) in self.dir.items():
            if not k:
                count += 1
        return count
        
    def connect_top(self):
        self.dir[(-1, 0)] = 1
        
    def connect_right(self):
        self.dir[(0, 1)] = 1
        
    def connect_bellow(self):
        self.dir[(1, 0)] = 1
        
    def connect_left(self):
        self.dir[(0, -1)] = 1
        
    def block_top(self):
        self.dir[(-1, 0)] = 0
        
    def block_right(self):
        self.dir[(0, 1)] = 0
        
    def block_bellow(self):
        self.dir[(1, 0)] = 0
        
    def block_left(self):
        self.dir[(0, -1)] = 0
    
    def is_totally_free(self):
        result = True
        for ((i, j), k) in self.dir.items():
            if not k:
                result = False
                break
        return result
        
#----------------------------------------------
#       A cell of wall intersections
#----------------------------------------------
class WallPoint:
    def __init__(self):
        self.dir = {(-1, 0):0, (0, 1):0, (1, 0):0, (0, -1):0}
        self.visited = False
        #These directions will be depleted by visit
        self.uv_dir = {(-1, 0):1, (0, 1):1, (1, 0):1, (0, -1):1}
        
    def unvisit(self):
        self.visited = False
        self.uv_dir = {(-1, 0):1, (0, 1):1, (1, 0):1, (0, -1):1}
        
    def get_num_of_wall_connections(self):
        count = 0
        for ((i, j), k) in self.dir.items():
            if k:
                count += 1
        return count
        
    def connect_top(self):
        self.dir[(-1, 0)] = 1
        
    def connect_right(self):
        self.dir[(0, 1)] = 1
        
    def connect_bellow(self):
        self.dir[(1, 0)] = 1
        
    def connect_left(self):
        self.dir[(0, -1)] = 1
        
    def block_top(self):
        self.dir[(-1, 0)] = 0
        
    def block_right(self):
        self.dir[(0, 1)] = 0
        
    def block_bellow(self):
        self.dir[(1, 0)] = 0
        
    def block_left(self):
        self.dir[(0, -1)] = 0
        
    def is_in_wall(self):
        result = False
        for ((i, j), k) in self.dir.items():
            if k:
                result = True
                break
        return result
    

class Maze:

#####################################################
#        Functions initializing a maze randomly
#####################################################

#----------------------------------------------
#       Create a raw 2D digit matrix
#       For example:
#
#       3333332
#       3333332
#       3333332
#       3333332
#       1111110
#---------------------------------------------- 
    def __create_raw_digit_matrix(self, xdim, ydim):
    
        if xdim < 1 or ydim < 1:
            print('Incorrect input.')
            sys.exit()
            
        matrix = []
        for i in range(ydim + 1):
            matrix.append([])
            for j in range(xdim + 1):
                if i < ydim:
                    if j < xdim:
                        matrix[-1].append(3)
                    else:
                        matrix[-1].append(2)
                else:
                    if j < xdim:
                        matrix[-1].append(1)
                    else:
                        matrix[-1].append(0)
                                                
        return matrix

#--------------------------------------------------
#       Demolish a wall where you are coming from
#--------------------------------------------------    
    def __demolish_wall(self, row, col, prev_i, prev_j):
        
        if prev_i == -1 and prev_j == 0:
            self.matrix[row][col] -= 1
            self.h_wall_matrix[row][col] = 0
            
            self.wall_point_matrix[row][col].block_right()
            self.wall_point_matrix[row][col + 1].block_left()
            
            self.maze_point_matrix[row][col].connect_top()
            if row > 0:
                self.maze_point_matrix[row - 1][col].connect_bellow()
            
        elif prev_i == 0 and prev_j == 1:
            self.matrix[row][col + 1] -= 2
            self.v_wall_matrix[row][col + 1] = 0
            
            self.wall_point_matrix[row][col + 1].block_bellow()
            self.wall_point_matrix[row + 1][col + 1].block_top()
            
            self.maze_point_matrix[row][col].connect_right()
            if col < self.xdim - 1:
                self.maze_point_matrix[row][col + 1].connect_left()
            
        elif prev_i == 1 and prev_j == 0:
            self.matrix[row + 1][col] -= 1
            self.h_wall_matrix[row + 1][col] = 0
            
            self.wall_point_matrix[row + 1][col].block_right()
            self.wall_point_matrix[row + 1][col + 1].block_left()
            
            self.maze_point_matrix[row][col].connect_bellow()
            if row < self.ydim - 1:
                self.maze_point_matrix[row + 1][col].connect_top()
            
        elif prev_i == 0 and prev_j == -1:
            self.matrix[row][col] -= 2
            self.v_wall_matrix[row][col] = 0
            
            self.wall_point_matrix[row][col].block_bellow()
            self.wall_point_matrix[row + 1][col].block_top()
            
            self.maze_point_matrix[row][col].connect_left()
            if col > 0:
                self.maze_point_matrix[row][col - 1].connect_right()

#----------------------------------------------------------
#       Demolish a piece of outside wall of the maze
#----------------------------------------------------------
    def __demolish_outside_wall(self, row, col):
        if row == -1:
            self.matrix[0][col] -= 1
            self.h_wall_matrix[0][col] = 0
            
            self.wall_point_matrix[0][col].block_right()
            self.wall_point_matrix[0][col + 1].block_left()
            
            self.maze_point_matrix[0][col].connect_top()
        
        elif col == -1:
            self.matrix[row][0] -= 2
            self.v_wall_matrix[row][0] = 0
            
            self.wall_point_matrix[row][0].block_bellow()
            self.wall_point_matrix[row + 1][0].block_top()
            
            self.maze_point_matrix[row][0].connect_left()
        
        elif row == self.ydim:
            self.matrix[row][col] -= 1
            self.h_wall_matrix[row][col] = 0
            
            self.wall_point_matrix[row][col].block_right()
            self.wall_point_matrix[row][col + 1].block_left()
            
            self.maze_point_matrix[row - 1][col].connect_bellow()
            
        elif col == self.xdim:
            self.matrix[row][col] -= 2
            self.v_wall_matrix[row][col] = 0
            
            self.wall_point_matrix[row][col].block_bellow()
            self.wall_point_matrix[row + 1][col].block_top()
            
            self.maze_point_matrix[row][col - 1].connect_right()


#----------------------------------------------------------------------------------------------
#       One step of randomized version of deep first search algorithm
#---------------------------------------------------------------------------------------------- 
    def __demolish_wall_and_visit_next_maze_point(self, stack):
        if len(stack) == 0:
            return
            
        (row, col, prev_i, prev_j) = stack[-1]
        
        #print(stack)
        
        #you are right at the border of maze, so you are about to enter
        #or about to leave the maze --- or at the end of stack popping 
        if row == -1 or col == -1 or row == self.ydim or col == self.xdim:
            
            #you are about to leave this maze if the stack is larger than 2
            #if you are going out of this maze, it means you have finshed one
            #route in this maze which starts from one entry and ends at
            #another antry of this maze
            if len(stack) > 1:
                #finish making one route in the maze
                # -- it is not decided if I should demolish wall here
                stack.pop()

            #you are about to enter the maze
            else:
                i = 0
                j = 0
                if row == -1:
                    i = 1
                    j = 0
                elif row == self.ydim:
                    i = -1
                    j = 0
                elif col == -1:
                    i = 0
                    j = 1
                else:
                    i = 0
                    j = -1
                if self.start_visiting:
                    #unvisited area is candidate for wall demolishing
                    if not self.maze_point_matrix[row + i][col + j].visited:
                        stack.append((row + i, col + j, -i, -j))
                    
                    #this entry is already visited, it means this area was already accessed
                    else:
                        stack.pop()
                    
                    self.start_visiting = False
                #visiting process is about to finish (pop the last stack)
                else:
                    stack.pop()
                    
        #you are inside the maze, keep on going !!!!!
        else:
            current_point = self.maze_point_matrix[row][col]
            if not current_point.visited:
                current_point.visited = True
                #We should demolish the wall you are coming from first
                self.__demolish_wall(row, col, prev_i, prev_j)                
                #remove the direction coming from to prevent duplicate visit
                if (prev_i, prev_j) in current_point.uv_dir:
                    del current_point.uv_dir[(prev_i, prev_j)]
                
                #randomly select one direction that is available
                (i, j) = current_point.rand_dir[randint(0, 3)]
                while not (i, j) in current_point.uv_dir:
                    (i, j) = current_point.rand_dir[randint(0, 3)]                    
                del current_point.uv_dir[(i, j)]
                #Do not visit maze node that was already visited
                if not self.maze_point_matrix[row + i][col + j].visited:
                    stack.append((row + i, col + j, -i, -j))
            else:
                if len(current_point.uv_dir) > 0:
                    #There are unvisited directions for use in this node
                    #randomly select one direction that is available
                    (i, j) = current_point.rand_dir[randint(0, 3)]
                    while not (i, j) in current_point.uv_dir:
                        (i, j) = current_point.rand_dir[randint(0, 3)]                    
                    del current_point.uv_dir[(i, j)]
                    #Do not visit maze node that was already visited
                    if not self.maze_point_matrix[row + i][col + j].visited:
                        stack.append((row + i, col + j, -i, -j))
                else:
                    #Can not visit other nodes from this node
                    #because all sub nodes have been visited or
                    #there is no available sub node to visit
                    #pop the stack
                    
                    stack.pop()
    
#----------------------------------------------------------------------------------------------
#       Demolish walls of this maze using randomized version of deep first search algorithm
#       from a start point
#----------------------------------------------------------------------------------------------
    def __demolish_walls_start_from(self, row, col):
        self.start_visiting = True
    
        stack = []
        
        if row == -1:
            stack.append((row, col, -1, 0))
        elif row == self.ydim:
            stack.append((row, col, 1, 0))
        elif col == -1:
            stack.append((row, col, 0, -1))
        elif col == self.xdim:
            stack.append((row, col, 0, 1))
        else:
            stack.append((row, col, 0, 0))           
   
        while len(stack) > 0:
            self.__demolish_wall_and_visit_next_maze_point(stack)
            
#--------------------------------------------------------------------------------
#       Open an maze entry randomly
#-------------------------------------------------------------------------------- 
    def __open_entry(self):
        side = randrange(0, 4)
        
        row = None
        col = None
        
        if side == 0:
            row = -1
            col = randrange(0, self.xdim)
        elif side == 1:
            row = randrange(0, self.ydim)
            col = self.xdim
        elif side == 2:
            row = self.ydim
            col = randrange(0, self.xdim)
        else:
            row = randrange(0, self.ydim)
            col = -1
            
        return (row, col)

#--------------------------------------------------------------------------------
#       Randomly generate 2 entries for this maze
#       And demolish walls randomly to generate a maze
#--------------------------------------------------------------------------------           
    def demolish_walls(self, the_seed):        
        #clear data of maze visiting
        for i in range(self.ydim + 1):
            for j in range(self.xdim + 1):
                self.maze_point_matrix[i][j].unvisit()
        
        seed(the_seed)
        row = randrange(0, self.ydim)
        col = randrange(0, self.xdim)
        self.__demolish_walls_start_from(row, col)
        
        (r1, c1) = self.__open_entry()
        self.__demolish_outside_wall(r1, c1)
            
        (r2, c2) = self.__open_entry()
        while r2 == r1 and c2 == c1:
            (r2, c2) = self.__open_entry()
            
        self.__demolish_outside_wall(r2, c2)
        
                

#####################################################
#        Functions initializing a maze from a file
#####################################################

#----------------------------------------------
#       initialize a maze from 2d digits
#----------------------------------------------
    def __initialize_maze_from_digit_matrix(self, matrix):
        self.__validate_matrix(matrix)
        
        self.matrix = matrix
        self.maze_point_matrix = self.__translate_to_maze_point_matrix(matrix)
        self.ydim = len(self.maze_point_matrix) - 1
        self.xdim = len(self.maze_point_matrix[0]) - 1
        
        self.h_wall_matrix = self.__translate_to_horizontal_walls(matrix)
        self.v_wall_matrix = self.__translate_to_vertical_walls(matrix)
              
        self.wall_point_matrix = self.__generate_wall_point_matrix(self.h_wall_matrix, self.v_wall_matrix)
        
        self.num_of_wallsets = 0
        self.num_of_accessible_areas = 0
        self.num_of_cul_de_sacs = 0
        self.routes = []
        self.start_visiting = False
        
#---------------------------------------------------------
#       initialize a maze 
#       This maze could be loaded from file of 2d digits
#       or from a raw matrix (a matrix of 100% walls)
#---------------------------------------------------------
    def __init__(self, input_file, ydim = 0, xdim = 0):
        matrix = None
        if input_file:
            matrix = self.__read_file(input_file)
        else:
            matrix = self.__create_raw_digit_matrix(xdim, ydim)
            
        self.__initialize_maze_from_digit_matrix(matrix)
        
#---------------------------------------------------------
#       Text File reading procedure 
#---------------------------------------------------------
    def __read_file(self, input_file):
        
        matrix = []

        try:
            with open(input_file, 'r') as myfile:
                str_list = myfile.readlines()
             
                xdim = 0

                #read string data into matrix of integers
                for str_item in str_list:
                    split_str = str_item.split()
                    solid_str = ''.join(split_str)
                    char_digit_list = list(solid_str)
                    
                    #print(char_digit_list)
                    
                    if len(char_digit_list) == 0:
                        continue
                    #This is to get length of longest row as amount of columns of matrix
                    if xdim < len(char_digit_list):
                        xdim = len(char_digit_list)

                    number_list = []
                    for str_number in char_digit_list:
                        try:
                            number = int(str_number)
                            if number < 0 or number > 3:
                                raise ValueError
                                
                            number_list.append(number)
                            
                        except ValueError:
                            print('Incorrect input.')
                            sys.exit()

                    matrix.append(number_list)

                for matrix_row in matrix:
                    if len(matrix_row) < xdim:
                        print('Incorrect input.')
                        sys.exit()
                            
        except IOError:
            print('Incorrect file name or file not found, giving up.')
            sys.exit()

        return matrix

#---------------------------------------------------------
#       2D digit matrix validation procedure
#       There are special requirements for the last row
#       and end digit of each row
#---------------------------------------------------------        
    def __validate_matrix(self, matrix):
        
        if len(matrix) < 2:
            print('Incorrect input.')
            sys.exit()
            
        for i in range(len(matrix)):
            if len(matrix[i]) < 2:
                print('Incorrect input.')
                sys.exit()
            if matrix[i][len(matrix[i]) - 1] in {1, 3}:
                print('Incorrect input.')
                sys.exit()
            
            if (i == len(matrix) - 1):
                for j in range(len(matrix[i])):
                    if matrix[i][j] in {2, 3}:
                        print('Incorrect input.')
                        sys.exit()

#-----------------------------------------------------------------
#       Translate 2D digit matrix into a matrix of maze cells
#       Each matrix cell has 4 directions to go:
#           top, right, bellow and left
#       However, some of these directions may be blocked by walls
#-----------------------------------------------------------------                    
    def __translate_to_maze_point_matrix(self, matrix):
        maze_point_matrix = []
        
        for i in range(len(matrix)):
            maze_point_matrix.append([])
            for j in range(len(matrix[i])):
                maze_point_matrix[-1].append(MazeNode())
                
                if matrix[i][j] == 0:
                    pass

                elif matrix[i][j] == 1:
                    if i > 0:
                        maze_point_matrix[i-1][j].block_bellow()
                    maze_point_matrix[i][j].block_top()   
                        
                elif matrix[i][j] == 2:
                    if j > 0:
                        maze_point_matrix[i][j-1].block_right()
                    maze_point_matrix[i][j].block_left()
                    
                elif matrix[i][j] == 3:
                    if i > 0:
                        maze_point_matrix[i-1][j].block_bellow()
                    if j > 0:
                        maze_point_matrix[i][j-1].block_right()
                        
                    maze_point_matrix[i][j].block_left()
                    maze_point_matrix[i][j].block_top()
        
        return maze_point_matrix

#-----------------------------------------------------------------
#       Translate 2D digit matrix into a matrix of horizontal walls
#       Digit 1 in this matrix represents wall
#       Digit 0 in this matrix represents nothing
#       This matrix is for TEX file writing
#-----------------------------------------------------------------
    def __translate_to_horizontal_walls(self, matrix):
        h_wall_matrix = []
        for i in range(len(matrix)):
            h_wall_matrix.append([])
            for j in range(len(matrix[i])):
                if matrix[i][j] == 1 or matrix[i][j] == 3:
                    h_wall_matrix[-1].append(1)          
                else:
                    h_wall_matrix[-1].append(0)
                    
        return h_wall_matrix

#-----------------------------------------------------------------
#       Translate 2D digit matrix into a matrix of vertical walls
#       Digit 1 in this matrix represents wall
#       Digit 0 in this matrix represents nothing
#       This matrix is for TEX file writing
#-----------------------------------------------------------------      
    def __translate_to_vertical_walls(self, matrix):
        v_wall_matrix = []
        for i in range(len(matrix)):
            v_wall_matrix.append([])
            for j in range(len(matrix[i])):
                if matrix[i][j] == 2 or matrix[i][j] == 3:
                    v_wall_matrix[-1].append(1)          
                else:
                    v_wall_matrix[-1].append(0)
                    
        return v_wall_matrix

#-----------------------------------------------------------------
#       Translate horizontal wall matrix and vertical wall matrix into a matrix of wall intersections.
#       Wall intersections are similar to maze cells.
#       We can assume walls consist another kind of maze and we can traverse walls using the same algorithm as traversing a maze
#       Each wall intersection has 4 directions to go:
#           top, right, bellow and left
#       However, some of these directions may be blocked if wall of this direction is demolished
#-----------------------------------------------------------------     
    def __generate_wall_point_matrix(self, h_wall_matrix, v_wall_matrix):
        
        wall_point_matrix = []
        #initialize all points
        for i in range(self.ydim + 1):
            wall_point_matrix.append([])
            for j in range(self.xdim + 1):
                wall_point_matrix[-1].append(WallPoint())
        
        #go through all h walls and record their points
        for i in range(self.ydim + 1):
            in_wall = False
            for j in range(self.xdim + 1):
                if self.h_wall_matrix[i][j] == 1:
                    if not in_wall:
                        in_wall = True
                        wall_point_matrix[i][j].connect_right()
                    else:
                        wall_point_matrix[i][j].connect_left()
                        wall_point_matrix[i][j].connect_right()
                else:
                    if in_wall:
                        in_wall = False
                        wall_point_matrix[i][j].connect_left()
                    else:
                        pass
        
        #go through all v walls and record their points
        for j in range(self.xdim + 1):
            in_wall = False
            for i in range(self.ydim + 1):
                if self.v_wall_matrix[i][j] == 1:
                    if not in_wall:
                        in_wall = True
                        wall_point_matrix[i][j].connect_bellow()
                    else:
                        wall_point_matrix[i][j].connect_top()
                        wall_point_matrix[i][j].connect_bellow()
                else:
                    if in_wall:
                        in_wall = False
                        wall_point_matrix[i][j].connect_top()

                    else:
                        pass

        return wall_point_matrix


#########################################################
#        Functions getting data from maze
#########################################################

#-------------------------------------------------------------
#       Write matrix of 2D digits into a txt file
#------------------------------------------------------------- 
    def write_to_txt_file(self, output_file):
        str_list = []
        for row in self.matrix:
            for number in row:
                str_list.append(str(number))
            str_list.append('\n')
                    
        try:
            with open(output_file, 'w') as myfile:               
                myfile.write(''.join(str_list))
        except IOError:
            print('Can not output maze to txt file.')

#----------------------------------------------------------------------------------------
#       Write the entire maze into a TEX file in simplified mode
#       if hight of this maze is larger than 50 or width of this maze is larger than 40
#---------------------------------------------------------------------------------------- 
    def __write_to_tex_file_simplified(self, output_file):
        str_list = []
        str_list.append('\\documentclass[10pt]{article}\n')
        str_list.append('\\usepackage{tikz}\n')
        str_list.append('\\usetikzlibrary{shapes.misc}\n')
        str_list.append('\\usepackage[margin=0cm]{geometry}\n')
        str_list.append('\\pagestyle{empty}\n')
        str_list.append('\\tikzstyle{every node}=[cross out, draw, red]\n\n')
        str_list.append('\\begin{document}\n\n')
        str_list.append('\\vspace*{\\fill}\n')
        str_list.append('\\begin{center}\n')
        str_list.append('\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, blue]\n')
# % Walls
        str_list.append('% Walls\n')                
        for i in range(self.ydim + 1):
            in_wall = False
            for j in range(self.xdim + 1):
                if self.h_wall_matrix[i][j] == 1:
                    if not in_wall:
                        in_wall = True
                        str_list.append('    \\draw ({0:.1f},{1:.1f}) -- '.format(j * 0.2, i * 0.2))
                    else:
                        pass
                else:
                    if in_wall:
                        in_wall = False
                        str_list.append('({0:.1f},{1:.1f});\n'.format(j * 0.2, i * 0.2))
                    else:
                        pass
                        
        for j in range(self.xdim + 1):
            in_wall = False
            for i in range(self.ydim + 1):
                if self.v_wall_matrix[i][j] == 1:
                    if not in_wall:
                        in_wall = True
                        str_list.append('    \\draw ({0:.1f},{1:.1f}) -- '.format(j * 0.2, i * 0.2))
                    else:
                        pass
                else:
                    if in_wall:
                        in_wall = False
                        str_list.append('({0:.1f},{1:.1f});\n'.format(j * 0.2, i * 0.2))
                    else:
                        pass

# % Entry-exit paths without intersections
        str_list.append('% Entry-exit paths without intersections\n')
        h_lines = {}
        v_lines = {}
        for route in self.routes:
            (pr, pc) = route[0]
            for i in range(len(route) - 1):
                (r, c) = route[i]
                (nr, nc) = route[i + 1]
                if (pr == r and r == nr) or (pc == c and c == nc):
                    pass
                else:
                    if pc == c:
                        if pr > r:
                            v_lines[c * (self.ydim + 2) + r] = (c + 0.5, r + 0.5, pc + 0.5, pr + 0.5)
                        else:
                            v_lines[pc * (self.ydim + 2) + pr] = (pc + 0.5, pr + 0.5, c + 0.5, r + 0.5)
                    else:
                        if pc > c:
                            h_lines[r * (self.xdim + 2) + c] = (c + 0.5, r + 0.5, pc + 0.5, pr + 0.5)
                        else:
                            h_lines[pr * (self.xdim + 2) + pc] = (pc + 0.5, pr + 0.5, c + 0.5, r + 0.5)
                        
                    #str_list.append('    \\draw[dashed, yellow] ({},{}) -- ({},{});\n'.format(pc + 0.5, pr + 0.5, c + 0.5, r + 0.5))
                    (pr, pc) = (r, c)
                    
            (r, c) = route[-1]
            if pc == c:
                if pr > r:
                    v_lines[c * (self.ydim + 2) + r] = (c + 0.5, r + 0.5, pc + 0.5, pr + 0.5)
                else:
                    v_lines[pc * (self.ydim + 2) + pr] = (pc + 0.5, pr + 0.5, c + 0.5, r + 0.5)
            else:
                if pc > c:
                    h_lines[r * (self.xdim + 2) + c] = (c + 0.5, r + 0.5, pc + 0.5, pr + 0.5)
                else:
                    h_lines[pr * (self.xdim + 2) + pc] = (pc + 0.5, pr + 0.5, c + 0.5, r + 0.5)
            
        for (k, (x1, y1, x2, y2)) in sorted(h_lines.items()):
            str_list.append('    \\draw[yellow] ({0:.1f},{1:.1f}) -- ({2:.1f},{3:.1f});\n'.format(x1 * 0.2, y1 * 0.2, x2 * 0.2, y2 * 0.2))
        for (k, (x1, y1, x2, y2)) in sorted(v_lines.items()):
            str_list.append('    \\draw[yellow] ({0:.1f},{1:.1f}) -- ({2:.1f},{3:.1f});\n'.format(x1 * 0.2, y1 * 0.2, x2 * 0.2, y2 * 0.2))
            
        str_list.append('\\end{tikzpicture}\n')
        str_list.append('\\end{center}\n')
        str_list.append('\\vspace*{\\fill}\n\n')
        str_list.append('\\end{document}\n')
        
        try:
            with open(output_file, 'w') as myfile:
                myfile.write(''.join(str_list))
        except IOError:
            print('Can not output maze to tex file.')
        
#----------------------------------------------------------------------------------------
#       Write the entire maze into a TEX file in traditional mode
#       if hight of this maze is within 50 or width of this maze is wihtin 40
#----------------------------------------------------------------------------------------         
    def write_to_tex_file(self, output_file):
        
        if self.xdim > 40 or self.ydim > 50:
            self.__write_to_tex_file_simplified(output_file)
            return
            
        str_list = []
        str_list.append('\\documentclass[10pt]{article}\n')
        str_list.append('\\usepackage{tikz}\n')
        str_list.append('\\usetikzlibrary{shapes.misc}\n')
        str_list.append('\\usepackage[margin=0cm]{geometry}\n')
        str_list.append('\\pagestyle{empty}\n')
        str_list.append('\\tikzstyle{every node}=[cross out, draw, red]\n\n')
        str_list.append('\\begin{document}\n\n')
        str_list.append('\\vspace*{\\fill}\n')
        str_list.append('\\begin{center}\n')
        str_list.append('\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]\n')
# % Walls
    # \draw (0,0) -- (1,0);
    # \draw (4,0) -- (5,0);
    # \draw (6,0) -- (7,0);
    # \draw (0,1) -- (1,1);
    # \draw (3,1) -- (4,1);
    # \draw (0,2) -- (1,2);
        str_list.append('% Walls\n')                
        for i in range(self.ydim + 1):
            in_wall = False
            for j in range(self.xdim + 1):
                if self.h_wall_matrix[i][j] == 1:
                    if not in_wall:
                        in_wall = True
                        str_list.append('    \\draw ({},{}) -- '.format(j, i))
                    else:
                        pass
                else:
                    if in_wall:
                        in_wall = False
                        str_list.append('({},{});\n'.format(j, i))
                    else:
                        pass
                        
        for j in range(self.xdim + 1):
            in_wall = False
            for i in range(self.ydim + 1):
                if self.v_wall_matrix[i][j] == 1:
                    if not in_wall:
                        in_wall = True
                        str_list.append('    \\draw ({},{}) -- '.format(j, i))
                    else:
                        pass
                else:
                    if in_wall:
                        in_wall = False
                        str_list.append('({},{});\n'.format(j, i))
                    else:
                        pass
#% Pillars
#    \fill[green] (1,3) circle(0.2);
#    \fill[green] (7,3) circle(0.2);
#    \fill[green] (3,4) circle(0.2);
        str_list.append('% Pillars\n')
        for i in range(self.ydim + 1):
            for j in range(self.xdim + 1):
                if 0 == self.wall_point_matrix[i][j].get_num_of_wall_connections():
                    str_list.append('    \\fill[green] ({},{}) circle(0.2);\n'.format(j, i))
# % Inner points in accessible cul-de-sacs
    # \node at (2.5,0.5) {};
    # \node at (2.5,1.5) {};
    # \node at (3.5,1.5) {};
    # \node at (4.5,4.5) {};
    # \node at (6.5,4.5) {};
        str_list.append('% Inner points in accessible cul-de-sacs\n')
        for i in range(self.ydim):
            for j in range(self.xdim):
                if self.maze_point_matrix[i][j].belongs_to_cul_de_sacs:
                    str_list.append('    \\node at ({},{}) {{}};\n'.format(j + 0.5, i + 0.5))
                #if self.maze_point_matrix[i][j].visited:
                #    str_list.append('    \\fill[blue] ({},{}) circle(0.1);\n'.format(j + 0.5, i + 0.5))
# % Entry-exit paths without intersections
    # \draw[dashed, yellow] (3.5,0.5) -- (4.5,0.5);
    # \draw[dashed, yellow] (4.5,1.5) -- (5.5,1.5);
    # \draw[dashed, yellow] (3.5,-0.5) -- (3.5,0.5);
    # \draw[dashed, yellow] (4.5,0.5) -- (4.5,1.5);
    # \draw[dashed, yellow] (5.5,-0.5) -- (5.5,1.5);
        str_list.append('% Entry-exit paths without intersections\n')
        h_lines = {}
        v_lines = {}
        for route in self.routes:
            (pr, pc) = route[0]
            for i in range(len(route) - 1):
                (r, c) = route[i]
                (nr, nc) = route[i + 1]
                if (pr == r and r == nr) or (pc == c and c == nc):
                    pass
                else:
                    if pc == c:
                        if pr > r:
                            v_lines[c * (self.ydim + 2) + r] = (c + 0.5, r + 0.5, pc + 0.5, pr + 0.5)
                        else:
                            v_lines[pc * (self.ydim + 2) + pr] = (pc + 0.5, pr + 0.5, c + 0.5, r + 0.5)
                    else:
                        if pc > c:
                            h_lines[r * (self.xdim + 2) + c] = (c + 0.5, r + 0.5, pc + 0.5, pr + 0.5)
                        else:
                            h_lines[pr * (self.xdim + 2) + pc] = (pc + 0.5, pr + 0.5, c + 0.5, r + 0.5)
                        
                    #str_list.append('    \\draw[dashed, yellow] ({},{}) -- ({},{});\n'.format(pc + 0.5, pr + 0.5, c + 0.5, r + 0.5))
                    (pr, pc) = (r, c)
                    
            (r, c) = route[-1]
            if pc == c:
                if pr > r:
                    v_lines[c * (self.ydim + 2) + r] = (c + 0.5, r + 0.5, pc + 0.5, pr + 0.5)
                else:
                    v_lines[pc * (self.ydim + 2) + pr] = (pc + 0.5, pr + 0.5, c + 0.5, r + 0.5)
            else:
                if pc > c:
                    h_lines[r * (self.xdim + 2) + c] = (c + 0.5, r + 0.5, pc + 0.5, pr + 0.5)
                else:
                    h_lines[pr * (self.xdim + 2) + pc] = (pc + 0.5, pr + 0.5, c + 0.5, r + 0.5)
            
        for (k, (x1, y1, x2, y2)) in sorted(h_lines.items()):
            str_list.append('    \\draw[dashed, yellow] ({},{}) -- ({},{});\n'.format(x1, y1, x2, y2))
        for (k, (x1, y1, x2, y2)) in sorted(v_lines.items()):
            str_list.append('    \\draw[dashed, yellow] ({},{}) -- ({},{});\n'.format(x1, y1, x2, y2))
                
            #str_list.append('    \\draw[dashed, yellow] ({},{}) -- ({},{});\n'.format(pc + 0.5, pr + 0.5, c + 0.5, r + 0.5))
            
        str_list.append('\\end{tikzpicture}\n')
        str_list.append('\\end{center}\n')
        str_list.append('\\vspace*{\\fill}\n\n')
        str_list.append('\\end{document}\n')
        
        try:
            with open(output_file, 'w') as myfile:
                myfile.write(''.join(str_list))
        except IOError:
            print('Can not output maze to tex file.')

    def print(self):
        for i in range(self.ydim):
            for j in range(self.xdim):
                print(self.maze_point_matrix[i][j].dir, end=' ')
            print('')

#----------------------------------------------------------------------------------------
#       Print information of all wall intersections
#       This is for debugging
#----------------------------------------------------------------------------------------             
    def print_wall_points(self):
        for row in self.wall_point_matrix:
            for point in row:
                print(point.dir, end=' ')
            print('')   

#----------------------------------------------------------------------------------------
#       Get amount of entries of this maze
#---------------------------------------------------------------------------------------- 
    def get_num_of_gates(self):
        count = 0
        
        #go through top and bottom border
        for j in range(self.xdim):
            if self.h_wall_matrix[0][j] == 0:
                count += 1
            if self.h_wall_matrix[-1][j] == 0:
                count += 1
                    
        #go through left border
        for i in range(self.ydim):
            if self.v_wall_matrix[i][0] == 0:
                count += 1
            if self.v_wall_matrix[i][-1] == 0:
                count += 1

        return count

#----------------------------------------------------------------------------------------
#       Get number of wall sets this maze
#---------------------------------------------------------------------------------------- 
    def get_num_of_wallsets(self):
        return self.num_of_wallsets

#----------------------------------------------------------------------------------------
#       Get number of inaccessible maze cells this maze
#---------------------------------------------------------------------------------------- 
    def get_num_of_inaccessible_maze_points(self):
        count = 0
        for i in range(self.ydim):
            for j in range(self.xdim):
                if (not self.maze_point_matrix[i][j].visited) and \
                    (not self.maze_point_matrix[i][j].belongs_to_cul_de_sacs):
                    count += 1
        return count

#----------------------------------------------------------------------------------------
#       Get number of accessible areas this maze
#----------------------------------------------------------------------------------------         
    def get_num_of_accessible_areas(self):
        return self.num_of_accessible_areas

#----------------------------------------------------------------------------------------
#       Get number of cul-de-sacs of this maze
#---------------------------------------------------------------------------------------- 
    def get_num_of_cul_de_sacs(self):
        return self.num_of_cul_de_sacs

#----------------------------------------------------------------------------------------
#       Get amount of inaccessible maze cells this maze
#---------------------------------------------------------------------------------------- 
    def get_num_of_no_intersection_routes(self):
        return len(self.routes)

        
#######################################################################
#        Functions visiting this maze
#######################################################################

#----------------------------------------------------------------------------------------
#       One step to visit a wall intersection (deep first search algorithm)
#---------------------------------------------------------------------------------------- 
    def __visit_next_wall_point(self, stack):
        if len(stack) == 0:
            return
        (row, col, prev_i, prev_j) = stack[-1]
        
        #keep inside boundary
        if row < 0 or col < 0 or row > self.ydim or col > self.xdim:
            stack.pop()
            return
            
        #print(stack)
        
        point = self.wall_point_matrix[row][col]
        if not point.visited:
            point.visited = True
            #remove the direction coming from
            if (prev_i, prev_j) in point.uv_dir:
                del point.uv_dir[(prev_i, prev_j)]

            ((i, j), k) = point.uv_dir.popitem()
            #if this direction is accessible (no walls)
            if point.dir[(i, j)] == 1:
                #Do not go outside boundary
                #Do not go to visited node
                if row + i >= 0 and row + i <= self.ydim and col + j >= 0 and col + j <= self.xdim and \
                    (not self.wall_point_matrix[row + i][col + j].visited):
                        stack.append((row + i, col + j, -i, -j))
        else:
            if len(point.uv_dir) > 0:
                ((i, j), k) = point.uv_dir.popitem()
                #if this direction is accessible (no walls)
                if point.dir[(i, j)] == 1:
                    #Do not go outside boundary
                    #Do not go to visited node
                    if row + i >= 0 and row + i <= self.ydim and col + j >= 0 and col + j <= self.xdim and \
                        (not self.wall_point_matrix[row + i][col + j].visited):
                            stack.append((row + i, col + j, -i, -j))
            else:
                stack.pop()

#----------------------------------------------------------------------------------------
#       Visit an entire wall set from a start point using deep first searth
#---------------------------------------------------------------------------------------- 
    def __visit_wallset(self, row, col):
        stack = []
        stack.append((row, col, 0, 0))
        while len(stack) > 0:
            self.__visit_next_wall_point(stack)

#----------------------------------------------------------------------------------------
#       Visit all wall-sets of this maze and calculate number of wall-sets
#---------------------------------------------------------------------------------------- 
    def visit_walls(self):
        #clear data of wall visiting
        for i in range(self.ydim + 1):
            for j in range(self.xdim + 1):
                self.wall_point_matrix[i][j].unvisit()
                
        self.num_of_wallsets = 0
        
        count = 0
        for i in range(self.ydim + 1):
            for j in range(self.xdim + 1):
                if (not self.wall_point_matrix[i][j].visited) \
                    and self.wall_point_matrix[i][j].is_in_wall():
                    #print('wall set plus!')
                    count += 1
                    self.__visit_wallset(i, j)
                
        self.num_of_wallsets = count

#----------------------------------------------------------------------------------------
#       One step to visit a maze cell (deep first search algorithm)
#----------------------------------------------------------------------------------------     
    def __visit_next_maze_point(self, stack):
        if len(stack) == 0:
            return
            
        (row, col, prev_i, prev_j) = stack[-1]
             
        #print(stack)
        
        #you are right at the border of maze, so you are about to enter
        #or about to leave the maze --- or at the end of stack popping 
        if row == -1 or col == -1 or row == self.ydim or col == self.xdim:
            
            #you are about to leave this maze if the stack is larger than 1
            #if you are going out of this maze, it means you have finshed one
            #route in this maze which starts from one entry and ends at
            #another antry of this maze
            if len(stack) > 1:
                self.routes.append([])
                for (r, c, pi, pj) in stack:
                    #Node in this stack should be inside the maze
                    if r != -1 and c != -1 and r != self.ydim and c != self.xdim:
                        #there should be at least 2 blockages of this node
                        #blockages can be walls or neighboring cul-de-sacs
                        cul_de_sacs = 0
                        walls = 0
                        for ((i, j), k) in self.maze_point_matrix[r][c].dir.items():
                            if not k:
                                walls += 1
                            
                            elif r + i >= 0 and r + i < self.ydim and c + j >= 0 and c + j < self.xdim \
                                and self.maze_point_matrix[r + i][c + j].belongs_to_cul_de_sacs:
                                cul_de_sacs += 1
                        #if there is one node who has blockages less than 2
                        #then the entire route should be invalid
                        if walls + cul_de_sacs < 2:
                            #print('########### Node ({}, {}) does not satisfy route requirement #################'.format(r, c))
                            self.routes.pop()
                            break
                            
                    self.routes[-1].append((r, c))

                stack.pop()

            #you are about to enter the maze
            else:
                i = 0
                j = 0
                if row == -1:
                    i = 1
                    j = 0
                elif row == self.ydim:
                    i = -1
                    j = 0
                elif col == -1:
                    i = 0
                    j = 1
                else:
                    i = 0
                    j = -1
                if self.start_visiting:
                    #unvisited area and cul_de_sacs area are both distinct accessible areas
                    if not self.maze_point_matrix[row + i][col + j].visited:
                        #Accessible area should be inside the maze
                        if row + i >= 0 and row + i < self.ydim and col + j >= 0 and col + j < self.xdim:
                            #print('Accessible area plus!')
                            self.num_of_accessible_areas += 1
                        #Do not need to visit cul_de_sacs area unless you don't know it
                        if not self.maze_point_matrix[row + i][col + j].belongs_to_cul_de_sacs:
                            stack.append((row + i, col + j, -i, -j))
                    
                    #this entry is already visited, it means this area was already accessed
                    else:
                        stack.pop()
                    
                    self.start_visiting = False
                #visiting process is about to finish (pop the last stack)
                else:
                    if self.maze_point_matrix[row + i][col + j].belongs_to_cul_de_sacs:
                        self.num_of_cul_de_sacs += 1
                    stack.pop()
                    
        #you are inside the maze, keep on going !!!!!
        else: 
            current_point = self.maze_point_matrix[row][col]
            if not current_point.visited:
                current_point.visited = True
                #remove the direction coming from to prevent duplicate visit
                if (prev_i, prev_j) in current_point.uv_dir:
                    del current_point.uv_dir[(prev_i, prev_j)]

                ((i, j), k) = current_point.uv_dir.popitem()
                
                #if this direction is accessible
                if current_point.dir[(i, j)] == 1:
                    #Do not visit maze node that was already visited
                    #Do not need to visit cul_de_sacs area unless you don't know it is
                    if (not self.maze_point_matrix[row + i][col + j].visited) and \
                        (not self.maze_point_matrix[row + i][col + j].belongs_to_cul_de_sacs):
                        stack.append((row + i, col + j, -i, -j))
            else:
                if len(current_point.uv_dir) > 0:
                    #There are unvisited directions for use in this node
                    ((i, j), k) = current_point.uv_dir.popitem()
                    
                    #if this direction is accessible (no blocking wall)
                    if current_point.dir[(i, j)] == 1:
                        #Do not visit maze node that was already visited
                        #Do not need to visit cul_de_sacs area unless you don't know it is
                        if (not self.maze_point_matrix[row + i][col + j].visited) and \
                            (not self.maze_point_matrix[row + i][col + j].belongs_to_cul_de_sacs):
                            stack.append((row + i, col + j, -i, -j))
                else:
                    #Can not visit other nodes from this node
                    #because all sub nodes have been visited or
                    #there is no available sub node to visit
                    #pop the stack
                    
                    cul_de_sacs = 0
                    walls = 0
                    for ((i, j), k) in current_point.dir.items():
                        if not k:
                            walls += 1
                        
                        elif row + i >= 0 and row + i < self.ydim and col + j >= 0 and col + j < self.xdim \
                            and self.maze_point_matrix[row + i][col + j].belongs_to_cul_de_sacs:
                            cul_de_sacs += 1
                            
                    if walls + cul_de_sacs == 3:
                        current_point.belongs_to_cul_de_sacs = True
                    elif cul_de_sacs > 0:
                        self.num_of_cul_de_sacs += cul_de_sacs
                    
                    stack.pop()
                    
                    
#----------------------------------------------------------------------------------------
#       Visit the maze from a start point using deep first searth
#----------------------------------------------------------------------------------------     
    def __visit_maze_start_from(self, row, col):
        self.start_visiting = True
    
        stack = []
        
        if row == -1:
            stack.append((row, col, -1, 0))
        elif row == self.ydim:
            stack.append((row, col, 1, 0))
        elif col == -1:
            stack.append((row, col, 0, -1))
        elif col == self.xdim:
            stack.append((row, col, 0, 1))
        else:
            stack.append((row, col, 0, 0))           
   
        while len(stack) > 0:
            self.__visit_next_maze_point(stack)
            
#----------------------------------------------------------------------------------------
#       Visit the maze from multiple entries
#---------------------------------------------------------------------------------------- 
    def __visit_maze(self):
        entries = []
        
        #go through top and bottom border to collect entries
        for j in range(self.xdim):
            if self.h_wall_matrix[0][j] == 0:
                entries.append((-1, j))
            if self.h_wall_matrix[-1][j] == 0:
                entries.append((self.ydim, j))
                    
        #go through left and right border to collect entries
        for i in range(self.ydim):
            if self.v_wall_matrix[i][0] == 0:
                entries.append((i, -1))
            if self.v_wall_matrix[i][-1] == 0:
                entries.append((i, self.xdim))
        
        for (i, j) in entries:
            if not self.maze_point_matrix[i][j].visited:
                self.__visit_maze_start_from(i, j)

#----------------------------------------------------------------------------------------
#       Visit the entire maze.
#       We should refresh some initial data before visiting the maze.
#       Cul-de-sacs will be marked automatically during the first time of visit.
#       Cul-de-sacs will NOT be visited during the second time of visit.
#       Number of cul-de-sacs will be calculated automatically.
#       Number of accessible areas will also be calculated during the visit.
#---------------------------------------------------------------------------------------- 
    def visit_maze(self):
        #clear data of visiting
        for i in range(self.ydim + 1):
            for j in range(self.xdim + 1):
                self.maze_point_matrix[i][j].unvisit()
                
        self.num_of_accessible_areas = 0
        self.num_of_cul_de_sacs = 0
        self.routes = []
        self.start_visiting = False
        
        self.__visit_maze()
                
#----------------------------------------------------------------------------------------
#       Visit the entire maze and mark cul-de-sacs
#----------------------------------------------------------------------------------------                 
    def mark_cul_de_sacs(self):
        self.visit_maze()
        

        
    
########################################################
#
#         Main entry of this program
#
########################################################           

if __name__ == '__main__':
 
###############################################
#        Deal with program arguments
###############################################

#-------------------------------------------------------- 
#    Examples of how to run this program:
#    python3 maze.py --file filename.txt 
#    python3 maze.py -print --file filename.txt
#    python3 maze.py --generate <ydim>:<xdim>:<seed>
#    python3 maze.py -print --generate <ydim>:<xdim>:<seed>
#--------------------------------------------------------
    input_file_name = None
    print_maze = False
    maze_generation_args = None
    try:
        if len(sys.argv) < 3:
            raise ValueError
        elif sys.argv[1] == '--file':
            input_file_name = sys.argv[2]
        elif sys.argv[1] == '--generate':
            maze_generation_args = sys.argv[2].split(':')
        elif sys.argv[1] == '-print' and len(sys.argv) > 3:
            if sys.argv[2] == '--file':
                input_file_name = sys.argv[3]
            elif sys.argv[2] == '--generate':
                maze_generation_args = sys.argv[3].split(':')
            else:
                raise ValueError
            print_maze = True
        else:
            raise ValueError
    except ValueError:
        print('I expect --file followed by filename and possibly -print as command line arguments.')
        sys.exit()
    
    the_maze = None
    if input_file_name:
#--------------------------------------------------------------
#   If this maze is loaded from a txt file of 2D digits
#--------------------------------------------------------------
        the_maze = Maze(input_file_name)
    else:
#--------------------------------------------------------------
#   If this maze is randomly generated by ydim, xdim and seed
#--------------------------------------------------------------
        ydim = int(maze_generation_args[0])
        xdim = int(maze_generation_args[1])
        the_seed = int(maze_generation_args[2])
        input_file_name = 'labyrinth_maze_{}_{}_{}.txt'.format(ydim, xdim, the_seed)
        the_maze = Maze(None, ydim, xdim)
        the_maze.demolish_walls(the_seed)
        #Write this auto generated maze into a txt file
        the_maze.write_to_txt_file(input_file_name)
        
    
    the_maze.visit_walls()
    the_maze.mark_cul_de_sacs()
    the_maze.visit_maze()

    if not print_maze:    
###############################################
#        Extremely stupid source code comes
###############################################
        num_gates = the_maze.get_num_of_gates()
        num_wallsets = the_maze.get_num_of_wallsets()
        num_inaccessible = the_maze.get_num_of_inaccessible_maze_points()
        num_accessible_areas = the_maze.get_num_of_accessible_areas()
        num_cul_de_sacs = the_maze.get_num_of_cul_de_sacs()
        num_no_intersection_routes = the_maze.get_num_of_no_intersection_routes()
        
        if num_gates == 0:
            print('The maze has no gate.')
        elif num_gates == 1:
            print('The maze has a single gate.')
        else:
            print('The maze has {} gates.'.format(num_gates))
        
        if num_wallsets == 0:
            print('The maze has no wall.')
        elif num_wallsets == 1:
            print('The maze has a single wall that are all connected.')
        else:
            print('The maze has {} sets of walls that are all connected.'.format(num_wallsets))
                    
        if num_inaccessible == 0:
            print('The maze has no inaccessible inner point.')
        elif num_inaccessible == 1:
            print('The maze has a unique inaccessible inner point.')
        else:
            print('The maze has {} inaccessible inner points.'.format(num_inaccessible))

        if num_accessible_areas == 0:
            print('The maze has no accessible area.')
        elif num_accessible_areas == 1:
            print('The maze has a unique accessible area.')
        else:
            print('The maze has {} accessible areas.'.format(num_accessible_areas))
        
        if num_cul_de_sacs == 0:
            print('The maze has no accessible cul-de-sac.')
        elif num_cul_de_sacs == 1:
            print('The maze has accessible cul-de-sacs that are all connected.')
        else:
            print('The maze has {} sets of accessible cul-de-sacs that are all connected.'.format(num_cul_de_sacs))
        
        if num_no_intersection_routes == 0:
            print('The maze has no entry-exit path with no intersection not to cul-de-sacs.')
        elif num_no_intersection_routes == 1:
            print('The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
        else:
            print('The maze has {} entry-exit paths with no intersections not to cul-de-sacs.'.format(num_no_intersection_routes))

###############################################
#     Print maze to TEX file if it is needed
###############################################    
    
    else:
        
        regex = '(.*)[\.][^\.]*|([^\.]+)'
        match = re.search(regex, input_file_name)
        if match:
            file_name = match.group(1)
            if not file_name:
                file_name = match.group(2)
            the_maze.write_to_tex_file('{}.{}'.format(file_name, 'tex'))
        





        