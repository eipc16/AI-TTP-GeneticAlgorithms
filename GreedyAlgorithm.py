from Individual import Individual
import random as r
import numpy as np

from TTP import TTP
from Loader import load_data
from Individual import Individual
import matplotlib.pyplot as plt

class GreedyAlgorithm:
    def __init__(self, ttp):
        self.ttp = ttp
        self.first_city = 0

        self.city_array = None

    def pop_next_best(self, city):
        #closest = min(self.city_array, key=lambda c: city.distance_to(c))
        random_index = np.random.randint(len(self.city_array))
        closest = self.city_array[random_index]
        self.city_array.remove(closest)
        return closest

    def find_best_route(self):
        self.city_array = self.ttp.city_array.copy()
        random_start = np.random.randint(self.ttp.dims)
        route = np.array([self.city_array.pop(random_start)])
        for i in range(self.ttp.dims - 1):
            best = self.pop_next_best(route[i])
            route = np.append(route, [best])
            
        return route

dims, capacity, min_speed, max_speed, cities = load_data("data/hard_3.ttp")
ttp = TTP(dims, capacity, min_speed, max_speed, cities)
ga = GreedyAlgorithm(ttp)

TEST_COUNT = 100

individuals = np.array([])
fitnesses = np.array([])

for i in range(TEST_COUNT):
    best_route = ga.find_best_route()
    individual = Individual(best_route)
    fitness = ttp.calc_fitness(individual)
    individuals = np.append(individuals, individual)
    fitnesses = np.append(fitnesses, fitness)
    print('Test %d - Fitness: %f' % (i + 1, fitness))

print('MAX: ' + str(np.max(fitnesses)))
print('AVG: ' + str(np.mean(fitnesses)))
print('MIN: ' + str(np.min(fitnesses)))

best = max(individuals, key=lambda i: ttp.calc_fitness(individual))
best_route = best.route

x = [c.get_x_pos() for c in best_route]
y = [c.get_y_pos() for c in best_route]

plt.plot(x, y)
plt.plot(best_route[0].get_x_pos(), best_route[0].get_y_pos(), marker="v", label='START')
plt.plot(best_route[-1].get_x_pos(), best_route[-1].get_y_pos(), marker="o", label='STOP')
plt.legend(loc='upper right')
plt.show()
