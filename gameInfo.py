class GameInfo:
    def __init__(self):
        self.__gameScreenWithoutHUB = None
        self.__gameScreenWithHUB = None
        self.__gameScore = None
        self.__gameBestScore = None
        self.__gameStep = None
        self.__gameBestStep = None
        self.__numberGame = None
        self.__lastDirection = None
        self.__stopGame = False
        self.__gameNumberAllStep = None

    def getGameScreenWithoutHUB(self):
        return self.__gameScreenWithoutHUB

    def getGameScreenWithHUB(self):
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

    def getLastDirection(self) -> str:
        return self.__lastDirection

    def getNumberAllStep(self) -> int:
        return self.__gameNumberAllStep

    def setStopGame(self, stop: bool):
        self.__stopGame = stop

