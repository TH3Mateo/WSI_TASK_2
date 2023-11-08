import numpy as np
import random
from datetime import datetime


def generate_field(n, fill, store=False):
    # generates a random matrix of vertexes of given size and
    # probability of their occurence

    # "store" parameter is used to save the generated seed to a file for future use

    field = np.zeros((n, n), dtype=int)  # makes matriz with 0s
    for i in range(n):
        for j in range(n):
            if random.random() <= fill:  # for every cell sets 1 with probability of "fill"
                field[i, j] = 1

    field = np.triu(field, k=1)  # cuts lower half of matrix to avoid repeating edges

    if store:
        with open("seeds.txt", "a") as f:
            f.write(
                f"--------------{datetime.date(datetime.now())}({datetime.time(datetime.now())})------------------\n")
            np.savetxt(f, field, delimiter=" ", fmt="%d")
            f.write("\n")
    return field


def load_field(file="seeds.txt"):
    # loads the seed from a file
    # to load a seed, mark the timestamp line with "/" at the beginning
    found = False
    with open(file, "r") as f:

        for l_no, line in enumerate(f):
            if "/" in line:
                marker_line = l_no
                dim = int(len(next(f)) / 2)
                found = True
                break
        if not found:
            print("No seed chosen, write '/' on the beginning of the line with seed's creation time ")
            exit()
        f.close()

    return dim, np.loadtxt(file, skiprows=marker_line + 1, max_rows=dim).astype(int)


def generate_population(n, count, percent=0.5):
    # function takes the number of nodes in the graph (n)
    # and the number of individuals in the population (count)

    # geenrates "count" individuals of size "n" with "percent" probability of nodes lit
    # ( works same as generate_field )

    population = np.zeros((count, n), dtype=int)
    for i in range(count):
        for j in range(n):
            if random.random() <= percent:
                population[i, j] = 1

    return population


def compare_matrix(vertexes, lit_nodes):
    # one of core functions, combines vertexes frame with currently checked solution,
    # and returns a sum of base and
    n = len(vertexes)
    mix = np.zeros((n, n), dtype=int)

    mix += lit_nodes

    mix += lit_nodes.reshape(n, 1)
    mix = mix.astype(bool).astype(int)
    mix = np.triu(mix, k=1)
    return mix


def filter_errors(base, test):
    return np.logical_not(np.logical_or(np.logical_not(base), test)).astype(int)


def count_errors(base, test):
    return np.sum(filter_errors(base, test))


def target_function(base, solution, loss_param=10):
    return np.sum(solution) + loss_param * count_errors(base, compare_matrix(base, solution)) ** 2


def selection(population, marks, win_prob=1):
    n = len(population)
    bests = np.zeros((n, len(population[0])), dtype=int)
    for i in range(n):
        a = np.random.randint(0, n)
        b = np.random.randint(0, n)
        if random.random() < win_prob:
            bests[i] = population[a] if marks[a] < marks[b] else population[b]
        else:
            bests[i] = population[a] if marks[a] > marks[b] else population[b]

    return bests


def mutation(population, probability):
    for i in population:
        if random.random() < probability:
            r = random.randint(0, len(i) - 1)
            i[r] = not i[r]
    return population
