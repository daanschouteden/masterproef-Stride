import csv
import sys


def convert_results(step, runtype):
    try:
        path = step + "/" + step.split('-')[1] + "_" + runtype + "/Successful runs/1/"

        first = []
        with open(path + 'first.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    first.append(int(val))

        second = []
        with open(path + 'second.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    second.append(int(val))  
        
        third = []
        with open(path + 'third.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    third.append(int(val))
        
        total = []
        with open(path + 'total.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    total.append(int(val))
        
        with open(step + "/" + runtype + '.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Updating', 'Tracing', 'Infector', 'Total'])
            for i in range(len(first)):
                csvwriter.writerow([first[i], second[i], third[i], total[i]])
    except:
        print("Error " + step + "_" + runtype + ":", sys.exc_info()[0])

def convert_pool_results(step, runtype):
    try:
        path = step + "/" + step.split('-')[1] + "_" + runtype + "/Successful runs/1/"

        household = []
        with open(path + '1household.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    household.append(int(val))
                else:
                    household.append(0)
        household = household[:-1]
        
        k12school = []
        with open(path + '2k12school.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    k12school.append(int(val))
                else:
                    k12school.append(0)
        k12school = k12school[:-1]

        college = []
        with open(path + '3college.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    college.append(int(val))
                else:
                    college.append(0)
        college = college[:-1]

        workplace = []
        with open(path + '4workplace.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    workplace.append(int(val))
                else:
                    workplace.append(0)
        workplace = workplace[:-1]

        primary = []
        with open(path + '5primary.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    primary.append(int(val))
                else:
                    primary.append(0)
        primary = primary[:-1]

        secondary = []
        with open(path + '6secondary.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    secondary.append(int(val))
                else:
                    secondary.append(0)
        secondary = secondary[:-1]

        cluster = []
        with open(path + '7cluster.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    cluster.append(int(val))
                else:
                    cluster.append(0)
        cluster = cluster[:-1]
        
        with open(step + "/" + runtype + '.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['household', 'k12school', 'college', 'workplace', 'primary', 'secondary', 'cluster'])
            for i in range(len(household)):
                csvwriter.writerow([household[i], k12school[i], college[i], workplace[i], primary[i], secondary[i], cluster[i]])
    except:
        print("Error " + step + "_" + runtype + ":", sys.exc_info()[0])


def step_results(step):
    convert_results(step, 'all_1')
    convert_results(step, 'all_2')
    convert_results(step, 'all_4')
    convert_results(step, 'all_8')
    convert_results(step, 'opt_1')
    convert_results(step, 'opt_2')
    convert_results(step, 'opt_4')
    convert_results(step, 'opt_8')
    convert_pool_results(step, 'all_1_pools')

if __name__== "__main__":
    step_results('0-basis')
    step_results('1-standard')
