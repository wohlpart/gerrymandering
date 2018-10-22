from util_methods import *

util = util_methods()
data = util.dummy_data()

lines = util.shortest_split_line(data, 30)
print(lines)