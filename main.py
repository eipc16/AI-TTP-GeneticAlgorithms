import numpy as np
import re
import csv

from GeneticAlgorithm import GeneticAlgorithm
from Loader import load_data
from TTP import TTP

POP_SIZE = 100
GEN = 100
PX = 0.7
PM = 0.01
TOUR = 10
TEST_NAME = 'hard_4'

dims, capacity, min_speed, max_speed, cities = load_data("data/" + TEST_NAME + ".ttp")

ttp = TTP(dims, capacity, min_speed, max_speed, cities)
ga = GeneticAlgorithm(POP_SIZE, GEN, PX, PM, TOUR, ttp, TEST_NAME, visualize=True)
best = ga.run()
ga.visualize()

import matplotlib.pyplot as plt

plt.plot([c.get_x_pos() for c in best.route], [c.get_y_pos() for c in best.route], '-o')
plt.plot(best.route[0].get_x_pos(), best.route[0].get_y_pos(), '-go', label='START')
plt.plot(best.route[-1].get_x_pos(), best.route[-1].get_y_pos(), '-ro', label='STOP')
plt.legend(loc='upper right')
plt.show()

print(best.route)
print(best.picked_items)
print("WEIGHT: %d | MAX_WEIGHT: %d" % (best.get_total_weight(), capacity))
print("PROFIT: %d" % (best.get_total_profit()))
print("FITNESS: %f" % (best.fitness))