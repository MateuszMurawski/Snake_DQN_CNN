import random
import cv2
import torch

import agent
import cnn
import dqn
import gameInfo
import memeory


class AgentRandom(agent.Agent):
    def __init__(self):
        self.__lastScore: int = 0
        self.__lastNumberGame: int = 1
        self.__award: int = 0
        self.__lastPicture = None
        self.__sizeResize: int = 12
        self.__lastDirection: int = None

        self.__lr: float = 0.001
        self.__gamma: float = 0.9
        self.__epsilon: float = 1.0
        self.__stepWithoutLearn: int = 200
        self.__batchSize: int = 128

        self.__memory: memeory.Memory = memeory.Memory(1000000)
        self.__model: cnn.CNN = cnn.CNN()
        self.__dqn: dqn.DQN = dqn.DQN(self.__model, self.__lr, self.__gamma)

        self.__device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Device: ", self.__device)

    def getNewDirection(self, gameInfo: gameInfo.GameInfo) -> str:
        if gameInfo.getNumberAllStep():
            if self.__lastNumberGame < gameInfo.getNumberGame():
                self.__award = -1.0
                print("Predict direction: ", self.__lastDirection)
                print("Real direction: ", gameInfo.getLastDirection())
                print("Epsilon: ", self.__epsilon)
            elif self.__lastScore < gameInfo.getGameScore():
                self.__award = 1.0
            else:
                self.__award = 0.9

            self.__memory.add(self.__compresionPicture(self.__lastPicture), self.__lastDirection, self.__award,
                              self.__compresionPicture(gameInfo.getGameScreenWithoutHUB()))

        self.__lastScore = gameInfo.getGameScore()
        self.__lastNumberGame = gameInfo.getNumberGame()
        self.__lastPicture = gameInfo.getGameScreenWithoutHUB()

        if gameInfo.getNumberAllStep() < self.__stepWithoutLearn:
            self.__lastDirection = random.randint(0, 3)
            return self.__lastDirection
        else:

            self.__trainOneStep(self.__memory.getLastSample()[0], self.__lastDirection, self.__award, self.__compresionPicture(gameInfo.getGameScreenWithoutHUB()))

            if self.__award == -1.0:
                self.__trainBatch(self.__batchSize)

            self.__epsilon -= 0.000002
            p = random.randint(0, 10000)/10000.0

            if p > self.__epsilon:
                state = torch.tensor(self.__compresionPicture(gameInfo.getGameScreenWithoutHUB()), dtype=torch.float).to(self.__device)
                state = torch.unsqueeze(state, 0).to(self.__device)
                prediction = self.__model(state).to(self.__device)
                self.__lastDirection = torch.argmax(prediction).item()
                return self.__lastDirection
            else:
                self.__lastDirection = random.randint(0, 3)
                return self.__lastDirection


    def __compresionPicture(self, screen):
        cvImage = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(cvImage, (self.__sizeResize, self.__sizeResize), interpolation=cv2.INTER_NEAREST)
        return [resized.transpose()[2]/255]

    def __trainBatch(self, batchSize):
        miniSample = self.__memory.getSamples(batchSize)
        states, actions, rewards, nextStates = zip(*miniSample)
        self.__dqn.train(states, actions, rewards, nextStates)

    def __trainOneStep(self, state, action, reward, nextState):
        self.__dqn.train(state, [action], reward, nextState)
