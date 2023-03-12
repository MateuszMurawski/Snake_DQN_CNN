from collections import deque
import random
from typing import List


class Memory:
    def __init__(self, capacity: int) -> None:
        self.__memory: deque = deque(maxlen=capacity)

    def add(self, state: List, action: int, reward: float, next_state: List) -> None:
        self.__memory.append((state, action, reward, next_state))

    def getSamples(self, batchSize: int) -> List:
        if batchSize > len(self.__memory):
            return random.sample(self.__memory, len(self.__memory))
        else:
            return random.sample(self.__memory, batchSize)

