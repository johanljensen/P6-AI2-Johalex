import pygame
import sys

from GameLoop import GameLoop

class MainStartup:

    def __init__(self):

        print('PyCharm')

        pygame.init()

        self.size = (800, 600)
        self.__screen = pygame.display.set_mode(self.size)

        self.__isInMenu = True
        self.__isPaused = False

        self.Widget1 = pygame.image.load('Graphics/Multiplayer_Buttons.png')

        self.font = pygame.font.Font('Fonts/COMIC.TTF', 20)
        self.blue = (0, 0, 128)

        self.text = self.font.render('Play', True, self.blue)
        self.text2 = self.font.render('Host', True, self.blue)
        self.text4 = self.font.render('Waiting for another Player', True, self.blue)
        self.text5 = self.font.render('Connecting please wait', True, self.blue)

        self.playCoordinates = (300, 200)
        self.hostCoordinates = (300, 280)

        self.girlAnimation = (360, 130)
        self.Widget1Length = 190
        self.Widget1Height = 50

        self.mx = None
        self.my = None

        self.menuState = "menu"
        self.playState = "play"
        self.hostState = "host"
        self.gameState = self.menuState

        self.counter = 0
        self.indexCount = 0
        self.isTrue = True

        self.spriteList = [(3 * 3, 3 * 3, 18 * 3, 29 * 3),
                           (27 * 3, 2 * 3, 18 * 3, 30 * 3),
                           (51 * 3, 3 * 3, 18 * 3, 29 * 3),
                           (27 * 3, 2 * 3, 18 * 3, 30 * 3),
                           (6 * 3, 35 * 3, 12 * 3, 29 * 3),
                           (30 * 3, 35 * 3, 12 * 3, 29 * 3),
                           (54 * 3, 36 * 3, 12 * 3, 28 * 3),
                           (30 * 3, 35 * 3, 12 * 3, 29 * 3),
                           (3 * 3, 67 * 3, 18 * 3, 29 * 3),
                           (27 * 3, 66 * 3, 18 * 3, 30 * 3),
                           (51 * 3, 67 * 3, 18 * 3, 29 * 3),
                           (27 * 3, 66 * 3, 18 * 3, 30 * 3),
                           (6 * 3, 100 * 3, 12 * 3, 28 * 3),
                           (30 * 3, 99 * 3, 12 * 3, 29 * 3),
                           (54 * 3, 100 * 3, 12 * 3, 29 * 3),
                           (30 * 3, 99 * 3, 12 * 3, 29 * 3)]
        self.switch = True
        self.t0 = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()

    def ClickMenuButton(self):
        if self.__isInMenu:
            self.MainMenu()

    def MainMenu(self):
        if self.gameState == self.menuState:
            while self.gameState == self.menuState:
                self.mx, self.my = pygame.mouse.get_pos()
                t1 = pygame.time.get_ticks()
                dt = t1 - self.t0
                self.clock.tick(60)
                self.__screen.blit(self.Widget1, self.playCoordinates, (0, 142, self.Widget1Length, self.Widget1Height))
                self.__screen.blit(self.text, (377, 207))
                if dt >= 200:
                    self.indexCount += 1
                    if self.indexCount == len(self.spriteList):
                        self.indexCount = 0
                    self.t0 = t1
                pygame.display.update()
                if self.isTrue:
                    self.counter += 1
                if self.counter == 800:
                    self.counter = 0
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.checkIfClicked()
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
        if self.gameState == "play":
            GameLoop().StartLoop()
            print('Play')

    def checkIfClicked(self):
        if self.mx >= self.playCoordinates[0]:
            if self.mx <= self.playCoordinates[0] + self.Widget1Length:
                if self.my >= self.playCoordinates[1]:
                    if self.my <= self.playCoordinates[1] + self.Widget1Height:
                        self.gameState = self.playState

MainStartup().ClickMenuButton()