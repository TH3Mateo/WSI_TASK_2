import numpy as np

# from datetime import datetime
import time

from graphs import *
from logic import *

# *****************number of nodes (problem size) ********************
s = 200
# *****************number of individuals in population ***************
n = 100
# *****************number of iterations ******************************
iterations = 4000
# *****************filling the graph *********************************
fill = 0.02
# ****************filling start population with ones *****************
fill_pop = 0.3
# *****************probability of mutation ***************************
mut = 0.1
# *****************loss multiplier ***********************************
loss_multiplier = 100
# *****************probability of better solution winning ************
good_win_prob = 1


def main():
    # if using previously generated seed, uncomment the line below
    # s,vertexes = load_field()
    # matrix_print(vertexes)
    #
    vertexes = generate_field(s, fill, store=True)
    matrix_print(vertexes)
    #
    # generating n individuals with s nodes
    population = generate_population(s, n, fill_pop)
    problem = show_field(vertexes)

    # first marking of individuals
    marks = [target_function(vertexes, i) for i in population]

    time_start = time.time()
    for i in range(iterations):
        population = selection(population, marks, good_win_prob)
        population = mutation(population, mut)
        marks = [target_function(vertexes, i, loss_param=loss_multiplier) for i in population]
        print(marks)
    time_end = time.time()

    print("Best mark: ", target_function(vertexes, population[np.argmin(marks)]))
    print("Best solution: ", population[np.argmin(marks)])
    out = compare_matrix(vertexes, population[np.argmin(marks)])
    err = filter_errors(vertexes, out)
    print("Time elapsed: ", time_end - time_start)
    # matrix_print(err)
    show_update(problem, out, vertexes, population[np.argmin(marks)])


if __name__ == '__main__':
    main()
