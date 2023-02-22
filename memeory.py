from collections import deque
import random


class Memory:
    def __init__(self, capacity) -> None:
        self.__memory = deque(maxlen=capacity)

    def add(self, state, action, reward: float, next_state) -> None:
        self.__memory.append((state, action, reward, next_state))

    def getSamples(self, batchSize: int):
        return random.sample(self.__memory, batchSize)

    def getLastSample(self):
        return self.__memory[-1]
