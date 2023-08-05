"""
SNEKTRIS
"""

__version__ = "0.0.2"

from enum import Enum
from itertools import product
import logging
from operator import attrgetter
import random
import time
from typing import Sequence, Tuple, Dict

import pygame
from pygame.locals import QUIT, K_SPACE


logger = logging.getLogger(__name__)


DELAY = 1 / 30
START_POSITION = 0, 4

GRID_HEIGHT = 20
GRID_WIDTH = 10


class Color(Enum):
    LINE_COLOR = (200, 200, 200)
    BACKGROUND = (50, 50, 50)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    CYAN = (0, 255, 255)
    PURPLE = (128, 0, 128)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)


class SingleBlock:
    def __init__(self, i, j, color):
        self.i = i
        self.j = j
        self.color = color

    def __repr__(self):
        return f"SingleBlock({self.i}, {self.j}, {self.color})"

    @property
    def coords(self):
        return self.i, self.j

    @coords.setter
    def coords(self, new_coords):
        self.i, self.j = new_coords

    def step_down(self):
        return SingleBlock(self.i + 1, self.j, self.color)

    def step_left(self):
        return SingleBlock(self.i, self.j - 1, self.color)

    def step_right(self):
        return SingleBlock(self.i, self.j + 1, self.color)

    def rotate_clockwise(self, i, j):
        ii = self.i - i
        jj = self.j - j
        return SingleBlock(i + jj, j - ii, self.color)

    def rotate_anticlockwise(self, i, j):
        ii = self.i - i
        jj = self.j - j
        return SingleBlock(i - jj, j + ii, self.color)


class Snektromino:
    """
    Base class for all snektrominos.
    Each snektromino needs a color and coordinates.
    """

    color: Color
    initial_coords: Sequence[Tuple[int, int]]

    def __init__(self, i, j, blocks=None):
        self.i = i
        self.j = j
        if blocks:
            self.blocks = blocks
        else:
            self.blocks = [
                SingleBlock(self.i + i, self.j + j, self.color)
                for i, j in self.initial_coords
            ]
        self.done = False

    def __repr__(self):
        return self.blocks.__repr__()

    def step_down(self):
        new_blocks = [block.step_down() for block in self.blocks]
        return self.__class__(self.i + 1, self.j, new_blocks)

    def fall_down(self, other_positions):
        new_piece = self.step_down()

        if new_piece.within_boundaries() and not new_piece.overlaps_with(
            other_positions
        ):
            return new_piece.fall_down(other_positions)
        self.done = True
        return self

    def step_left(self):
        new_blocks = [block.step_left() for block in self.blocks]
        return self.__class__(self.i, self.j - 1, new_blocks)

    def step_right(self):
        new_blocks = [block.step_right() for block in self.blocks]
        return self.__class__(self.i, self.j + 1, new_blocks)

    def rotate_clockwise(self):
        logger.debug("Before rotation: %s", self)
        new_blocks = [block.rotate_clockwise(self.i, self.j) for block in self.blocks]
        return self.__class__(self.i, self.j, new_blocks)

    def rotate_anticlockwise(self):
        logger.debug("Before rotation: %s", self)
        new_blocks = [
            block.rotate_anticlockwise(self.i, self.j) for block in self.blocks
        ]
        return self.__class__(self.i, self.j, new_blocks)

    def within_boundaries(self):
        for block in self.blocks:
            if block.j < 0:
                return False

            if block.j > GRID_WIDTH - 1:
                return False

            if block.i > GRID_HEIGHT - 1:
                return False
        return True

    def overlaps_with(self, other_blocks: Dict[Tuple[int, int], SingleBlock]):
        return any(block.coords in other_blocks for block in self.blocks)


# fmt: off
class LShaped(Snektromino):
    color = Color.BLUE
    initial_coords = (
        (-1, 0),
        (0, 0),
        (1, 0),
        (1, 1)
    )


class JShaped(Snektromino):
    color = Color.ORANGE
    initial_coords = (
        (-1, 0),
        (0, 0),
        (1, 0),
        (1, -1)
    )


class SShaped(Snektromino):
    color = Color.GREEN
    initial_coords = (
        (-1, 0),
        (0, 0),
        (0, 1),
        (1, 1)
    )


class TShaped(Snektromino):
    color = Color.PURPLE
    initial_coords = (
        (-1, 0),
        (0, -1),
        (0, 0),
        (1, 0)
    )


class ZShaped(Snektromino):
    color = Color.RED
    initial_coords = (
        (-1, 0),
        (0, 0),
        (0, -1),
        (1, -1)
    )


