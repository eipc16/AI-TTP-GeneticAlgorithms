import random as r

class Route:
    def __init__(self, num_of_cities):
        self._route = r.sample(range(num_of_cities), num_of_cities)
        self._fitness = 0

    def set_fitness(self, fitness):
        self._fitness = fitness

    def get_fitness(self):
        return self._fitness

    def get_cities(self):
        return self._route

    def mutate(self):
        pass

    def cross(self, other):
        pass

    def __repr__(self):
        return str(self._route)