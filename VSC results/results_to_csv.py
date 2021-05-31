import csv
import sys

basis_path = '0-basis'
standard_path = '1-standard'
ii_path = '2-iterative_intervals'
swi_path = '3-sampling_with_iteration'
fs_path = '4-full_sampling'
afs_path = '5-adjusted_full_sampling'
its_path = 'inf-to-sus'


def convert_results(step, runtype):
    try:
        path = step + "/" + step.split('-')[1] + "_" + runtype + "/Successful runs/1/"
        #path = step + "/" + "full_sampling_"+ runtype + "/Successful runs/1/"

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

def convert_its_results(step, runtype):
    try:
        path = step + "/" + runtype + "/Successful runs/1/"

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
            csvwriter.writerow(['Household', 'K-12 school', 'College', 'Workplace', 'Primary', 'Secondary', 'Cluster'])
            for i in range(len(household)):
                csvwriter.writerow([household[i], k12school[i], college[i], workplace[i], primary[i], secondary[i], cluster[i]])
    except:
        print("Error " + step + "_" + runtype + ":", sys.exc_info()[0])

def convert_poolsize_times(step, runtype):
    try:
        path_weekday = step + "/" + step.split('-')[1] + "_" + runtype + "/Successful runs/weekday/"
        path_weekend = step + "/" + step.split('-')[1] + "_" + runtype + "/Successful runs/weekend/"

        weekday_average = []
        with open(path_weekday + 'poolsizes_time_averages.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    weekday_average.append(int(val))
                else:
                    weekday_average.append(0)
        weekday_average = weekday_average[:-1]
        
        weekday_counts = []
        with open(path_weekday + 'poolsizes_time_counts_.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    weekday_counts.append(int(val))
                else:
                    weekday_counts.append(0)
        weekday_counts = weekday_counts[:-1]

        weekday_totals = []
        with open(path_weekday + 'poolsizes_time_totals_.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    weekday_totals.append(int(val))
                else:
                    weekday_totals.append(0)
        weekday_totals = weekday_totals[:-1]

        weekend_averages = []
        with open(path_weekend + 'poolsizes_time_averages.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    weekend_averages.append(int(val))
                else:
                    weekend_averages.append(0)
        weekend_averages = weekend_averages[:-1]

        weekend_counts = []
        with open(path_weekend + 'poolsizes_time_counts_.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    weekend_counts.append(int(val))
                else:
                    weekend_counts.append(0)
        weekend_counts = weekend_counts[:-1]

        weekend_totals = []
        with open(path_weekend + 'poolsizes_time_totals_.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    weekend_totals.append(int(val))
                else:
                    weekend_totals.append(0)
        weekend_totals = weekend_totals[:-1]
        
        with open(step + "/" + runtype + '.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['weekday_averages', 'weekday_counts', 'weekday_totals', 'weekend_averages', 'weekend_counts', 'weekend_totals'])
            for i in range(len(weekday_average)):
                csvwriter.writerow([weekday_average[i], weekday_counts[i], weekday_totals[i], weekend_averages[i], weekend_counts[i], weekend_totals[i]])
    except:
        print("Error " + step + "_" + runtype + ":", sys.exc_info()[0])

def convert_times_counts(step, runtype):
    try:
        path = step + "/" + step.split('-')[1] + "_" + runtype + "/Successful runs/1/"

        times_household = []
        with open(path + 'totals_household.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    times_household.append(int(val))
                else:
                    times_household.append(0)
        times_household = times_household[:-1]

        counts_household = []
        with open(path + 'counts_household.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    counts_household.append(int(val))
                else:
                    counts_household.append(0)
        counts_household = counts_household[:-1]
        
        times_k12school = []
        with open(path + 'totals_k12school.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    times_k12school.append(int(val))
                else:
                    times_k12school.append(0)
        times_k12school = times_k12school[:-1]

        counts_k12school = []
        with open(path + 'counts_k12school.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    counts_k12school.append(int(val))
                else:
                    counts_k12school.append(0)
        counts_k12school = counts_k12school[:-1]

        times_college = []
        with open(path + 'totals_college.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    times_college.append(int(val))
                else:
                    times_college.append(0)
        times_college = times_college[:-1]

        counts_college = []
        with open(path + 'counts_college.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    counts_college.append(int(val))
                else:
                    counts_college.append(0)
        counts_college = counts_college[:-1]

        times_workplace = []
        with open(path + 'totals_workplace.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    times_workplace.append(int(val))
                else:
                    times_workplace.append(0)
        times_workplace = times_workplace[:-1]

        counts_workplace = []
        with open(path + 'counts_workplace.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    counts_workplace.append(int(val))
                else:
                    counts_workplace.append(0)
        counts_workplace = counts_workplace[:-1]

        times_primary = []
        with open(path + 'totals_primary.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    times_primary.append(int(val))
                else:
                    times_primary.append(0)
        times_primary = times_primary[:-1]

        counts_primary = []
        with open(path + 'counts_primary.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    counts_primary.append(int(val))
                else:
                    counts_primary.append(0)
        counts_primary = counts_primary[:-1]

        times_secondary = []
        with open(path + 'totals_secondary.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    times_secondary.append(int(val))
                else:
                    times_secondary.append(0)
        times_secondary = times_secondary[:-1]

        counts_secondary = []
        with open(path + 'counts_secondary.txt', 'r') as file:
            for line in file.readlines():
                val = line.rstrip('\n')
                if val != "":
                    counts_secondary.append(int(val))
                else:
                    counts_secondary.append(0)
        counts_secondary = counts_secondary[:-1]
        
        with open(step + "/" + runtype + '.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['times_household', 'counts_household', 'times_k12school', 'counts_k12school', 'times_college', 'counts_college',
                'times_workplace', 'counts_workplace', 'times_primary', 'counts_primary', 'times_secondary', 'counts_secondary'])
            for i in range(1,len(times_household)):
                csvwriter.writerow([times_household[i], counts_household[i], times_k12school[i], counts_k12school[i], times_college[i], counts_college[i], 
                    times_workplace[i], counts_workplace[i], times_primary[i], counts_primary[i], times_secondary[i], counts_secondary[i]])
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
    #step_results('0-basis')
    #step_results('1-standard')
    #step_results('2-iterative_intervals')
    
    #convert_poolsize_times('1-standard', 'all_1_poolsize_times')

    #convert_times_counts('1-standard', 'all_1_times_counts')
    #convert_results(ii_path, 'all_1')
    #convert_times_counts(ii_path, 'all_1_times_counts')
    #convert_results(swi_path, 'all_1_pType')
    #convert_times_counts(swi_path, 'all_1_times_counts_pType')
    #convert_times_counts(swi_path, 'all_1_times_counts_pSize')
    #convert_results(fs_path, 'all_1_pType')
    #convert_times_counts(fs_path, 'all_1_times_counts_pType')
    #convert_results(fs_path, 'all_1_pSize')
    #convert_times_counts(fs_path, 'all_1_times_counts_pSize')

    #convert_its_results(its_path, 'ii_sort_both')
    #convert_its_results(its_path, 'ii_sort_sus')
    #convert_its_results(its_path, 'sample_contacts_sort_both')
    #convert_its_results(its_path, 'sample_contacts_sort_sus')
    #convert_its_results(its_path, 'sample_sort_both')
    #convert_its_results(its_path, 'sample_sort_sus')
    
    #convert_results(fs_path, 'all_1')
    #convert_results(afs_path, 'all_1')
    #convert_times_counts(fs_path, 'all_1_times_counts')
    #convert_times_counts(afs_path, 'all_1_times_counts')

    #------ wrong node adjustments
    #convert_results(basis_path, 'all_1')
    #convert_results(standard_path, 'all_1')
    #convert_results(standard_path, 'all_4')
    #convert_results(ii_path, 'all_1')
    #convert_results(swi_path, 'all_1_pType')
    #convert_results('full_sampling initially', 'all_1_pSize')
    convert_its_results(its_path, 'ii_sort_both')
    convert_its_results(its_path, 'ii_sort_sus')
    convert_its_results(its_path, 'sample_contacts_sort_both')
