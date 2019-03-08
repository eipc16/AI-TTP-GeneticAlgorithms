import random as r

class Individual:
    def __init__(self, num_of_cities):
        self._route = r.sample(range(num_of_cities), num_of_cities)
        #self._route = [0, 4, 2, 5]
        self._picked_items = []
        self._fitness = 0

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

    def pick_best_items(self, city_array, max_capacity):
        for city_index in self._route:
            curr_city = city_array[city_index]
            best_item = curr_city.get_best_item()
            
            curr_weight = 0

            if best_item is not None and (curr_weight + best_item.get_weight() < max_capacity):
                self._picked_items.append(best_item)
                curr_weight += best_item.get_weight()
            else:
                self._picked_items.append(None)

    def mutate(self):
        pass

    def __repr__(self):
        return str(self._route)