import random

import agent
import gameInfo


class AgentRandom(agent.Agent):
    def getNewDirection(self, gameInfo: gameInfo.GameInfo) -> int:
        return random.randint(0, 3)
