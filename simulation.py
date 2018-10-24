from util_methods import *

util = util_methods()

data = util.generate_mapping("ohio_cord", "ohio_dens")
total_pop = 0
for d in data:
    for j in d:
        total_pop += j
district_size = round(total_pop / 16, 2)

lines = util.shortest_split_line(data, district_size)

for line in lines:
    start, end = line
    x1, y1 = util.get_cor(start[0], start[1])
    x2, y2 = util.get_cor(end[0], end[1])
    print(str(x1) + " " + str(y1) + " -> " + str(x2) + " " + str(y2))
