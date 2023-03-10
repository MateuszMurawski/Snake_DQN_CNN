from collections import deque
from typing import List


class Frame:
    def __init__(self, capacity: int) -> None:
        self.__memory: deque = deque(maxlen=capacity)

    def add(self, state: List) -> None:
        self.__memory.append(state)

    def getNow(self) -> List:
        elements = []

        for i in range(0, len(self.__memory) -1):
            elements.append(self.__memory[i])

        return elements

    def getNext(self) -> List:
        elements = []

        for i in range(1, len(self.__memory)):
            elements.append(self.__memory[i])

        return elements

    def getSize(self) -> int:
        return len(self.__memory)

    def clear(self) -> None:
        self.__memory.clear()