class IShaped(Snektromino):
    color = Color.CYAN
    initial_coords = (
        (-1, 0),
        (0, 0),
        (1, 0),
        (2, 0)
    )


class OShaped(Snektromino):
    color = Color.YELLOW
    initial_coords = (
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1)
    )

    def rotate_clockwise(self):
        pass

    def rotate_anticlockwise(self):
        pass

# fmt: on


class Grid:
    def __init__(self, width, height):
        self.height = height
        self.width = width

        self.grid_height = GRID_HEIGHT
        self.grid_width = GRID_WIDTH

        self.pixel_width = self.width // self.grid_width
        self.pixel_height = self.height // self.grid_height

        self.blocks = {}
        self.active_snektromino = None

    @staticmethod
    def draw_background(screen):
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill(Color.LINE_COLOR.value)
        screen.blit(background, (0, 0))

    def draw_grid(self, screen):
        pix_width = self.pixel_width
        pix_height = self.pixel_height
        for i, j in product(range(self.grid_height), range(self.grid_width)):
            rect = pygame.Rect(
                j * pix_width, i * pix_height, pix_width - 1, pix_height - 1
            )
            pygame.draw.rect(screen, Color.BACKGROUND.value, rect)

    def draw_snektrominos(self, screen, active_snektromino):
        pix_width = self.pixel_width
        pix_height = self.pixel_height
        for block in [*active_snektromino.blocks, *self.blocks.values()]:
            i, j = block.coords
            color = block.color
            rect = pygame.Rect(
                j * pix_width, i * pix_height, pix_width - 1, pix_height - 1
            )
            pygame.draw.rect(screen, color.value, rect)

    def update_blocks(self, new_blocks):
        for block in new_blocks:
            self.blocks[block.coords] = block

    def clear_lines(self):
        lines_to_be_deleted = []
        steps_to_take = [0] * GRID_HEIGHT
        new_blocks = {}

        steps = 0
        for i in reversed(range(GRID_HEIGHT)):
            steps_to_take[i] = steps
            if all((i, j) in self.blocks for j in range(GRID_WIDTH)):
                lines_to_be_deleted.append(i)
                steps += 1

        if lines_to_be_deleted:

            for (ii, jj), block in self.blocks.items():
                if ii in lines_to_be_deleted:
                    continue

                new_block = block
                steps = steps_to_take[ii]
                for _ in range(steps):
                    new_block = new_block.step_down()
                new_blocks[(ii + steps, jj)] = new_block

            self.blocks = new_blocks


def main():
    pygame.display.init()
    screen = pygame.display.set_mode((300, 600))
    grid = Grid(300, 600)
    pygame.display.set_caption("Snektris")

    counter = 0
    game_over = False

    while not game_over:

        snektromino_class = random.choice(
            [SShaped, TShaped, ZShaped, LShaped, IShaped, JShaped, OShaped]
        )
        active_snektromino = snektromino_class(*START_POSITION)
        grid.active_snektromino = active_snektromino

        while True:
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():

                if event.type == QUIT:
                    return

                new_snektromino = None

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_x:
                        new_snektromino = active_snektromino.rotate_clockwise()

                    elif event.key == pygame.K_y:
                        new_snektromino = active_snektromino.rotate_anticlockwise()

                    if event.key == pygame.K_LEFT:
                        new_snektromino = active_snektromino.step_left()

                    if event.key == pygame.K_RIGHT:
                        new_snektromino = active_snektromino.step_right()

                    if event.key == pygame.K_DOWN:
                        new_snektromino = active_snektromino.step_down()

                    if event.key == pygame.K_UP:
                        new_snektromino = active_snektromino.fall_down(grid.blocks)

            if (
                new_snektromino
                and new_snektromino.within_boundaries()
                and not new_snektromino.overlaps_with(grid.blocks)
            ):
                active_snektromino = new_snektromino

            grid.draw_background(screen)
            grid.draw_grid(screen)
            grid.draw_snektrominos(screen, active_snektromino)

            pygame.display.flip()
            time.sleep(DELAY)

            if counter == 30:
                new_snektromino = active_snektromino.step_down()
                if new_snektromino.within_boundaries() and not new_snektromino.overlaps_with(
                    grid.blocks
                ):
                    active_snektromino = new_snektromino
                else:
                    active_snektromino.done = True

                counter = 0

            counter += 1

            if active_snektromino.done:
                grid.update_blocks(active_snektromino.blocks)

                if START_POSITION in grid.blocks:
                    game_over = True
                break

            grid.clear_lines()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
