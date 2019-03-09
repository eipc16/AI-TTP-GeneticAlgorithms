from Individual import Individual
import numpy as np
import random as r

class GA:
    def __init__(self, pop_size, gen_count, cross_prob, mutation_prob, tour_size):
        self._pop_size = pop_size
        self._gen_count = gen_count
        self._cross_prob = cross_prob
        self._mutation_prob = mutation_prob
        self._tour_size = tour_size

        self._population = []

        self._dims = None
        self._max_capacity = None
        self._min_speed = None
        self._max_speed = None

        self._city_array = None

    def set_data(self, dims, max_capacity, min_speed, max_speed, city_array):
        self._dims = dims
        self._max_capacity = max_capacity
        self._min_speed, self._max_speed = min_speed, max_speed
        self._city_array = city_array

    def init_population(self):
        if self._city_array is not None:
            self._population = []
            for i in range(self._pop_size):
                random_indexes = r.sample(range(self._dims), self._dims)
                #random_indexes = [0, 4, 2, 5]
                random_route = list(map(lambda i: self._city_array[i], random_indexes))
                individual = Individual(random_route, self._min_speed, self._max_speed, self._max_capacity)
                self._population.append(individual)
        else:
            print("Nie podano ilości miast")

    def calc_fitness(self, individual):
        individual.mutate()
        individual.pick_best_items()
        return individual.get_total_profit() - individual.calc_total_time()

    def selection(self, tour_size):
        self._population.sort(key=lambda x: self.calc_fitness(x), reverse=True)
        return self._population[:tour_size]

    def mutate(self):
        pass

    def crossover(self):
        pass
