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



def ScanFishingTowns(towns, distances):

    for i in range(len(towns) - 1):
        if towns[i] < towns[i + 1]:
            towns[i + 1] -= 1
            if distances[i] > 0:
                distances[i] -= 1
            else:
                towns[i] += 1
        elif towns[i] > towns[i + 1]:
            towns[i] -= 1
            if distances[i] > 0:
                distances[i] -= 1
            else:
                towns[i + 1] += 1

    #print(towns)
    #print(distances)



def DealWithFishingTowns(towns, distances):

    while True:
        ma = max(towns)
        mi = min(towns)
        
        if ma - mi == 0:
            break
        if (sum(distances) == 0 and ma - mi < 2):
            break

        ScanFishingTowns(towns, distances)


    return max(towns)



    
    
if __name__ == '__main__':

    file_name = input('Which data file do you want to use? ')

    (towns, distances) = ReadFishingTowns (file_name)

    maximum = DealWithFishingTowns(towns, distances)
    
    print('The maximum quantity of fish that each town can have is {0}'.format(maximum))
