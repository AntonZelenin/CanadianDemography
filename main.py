import csv
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import time

default_dpi = mpl.rcParamsDefault['figure.dpi']
mpl.rcParams['figure.dpi'] = default_dpi*2.1


def parse_csv(file_name):
    array = np.zeros(shape=101)

    with open(file_name, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')

        for row in reader:
            array[int(row[0])] = row[1]

    return array


def calc_children(females):
    children_am = 0

    for ind, amount in enumerate(females):
        children_am += amount * (birth_rate_per_thousand[ind] / 1000)

    return children_am


def calc_population(population, mortality_per_thousand):
    new_population = np.zeros(shape=101)

    var = population * mortality_per_thousand / 1000

    for ind, val in enumerate(population - (population * (mortality_per_thousand / 1000))):
        if ind == 100:
            continue

        new_population[ind + 1] = val

    return new_population


males_age = parse_csv('data/age_males.csv')
females_age = parse_csv('data/age_females.csv')
birth_rate_per_thousand = parse_csv('data/birth_rate.csv')
males_mortality_per_thousand = parse_csv('data/mortality_males.csv')
females_mortality_per_thousand = parse_csv('data/mortality_females.csv')
age_immigrants = parse_csv('data/age_immigrants.csv')

male_children_coefficient = 0.5131
female_children_coefficient = 0.4869

female_immigrants_coefficient = 0.5167
male_immigrants_coefficient = 0.4833

for i in range(100):
    if i != 0:
        plt.clf()
        children = calc_children(females_age)

        males_age = calc_population(males_age, males_mortality_per_thousand)
        females_age = calc_population(females_age, females_mortality_per_thousand)

        males_age[0] = children * male_children_coefficient
        females_age[0] = children * female_children_coefficient

        males_age = males_age + (age_immigrants * male_immigrants_coefficient)
        females_age = females_age + (age_immigrants * female_immigrants_coefficient)

    total_population = males_age + females_age

    heights = total_population
    bars = np.arange(len(total_population))

    y_pos = np.arange(len(total_population))

    plt.bar(y_pos, heights)
    plt.xticks(y_pos, bars, rotation=90)

    plt.xlabel('Age')
    plt.ylabel('Amount of people')

    plt.tick_params(labelsize=3)

    total = "{:,}".format(int(total_population.sum()))

    plt.title("Year " + str(2017 + i) + ". Total population " + str(total))
    plt.ylim([0, 700000])

    plt.savefig("temp.png")
    time.sleep(0.2)
