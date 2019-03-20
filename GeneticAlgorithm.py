from Individual import Individual
import random as r
import numpy as np
import csv
import matplotlib.pyplot as plt
import copy

class GeneticAlgorithm:
    def __init__(self, pop_size, gen_limit, px, pm, tour_size, ttp, test_name, visualize=False):
        self.pop_size = pop_size
        self.gen_limit = gen_limit
        self.px = px
        self.pm = pm
        self.tour_size = tour_size
        self.ttp = ttp
        self.test_name = test_name

        self.population = []
        self.old_population = []
        
        if visualize:
            self.bests = []
            self.avgs = []
            self.worsts = []

    def init_population(self):
        self.population.clear()
        for i in range(self.pop_size):
            self.population.append(self.ttp.get_random_individual())

    def visualize(self):
        if self.visualize:
            gens = [i for i in range(self.gen_limit + 1)]
            plt.plot(gens, self.bests, label="BEST")
            plt.plot(gens, self.avgs, label="AVERAGE")
            plt.plot(gens, self.worsts, label="WORST")
            plt.show()
        else:
            print("You have to initiate GeneticAlgorithm class with visualize=True parameter")

    def run(self):
        self.bests, self.avgs, self.worsts = [], [], []
        with open('results/' + self.test_name + '.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['GENERATION', 'BEST', 'AVG', 'WORST'])

            gen = 0
            self.init_population()
            self.evaluate()

            while gen <= self.gen_limit:
                self.selection_tournament()
                self.crossover()
                self.fix_population()
                self.mutation()

                best, avg, worst = self.evaluate()
                print("GEN: %d, BEST: %f\tAVG: %f\tWORST: %f\tPOPULATION: %d" % (gen, best, avg, worst, len(self.population)))
                writer.writerow([str(gen), str(best), str(avg), str(worst)])

                if self.visualize:
                    self.bests.append(best)
                    self.worsts.append(worst)
                    self.avgs.append(avg)

                gen = gen + 1

        return self.select_best(self.population)

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
                

    def selection_tournament(self):
        if self.tour_size == 0:
            return

        r.shuffle(self.population)
        winners = []
        tour_pop = []
        while len(winners) < int(0.5 * len(self.population)):
            tour_pop = r.sample(self.population, self.tour_size)
            best = Individual(self.select_best(tour_pop).route)
            winners.append(best)
            tour_pop.clear()

        self.old_population.clear()
        self.old_population = [i for i in self.population]
        self.population = winners

    def fix_population(self):
        sorted(self.old_population, key=lambda p: p.fitness, reverse=True)
        while len(self.population) < self.pop_size:
           self.population.append(self.old_population.pop())
        # for individual in self.ttp.get_random_individuals(self.pop_size - len(self.population)):
        #     self.population.append(individual)

    def selection_elite(self, percentage):
        sorted_pop = sorted(self.population, key=lambda i: i.fitness, reverse=True)
        elite_threshold = int(self.pop_size * percentage)
        winners = sorted_pop[:elite_threshold]
        self.population = winners

    def mutation(self):
        for individual in self.population:
            mutations_per_individual = sum(np.random.rand(self.ttp.dims) < self.pm)
            for i in range(mutations_per_individual):
                self.mutation_swap(individual.route)
                individual.fitness = None

    def mutation_2(self):
        for individual in self.population:
            if r.random() < self.pm:
                self.mutation_swap(individual.route)
                individual.fitness = None

    def crossover(self):
        r.shuffle(self.population)
        parent_pop_size = len(self.population)
        for i in range(parent_pop_size):
            if r.random() < self.px:
                parent_1, parent_2 = self.population[i], self.population[np.random.randint(parent_pop_size)]
                route_child_1, route_child_2 = self.crossing_ox([c.index for c in parent_1.route], [c.index for c in parent_2.route])
                self.population.append(Individual(self.ttp.get_city_array(route_child_1)))
                self.population.append(Individual(self.ttp.get_city_array(route_child_2)))
                #self.population[i], self.population[i + 1] = Individual(route_child_1), Individual(route_child_2)
        self.population = self.population[parent_pop_size:]

    @staticmethod
    def select_best(group):
        return max(group, key=lambda p: p.fitness)

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
