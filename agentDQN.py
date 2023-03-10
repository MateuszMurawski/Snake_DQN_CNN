import math
import random
import time
from collections import deque
from typing import Optional, List
import cv2
import numpy
import numpy as np
import torch
import torch.nn as nn

import agent
import cnnDQN
import cnnDDQN
import ddqn
import dqn
import frame
import gameInfo
import memeory


class AgentDQN(agent.Agent):
    def __init__(self, learningRate: Optional[float] = 0.001, gamma: Optional[float] = 0.9,
                 stepWithoutLearn: Optional[int] = 77000, batchSize: Optional[int] = 128,
                 memorySize: Optional[int] = 500000, epsilonReduction: Optional[float] = 0.000001,
                 sizeResize: Optional[int] = 12, tau: Optional[float] = 0.01, fileName: Optional[str] = 'model'):

        self.__learningRate: float = learningRate
        self.__gamma: float = gamma
        self.__stepWithoutLearn: int = stepWithoutLearn
        self.__batchSize: int = batchSize
        self.__epsilonReduction: float = epsilonReduction
        self.__sizeResize: int = sizeResize
        self.__tau: float = tau
        self.__fileName: str = fileName

        self.__lastScore: int = 0
        self.__lastNumberGame: int = 1
        self.__award: int = 0
        self.__lastDirection: int = None
        self.__epsilon: float = 1.0
        self.__counterSkip: int = 0

        self.__memory: memeory.Memory = memeory.Memory(memorySize)
        self.__lastFrames: frame.Frame = frame.Frame(5)
        self.__model: nn.Module = cnnDQN.cnnDQN()
        self.__dqn: dqn.DQN = dqn.DQN(self.__model, self.__learningRate, self.__gamma)

        self.__device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Device: ", self.__device)

    def getNewDirection(self, gameInfo: gameInfo.GameInfo) -> int:
        self.__lastFrames.add(self.__compresionPicture(gameInfo.getGameScreenWithoutHUB()))
        self.__counterSkip += 1

        if self.__lastFrames.getSize() > 4:
            if self.__lastNumberGame < gameInfo.getNumberGame():
                self.__award = -1.0
                self.__counterSkip = 0

            elif self.__lastScore < gameInfo.getGameScore():
                self.__award = 1.0
                self.__counterSkip = 0

            else:
                self.__award = -0.1

            if self.__counterSkip > 4:
                self.__memory.add(self.__lastFrames.getNow(), self.__lastDirection, self.__award, self.__lastFrames.getNext())

        if gameInfo.getNumberGame() % 1000 == 0 and self.__award == -1.0:
            print("Epsilon: ", self.__epsilon)
            self.__model.save(self.__fileName + str(gameInfo.getNumberGame() // 1000))

        self.__lastScore = gameInfo.getGameScore()
        self.__lastNumberGame = gameInfo.getNumberGame()

        if gameInfo.getNumberAllStep() < self.__stepWithoutLearn:
            self.__lastDirection = random.randint(0, 3)
            return self.__lastDirection
        else:
            if self.__counterSkip > 4:
                self.__trainOneStep(self.__lastFrames.getNow(), self.__lastDirection, self.__award, self.__lastFrames.getNext())

            if self.__award == -1.0:
                self.__trainBatch(self.__batchSize)
                self.__award = 0.0

            self.__epsilon -= self.__epsilonReduction
            p = random.randint(0, 10000) / 10000.0

            if p > self.__epsilon and self.__lastFrames.getSize() > 4:
                state = torch.tensor(self.__lastFrames.getNext(), dtype=torch.float).to(self.__device)
                state = torch.unsqueeze(state, 0).to(self.__device)
                prediction = self.__model(state).to(self.__device)
                self.__lastDirection = torch.argmax(prediction).item()
                return self.__lastDirection
            else:
                self.__lastDirection = random.randint(0, 3)
                return self.__lastDirection

    def __compresionPicture(self, screen: numpy.ndarray) -> List:
        cvImage = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(cvImage, (self.__sizeResize, self.__sizeResize), interpolation=cv2.INTER_NEAREST)
        ret, binImg = cv2.threshold(resized, 1, 1, cv2.THRESH_BINARY)

        return binImg.transpose().tolist()

    def __trainBatch(self, batchSize: int) -> None:
        samples = self.__memory.getSamples(batchSize)
        states, actions, rewards, nextStates = zip(*samples)
        self.__dqn.train(states, actions, rewards, nextStates)

    def __trainOneStep(self, state: List, action: int, reward: float, nextState: List) -> None:
        self.__dqn.train(state, [action], [reward], nextState)