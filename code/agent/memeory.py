from collections import deque
from random import sample
from typing import List


class Memory:
    """
    A replay memory implementation that stores experiences as tuples of (state, action, reward, nextState).
    """

    def __init__(self, capacity: int) -> None:
        """
        Initializes the memory with the given capacity.

        Args:
            capacity (int): The maximum number of experiences that can be stored in the memory.

        Returns:
            None
        """

        self.__memory: deque = deque(maxlen=capacity)

    def add(self, state: List, action: int, reward: float, nextState: List) -> None:
        """
        Adds a new experience to the memory.

        Args:
            state (List): The state observed by the agent.
            action (int): The action taken by the agent.
            reward (float): The reward received by the agent.
            nextState (List): The next state observed by the agent after taking the action.

        Returns:
            None
        """

        self.__memory.append((state, action, reward, nextState))

    def getSamples(self, batchSize: int) -> List:
        """
        Returns a random batch of experiences from the memory.

        Args:
            batchSize (int): The number of experiences to return in the batch.

        Returns:
            A list of experiences, where each experience is a tuple of (state, action, reward, nextState).
        """

        if batchSize > len(self.__memory):
            return sample(self.__memory, len(self.__memory))
        else:
            return sample(self.__memory, batchSize)
