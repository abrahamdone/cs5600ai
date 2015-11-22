#!/usr/bin/env python
"""
http://codereview.stackexchange.com/questions/15304/generating-a-1d-cellular-automata-in-python
"""
from pyevolve import G1DList, GSimpleGA
from backports import lzma
from Hex.hexRule import *
import operator


calculated_rules = dict()


def compress_image(image):
    compressed = lzma.compress(bytearray(image))
    return compressed.__sizeof__()


def compress_images(images):
    compressed = []
    for image in images:
        compressed.append(compress_image(image))

    return compressed


def normalized_compression_distance(comp_i_j, comp_i, comp_j):
    num = comp_i_j - min(comp_i, comp_j)
    return num / (1.0 * max(comp_i, comp_j))


def normalized_compression_distance_matrix(images, compressed):
    normalized = []
    for i in xrange(0, len(compressed)):
        row = []
        for j in xrange(0, len(compressed)):
            if i > j:
                comp = images[i]
                comp.extend(images[j])
                comp_i_j = compress_image(comp)
                row.append(normalized_compression_distance(comp_i_j, compressed[i], compressed[j]))

        normalized.append(row)

    return normalized


def evaluate_set_complexity(images):
    compressed = compress_images(images)
    normalized = normalized_compression_distance_matrix(images, compressed)

    set_complexity = 0
    for i, row in enumerate(normalized):
        sum_p = 0
        for p in row:
            sum_p += p * (1 - p)
        set_complexity += compressed[i] * sum_p

    return set_complexity


def evaluate_rule(grid, rule, burn_in, store):
    tick = 0
    images = []

    while tick <= burn_in + store:
        new_grid = rule.apply_rule(grid)

        if grid.array == new_grid.array:
            return 0
        else:
            grid = new_grid

        if tick > burn_in:
            grid_array = []
            for row in grid.array:
                grid_array.extend(row)
            images.append(grid_array)

        tick += 1

    value = evaluate_set_complexity(images)

    return value


def fitness_function(rule=random.randint(0, 2**46 + 1)):

    seed = 1234
    n = 16
    burn_in = 50
    save_states = 5

    hex_rule = HexRule(rule)
    print hex_rule

    if not hex_rule.rule_as_int() in calculated_rules:

        light = evaluate_rule(LIGHT_GRID, hex_rule, burn_in, save_states)
        print "    light: " + str(light)
        medium = evaluate_rule(MEDIUM_GRID, hex_rule, burn_in, save_states)
        print "    medium: " + str(medium)
        dense = evaluate_rule(DARK_GRID, hex_rule, burn_in, save_states)
        print "    dense: " + str(dense)

        max_value = max(light, medium, dense)
        calculated_rules[hex_rule.rule_as_int()] = max_value

    else:
        print("    already know this one")

        max_value = calculated_rules[hex_rule.rule_as_int()]

    print "    max value: " + str(max_value)
    print "    number of known rules: " + str(len(calculated_rules))

    return max_value + 1000000  # the adder insures that it is always positive (-2000 is the max negative)


def crossover_function(genome, **args):
    sister = None
    brother = None
    mom = args["mom"]
    dad = args["dad"]

    cut = random.randint(1, len(mom) - 1)

    if args["count"] >= 1:
        sister = mom.clone()
        sister.resetStats()
        sister[cut:] = dad[cut:]
        flips = random.randint(0, 4)
        for i in xrange(flips):
            location = random.randint(0, len(mom) - 1)
            if sister[location] == 1:
                sister[location] = 0
            else:
                sister[location] = 1

    if args["count"] == 2:
        brother = dad.clone()
        brother.resetStats()
        brother[cut:] = mom[cut:]
        flips = random.randint(0, 4)
        for i in xrange(flips):
            location = random.randint(0, len(dad) - 1)
            if brother[location] == 1:
                brother[location] = 0
            else:
                brother[location] = 1

    return sister, brother


if __name__ == '__main__':

    # genome = G1DList.G1DList(46)
    # genome.evaluator.set(fitness_function)
    # genome.setParams(rangemin=0, rangemax=1)
    # genome.crossover.set(crossover_function)
    #
    # ga = GSimpleGA.GSimpleGA(genome)
    # ga.setGenerations(80)
    # ga.setPopulationSize(80)
    # ga.evolve(freq_stats=1)
    #
    # sorted_rules = sorted(calculated_rules.items(), key=operator.itemgetter(1), reverse=True)
    # end = min(len(calculated_rules) - 1, 20)
    #
    # for i in xrange(0, end):
    #     print sorted_rules[i]
    #
    # print ga.bestIndividual()

    fitness_function(4352283961441)
