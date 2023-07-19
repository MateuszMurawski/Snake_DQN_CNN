import abc
from game.gameInfo import GameInfo


class Agent:
    """
    An abstract class representing an agent in the snake game.
    """

    @abc.abstractmethod
    def getNewDirection(self, gameInfo: GameInfo) -> int:
        """
        An abstract method that returns a new direction for an agent.

        Args:
             gameInfo (GameInfo): an object of class GameInfo representing the current state of the game.

        Returns:
             int: value representing the random direction.
        """

        pass
