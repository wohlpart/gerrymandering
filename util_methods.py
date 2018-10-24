import numpy as np
from copy import deepcopy

class util_methods:
    def __init__(self):
        self.size = 50
        self.tl = 0
        self.bl = 0
        self.br = 0

    def dummy_data(self):
        data = []
        for i in range(self.size):
            data.append(np.zeros(self.size))

        for i in range(self.size):
            for j in range(self.size):
                data[i][j] = np.random.randint(10)
        return data

    def shortest_split_line(self, data, district_size):
        total_mass = 0
        x_mass = 0
        y_mass = 0
        for i in range(len(data)):
            for j in range(len(data[0])):
                x_mass += data[i][j] * i
                y_mass += data[i][j] * j
                total_mass += data[i][j]
        if abs(district_size - total_mass) < 100 or total_mass <= district_size:
            return []
        x_center = round(x_mass / total_mass)
        y_center = round(y_mass / total_mass)

        shortest_line = (0, 0)
        shortest_len = 1000000000

        total_districts = round(total_mass / district_size)

        for i in range(len(data) + 1):
            x1 = i
            y1 = 0
            (x2, y2) = self.get_point2(data, x1, y1, x_center, y_center)
            if self.even_split(data, x1, y1, x2, y2, total_districts, district_size):
                dist = self.get_line_len(data, x1, y1, x2, y2)
                if dist < shortest_len:
                    shortest_line = (x1, y1)
                    shortest_len = dist

        for i in range(len(data[0]) + 1):
            x1 = len(data)
            y1 = i
            (x2, y2) = self.get_point2(data, x1, y1, x_center, y_center)

            if self.even_split(data, x1, y1, x2, y2, total_districts, district_size):
                dist = self.get_line_len(data, x1, y1, x2, y2)
                if dist < shortest_len:
                    shortest_line = (x1, y1)
                    shortest_len = dist

        start = shortest_line

        end = self.get_point2(data, shortest_line[0], shortest_line[1], x_center, y_center)

        first_data = [deepcopy(row) for row in data]
        second_data = [deepcopy(row) for row in data]

        for i in range(len(data)):
            for j in range(len(data[0])):
                d = ((i - start[0]) * (end[1] - start[1])) - ((j - start[1]) * (end[0] - start[0]))
                if d < 0:
                    first_data[i][j] = 0
                else:
                    second_data[i][j] = 0

        return [self.trim(data, start[0], start[1], end[0], end[1])] + \
               self.shortest_split_line(first_data, district_size) + \
               self.shortest_split_line(second_data, district_size)

    def even_split(self, data, x1, y1, x2, y2, total, size):
        tolerance = 0.05
        first = 0
        sec = 0

        for i in range(len(data)):
            for j in range(len(data[0])):
                d = ((j - x1) * (y2 - y1)) - ((i - y1) * (x2 - x1))
                if d < 0:
                    first += data[i][j]
                else:
                    sec += data[i][j]

        if total % 2 == 0:
            if first - sec < total * tolerance:
                return True
            return False

        else:
            if first - sec < size + total * tolerance:
                return True
            return False

    def get_line_len(self, data, x1, y1, x2, y2):
        (x1_new, y1_new), (x2_new, y2_new) = self.trim(data, x1, y1, x2, y2)
        return np.sqrt((x1_new - x2_new) ** 2 + (y1_new - y2_new) ** 2)

    def get_point2(self, data, x, y, center_x, center_y):
        x1 = 0
        x2 = len(data)
        y1 = 0
        y2 = len(data[0])
        if int(x) == int(center_x):
            if int(y) == int(y2):
                return (x, y1)
            return (x, y2)
        if int(y) == int(center_y):
            if int(x) == int(x2):
                return (x1, y)
            return (x2, y)

        slope = (y - center_y) / (x - center_x)
        b = y - (slope * x)

        for x_pt in [x1, x2]:
            y_pt = round(x_pt * slope + b)

            if (abs(x_pt - x) > 2 or abs(y_pt - y) > 2) and 0 <= y_pt <= y2:
                return (x_pt, y_pt)

        for y_pt in [y1, y2]:

            x_pt = round((y_pt - b) / slope)
            if (abs(x_pt - x) > 2 or abs(y_pt - y) > 2) and 0 <= x_pt <= x2:
                return (x_pt, y_pt)
        return False

    def trim(self, data, x1, y1, x2, y2):
        x1_trim = round(x1)
        y1_trim = round(y1)

        x2_trim = round(x2)
        y2_trim = round(y2)

        x1_start = round(x1)
        y1_start = round(y1)

        x2_start = round(x2)
        y2_start = round(y2)

        v_x = x2 - x1
        v_y = y2 - y1
        len_v = np.sqrt(v_x ** 2 + v_y ** 2)
        i = 1

        x_mod = 0
        y_mod = 0
        if x1_trim == self.size:
            x_mod = 1
            x1_start -= 1
            x1_trim -= 1
        if y1_trim == self.size:
            y_mod = 1
            y1_start -= 1
            y1_trim -= 1

        while data[int(x1_trim)][int(y1_trim)] == 0 and i < len_v/2:
            x1_trim = x1_start + round(v_x * i / len_v)
            y1_trim = y1_start + round(v_y * i / len_v)
            i += 1
        x1_trim += x_mod
        y1_trim += y_mod

        v_x = x1 - x2
        v_y = y1 - y2
        i = 1

        x_mod = 0
        y_mod = 0
        if x2_trim == self.size:
            x_mod = 1
            x2_start -= 1
            x2_trim -= 1
        if y2_trim == self.size:
            y_mod = 1
            y2_start -= 1
            y2_trim -= 1

        while data[int(x2_trim)][int(y2_trim)] == 0 and i < len_v/2:
            x2_trim = x2_start + round(v_x * i / len_v)
            y2_trim = y2_start + round(v_y * i / len_v)
            i += 1

        x2_trim += x_mod
        y2_trim += y_mod
        return (x1_trim, y1_trim), (x2_trim, y2_trim)

    def generate_mapping(self, coordinates, density):
        dat = []
        for i in range(self.size):
            temp = []
            for j in range(self.size):
                temp.append(0)
            dat.append(temp)

        f = open(coordinates, "r")
        cor = f.read()
        cor = cor.replace("\"", " ")
        cor = cor.replace("\'", " ")
        cor = cor.replace("\t", " ")
        cor = cor.replace(" ", " ")
        ls = cor.split("\n")

        vals = {}
        for line in ls:
            i = 1
            lst = line.split(" ")
            name = lst[0]
            left = int(lst[i+1] + lst[i+2] + lst[i+3])
            i = 2
            right = int(lst[i+5] + lst[i+6] + lst[i+7])
            i=3
            up = int(lst[i+9] + lst[i+10] + lst[i+11])
            i=4
            down = int(lst[i+13] + lst[i+14] + lst[i+15])
            vals[name] = [left, right, up, down]
        x_min = 100000000
        y_min = 100000000
        x_max = 0
        y_max = 0
        for key in vals.keys():
            p = vals[key]
            if p[1] < x_min:
                x_min = p[1]
            if p[0] > x_max:
                x_max = p[0]
            if p[3] < y_min:
                y_min = p[3]
            if p[2] > y_max:
                y_max = p[2]

        self.tl, self.bl, self.br = [x_max, y_max], [x_max, y_min], [x_min, y_min]

        f = open(density, "r")
        dens = f.read()
        lines = dens.split("\n")
        pop_dens = {}
        for line in lines:
            data = line.split(" - ")[1].split(",")
            name = data[0].split(" ")[0]
            pop = float(data[2])
            area = float(data[4].split(".")[0])
            pop_dens[name] = round(pop/area, 2)

        to_remove = []
        for c in vals:
            if c not in pop_dens.keys():
                to_remove.append(c)
        for c in to_remove:
            vals.pop(c)

        for i in range(self.size):
            for j in range(self.size):
                place = self.get_cor(i, j)
                for key in vals.keys():
                    val = vals[key]
                    if self.con(place, val):
                        dat[i][j] = pop_dens[key]
        return dat

    def get_cor(self, x, y):
        width = abs(self.bl[0] - self.br[0])
        height = abs(self.tl[1] - self.bl[1])

        unit_width = width / self.size
        x_cor = unit_width * x + self.br[0]

        unit_height = height / self.size
        y_cor = unit_height * y + self.br[1]

        return x_cor, y_cor

    def con(self, place, val):
        x_cor, y_cor = place
        west, east, north, south = val

        return east <= x_cor <= west and south <= y_cor <= north