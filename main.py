import numpy as np
import matplotlib.pyplot as plt

from GeneticAlgorithm import GeneticAlgorithm
from Loader import load_data
from TTP import TTP


def run_tests(tests_array):
    print("Number of tests: %d" % (len(tests_array)))
    for test in tests_array:
        save_path = ("results/%s/gen=%d_pop=%d_px=%.2f_pm=%.3f_tour=%d_testCount=%d_%s_%s"
                     % (test['test_name'], test['generations'], test['pop_size'], test['px'],
                        test['pm'], test['tour'], test['testCount'], test['selection_type'], test['mutation_type']))

        print("Starting test")
        print(test)
        dims, capacity, min_speed, max_speed, cities = load_data("data/" + test['test_name'] + ".ttp")
        ttp = TTP(dims, capacity, min_speed, max_speed, cities)
        ga = GeneticAlgorithm(test['pop_size'], test['generations'], test['px'], test['pm'], test['tour'],
                              ttp, test['test_name'], selection_type=test['selection_type'],
                              mutation_type=test['mutation_type'])

        time = [i for i in range(test['generations'] + 1)]

        bests, avgs, worsts = run_algorithm(ga, test['testCount'])
        #save_plot(time, bests, avgs, worsts, save_path, test['testCount'])
        #save_text_data(bests, avgs, worsts, save_path)


def run_algorithm(ga, testCount):
    bests, avgs, worsts = np.array([]), np.array([]), np.array([])
    for i in range(testCount):
        print("Test - %d" % i)
        b, a, w = ga.run()

        if i == 0:
            bests = np.asarray(b)
            avgs = np.asarray(a)
            worsts = np.asarray(w)
        else:
            bests = np.column_stack((bests, np.asarray(b)))
            avgs = np.column_stack((avgs, np.asarray(a)))
            worsts = np.column_stack((worsts, np.asarray(w)))

    return bests, avgs, worsts


def save_plot(time, bests, avgs, worsts, path, testCount):
    plt.plot(time, np.mean(bests, axis=1), label="Najlepszy")
    plt.plot(time, np.mean(avgs, axis=1), label="Średni")
    plt.plot(time, np.mean(worsts, axis=1), label="Najgorszy")
    plt.xlabel("GENERACJA")
    plt.ylabel("FITNESS")
    plt.title("Średni fitness w generacji dla %d prób" % (testCount))
    plt.legend(loc='lower right')
    plt.savefig(path + ".png")
    plt.close()


def save_text_data(bests, avgs, worsts, path):
    with open(path + ".txt", 'w') as file:
        file.write('Średnia fitnessu najlepszych: %f\n' % (np.mean(bests)))
        file.write('Odchylenie standardowe dla najlepszych: %f\n' % (np.std(bests)))
        file.write('Średnia fitnessu w populacji: %f\n' % (np.mean(avgs)))
        file.write('Odchylenie standardowe dla najlepszych: %f\n' % (np.std(avgs)))
        file.write('Sreðnia fitnessu najgorszych: %f\n' % (np.mean(worsts)))
        file.write('Odchylenie standardowe dla najlepszych: %f\n' % (np.std(worsts)))

        file.close()


tests = [
    # {"pop_size": 100, "generations": 100, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "trivial_0", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 100, "generations": 100, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "trivial_1", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # #end of trivial_tests
    # {"pop_size": 100, "generations": 1000, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    {"pop_size": 100, "generations": 100, "px": 0.75, "pm": 0.01,
     "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
     "mutation_type": "swap", "testCount": 1},
    # #end of selection method tests
    # {"pop_size": 20, "generations": 100, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 50, "generations": 100, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 100, "generations": 100, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 500, "generations": 100, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 1000, "generations": 100, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # # end of population size tests
    # {"pop_size": 100, "generations": 20, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 100, "generations": 50, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 100, "generations": 100, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 100, "generations": 500, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 100, "generations": 1000, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # # end of generation count tests
    # {"pop_size": 100, "generations": 100, "px": 0.75, "pm": 0.0,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "inverse", "testCount": 10},
    # {"pop_size": 100, "generations": 100, "px": 0.75, "pm": 0.005,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "inverse", "testCount": 10},
    # {"pop_size": 100, "generations": 100, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "inverse", "testCount": 10},
    # {"pop_size": 100, "generations": 100, "px": 0.75, "pm": 0.1,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "inverse", "testCount": 10},
    # {"pop_size": 100, "generations": 100, "px": 0.75, "pm": 0.5,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "inverse", "testCount": 10},
    # {"pop_size": 100, "generations": 100, "px": 0.75, "pm": 1.0,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "inverse", "testCount": 10},
    # #end of mutation probability tests
    # {"pop_size": 100, "generations": 100, "px": 0.0, "pm": 0.01,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 100, "generations": 100, "px": 0.25, "pm": 0.01,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 100, "generations": 100, "px": 0.5, "pm": 0.01,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 100, "generations": 100, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 100, "generations": 100, "px": 1.0, "pm": 0.01,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # #end of crossover probability tests
    # {"pop_size": 100, "generations": 100, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "inverse", "testCount": 10},
    # {"pop_size": 100, "generations": 100, "px": 0.75, "pm": 0.05,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "inverse", "testCount": 10},
    # end of inverse mutation method tests
    # {"pop_size": 100, "generations": 100, "px": 0.75, "pm": 0.01,
    #  "tour": 0, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 100, "generations": 100, "px": 0.75, "pm": 0.01,
    #  "tour": 1, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 100, "generations": 100, "px": 0.75, "pm": 0.01,
    #  "tour": 25, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 100, "generations": 1000, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 100, "generations": 1000, "px": 0.75, "pm": 0.01,
    #  "tour": 100, "test_name": "medium_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # end of tour size tests
    # {"pop_size": 100, "generations": 500, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "hard_0", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 100, "generations": 500, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "hard_1", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 100, "generations": 500, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "hard_2", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 100, "generations": 500, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "hard_3", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 100, "generations": 500, "px": 0.75, "pm": 0.01,
    #  "tour": 5, "test_name": "hard_4", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # {"pop_size": 100, "generations": 500, "px": 0.75, "pm": 0.01,
    #  "tour": 100, "test_name": "hard_0", "selection_type": "tournament",
    #  "mutation_type": "swap", "testCount": 10},
    # end of hard tests
]

if __name__ == '__main__':
    run_tests(tests)
