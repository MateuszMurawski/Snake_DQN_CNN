from os import environ
from random import randrange
from time import sleep
from typing import List, Optional
import pygame

from game.agent import Agent
from game.plot import Plot
from game.gameInfo import GameInfo


class Game:
    """
    A class representing a game.
    """

    def __init__(self, agent: Agent, maxNumberGame: int, showGame: Optional[bool] = True) -> None:
        """
        Initializes a new instance of the Game class.

        Args:
            agent (Agent): agent object returning movements for the snake
            maxNumberGame (int): maximum number of games to play
            showGame (bool): flag representing whether the game should be displayed in a window or run in the background. Defaults to True.

        Returns:
            None
        """

        if not showGame:
            environ['SDL_VIDEODRIVER'] = 'dummy'

        self.__agent: Agent = agent
        self.__maxNumberGame: int = maxNumberGame

        self.__backgroundColor: pygame.Color = pygame.Color(0, 0, 0)
        self.__scoreColor: pygame.Color = pygame.Color(0, 255, 255)
        self.__appleColor: pygame.Color = pygame.Color(255, 0, 0)
        self.__snakeBodyColor: pygame.Color = pygame.Color(85, 255, 0)
        self.__snakeHeadColor: pygame.Color = pygame.Color(170, 0, 200)

        self.__snakeSpeed: int = 1
        self.__windowX: int = 240
        self.__windowY: int = 240
        self.__unitSize: int = 20
        self.__showScoreOnBoard: bool = True
        self.__showStepOnBoard: bool = False
        self.__showPlot: bool = False

        self.__bestScore: int = 0
        self.__bestStep: int = 0
        self.__numberGame: int = 0
        self.__numberAllStep: int = 0
        self.__resultsHistory: List = [[], [], []]

        self.__gameInfo: GameInfo = GameInfo()
        self.__fruitSpawn: bool = False
        self.__fruitPosition: List = None
        self.__snakeBody: List = None
        self.__changeTo: int = -1
        self.__direction: int = -1

        self.__UP = 0
        self.__RIGHT = 1
        self.__DOWN = 2
        self.__LEFT = 3

        pygame.init()
        pygame.display.set_caption('Snake Game')
        self.__gameWindow: pygame.display = pygame.display.set_mode((self.__windowX, self.__windowY))
        self.__fps: pygame.time.Clock = pygame.time.Clock()

    def setSnakeSpeed(self, speed: int) -> None:
        """
        Set the speed of the snake in the game.

        Args:
            speed (int): The speed of the snake in the game, maximum frames per second.

        Returns:
            None
        """

        self.__snakeSpeed = speed

    def setWindow(self, windowX: int, windowY: int) -> None:
        """
        Set the dimensions of the game window.

        Args:
            windowX (int): The width of the game window.
            windowY (int): The height of the game window.

        Returns:
            None
        """

        self.__windowX = windowX
        self.__windowY = windowY

    def setUnitSize(self, unitSize: int) -> None:
        """
        Set the size of each unit in the game.

        Args:
            unitSize (int): The size of each unit in the game.

        Returns:
            None
        """

        self.__unitSize = unitSize

    def setBackgroundColor(self, r: int, g: int, b: int) -> None:
        """
        Set the background color of the game window.

        Args:
            r (int): The red value of the background color (0-255).
            g (int): The green value of the background color (0-255).
            b (int): The blue value of the background color (0-255).

        Returns:
            None
        """

        self.__backgroundColor = pygame.Color(r, g, b)

    def setScoreColor(self, r: int, g: int, b: int) -> None:
        """
        Sets the color of the score text.

        Args:
            r (int): The red value of the background color (0-255).
            g (int): The green value of the background color (0-255).
            b (int): The blue value of the background color (0-255).

        Returns:
            None
        """

        self.__scoreColor = pygame.Color(r, g, b)

    def setAppleColor(self, r: int, g: int, b: int) -> None:
        """
        Sets the color of the Apple/Fruit.

        Args:
            r (int): The red value of the background color (0-255).
            g (int): The green value of the background color (0-255).
            b (int): The blue value of the background color (0-255).

        Returns:
            None
        """
        self.__appleColor = pygame.Color(r, g, b)

    def setSnakeBodyColor(self, r: int, g: int, b: int) -> None:
        """
        Sets the color of the snake body.

        Args:
            r (int): The red value of the background color (0-255).
            g (int): The green value of the background color (0-255).
            b (int): The blue value of the background color (0-255).

        Returns:
            None
        """

        self.__snakeBodyColor = pygame.Color(r, g, b)

    def setSnakeHeadColor(self, r: int, g: int, b: int) -> None:
        """
        Sets the color of the snake head.

        Args:
            r (int): The red value of the background color (0-255).
            g (int): The green value of the background color (0-255).
            b (int): The blue value of the background color (0-255).

        Returns:
            None
        """

        self.__snakeHeadColor = pygame.Color(r, g, b)

    def setShowScore(self, show: Optional[bool] = True) -> None:
        """
        Set whether to show the score on the game board.

        Args:
            show (bool): Whether to show the score. Defaults to True.

        Returns:
            None
        """

        self.__showScoreOnBoard = show

    def setShowStep(self, show: Optional[bool] = True) -> None:
        """
        Set whether to show the step on the game board.

        Args:
            show (bool): Whether to show the step. Defaults to True.

        Returns:
            None
        """

        self.__showStepOnBoard = show

    def setShowPlot(self, show: Optional[bool] = True) -> None:
        """
        Sets the flag for the server displaying the game score graph on the website. The default site address is: 127.0.0.1:8050

        Args:
            show (bool): If True, the server will be started and will display the graph on the web page. The default value is True.

        Returns:
            None
        """

        if show:
            Plot.startServerPlot()
            self.__showPlot = True

    def __showScore(self, color: pygame.Color, font: str, size: int) -> None:
        """
        Display the score and the best score on the game window using the given color, font and size.

        Args:
            color (pygame.Color): object representing the color of the text.
            font (string): a string representing the name of the font to use.
            size (int): an integer representing the size of the font to use.

        Returns:
            None
        """

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
        """
        Display the step and the best step on the game window using the given color, font and size.

        Args:
            color (pygame.Color): object representing the color of the text.
            font (string): a string representing the name of the font to use.
            size (int): an integer representing the size of the font to use.

        Returns:
            None
        """

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
        """
        Ends the current game by updating the best scores and step count, storing the results in the results history, and starting a new game.
        If the `showPlot` attribute is set to True, updates the plot with the game results.
        Prints the number of the game, the score, the step count, and the sum of all steps.

        Returns:
            None
        """

        if self.__score > self.__bestScore:
            self.__bestScore = self.__score

        if self.__step > self.__bestStep:
            self.__bestStep = self.__step

        self.__gameInfo._GameInfo__lastDirection = self.__direction
        self.__resultsHistory[0].append(self.__numberGame)
        self.__resultsHistory[1].append(self.__score)
        self.__resultsHistory[2].append(self.__step)

        if self.__showPlot:
            Plot.updateData(self.__numberGame, self.__score, self.__step)

        print("Number game: ", self.__numberGame)
        print("Score: ", self.__score)
        print("Step: ", self.__step)
        print("Sum all steps: ", self.__numberAllStep)
        print("------------------------------------------------")

        self.__newGame()

    def __info(self) -> None:
        """
        Prints the game settings.

        Returns:
            None
        """

        print("\n------------------------------------------------")
        print("* Settings game *")
        print("Resolution: ", self.__windowX, " x ", self.__windowY)
        print("Unit size: ", self.__unitSize, " x ", self.__unitSize)
        print("Speed snake: ", self.__snakeSpeed)
        print("------------------------------------------------\n")

    def __finalStats(self) -> None:
        """
        Prints the final game stats.

        Returns:
            None
        """

        print("\n------------------------------------------------")
        print("* Final stats *")
        print("Best Score: ", self.__bestScore)
        print("Best Step: ", self.__bestStep)
        print("------------------------------------------------\n")

    def __newGame(self) -> None:
        """
        Resets the game state to start a new game. Initializes the snake position and body, spawns a fruit, and resets the direction, score, and step count.

        Returns:
            None
        """

        self.__snakePosition = [self.__windowX / 4 + self.__unitSize, self.__windowY / 2]
        self.__snakeBody = [[self.__windowX / 4, self.__windowY / 2],
                            [self.__windowX / 4 - self.__unitSize, self.__windowY / 2],
                            [self.__windowX / 4 - self.__unitSize * 2, self.__windowY / 2]]

        self.__fruitSpawn = False

        while not self.__fruitSpawn:
            self.__fruitPosition = [randrange(1, (self.__windowX // self.__unitSize)) * self.__unitSize, randrange(1, (self.__windowY // self.__unitSize)) * self.__unitSize]
            self.__fruitSpawn = True

            for pos in self.__snakePosition + self.__snakeBody:
                if pos == self.__fruitPosition:
                    self.__fruitSpawn = False
                    break

        self.__direction = self.__RIGHT
        self.__changeTo = self.__direction
        self.__score = 0
        self.__step = 0
        self.__numberGame += 1

    def startGame(self) -> None:
        """
        Starts the snake game. The function initializes a new game and then handles snake movement and checks for collisions with fruits and board borders in a while loop.
        In each iteration, it updates the board state, calls helper functions such as displaying the score, and checks if the game has ended.

        Returns:
            None
        """

        sleep(1)
        self.__info()
        self.__newGame()

        while True:
            ifContinue = False
            self.__snakeBody.insert(0, list(self.__snakePosition))

            if self.__snakePosition == self.__fruitPosition:
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
                if self.__snakePosition == block:
                    ifContinue = True
                    self.__gameOver()
                    break

            if ifContinue:
                continue

            if not self.__fruitSpawn:
                while not self.__fruitSpawn:
                    self.__fruitPosition = [randrange(1, (self.__windowX // self.__unitSize)) * self.__unitSize,
                                            randrange(1, (self.__windowY // self.__unitSize)) * self.__unitSize]
                    self.__fruitSpawn = True

                    for pos in self.__snakeBody:
                        if pos == self.__fruitPosition:
                            self.__fruitSpawn = False
                            break

            self.__gameWindow.fill(self.__backgroundColor)

            for pos in self.__snakeBody:
                pygame.draw.rect(self.__gameWindow, self.__snakeBodyColor, pygame.Rect(pos[0], pos[1], self.__unitSize, self.__unitSize))

            pygame.draw.rect(self.__gameWindow, self.__appleColor,  pygame.Rect(self.__fruitPosition[0], self.__fruitPosition[1], self.__unitSize, self.__unitSize))
            pygame.draw.rect(self.__gameWindow, self.__snakeHeadColor, pygame.Rect(self.__snakeBody[0][0], self.__snakeBody[0][1], self.__unitSize, self.__unitSize))

            self.__gameInfo._GameInfo__gameScreenWithoutHUB = pygame.surfarray.array3d(self.__gameWindow)

            if self.__showScoreOnBoard:
                self.__showScore(self.__scoreColor, 'times new roman', self.__windowX // 12)

            if self.__showStepOnBoard:
                self.__showStep(self.__scoreColor, 'times new roman', self.__windowX // 12)

            self.__gameInfo._GameInfo__gameScreenWithHUB = pygame.surfarray.array3d(self.__gameWindow)

            self.__gameInfo._GameInfo__snakePosition = self.__snakePosition
            self.__gameInfo._GameInfo__snakeBodyPosition = self.__snakeBody
            self.__gameInfo._GameInfo__fruitPosition = self.__fruitPosition
            self.__gameInfo._GameInfo__gameBestStep = self.__bestStep
            self.__gameInfo._GameInfo__gameStep = self.__step
            self.__gameInfo._GameInfo__gameBestStep = self.__bestScore
            self.__gameInfo._GameInfo__gameScore = self.__score
            self.__gameInfo._GameInfo__gameNumberAllStep = self.__numberAllStep

            if self.__gameInfo._GameInfo__numberGame is None or self.__gameInfo._GameInfo__numberGame >= self.__numberGame:
                self.__gameInfo._GameInfo__lastDirection = self.__direction

            self.__gameInfo._GameInfo__numberGame = self.__numberGame
            self.__changeTo = self.__agent.getNewDirection(self.__gameInfo)

            if self.__numberGame > self.__maxNumberGame:
                pygame.quit()
                self.__finalStats()
                return

            self.__step += 1
            self.__numberAllStep += 1

            if self.__changeTo == self.__UP and self.__direction != self.__DOWN:
                self.__direction = self.__UP
            if self.__changeTo == self.__DOWN and self.__direction != self.__UP:
                self.__direction = self.__DOWN
            if self.__changeTo == self.__LEFT and self.__direction != self.__RIGHT:
                self.__direction = self.__LEFT
            if self.__changeTo == self.__RIGHT and self.__direction != self.__LEFT:
                self.__direction = self.__RIGHT

            if self.__direction == self.__UP:
                self.__snakePosition[1] -= self.__unitSize
            if self.__direction == self.__DOWN:
                self.__snakePosition[1] += self.__unitSize
            if self.__direction == self.__LEFT:
                self.__snakePosition[0] -= self.__unitSize
            if self.__direction == self.__RIGHT:
                self.__snakePosition[0] += self.__unitSize

            pygame.event.pump()
            pygame.display.update()
            self.__fps.tick(self.__snakeSpeed)
