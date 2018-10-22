import numpy as np
from copy import deepcopy

class util_methods:
    def __init__(self):
        self.size = 10

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
                x_mass += data[i][j] * j
                y_mass += data[i][j] * i
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

        print(start)
        print(end)
        print(y_center)
        print(x_center)

        for i in range(len(data)):
            for j in range(len(data[0])):
                d = ((j - start[0]) * (end[1] - start[1])) - ((i - start[1]) * (end[0] - start[0]))
                if d < 0:
                    first_data[i][j] = 0
                else:
                    second_data[i][j] = 0
        for d in data:
            print(d)
        print()
        for d in first_data:
            print(d)
        print()
        for d in second_data:
            print(d)
        print()
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
        if x == center_x:
            if x == x2:
                return (x1, y)
            return (x2, y)

        slope = (y - center_y) / (x - center_x)
        b = y - (slope * x)

        for x_pt in [x1, x2]:
            y_pt = round(x_pt * slope + b)

            if (x_pt != x or y_pt != y) and 0 <= y_pt <= y2:
                return (x_pt, y_pt)

        for y_pt in [y1, y2]:

            x_pt = round((y_pt - b) / slope)
            if (x_pt != x or y_pt != y) and 0 <= x_pt <= x2:
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
