import time
import matplotlib.pyplot as plt
import pandas as pd

person_age = dict()                 # (personID, age)
person_total_contacts = dict()      # (personID, contacts)

aggregation = dict()
aggregation_counter = dict()

results = dict()
#results2 = dict()

FILENAME = "event_log.txt"
# FILENAME2 = "test.txt"
EVENT_TYPE = "[CONT]"
POOL_TYPE = 0

pool_simulation_days = set()           # list of simulation days this pool is active

# Wordt niet gebruikt, louter voor overzicht
POOLS = {
    0: "Household", 1: "K12School", 2: "College", 3: "Workplace", 4: "Primary", 5: "Secondary", 6: "Cluster"
}


def plotter():
    plt.plot(list(results.keys()), list(results.values()), "o", label="Original")
    #plt.plot(list(results2.keys()), list(results2.values()), "ro", label="Test")
    plt.xlabel("Age")
    plt.ylabel("Contact rate")
    plt.legend()
    plt.show()


def printDict(dct):
    for key, value in dct.items():
        print(key, "\t", value)


def averageContacts(dct):
    for age, count in aggregation.items():
        if aggregation_counter[age] == 0:
            dct[age] = 0
        else:
            dct[age] = round(aggregation[age] / aggregation_counter[age] / len(pool_simulation_days), 2)


def aggregateContactsByAge():
    for i in range(0, 120):
        for person, age in person_age.items():
            age = int(age)
            if age == i:
                if age not in aggregation:
                    aggregation[age] = person_total_contacts[person]
                else:
                    aggregation[age] += person_total_contacts[person]

                if age not in aggregation_counter:
                    aggregation_counter[age] = 1
                else:
                    aggregation_counter[age] += 1


def personHadContact(person, age):
    if person not in person_age:
        person_age[person] = age
    
    if person not in person_total_contacts:
        person_total_contacts[person] = 1
    else:
        person_total_contacts[person] += 1


def parseLine(line):
    values = line.split()                   # Split line on spaces

    if values[0] != EVENT_TYPE:             # First value of the line
        return

    pools = values[4:11]
    if pools.index("1") != POOL_TYPE:       # Check the correct pooltype
        return

    pool_simulation_days.add(values[11])
    personHadContact(values[1], values[2])


def parseFile(filename, result):
    with open(filename) as infile:
            for line in infile:
                parseLine(line)

    aggregateContactsByAge()
    averageContacts(result)


def clearGlobals():
    global person_age, person_total_contacts, aggregation, aggregation_counter, pool_simulation_days, results
    person_age.clear()
    person_total_contacts.clear()

    aggregation.clear()
    aggregation = dict.fromkeys(range(0,101), 0)
    aggregation_counter.clear()
    aggregation_counter = dict.fromkeys(range(0,101), 0)

    pool_simulation_days.clear()

    results.clear()


if __name__ == '__main__':
    begin = time.time()

    df = pd.DataFrame()
    df['age'] = range(0,101)
    print(df)

    # Household
    POOL_TYPE = 0
    print("Household")
    clearGlobals()
    parseFile(FILENAME, results)
    df['Household'] = list(results.values())[:101]

    # K-12 school
    POOL_TYPE = 1
    print("K-12 School")
    clearGlobals()
    parseFile(FILENAME, results)
    df['K-12 school'] = list(results.values())[:101]

    # College
    POOL_TYPE = 2
    print("College")
    clearGlobals()
    parseFile(FILENAME, results)
    df['College'] = list(results.values())[:101]

    # Workplace
    POOL_TYPE = 3
    print("Workplace")
    clearGlobals()
    parseFile(FILENAME, results)
    df['Workplace'] = list(results.values())[:101]

    # Primary community
    POOL_TYPE = 4
    print("Primary")
    clearGlobals()
    parseFile(FILENAME, results)
    df['Primary'] = list(results.values())[:101]

    # Secondary community
    POOL_TYPE = 5
    print("Secondary")
    clearGlobals()
    parseFile(FILENAME, results)
    df['Secondary'] = list(results.values())[:101]

    df.to_csv('reverse_contacts_full_sampling_pSize.csv', index=False)

    '''
    parseFile(FILENAME2, results2)

    for i in range(0,80):
        if (i in results and i in results2):
            print(i, ": ", results[i], "\t", results2[i])

    '''
    end = time.time()
    print("Time: ", end - begin, " seconds\n")

    #plotter()
