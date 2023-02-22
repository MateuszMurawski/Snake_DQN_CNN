import abc
import gameInfo


class Agent:
    @abc.abstractmethod
    def getNewDirection(self, gameInfo: gameInfo.GameInfo) -> int:
        pass
