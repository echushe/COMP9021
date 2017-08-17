from random import seed, randrange
import sys

maze_height = int(sys.argv[1])
maze_width = int(sys.argv[2])
the_seed = int(sys.argv[3])
file_name = 'random_maze_{}_{}_{}.txt'.format(maze_height, maze_width, the_seed)

seed(the_seed)

maze = []
random_pool = [0, 1, 2, 3]

for i in range(maze_height + 1):
    maze.append([])
    for j in range(maze_width + 1):
        digit = random_pool[randrange(len(random_pool))]
        
        if i < maze_height:
            if j == maze_width:
                while digit in {1, 3}:
                    digit = random_pool[randrange(len(random_pool))]
        elif j < maze_width:
            while digit in {2, 3}:
                digit = random_pool[randrange(len(random_pool))]
        else:
            while digit in {1, 2, 3}:
                digit = random_pool[randrange(len(random_pool))]
                
        maze[-1].append(str(digit))  

output = []
for row in maze:
    output.append(''.join(row))
    output.append('\n')

try:
    with open(file_name, 'w') as myfile:
        myfile.write(''.join(output))
except IOError:
    print('Can not output maze to txt file.')