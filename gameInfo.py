import numpy
from dataclasses import dataclass

@dataclass
class GameInfo:
    def __init__(self):
        self.__gameScreenWithoutHUB = None
        self.__gameScreenWithHUB = None
        self.__gameScore: int = 0
        self.__gameBestScore: int = 0
        self.__gameStep: int = 0
        self.__gameBestStep: int = 0
        self.__numberGame: int = 0
        self.__lastDirection: str = ''
        self.__stopGame: bool = False
        self.__gameNumberAllStep: int = 0

    def getGameScreenWithoutHUB(self) -> numpy.ndarray:
        return self.__gameScreenWithoutHUB

    def getGameScreenWithHUB(self) -> numpy.ndarray:
        return self.__gameScreenWithHUB

    def getGameScore(self) -> int:
        return self.__gameScore

    def getGameBestScore(self) -> int:
        return self.__gameBestScore

    def getGameStep(self) -> int:
        return self.__gameStep

    def getGameBestStep(self) -> int:
        return self.__gameBestStep

    def getNumberGame(self) -> int:
        return self.__numberGame

    def getLastDirection(self) -> int:
        return self.__lastDirection

    def getNumberAllStep(self) -> int:
        return self.__gameNumberAllStep

    def setStopGame(self, stop: bool) -> None:
        self.__stopGame = stop

