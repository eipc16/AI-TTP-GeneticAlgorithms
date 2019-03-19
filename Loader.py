from City import City
from Item import Item

import re

def format_string(string):
    r_chars = ["\t", "\n", ":"]
    f_string = string
    for char in r_chars:
        f_string = f_string.replace(char, "")

    return ''.join(filter(lambda x: x.isdigit() or x == ".", f_string))

def get_meta_data(data):
    dimension, number_of_items = int(format_string(data[0])), int(format_string(data[1]))
    knapsack_capacity = int(format_string(data[2]))
    min_speed, max_speed = float(format_string(data[3])), float(format_string(data[4]))
    rent_ratio = float(format_string(data[5]))

    return dimension, number_of_items, knapsack_capacity, min_speed, max_speed

def load_cities(city_data):
    city_array = []

    for i in range(len(city_data)):
        index, x_pos, y_pos = re.findall(r"[-+]?\d*\.\d+|\d+", city_data[i])
        city_array.append(City(int(index), float(x_pos), float(y_pos)))

    return city_array

def assign_items_to_city(city_array, item_data):
    for i in range(len(item_data)):
        index, profit, weight, city_id = re.findall("\d+", item_data[i])
        city_array[int(city_id) - 1].add_item(Item(int(index), int(profit), int(weight), int(city_id)))
    
def load_data(filename):
    with open(filename, "r") as f:
        data = f.readlines()

        meta_data = get_meta_data(data[2:10])
        dims, num_items, capacity, min_speed, max_speed = meta_data

        city_array = load_cities(data[10:dims+10])
        assign_items_to_city(city_array, data[dims+11: dims+num_items+11])

    return dims, capacity, min_speed, max_speed, city_array