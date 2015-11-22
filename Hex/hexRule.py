from hex import *
from Grid.grid import *


class HexRule(object):

    _rule = []
    _life_rule_offset = 0
    _rule_offset = 7
    _death_rule_offset = 39

    def __init__(self, rule=random.randint(0, 2**46 + 1)):
        if type(rule) is int or type(rule) is long:
            binary_array = []

            for index in xrange(46):
                if (rule & (1 << (45 - index))) != 0:
                    binary_array.append(1)
                else:
                    binary_array.append(0)

            self._rule = binary_array

        else:
            self._rule = rule[0:46]

    def __str__(self):
        rule = "rule(" + str(self.rule_as_int()) + "): " + str(self._rule[7:39]) + "\n"
        rule += "    birth: " + str(self._rule[0:7]) + "\n    death: " + str(self._rule[39:46])
        return rule

    def rule_as_int(self):
        binary_number = 0b0

        for index in xrange(len(self._rule)):
            binary_number += self._rule[index] << (45 - index)

        return binary_number

    def apply_rule(self, grid):
        newGrid = Grid(grid.width, grid.height)
        for x in xrange(grid.width):
            for y in xrange(grid.height):
                value = self.apply_rule_to_cell(x, y, grid)
                newGrid.set(x, y, value)
        return newGrid

    def apply_rule_to_cell(self, x, y, grid):
        hex = roffset_to_cube(EVEN, OffsetCoord(x, y))

        rule_results = 0
        for direction in xrange(6):
            neighborhood = hex_neighbors_to_right_in_direction(hex, direction)
            lookup = self._evaluate_neighborhood(neighborhood, grid)
            if self._rule[lookup + self._rule_offset]:
                rule_results += 1

        life = grid.get(x, y) * self._death_rule_offset
        return self._rule[life + rule_results]

    @staticmethod
    def _evaluate_neighborhood(neighborhood, grid):
        height = grid.height
        width = grid.width

        return_value = 0
        i = 0
        for neighbor in neighborhood:
            offset = roffset_from_cube(EVEN, neighbor)
            x = offset.col
            y = offset.row

            if x < 0:
                x = width + x
            elif x >= width:
                x = x - width

            if y < 0:
                y = height + y
            elif y >= height:
                y = y - height

            return_value += grid.get(x, y) << i
            i += 1

        return return_value
