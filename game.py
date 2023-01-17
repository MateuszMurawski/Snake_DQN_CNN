import random
import time

import pygame
from matplotlib import pyplot as plt

import agent
import gameInfo


class Game:
    def __init__(self, __agent: agent.Agent, maxNumberGame):
        self.__backgroundColor = pygame.Color(0, 0, 0)
        self.__scoreColor = pygame.Color(0, 255, 255)
        self.__appleColor = pygame.Color(255, 0, 0)
        self.__snakeBodyColor = pygame.Color(85, 255, 0)
        self.__snakeHeadColor = pygame.Color(170, 0, 200)

        self.__agent = __agent
        self.__gameInfo = gameInfo.GameInfo()
        self.__snakeSpeed = 1
        self.__windowX = 240
        self.__windowY = 240
        self.__unitSize = 20
        self.__bestScore = 0
        self.__bestStep = 0
        self.__numberGame = 0
        self.__numberAllStep = 0
        self.__maxNumberGame = maxNumberGame
        self.__showScoreOnBoard = True
        self.__showStepOnBoard = False
        self.__fruitSpawn = False
        self.__resultsHistory = []

        pygame.init()
        pygame.display.set_caption('Snake Game')
        self.__gameWindow = pygame.display.set_mode((self.__windowX, self.__windowY))
        self.__fps = pygame.time.Clock()

    def setSnakeSpeed(self, speed: int):
        self.__snakeSpeed = speed

    def setWindow(self, windowX: int, windowY: int):
        self.__windowX = windowX
        self.__windowY = windowY

    def setUnitSize(self, unitSize: int):
        self.__unitSize = unitSize

    def setBackgroundColor(self, r: int, g: int, b: int):
        self.__backgroundColor = pygame.Color(r, g, b)

    def setScoreColor(self, r: int, g: int, b: int):
        self.__scoreColor = pygame.Color(r, g, b)

    def setAppleColor(self, r: int, g: int, b: int):
        self.__appleColor = pygame.Color(r, g, b)

    def setSnakeBodyColor(self, r: int, g: int, b: int):
        self.__snakeBodyColor = pygame.Color(r, g, b)

    def setSnakeHeadColor(self, r: int, g: int, b: int):
        self.__snakeHeadColor = pygame.Color(r, g, b)

    def setShowScore(self, show: bool):
        self.__showScoreOnBoard = show

    def setShowStep(self, show: bool):
        self.__showStepOnBoard = show

    def __showScore(self, color: pygame.Color, font: str, size: int):
        scoreFont = pygame.font.SysFont(font, size)
        scoreSurface = scoreFont.render('Score : ' + str(self.__score), True, color)
        scoreRect = scoreSurface.get_rect()
        self.__gameWindow.blit(scoreSurface, scoreRect)

        bestScoreFont = pygame.font.SysFont(font, size)
        bestScoreSurface = bestScoreFont.render('Best score : ' + str(self.__bestScore), True, color)
        bestScoreRect = bestScoreSurface.get_rect()
        bestScoreRect.topright = (self.__windowX, 0)
        self.__gameWindow.blit(bestScoreSurface, bestScoreRect)

    def __showStep(self, color: pygame.Color, font: str, size: int):
        stepFont = pygame.font.SysFont(font, size)
        stepSurface = stepFont.render('Step : ' + str(self.__step), True, color)
        stepRect = stepSurface.get_rect()
        stepRect.bottomleft = (0, self.__windowY)
        self.__gameWindow.blit(stepSurface, stepRect)

        bestStepFont = pygame.font.SysFont(font, size)
        bestStepSurface = bestStepFont.render('Best step : ' + str(self.__bestStep), True, color)
        bestStepRect = bestStepSurface.get_rect()
        bestStepRect.bottomright = (self.__windowX, self.__windowY)
        self.__gameWindow.blit(bestStepSurface, bestStepRect)

    def __gameOver(self):
        if self.__score > self.__bestScore:
            self.__bestScore = self.__score

        if self.__step > self.__bestStep:
            self.__bestStep = self.__step

        self.__gameInfo._GameInfo__lastDirection = self.__direction
        self.__resultsHistory.append([self.__score, self.__step])

        self.__newGame()

    def __newGame(self):
        self.__snakePosition = [self.__windowX / 4 + self.__unitSize, self.__windowY / 2]
        self.__snakeBody = [[self.__windowX / 4, self.__windowY / 2], [self.__windowX / 4 - self.__unitSize, self.__windowY / 2], [self.__windowX / 4 - self.__unitSize * 2, self.__windowY / 2]]

        if not self.__fruitSpawn:
            while not self.__fruitSpawn:
                self.__fruitPosition = [random.randrange(1, (self.__windowX // self.__unitSize)) * self.__unitSize, random.randrange(1, (self.__windowY // self.__unitSize)) * self.__unitSize]
                self.__fruitSpawn = True

                for pos in self.__snakeBody:
                    if pos == self.__fruitPosition:
                        self.__fruitSpawn = False
                        break

        self.__direction = 'RIGHT'
        self.__changeTo = self.__direction
        self.__score = 0
        self.__step = 0
        self.__numberGame += 1

    def __plot(self):
        plt.plot(self.__resultsHistory)
        plt.xlabel('Number game')
        plt.ylabel('Score / Step')
        plt.title('Result history')
        plt.gca().legend(('Score', 'Step'))
        plt.show()

    def startGame(self):
        self.__newGame()

        while True:
            self.__snakeBody.insert(0, list(self.__snakePosition))

            if self.__snakePosition[0] == self.__fruitPosition[0] and self.__snakePosition[1] == self.__fruitPosition[1]:
                self.__score += 1
                self.__fruitSpawn = False
            else:
                self.__snakeBody.pop()

            if self.__snakePosition[0] < 0 or self.__snakePosition[0] > self.__windowX - self.__unitSize:
                self.__gameOver()
                continue

            if self.__snakePosition[1] < 0 or self.__snakePosition[1] > self.__windowY - self.__unitSize:
                self.__gameOver()
                continue

            for block in self.__snakeBody[1:]:
                if self.__snakePosition[0] == block[0] and self.__snakePosition[1] == block[1]:
                    self.__gameOver()
                    continue

            if not self.__fruitSpawn:
                while not self.__fruitSpawn:
                    self.__fruitPosition = [random.randrange(1, (self.__windowX // self.__unitSize)) * self.__unitSize, random.randrange(1, (self.__windowY // self.__unitSize)) * self.__unitSize]
                    self.__fruitSpawn = True

                    for pos in self.__snakeBody:
                        if pos == self.__fruitPosition:
                            self.__fruitSpawn = False
                            break

            self.__gameWindow.fill(self.__backgroundColor)

            for pos in self.__snakeBody:
                pygame.draw.rect(self.__gameWindow, self.__snakeBodyColor, pygame.Rect(pos[0], pos[1], self.__unitSize, self.__unitSize))

            pygame.draw.rect(self.__gameWindow, self.__appleColor, pygame.Rect(self.__fruitPosition[0], self.__fruitPosition[1], self.__unitSize, self.__unitSize))
            pygame.draw.rect(self.__gameWindow, self.__snakeHeadColor, pygame.Rect(self.__snakeBody[0][0], self.__snakeBody[0][1], self.__unitSize, self.__unitSize))

            self.__gameInfo._GameInfo__gameScreenWithoutHUB = pygame.surfarray.array3d(self.__gameWindow)

            if self.__showScoreOnBoard:
                self.__showScore(self.__scoreColor, 'times new roman', self.__windowX // 12)

            if self.__showStepOnBoard:
                self.__showStep(self.__scoreColor, 'times new roman', self.__windowX // 12)

            self.__gameInfo._GameInfo__gameScreenWithHUB = pygame.surfarray.array3d(self.__gameWindow)

            self.__gameInfo._GameInfo__gameBestStep = self.__bestStep
            self.__gameInfo._GameInfo__gameStep = self.__step
            self.__gameInfo._GameInfo__gameBestStep = self.__bestScore
            self.__gameInfo._GameInfo__gameScore = self.__score
            self.__gameInfo._GameInfo__gameNumberAllStep = self.__numberAllStep

            if self.__gameInfo._GameInfo__numberGame == None or self.__gameInfo._GameInfo__numberGame >= self.__numberGame:
                self.__gameInfo._GameInfo__lastDirection = self.__direction

            self.__gameInfo._GameInfo__numberGame = self.__numberGame

            self.__changeTo = self.__agent.getNewDirection(self.__gameInfo)

            if self.__numberGame > self.__maxNumberGame or self.__gameInfo._GameInfo__stopGame:
                self.__plot()
                return

            self.__step += 1
            self.__numberAllStep += 1

            if self.__changeTo == 'UP' and self.__direction != 'DOWN':
                self.__direction = 'UP'
            if self.__changeTo == 'DOWN' and self.__direction != 'UP':
                self.__direction = 'DOWN'
            if self.__changeTo == 'LEFT' and self.__direction != 'RIGHT':
                self.__direction = 'LEFT'
            if self.__changeTo == 'RIGHT' and self.__direction != 'LEFT':
                self.__direction = 'RIGHT'

            if self.__direction == 'UP':
                self.__snakePosition[1] -= self.__unitSize
            if self.__direction == 'DOWN':
                self.__snakePosition[1] += self.__unitSize
            if self.__direction == 'LEFT':
                self.__snakePosition[0] -= self.__unitSize
            if self.__direction == 'RIGHT':
                self.__snakePosition[0] += self.__unitSize

            pygame.display.update()
            self.__fps.tick(self.__snakeSpeed)





