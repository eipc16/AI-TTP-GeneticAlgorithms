import random as r
import copy


class Individual:
    def __init__(self, route):
        self.route = route
        self.picked_items = []
        self.fitness = None

    def get_total_weight(self):
        return sum(map(lambda x: x.get_weight() if x is not None else 0, self.picked_items))

    def get_total_profit(self):
        return sum(map(lambda x: x.get_profit() if x is not None else 0, self.picked_items))

    def pick_best_items(self, max_capacity):
        curr_weight = 0
        self.picked_items = []
        for city in self.route:
            best_item = city.get_best_item(max_capacity - curr_weight)

            if best_item is not None and (curr_weight + best_item.get_weight() <= max_capacity):
                self.picked_items.append(best_item)
                curr_weight += best_item.get_weight()
            else:
                self.picked_items.append(None)

    def __repr__(self):
        return str(self.route)
