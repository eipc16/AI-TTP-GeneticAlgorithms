from Individual import Individual
import numpy as np

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
        self._dist_matrix = None

    def calc_dist_matrix(self):
        self._dist_matrix = np.zeros([self._dims, self._dims])
        
        for i in range(self._dist_matrix.shape[0]):
            for j in range(self._dist_matrix.shape[1]):
                self._dist_matrix[i, j] = self._city_array[i].distance_to(self._city_array[j])

    def set_data(self, dims, max_capacity, min_speed, max_speed, city_array):
        self._dims = dims
        self._max_capacity = max_capacity
        self._min_speed, self._max_speed = min_speed, max_speed
        self._city_array = city_array

        self.calc_dist_matrix()

    def init_population(self):
        if self._dims is not None:
            for i in range(self._pop_size):
                individual = Individual(self._dims)
                individual.pick_best_items(self._city_array, self._max_capacity)
                self._population.append(individual)
        else:
            print("Nie podano ilości miast")

    def get_curr_speed(self, curr_weight):
        return self._max_speed - (curr_weight / self._max_capacity) * (self._max_speed - self._min_speed) 

    def calc_time_btn_cities(self, start, stop, curr_weight):
        return self._dist_matrix[start, stop] / self.get_curr_speed(curr_weight)

    def calc_total_time(self, route, items):
        curr_weight, curr_profit = 0, 0
        total_time = 0

        curr_city = None

        for i in range(len(route)):
            curr_city = self._city_array[route[i]]
            
            for item in items:
                if item.is_from_city(self._city_array[route[i]]):
                    curr_weight += item.get_weight()
        
            total_time += self.calc_time_btn_cities(route[i], route[i + 1], curr_weight) if i < len(route) - 1 else 0
        
        total_time += self.calc_time_btn_cities(route[len(route) - 1], route[0], curr_weight)

        return total_time

    def calc_fitness(self, individual):
        return individual.get_total_profit() - self.calc_total_time(individual.get_route(), individual.get_items())