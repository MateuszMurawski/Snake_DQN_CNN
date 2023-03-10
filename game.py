import random
import time
from typing import List, Optional
import pygame

import agent
import gameInfo
import plot


class Game:
    def __init__(self, __agent: agent.Agent, maxNumberGame: int) -> None:
        self.__backgroundColor: pygame.Color = pygame.Color(0, 0, 0)
        self.__scoreColor: pygame.Color = pygame.Color(0, 255, 255)
        self.__appleColor: pygame.Color = pygame.Color(255, 0, 0)
        self.__snakeBodyColor: pygame.Color = pygame.Color(85, 255, 0)
        self.__snakeHeadColor: pygame.Color = pygame.Color(170, 0, 200)

        self.__agent: agent.Agent = __agent
        self.__gameInfo: gameInfo.GameInfo = gameInfo.GameInfo()
        self.__snakeSpeed: int = 1
        self.__windowX: int = 240
        self.__windowY: int = 240
        self.__unitSize: int = 20
        self.__bestScore: int = 0
        self.__bestStep: int = 0
        self.__numberGame: int = 0
        self.__numberAllStep: int = 0
        self.__changeTo: str = ''
        self.__maxNumberGame: int = maxNumberGame
        self.__showScoreOnBoard: bool = True
        self.__showStepOnBoard: bool = False
        self.__showPlot: bool = False
        self.__fruitSpawn: bool = False
        self.__direction: str = ''
        self.__resultsHistory: List[List[int], List[int], List[int]] = [[], [], []]

        pygame.init()
        pygame.display.set_caption('Snake Game')
        self.__gameWindow: pygame.display = pygame.display.set_mode((self.__windowX, self.__windowY), pygame.HIDDEN)
        self.__fps: pygame.time.Clock = pygame.time.Clock()

    def setSnakeSpeed(self, speed: int) -> None:
        self.__snakeSpeed = speed

    def setWindow(self, windowX: int, windowY: int) -> None:
        self.__windowX = windowX
        self.__windowY = windowY

    def setUnitSize(self, unitSize: int) -> None:
        self.__unitSize = unitSize

    def setBackgroundColor(self, r: int, g: int, b: int) -> None:
        self.__backgroundColor = pygame.Color(r, g, b)

    def setScoreColor(self, r: int, g: int, b: int) -> None:
        self.__scoreColor = pygame.Color(r, g, b)

    def setAppleColor(self, r: int, g: int, b: int) -> None:
        self.__appleColor = pygame.Color(r, g, b)

    def setSnakeBodyColor(self, r: int, g: int, b: int) -> None:
        self.__snakeBodyColor = pygame.Color(r, g, b)

    def setSnakeHeadColor(self, r: int, g: int, b: int) -> None:
        self.__snakeHeadColor = pygame.Color(r, g, b)

    def setShowScore(self, show: Optional[bool] = True) -> None:
        self.__showScoreOnBoard = show

    def setShowStep(self, show: Optional[bool] = True) -> None:
        self.__showStepOnBoard = show

    def setShowPlot(self, show: Optional[bool] = True) -> None:
        if show:
            plot.Plot.startServerPlot()
            self.__showPlot = True

    def setShowGame(self, show: Optional[bool] = True) -> None:
        if show:
            self.__gameWindow: pygame.display = pygame.display.set_mode((self.__windowX, self.__windowY))
        else:
            self.__gameWindow: pygame.display = pygame.display.set_mode((self.__windowX, self.__windowY), pygame.HIDDEN)

    def __showScore(self, color: pygame.Color, font: str, size: int) -> None:
        scoreFont = pygame.font.SysFont(font, size)
        scoreSurface = scoreFont.render('Score : ' + str(self.__score), True, color)
        scoreRect = scoreSurface.get_rect()
        self.__gameWindow.blit(scoreSurface, scoreRect)

        bestScoreFont = pygame.font.SysFont(font, size)
        bestScoreSurface = bestScoreFont.render('Best score : ' + str(self.__bestScore), True, color)
        bestScoreRect = bestScoreSurface.get_rect()
        bestScoreRect.topright = (self.__windowX, 0)
        self.__gameWindow.blit(bestScoreSurface, bestScoreRect)

    def __showStep(self, color: pygame.Color, font: str, size: int) -> None:
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

    def __gameOver(self) -> None:
        if self.__score > self.__bestScore:
            self.__bestScore = self.__score

        if self.__step > self.__bestStep:
            self.__bestStep = self.__step

        self.__gameInfo._GameInfo__lastDirection = self.__direction
        self.__resultsHistory[0].append(self.__numberGame)
        self.__resultsHistory[1].append(self.__score)
        self.__resultsHistory[2].append(self.__step)

        if self.__showPlot:
            plot.Plot.updateData(self.__numberGame, self.__score, self.__step)

        print("Number game: ", self.__numberGame)
        print("Score: ", self.__score)
        print("Step: ", self.__step)
        print("------------------------------------------------")

        self.__newGame()

    def __info(self) -> None:
        print("\n------------------------------------------------")
        print("Settings game")
        print("Resolution: ", self.__windowX, " x ", self.__windowY)
        print("Unit size: ", self.__unitSize, " x ", self.__unitSize)
        print("Speed snake: ", self.__snakeSpeed)
        print("------------------------------------------------\n")

    def __newGame(self) -> None:
        self.__snakePosition = [self.__windowX / 4 + self.__unitSize, self.__windowY / 2]
        self.__snakeBody = [[self.__windowX / 4, self.__windowY / 2],
                            [self.__windowX / 4 - self.__unitSize, self.__windowY / 2],
                            [self.__windowX / 4 - self.__unitSize * 2, self.__windowY / 2]]

        if not self.__fruitSpawn:
            while not self.__fruitSpawn:
                self.__fruitPosition = [random.randrange(1, (self.__windowX // self.__unitSize)) * self.__unitSize,
                                        random.randrange(1, (self.__windowY // self.__unitSize)) * self.__unitSize]
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

    def startGame(self) -> None:
        time.sleep(1)
        self.__info()
        self.__newGame()

        while True:
            self.__snakeBody.insert(0, list(self.__snakePosition))

            if self.__snakePosition[0] == self.__fruitPosition[0] and self.__snakePosition[1] == self.__fruitPosition[
                1]:
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
                    self.__fruitPosition = [random.randrange(1, (self.__windowX // self.__unitSize)) * self.__unitSize,
                                            random.randrange(1, (self.__windowY // self.__unitSize)) * self.__unitSize]
                    self.__fruitSpawn = True

                    for pos in self.__snakeBody:
                        if pos == self.__fruitPosition:
                            self.__fruitSpawn = False
                            break

            self.__gameWindow.fill(self.__backgroundColor)

            for pos in self.__snakeBody:
                pygame.draw.rect(self.__gameWindow, self.__snakeBodyColor,
                                 pygame.Rect(pos[0], pos[1], self.__unitSize, self.__unitSize))

            pygame.draw.rect(self.__gameWindow, self.__appleColor,
                             pygame.Rect(self.__fruitPosition[0], self.__fruitPosition[1], self.__unitSize,
                                         self.__unitSize))
            pygame.draw.rect(self.__gameWindow, self.__snakeHeadColor,
                             pygame.Rect(self.__snakeBody[0][0], self.__snakeBody[0][1], self.__unitSize,
                                         self.__unitSize))

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

            if self.__gameInfo._GameInfo__numberGame is None or self.__gameInfo._GameInfo__numberGame >= self.__numberGame:
                self.__gameInfo._GameInfo__lastDirection = self.__direction

            self.__gameInfo._GameInfo__numberGame = self.__numberGame

            self.__changeTo = self.__agent.getNewDirection(self.__gameInfo)

            if self.__numberGame > self.__maxNumberGame or self.__gameInfo._GameInfo__stopGame:
                pygame.quit()
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

            pygame.event.pump()
            pygame.display.update()
            self.__fps.tick(self.__snakeSpeed)
