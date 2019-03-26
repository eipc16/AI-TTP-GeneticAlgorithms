from Individual import Individual
import numpy as np
import random as r


class TTP:
    def __init__(self, dims, max_capacity, min_speed, max_speed, city_array):
        self.dims = dims
        self.max_capacity = max_capacity
        self.min_speed, self.max_speed = min_speed, max_speed
        self.city_array = city_array

        self.dist_matrix = self.calc_dist_matrix(city_array)

    def get_random_individual(self):
        random_indexes = r.sample(range(self.dims), self.dims)
        return Individual(self.get_city_array(random_indexes))

    def get_random_individuals(self, number):
        individuals = []
        for i in range(number):
            individuals.append(self.get_random_individual())
        return individuals

    def get_city_array(self, indexes):
        return list(map(lambda i: self.city_array[i], indexes))

    def calc_dist_matrix(self, city_array):
        dist_matrix = np.zeros([self.dims, self.dims])

        for i in range(len(city_array)):
            for j in range(len(city_array)):
                dist_matrix[i, j] = self.city_array[i].distance_to(self.city_array[j])

        return dist_matrix

    def get_curr_speed(self, curr_weight):
        return self.max_speed - (curr_weight / self.max_capacity) * (self.max_speed - self.min_speed)

    def calc_time_btn_cities(self, start, stop, curr_weight):
        return self.dist_matrix[start, stop] / self.get_curr_speed(curr_weight)

    def calc_total_time(self, route):
        curr_weight, curr_profit = 0, 0
        total_time = 0

        curr_city = None

        for i in range(len(route)):
            curr_city = self.city_array[i]
            curr_item = curr_city.get_best_item(self.max_capacity - curr_weight)

            if curr_item is not None:
                curr_weight += curr_item.get_weight()

            total_time += self.calc_time_btn_cities(route[i].index, route[i + 1].index, curr_weight) if i < len(
                route) - 1 else 0

        total_time += self.calc_time_btn_cities(route[-1].index, route[0].index, curr_weight)

        return total_time

    def calc_fitness(self, individual):
        individual.pick_best_items(self.max_capacity)
        return np.round(individual.get_total_profit() - self.calc_total_time(individual.route),
                        decimals=2)
