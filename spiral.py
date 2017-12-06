import math


class Edge:
    def __init__(self, length, p1, p2):
        self.length = length
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" ' \
               'stroke="rgb({color},{color2},{color})" ' \
               'stroke-width="{width}" ' \
               'stroke-linecap="round"/>' \
               '\n'.format(
                    x1=self.p1[0],
                    y1=self.p1[1],
                    x2=self.p2[0],
                    y2=self.p2[1],
                    color=0,#-math.floor(self.length),
                    color2=0,#-math.floor(self.length),
                    width=self.length*0.05+1
                )


class Tree:
    def __init__(self, point, length):
        self.branches = []
        self.ANGLE_CHANGE = math.pi / 5
        self.LENGTH_CHANGE = 9 / 10
        self.branch((point[0], point[1] - length), length, -math.pi / 2 + self.ANGLE_CHANGE, True)

    def branch(self, point, length, angle, is_left):
        if length <= 1:
            return

        left_angle = (angle - self.ANGLE_CHANGE)  # if is_left else (angle + self.angle_change)
        left_point = move_point(point, length,
                                left_angle)  #(point[0] + math.cos(left_angle)*length, point[1] + math.sin(left_angle)*length)
        self.branches.append(Edge(length, point, left_point))
        self.branch(left_point, length * self.LENGTH_CHANGE, left_angle, is_left)

        # todo: set depth
        new_angle = angle + self.ANGLE_CHANGE * 3# if is_left else angle - self.angle_change*3
        self.branch(left_point, length * self.LENGTH_CHANGE / 3, new_angle, not is_left)

        '''
        right_angle = angle + self.angle_change
        right_point = (point[0] + math.cos(right_angle)*length, point[1] + math.sin(right_angle)*length)
        self.branches.append(Branch(length, point, right_point))
        self.branch(right_point, length/self.length_change, right_angle)
        '''


class SnowFlake:
    def __init__(self, point, length):
        self.branches = []
        self.LENGTH_CHANGE = 1/2
        self.NUMBER_OF_WINGS = 6
        self.ANGLE = math.pi * 2/5
        self.star(point, length)

    def star(self, point, length):
        for i in range(self.NUMBER_OF_WINGS):
            self.branch(point, length, -math.pi/2 + i * 2*math.pi/self.NUMBER_OF_WINGS)

    def branch(self, point, length, angle):
        if length < 1:
            return

        end_point = move_point(point, length, angle)
        self.branches.append(Edge(length, point, end_point))

        for i in range(3):
            first_point = move_point(point, length/2 - i * length / 6, angle)
            self.create_sub_branches(first_point, length / (3 + 2*i), angle)

            if i == 0: # in the center; would be duplicate
                continue
            second_point = move_point(point, length/2 + i * length / 6, angle)
            self.create_sub_branches(second_point, length / (3 + 2*i), angle)

    def create_sub_branches(self, new_point, new_length, angle):
        left_angle = angle - self.ANGLE
        self.branch(new_point, new_length, left_angle)

        right_angle = angle + self.ANGLE
        self.branch(new_point, new_length, right_angle)


def move_point(point, distance, angle):
    return point[0] + math.cos(angle) * distance, point[1] + math.sin(angle) * distance


def export_SVG(name, fractal_edges, canvas):
    with open(name + ".svg", 'w') as file:
        file.write('<svg height="' + str(canvas[0]) + '" width="' + str(canvas[1]) +
                   '" xmlns="http://www.w3.org/2000/svg" version="1.1">\n')
        file.writelines(map(str, fractal_edges))
        file.write('</svg>\n')


tree = Tree((500, 600), 150)
export_SVG("Spiral", tree.branches, (600, 650))

flake = SnowFlake((250, 250), 200)
export_SVG("Snowflake", flake.branches, (500, 500))
