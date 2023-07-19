from typing import List

from numpy import ndarray
from dataclasses import dataclass


@dataclass
class GameInfo:
    """
    A class representing the current state of the game.
    """

    def __init__(self):
        """
        Initializes a new instance of the GameInfo class.
        """

        self.__gameScreenWithoutHUB: ndarray = None
        self.__gameScreenWithHUB: ndarray = None
        self.__gameScore: int = 0
        self.__gameBestScore: int = 0
        self.__gameStep: int = 0
        self.__gameBestStep: int = 0
        self.__numberGame: int = 0
        self.__lastDirection: int = None
        self.__gameNumberAllStep: int = 0
        self.__snakePosition: List = None
        self.__fruitPosition: List = None
        self.__snakeBodyPosition: List = None

    def getGameScreenWithoutHUB(self) -> ndarray:
        """
        Returns an image of the game without information such as points and steps on the screen

        Returns:
             ndarray: numpy array image representation of the game
        """

        return self.__gameScreenWithoutHUB

    def getGameScreenWithHUB(self) -> ndarray:
        """
        Returns the game image with information such as points and steps on the screen

        Returns:
             ndarray: numpy array image representation of the game
        """

        return self.__gameScreenWithHUB

    def getGameScore(self) -> int:
        """
        Returns the current score of the game.

        Returns:
             int: a value representing the number of points.
        """

        return self.__gameScore

    def getGameBestScore(self) -> int:
        """
        Returns the highest score achieved in the game so far.

        Returns:
            int: a value representing the best score.
        """

        return self.__gameBestScore

    def getGameStep(self) -> int:
        """
        Returns the current number step of the game.

        Returns:
             int: a value representing the number of steps.
        """

        return self.__gameStep

    def getGameBestStep(self) -> int:
        """
        Returns the highest number of steps achieved so far in the game.

        Returns:
             int: a value representing the highest number of steps.
        """

        return self.__gameBestStep

    def getNumberGame(self) -> int:
        """
        Returns the number of games played so far.

        Returns:
             int: a value representing the number of games played.
        """

        return self.__numberGame

    def getLastDirection(self) -> int:
        """
        Returns the last direction taken by the snake.

        Returns:
             int: a value representing the direction of the last move, using the following encoding:
                0: up
                1: right
                2: down
                3: left
        """

        return self.__lastDirection

    def getNumberAllStep(self) -> int:
        """
        Returns the total number of steps taken in games.

        Returns:
             int: a value representing the number of steps taken.
        """

        return self.__gameNumberAllStep

    def getSnakePosition(self) -> List:
        """
        Returns the position of the snake's head.

        Returns:
            List: Array representing the [x, y] coordinates of the snake's head.
        """

        return self.__snakePosition

    def getFruitPosition(self) -> List:
        """
        Returns the position of the fruit.

        Returns:
             List: Array representing the [x, y] coordinates of the fruit.
        """

        return self.__fruitPosition

    def getSnakeBodyPosition(self) -> List:
        """
        Returns a list of positions of the snake's body segments.

        Returns:
             List: a list representing the [[x, y], [x, y], ...] coordinates of each body segment.
        """

        return self.__snakeBodyPosition
