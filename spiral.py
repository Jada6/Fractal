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
                    color=50+math.floor(self.length),
                    color2=100+math.floor(self.length),
                    width=self.length*0.1+2
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
        left_point = (point[0] + math.cos(left_angle)*length, point[1] + math.sin(left_angle)*length)
        self.branches.append(Edge(length, point, left_point))
        self.branch(left_point, length * self.LENGTH_CHANGE, left_angle, is_left)

        #if not is_first:
        new_angle = angle + self.ANGLE_CHANGE * 3# if is_left else angle - self.angle_change*3
        self.branch(left_point, length * self.LENGTH_CHANGE / 3, new_angle, not is_left)

        '''
        right_angle = angle + self.angle_change
        right_point = (point[0] + math.cos(right_angle)*length, point[1] + math.sin(right_angle)*length)
        self.branches.append(Branch(length, point, right_point))
        self.branch(right_point, length/self.length_change, right_angle)
        '''

    def export_SVG(self):
        with open("spiral.svg", 'w') as file:
            file.write('<svg height="500" width="800" xmlns="http://www.w3.org/2000/svg" version="1.1">\n')
            file.writelines(map(str, self.branches))
            file.write('</svg>\n')


tree = Tree((400, 400), 100)
tree.export_SVG()
