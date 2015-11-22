from Hex.hexRule import *
from Grid.grid import *
from Grid.render import *

gen = NoiseGenerator(seed=1234, density=0.1)(16)


def play_game(grid=MEDIUM_GRID, rule=HexRule(),
              duration=0, renderer=PygameRenderer(n=16, pixel_size=4)):
    tick = 0

    while tick <= duration:
        renderer.render(grid)
        renderer.refresh()

        grid = rule.apply_rule(grid)

        if duration != 0:
            tick += 1


if __name__ == '__main__':

    hex_rule = HexRule(22063225121788)
    print hex_rule

    # play_game(grid=LIGHT_GRID, rule=hex_rule, duration=50)
    # play_game(grid=MEDIUM_GRID, rule=hex_rule, duration=50)
    # play_game(grid=DARK_GRID, rule=hex_rule, duration=50)
    play_game(rule=hex_rule)
