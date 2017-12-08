import math
import random


class Edge:
    def __init__(self, length, p1, p2):
        self.length = length
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" ' \
               'stroke="rgb(0,0,0)" ' \
               'stroke-width="{width}" ' \
               'stroke-linecap="round"/>' \
               '\n'.format(
                    x1=self.p1[0],
                    y1=self.p1[1],
                    x2=self.p2[0],
                    y2=self.p2[1],
                    width=self.length*0.05+1
                )


class Spiral:
    def __init__(self, point, length):
        self.branches = []
        self.ANGLE_CHANGE = math.pi / 5
        self.LENGTH_CHANGE = 9 / 10
        self.branch((point[0], point[1] - length), length, -math.pi / 2 + self.ANGLE_CHANGE, True)

    def branch(self, point, length, angle, is_left):
        """ The recursive algorithm of the spiral: in each vertex, it continues with the spiral
         and creates new smaller spiral with opposite direction """
        if length <= 1:
            return

        new_angle = (angle - self.ANGLE_CHANGE) if is_left else (angle + self.ANGLE_CHANGE)
        new_point = move_point(point, length, new_angle)
        self.branches.append(Edge(length, point, new_point))

        self.branch(new_point, length * self.LENGTH_CHANGE, new_angle, is_left)  # Continue with the spiral
        self.branch(new_point, length * self.LENGTH_CHANGE / 3, new_angle, not is_left)  # New spiral


class Snowflake:
    """ Randomly generated snowflake fractal """
    def __init__(self, point, length):
        self.branches = []
        self.LENGTH_CHANGE = 1/2
        self.N_OF_INITIAL_WINGS = random.randint(5, 8)
        self.N_OF_SUBWINGS = random.randint(2, 4)
        self.LENGTH_FACTOR_1 = random.random()/2 + 1  # changes the initial length of edges
        self.LENGTH_FACTOR_2 = random.random() + 0.8  # changes the decreasing factor of edges
        self.ANGLE = math.pi * (random.random()/5 + 0.3)
        self.star(point, length)

    def star(self, point, length):
        """ Create the initial wings of the snowflake """
        for i in range(self.N_OF_INITIAL_WINGS):
            self.branch(point, length, -math.pi / 2 + i * 2 * math.pi / self.N_OF_INITIAL_WINGS)

    def branch(self, point, length, angle):
        """ The recursive algorithm: edges on both sides of the bigger edge,
        with increasing and then decreasing length """
        if length < 1:
            return

        end_point = move_point(point, length, angle)
        self.branches.append(Edge(length, point, end_point))

        # start from the central longest edge and continue to vertices in both directions
        for i in range(self.N_OF_SUBWINGS):
            for side in (1, -1):
                new_point = move_point(point, length/2 + side * i * length / (2 * self.N_OF_SUBWINGS), angle)
                new_length = length * self.LENGTH_CHANGE / (self.LENGTH_FACTOR_1 + self.LENGTH_FACTOR_2 * i)
                self.create_sub_branches(new_point, new_length, angle)

                # don't draw the center wing again
                if i == 0:
                    break

    def create_sub_branches(self, new_point, new_length, angle):
        """ Create left and right wing of the snowflake """
        for direction in (1, -1):
            new_angle = angle + direction * self.ANGLE
            self.branch(new_point, new_length, new_angle)


class KochFlake:
    def __init__(self, point, length):
        self.edges = []
        self.NUMBER_OF_EDGES = 3
        self.start(point, length)

    def start(self, point, length):
        angle = -math.pi/self.NUMBER_OF_EDGES

        for i in range(self.NUMBER_OF_EDGES):
            self.edge(point, length, angle)
            new_point = move_point(point, length, angle)
            angle += math.pi*2/self.NUMBER_OF_EDGES
            point = new_point

    def edge(self, point, length, angle):
        last_vertex = move_point(point, length, angle)

        if length < 5:
            self.edges.append(Edge(length, point, last_vertex))
            return

        new_length = length/3
        for angle_change in (0, -math.pi/3, math.pi*2/3, -math.pi/3):
            angle += angle_change
            self.edge(point, new_length, angle)
            point = move_point(point, new_length, angle)


def move_point(point, distance, angle):
    return point[0] + math.cos(angle) * distance, point[1] + math.sin(angle) * distance


def export_SVG(name, fractal_edges, canvas):
    with open(name + ".svg", 'w') as file:
        file.write('<svg height="' + str(canvas[0]) + '" width="' + str(canvas[1]) +
                   '" xmlns="http://www.w3.org/2000/svg" version="1.1">\n')
        file.writelines(map(str, fractal_edges))
        file.write('</svg>\n')


def main():
    spiral = Spiral((500, 600), 150)
    export_SVG("Spiral", spiral.branches, (600, 650))

    for i in range(8):
        flake = Snowflake((250, 250), 200)
        export_SVG("Snowflake" + str(i), flake.branches, (500, 500))

    koch = KochFlake((20, 165), 180)
    export_SVG("Kochflake", koch.edges, (220, 220))


if __name__ == "__main__":
    main()
