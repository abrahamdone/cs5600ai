import pygame
import sys


class PygameRenderer(object):
    """Renders a grid object using Pygame, and also contains code to
    save the current grid."""
    def __init__(self, n, pixel_size,
                    background=(255, 255, 255), foreground=(0, 0, 0)):
        self.pixel_size = pixel_size
        side_length = n * 2 - 1
        self.size = (side_length * self.pixel_size,
                     side_length * self.pixel_size)
        self.background = background
        self.foreground = foreground

        self._configure_pygame()
        self._configure_graphics()

        self.grid = None

    def _configure_pygame(self):
        pygame.init()
        pygame.display.set_mode(self.size)
        self.surface = pygame.display.get_surface()

    def _configure_graphics(self):
        self.tile = pygame.Surface((self.pixel_size, self.pixel_size))
        self.tile.fill(self.foreground)

    def render(self, grid):
        """Renders the grid, and prints the current seed to stdout."""
        self.grid = grid
        self.surface.fill(self.background)
        for x, col in enumerate(grid.array):
            xc = x * self.pixel_size
            for y, cell in enumerate(col):
                if cell:
                    self.surface.blit(
                        self.tile,
                        (xc, y * self.pixel_size)
                    )
        pygame.display.flip()

    def wait(self):
        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def refresh(self):
        """Waits until Pygame is closed. Clicking any keyboard
        button will save the current image to the current directory,
        and clicking the mouse will break from the mainloop so that
        the containing function can create a new grid."""
        # while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return # Returns so that a new grid can be generated.
        elif event.type == pygame.KEYDOWN:
            filename = str(self.grid.seed) + '.png'
            pygame.image.save(self.surface, filename)


class AsciiRenderer(object):
    """Creates an ASCII version of the grid."""
    def to_string(self, grid):
        out = []
        for x in xrange(grid.width):
            row = ['[']
            for y in xrange(grid.height):
                if grid.get(x, y):
                    row.append('#')
                else:
                    row.append(' ')
            row.append(']')
            out.append(''.join(row))
        return '\n'.join(out)

    def render(self):
        print self.to_string()
