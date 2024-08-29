import pygame as pg
from settings import *
from sprites import *

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

    def new(self):
        self.board = Board()
        self.color = None

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.board.draw(self.screen)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit(0)
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                self.color = self.board.selectColor(mx, my, self.color)
                if self.color is not None:
                    self.board.placePin(mx, my, self.color)

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if self.board.checkRow():
                        clues_color_list = self.board.checkClues()
                        self.board.setClues(clues_color_list)
                        if self.checkWin(clues_color_list):
                            print("You Won!")
                            self.board.revealCode()
                            self.endScreen()
                        elif not self.board.nextRound():
                            print("Game Over!")
                            self.board.revealCode()
                            self.endScreen()

    def checkWin(self, color_list):
        return len(color_list) == 4 and all(color == RED for color in color_list)

    def endScreen(self):
        while True:
            event = pg.event.wait()
            if event.type == pg.QUIT:
                pg.quit()
                quit(0)

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.playing = False
                    return

            self.draw()

game = Game()
while True:
    game.new()
    game.run()



