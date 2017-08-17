import sys

def ReadFishingTowns (file_name):
    towns = []
    raw_distances = []
    distances = []

    try:
        with open(file_name, 'r') as myfile:
            str_list = myfile.readlines()

            #read string data into towns and distances
            for str_item in str_list:
                str_numbers = str_item.split()

                try:
                    if len(str_numbers) == 2:
                        raw_distances.append(int(str_numbers[0]))
                        towns.append(int(str_numbers[1]))
                except ValueError:
                    print('Incorrect data in file, giving up.')
                    sys.exit()
    except IOError:
        print('Incorrect file name or file not found, giving up.')
        sys.exit()

    for i in range(len(raw_distances)):
        if i > 0:
            if raw_distances[i] < raw_distances[i-1]:
                print('First number in each line should be increment!')
                sys.exit()
            distances.append(raw_distances[i] - raw_distances[i-1])

    return (towns, distances)



def ErrorByExpectation(expect, towns, distances):

    towns_temp = list(towns)
    
    if len(towns_temp) > 0:      
        for i in range(len(towns_temp) - 1):
            offset = expect - towns_temp[i]
            towns_temp[i] = expect
            if offset > 0:
                towns_temp[i + 1] -= offset + distances[i]
            elif offset < 0:
                offset *= -1
                if distances[i] < offset:
                    towns_temp[i + 1] += offset - distances[i]
                else:
                    pass

    #print(towns_temp)
    
    return (towns_temp, towns_temp[-1] - expect)
            



def DealWithFishingTowns(towns, distances):

    down_limit = min(towns)
    up_limit = max(towns)
    error = -1
    min_in_result = 0

    while True:
        mid = (up_limit + down_limit) // 2
        (result, error) = ErrorByExpectation(mid, towns, distances)
        if error > 0:
            down_limit = mid
        elif error < 0:
            up_limit = mid
        else:
            min_in_result = min(result)
            break

##        print(up_limit)
##        print(down_limit)
##        print(mid)

        # Error != 0 but the range can not continue to be narrowed again
        if up_limit - down_limit <= 1:
            # If the range is exactly one number
            if up_limit - down_limit == 0:
                min_in_result = min(result)
            else:
                # If there are 2 numbers (e.g. 100 and 101)
                # Choose the one which produces better result
                (result1, error1) = ErrorByExpectation(up_limit, towns, distances)
                (result2, error2) = ErrorByExpectation(down_limit, towns, distances)
                if min(result1) > min(result2):
                    min_in_result = min(result1)
                else:
                    min_in_result = min(result2)
            break

    return min_in_result



    
    
if __name__ == '__main__':

    file_name = input('Which data file do you want to use? ')

    (towns, distances) = ReadFishingTowns (file_name)

    maximum = DealWithFishingTowns(towns, distances)
    
    print('The maximum quantity of fish that each town can have is {0}.'.format(maximum))
