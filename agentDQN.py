import math
import random
from typing import Optional, List
import cv2
import numpy
import torch
import torch.nn as nn

import agent
import cnnDQN
import cnnDDQN
import ddqn
import dqn
import gameInfo
import memeory


class AgentDQN(agent.Agent):
    def __init__(self, learningRate: Optional[float] = 0.001, gamma: Optional[float] = 0.9,
                 stepWithoutLearn: Optional[int] = 77000, batchSize: Optional[int] = 128,
                 memorySize: Optional[int] = 500000, epsilonReduction: Optional[float] = 0.000001,
                 sizeResize: Optional[int] = 12, eta: Optional[float] = 0.8, tau: Optional[float] = 0.01):

        self.__learningRate: float = learningRate
        self.__gamma: float = gamma
        self.__stepWithoutLearn: int = stepWithoutLearn
        self.__batchSize: int = batchSize
        self.__epsilonReduction: float = epsilonReduction
        self.__sizeResize: int = sizeResize
        self.__eta: float = eta
        self.__tau: float = tau

        self.__lastScore: int = 0
        self.__lastNumberGame: int = 1
        self.__award: int = 0
        self.__lastPicture: numpy.ndarray = None
        self.__lastPictureAddToMemory: numpy.ndarray = None
        self.__lastDirection: int = None
        self.__epsilon: float = 1.0
        self.__awardReductionStep: float = 0.0
        self.__lastDistance: float = None

        self.__memoryGood: memeory.Memory = memeory.Memory(memorySize // 2)
        self.__memoryBad: memeory.Memory = memeory.Memory(memorySize // 2)
        self.__model: nn.Module = cnnDDQN.cnnDDQN()
        self.__dqn: ddqn.DDQN = ddqn.DDQN(self.__model, self.__learningRate, self.__gamma, self.__tau)

        self.__device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Device: ", self.__device)

    def getNewDirection(self, gameInfo: gameInfo.GameInfo) -> int:
        if gameInfo.getNumberAllStep():
            if self.__lastNumberGame < gameInfo.getNumberGame():
                self.__award = -1.0
                self.__awardReductionStep = 0.0
                if gameInfo.getNumberGame() % 1000 == 0:
                    print("Epsilon: ", self.__epsilon)
                    self.__model.save('1.pth')
            elif self.__lastScore < gameInfo.getGameScore():
                self.__award = 1.0
                self.__awardReductionStep = 0.0
            else:
                distance = self.__distance(gameInfo.getSnakePosition(), gameInfo.getFruitPosition())
                self.__award = math.log((((gameInfo.getGameScore() + 3) + self.__lastDistance) / (
                            (gameInfo.getGameScore() + 3) + distance)), gameInfo.getGameScore() + 3)
                self.__lastDistance = distance

                self.__awardReductionStep += (0.0015 / (gameInfo.getGameScore() + 1))
                self.__award -= self.__awardReductionStep

                if self.__award < -0.8:
                    self.__award = -0.8
                elif self.__award > 0.8:
                    self.__award = 0.8

            self.__lastPictureAddToMemory = self.__compresionPicture(self.__lastPicture)

            if self.__award > 0.5:
                self.__memoryGood.add(self.__lastPictureAddToMemory, self.__lastDirection, self.__award,
                                      self.__compresionPicture(gameInfo.getGameScreenWithoutHUB()))
            else:
                self.__memoryBad.add(self.__lastPictureAddToMemory, self.__lastDirection, self.__award,
                                     self.__compresionPicture(gameInfo.getGameScreenWithoutHUB()))

        self.__lastScore = gameInfo.getGameScore()
        self.__lastNumberGame = gameInfo.getNumberGame()
        self.__lastPicture = gameInfo.getGameScreenWithoutHUB()

        self.__lastDistance = self.__distance(gameInfo.getSnakePosition(), gameInfo.getFruitPosition())

        if gameInfo.getNumberAllStep() < self.__stepWithoutLearn:
            self.__lastDirection = random.randint(0, 3)
            return self.__lastDirection
        else:
            self.__trainOneStep(self.__lastPictureAddToMemory, self.__lastDirection, self.__award,
                                self.__compresionPicture(gameInfo.getGameScreenWithoutHUB()))

            if self.__award == -1.0:
                self.__trainBatch(self.__batchSize)

            self.__epsilon -= self.__epsilonReduction
            p = random.randint(0, 10000) / 10000.0

            if p > self.__epsilon:
                state = torch.tensor(self.__compresionPicture(gameInfo.getGameScreenWithoutHUB()),
                                     dtype=torch.float).to(self.__device)
                state = torch.unsqueeze(state, 0).to(self.__device)
                prediction = self.__model(state).to(self.__device)
                self.__lastDirection = torch.argmax(prediction).item()
                return self.__lastDirection
            else:
                self.__lastDirection = random.randint(0, 3)
                return self.__lastDirection

    def __compresionPicture(self, screen: numpy.ndarray) -> List:
        cvImage = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(cvImage, (self.__sizeResize, self.__sizeResize), interpolation=cv2.INTER_NEAREST)
        return [(resized.transpose()[2] / 255).tolist()]

    def __distance(self, x: List, y: List) -> float:
        return ((float(y[0] - x[0])) ** 2 + (float(y[1] - x[1])) ** 2) ** (1 / 2)

    def __trainBatch(self, batchSize: int) -> None:
        miniSamples = self.__memoryGood.getSamples(int(batchSize * self.__eta))
        miniSamples += self.__memoryBad.getSamples(int(batchSize * (1 - self.__eta)))
        states, actions, rewards, nextStates = zip(*miniSamples)
        self.__dqn.train(states, actions, rewards, nextStates)

        if self.__eta > 0.5:
            self.__eta -= 0.00003

    def __trainOneStep(self, state: List, action: int, reward: float, nextState: numpy.ndarray) -> None:
        self.__dqn.train(state, [action], [reward], nextState)
