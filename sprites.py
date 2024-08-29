import random

import pygame as pg
from settings import *

class Pin:
    def __init__(self, x, y, color=None, revealed=True):
        self.x, self.y = x, y
        self.color = color
        self.revealed = revealed

    def draw(self, screen):
        center = (self.x + (TILESIZE/2), self.y + (TILESIZE/2))
        if self.color is not None and self.revealed:
            pg.draw.circle(screen, tuple(x * 0.3 for x in self.color), tuple(x + 1 for x in center), 15)
            pg.draw.circle(screen, self.color, center, 15)
        elif not self.revealed:
            pg.draw.circle(screen, LIGHTBLUE, center, 15)
            pg.draw.circle(screen, BLACK, center, 15, 3)

        else:
            pg.draw.circle(screen, DARKBROWN, center, 10)

class CluePin(Pin):
    def draw(self, screen):
        center = (self.x + (TILESIZE / 2.5), self.y + (TILESIZE / 2.5))
        if self.color is not None:
            pg.draw.circle(screen, self.color, center, 6)
        else:
            pg.draw.circle(screen, DARKBROWN, center, 5)

class Board:
    def __init__(self):
        self.tries = 12
        self.pins_surface = pg.Surface((4*TILESIZE, 13*TILESIZE))
        self.pins_surface.fill(BGCOLOR)

        self.clue_surface = pg.Surface((TILESIZE, 13*TILESIZE))
        self.clue_surface.fill(BGCOLOR)

        self.color_selection_surface = pg.Surface((4*TILESIZE, 2*TILESIZE))
        self.color_selection_surface.fill(LIGHTBLUE)

        self.color_selection = []
        self.board_pins = []
        self.board_clues = []

        self.createSelectionPins()
        self.createPins()
        self.createClues()
        self.createCode()

    def createClues(self):
        for i in range(1, 13):
            temp_row = []
            for row in range(2):
                for col in range(2):
                    temp_row.append(CluePin(col * (TILESIZE//4), (row * (TILESIZE//4)) + i * TILESIZE))
            self.board_clues.append(temp_row)

    def createPins(self):
        for row in range(13):
            temp_row = []
            for col in range(4):
                temp_row.append(Pin(col * TILESIZE, row * TILESIZE))
            self.board_pins.append(temp_row)

    def createSelectionPins(self):
        color_index = 0
        for y in range(2):
            for x in range(4):
                if color_index < AMOUNT_COLOR:
                    self.color_selection.append(Pin(x*TILESIZE, y*TILESIZE, COLORS[color_index]))
                    color_index += 1
                else:
                    break

    def draw(self, screen):
        # draw the placeholder for the colored pins
        for pin in self.color_selection:
            pin.draw(self.color_selection_surface)

        # draw the pins
        for row in self.board_pins:
            for pin in row:
                pin.draw(self.pins_surface)

        # draw clue pins
        for row in self.board_clues:
            for pin in row:
                pin.draw(self.clue_surface)

        screen.blit(self.pins_surface, (0, 0))
        screen.blit(self.clue_surface, (4*TILESIZE, 0))
        screen.blit(self.color_selection_surface, (0, 13*TILESIZE))

        # draw row indicator
        pg.draw.rect(screen, INDICATOR, (0, TILESIZE*self.tries, 4*TILESIZE, TILESIZE), 2)

        for x in range(0, WIDTH, TILESIZE):
            for y in range(0, HEIGHT, TILESIZE):
                pg.draw.line(screen, LIGHTGREY, (x, 0), (x, HEIGHT))
                pg.draw.line(screen, LIGHTGREY, (0, y), (WIDTH, y))

    def selectColor(self, mx, my, previous_color):
        for pin in self.color_selection:
            if pin.x < mx < pin.x + TILESIZE and pin.y < my - 13*TILESIZE < pin.y + TILESIZE:
                return pin.color

        return previous_color

    def placePin(self, mx, my, color):
        for pin in self.board_pins[self.tries]:
            if pin.x < mx < pin.x + TILESIZE and pin.y < my < pin.y + TILESIZE:
                pin.color = color
                break

    def checkRow(self):
        return all(pin.color is not None for pin in self.board_pins[self.tries])
        # for pin in self.board_pins[self.tries]:
        #     if pin.color is None:
        #         return False
        # return True

    def checkClues(self):
        color_list = []
        for i, code_pin in enumerate(self.board_pins[0]):
            color = None
            for j, user_pin in enumerate(self.board_pins[self.tries]):
                if user_pin.color == code_pin.color:
                    color = WHITE
                    if i == j:
                        color = RED
                        break
            if color is not None:
                color_list.append(color)

        color_list.sort()
        return color_list

    def setClues(self, color_list):
        for color, pin in zip(color_list, self.board_clues[self.tries-1]):
            pin.color = color

    def createCode(self):
        # generate ramdon code
        random_code = random.sample(COLORS, 4)
        for i, pin in enumerate(self.board_pins[0]):
            pin.color = random_code[i]
            pin.revealed = False
        print(random_code)

    def nextRound(self):
        self.tries -= 1
        return self.tries > 0

    def revealCode(self):
        for pin in self.board_pins[0]:
            pin.revealed = True
