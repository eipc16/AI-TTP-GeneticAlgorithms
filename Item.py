class Item:
    def __init__(self, index, profit, weight, city_id):
        self._index =  index
        self._profit = profit
        self._weight = weight
        self._city_id = city_id

    def get_city_id(self):
        return self._city_id

    def is_from_city(self, city_id):
        return self._city_id == city_id

    def calc_value(self):
        return self._profit

    def get_weight(self):
        return self._weight

    def get_profit(self):
        return self._profit

    def __repr__(self):
        return  "(Item: %d, Profit:%d, Weight:%d)" %(self._index, self._profit, self._weight)
