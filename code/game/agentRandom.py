from random import randint

from game.gameInfo import GameInfo
from game.agent import Agent


class AgentRandom(Agent):
    """
    A class representing an agent that chooses a random direction.
    """

    def getNewDirection(self, gameInfo: GameInfo) -> int:
        """
        A method that returns a random direction.

        Args:
            gameInfo (GameInfo): an object of class GameInfo representing the current state of the game.

        Returns:
            int: value representing the new direction for the agent, using the following encoding:
                0: up
                1: right
                2: down
                3: left
        """

        return randint(0, 3)
