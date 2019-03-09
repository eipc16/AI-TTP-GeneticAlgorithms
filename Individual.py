import random as r

class Individual:
    def __init__(self, route, min_speed, max_speed, max_capacity):
        self._route = route
        self._picked_items = []
        self._fitness = 0

        self._min_speed = min_speed
        self._max_speed = max_speed
        self._max_capacity = max_capacity

    def get_fitness(self):
        return self._fitness

    def get_route(self):
        return self._route

    def add_item(self, item):
        self._picked_items.append(item)

    def get_items(self):
        return self._picked_items

    def get_total_weight(self):
        return sum(map(lambda x: x.get_weight() if x is not None else 0, self._picked_items))

    def get_total_profit(self):
        return sum(map(lambda x: x.get_profit() if x is not None else 0, self._picked_items))

    def pick_best_items(self):
        self._picked_items = []

        for city in self._route:
            best_item = city.get_best_item()

            curr_weight = 0

            if best_item is not None and (curr_weight + best_item.get_weight() < self._max_capacity):
                self._picked_items.append(best_item)
                curr_weight += best_item.get_weight()
            else:
                self._picked_items.append(None)

    def get_curr_speed(self, curr_weight):
        return self._max_speed - (curr_weight / self._max_capacity) * (self._max_speed - self._min_speed) 

    def calc_time_btn_cities(self, start, stop, curr_weight):
        return start.distance_to(stop) / self.get_curr_speed(curr_weight)

    def calc_total_time(self):
        curr_weight, curr_profit = 0, 0
        total_time = 0

        
        for i in range(len(self._picked_items)):
            curr_item = self._picked_items[i]

            if curr_item is not None:
                curr_weight += curr_item.get_weight()

            total_time += self.calc_time_btn_cities(self._route[i], self._route[i + 1], curr_weight) if i < len(self._route) - 1 else 0

        total_time += self.calc_time_btn_cities(self._route[len(self._route) - 1], self._route[0], curr_weight)

        return total_time

    def mutate(self):
        [first, second] = r.sample(range(len(self._route)), 2)
        self._route[first], self._route[second] = self._route[second], self._route[first]

    def crossover(self, other):
        pass

    def __repr__(self):
        return str(self._route)