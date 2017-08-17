import sys
import collections

def ReadMatrixFromFile (file_name):
    matrix = []

    try:
        with open(file_name, 'r') as myfile:
            str_list = myfile.readlines()

            amount_of_rows = len(str_list)
            amount_of_columns = 0

            #read string data into matrix of integers
            for str_item in str_list:
                str_numbers = str_item.split()

                #This is to get length of longest row as amount of columns of matrix
                if amount_of_columns < len(str_numbers):
                    amount_of_columns = len(str_numbers)

                number_list = []
                for str_number in str_numbers:
                    try:
                        number_list.append(float(str_number))
                    except ValueError:
                        print('Incorrect data in file, giving up.')
                        sys.exit()

                matrix.append(number_list)

            #fill in empty parts of this matrix with zeros
            for matrix_row in matrix:
                if len(matrix_row) < amount_of_columns:
                    start = len(matrix_row)
                    for _ in range(start, amount_of_columns):
                        matrix_row.append(0.0)
    except IOError:
        print('Incorrect file name or file not found, giving up.')
        sys.exit()

    return matrix



def GenerateElevationList(matrix):
    levels = {}
    for row in matrix:
        for item in row:
            if item in levels:
                levels[item] += 100
            else:
                levels[item] = 100

    levels = collections.OrderedDict(sorted(levels.items()))

    #print(levels)
    
    return levels


def GenerateWaterAreaList(ordered_levels):
    water_areas = {}

    index = 0
    previous_key = 0
    for key, value in ordered_levels.items():
        water_areas[key] = value
        if index > 0:
            water_areas[key] += water_areas[previous_key]

        previous_key = key
        index += 1
        
    water_areas = collections.OrderedDict(sorted(water_areas.items()))

    #print(water_areas)

    return water_areas



def CalculateWaterLevel(water_areas, water):

    index = 0
    previous_h = 0
    previous_area = 0
    water_level = 0
    water_level_done = False
    for h, area in water_areas.items():
        if index > 0:
            if water < previous_area * (h - previous_h):
                water_level = previous_h + water / previous_area
                water_level_done = True
                water = 0
                break
            
            water -= previous_area * (h - previous_h)

        previous_h = h
        previous_area = area
        index += 1

    if not water_level_done:
        water_level = previous_h + water / previous_area

    return water_level
    

def Rain(water, matrix):
    elevations = GenerateElevationList(matrix)
    water_areas = GenerateWaterAreaList(elevations)
    water_level = CalculateWaterLevel(water_areas, water)    

    return water_level

      

if __name__ == '__main__':

    file_name = input('Which data file do you want to use? ')
    
    the_matrix = ReadMatrixFromFile(file_name)

    #for row in the_matrix:
    #    print(row)

    try:
        water = float(input('How many decilitres of water do you want to pour down? '))
        if water < 0:
            raise ValueError
        
        print('The water rises to {0:.2f} centimetres.'.format(Rain(water * 100, the_matrix)))
    except ValueError:
        print('Incorrect input, giving up.')
        sys.exit()


