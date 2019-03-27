from Individual import Individual
import random as r
import numpy as np
import csv
import matplotlib.pyplot as plt
import copy


class GeneticAlgorithm:
    def __init__(self, pop_size, gen_limit, px, pm, tour_size, ttp, test_name, elitism=0.0, selection_type='tournament',
                 mutation_type='swap'):
        self.pop_size = pop_size
        self.gen_limit = gen_limit
        self.px = px
        self.pm = pm
        self.tour_size = tour_size
        self.ttp = ttp
        self.test_name = test_name

        self.population = []
        self.old_population = []

        self.bests = []
        self.avgs = []
        self.worsts = []

        self.elitism = elitism
        self.mutation_type = mutation_type
        self.selection_type = selection_type

    def init_population(self):
        self.population.clear()
        for i in range(self.pop_size):
            self.population.append(self.ttp.get_random_individual())

    def run(self):
        self.bests, self.avgs, self.worsts = [], [], []
        gen = 0
        self.init_population()
        self.evaluate()

        while gen <= self.gen_limit:
            self.selection()
            self.crossover()
            self.mutation()

            best, avg, worst = self.evaluate()
            # print("GEN: %d, BEST: %f\tAVG: %f\tWORST: %f\tPOPULATION: %d" % (gen, best, avg, worst, len(self.population)))

            self.bests.append(best)
            self.worsts.append(worst)
            self.avgs.append(avg)

            gen = gen + 1

        # best = self.select_best(self.population)
        # best_route = best.route

        # x = [c.get_x_pos() for c in best_route]
        # y = [c.get_y_pos() for c in best_route]

        # plt.plot(x, y)
        # plt.plot(x[0], y[0], marker="v", label='START')
        # plt.plot(x[-1], y[-1], marker="o", label='STOP')
        # plt.legend(loc='upper right')
        # plt.show()
        
        return self.bests, self.avgs, self.worsts

    def evaluate(self):
        best, avg, worst = -np.inf, 0.0, np.inf
        for i in range(self.pop_size):
            if self.population[i].fitness is None:
                self.population[i].fitness = self.ttp.calc_fitness(self.population[i])

            if self.population[i].fitness > best:
                best = self.population[i].fitness
            elif self.population[i].fitness < worst:
                worst = self.population[i].fitness

            avg += self.population[i].fitness

        return best, np.round(avg / self.pop_size, decimals=2), worst

    def select_elite(self, percent):
        sorted_pop = sorted(self.population, key=lambda k: k.fitness, reverse=True)
        threshold = int(self.pop_size * percent)
        return sorted_pop[:threshold]

    def selection(self):
        if self.selection_type == 'tournament':
            self.selection_tournament()
        elif self.selection_type == 'roulette':
            self.selection_roulette()

    def selection_tournament(self):
        if self.tour_size == 0:
            return
        r.shuffle(self.population)
        selected = []
        while len(selected) < len(self.population):
            tour_pop = r.sample(self.population, self.tour_size)
            best = self.select_best(tour_pop)
            selected.append(best)
            tour_pop.clear()

        self.population = selected

    def selection_roulette(self):
        selected = []
        for i in range(self.pop_size):
            r.shuffle(self.population)
            selected.append(self.selection_roulette_pick())
        self.population = selected

    def selection_roulette_pick(self):
        worst = self.select_worst(self.population)
        fitness_sum = sum((individual.fitness - worst.fitness * 0.95) for individual in self.population)
        pick = r.uniform(0, fitness_sum)
        current = 0
        for individual in self.population:
            current += (individual.fitness - worst.fitness * 0.95)
            if current > pick:
                return individual

    def crossover(self):
        r.shuffle(self.population)
        parent_pop_size = len(self.population)
        for i in range(0, parent_pop_size, 2):
            if r.random() < self.px and i + 1 < parent_pop_size:
                parent_1, parent_2 = self.population[i], self.population[i + 1]
                route_child_1, route_child_2 = self.crossing_ox([c.index for c in parent_1.route],
                                                                [c.index for c in parent_2.route])
                child_1, child_2 = Individual(self.ttp.get_city_array(route_child_1)), Individual(
                    self.ttp.get_city_array(route_child_2))
                self.population[i], self.population[i + 1] = child_1, child_2

    def mutation(self):
        for individual in self.population:
            mutations_per_individual = sum(np.random.rand(self.ttp.dims) < self.pm)
            for i in range(mutations_per_individual):
                if self.mutation_type == 'swap':
                    self.mutation_swap(individual.route)
                elif self.mutation_type == 'inverse':
                    self.mutation_inverse(individual.route)
                individual.fitness = None

    @staticmethod
    def select_best(group):
        return max(group, key=lambda p: p.fitness)

    def select_worst(self, group):
        return min(group, key=lambda p: p.fitness)

    @staticmethod
    def mutation_swap(route):
        index_1, index_2 = r.sample(range(len(route)), 2)
        route[index_1], route[index_2] = route[index_2], route[index_1]

    @staticmethod
    def mutation_inverse(route):
        index_1, index_2 = r.sample(range(len(route)), 2)
        min_, max_ = min(index_1, index_2), max(index_1, index_2)
        route[min_: max_] = reversed(route[min_:max_])

    @staticmethod
    def crossing_ox(route_parent_1, route_parent_2):
        def fix(child, parent):
            rest = [i for i in parent if i not in child]
            return list(map(lambda i: i if i != -1 else rest.pop(0), child))

        index_1, index_2 = r.sample(range(len(route_parent_1)), 2)
        min_, max_ = min(index_1, index_2), max(index_1, index_2)
        route_child_1, route_child_2 = [-1] * len(route_parent_1), [-1] * len(route_parent_1)
        route_child_1[min_:max_], route_child_2[min_:max_] = route_parent_1[min_:max_], route_parent_2[min_:max_]
        return fix(route_child_1, route_parent_2), fix(route_child_2, route_parent_1)
