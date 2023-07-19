from random import randint
from typing import Optional, List
import cv2
from numpy import ndarray
import torch

from agent.cnnDDQN import CNNDDQN
from agent.cnnDQN import CNNDQN
from agent.ddqn import DDQN
from agent.dqn import DQN
from game.agent import Agent
from agent.memeory import Memory
from game.gameInfo import GameInfo


class AgentDQN(Agent):
    """
    This class implements an agent that uses Deep Q-Network (DQN) / Double Deep Q-Network (DDQN) / Dueling Deep Q-Network (DDQN) / Dueling Double Q-Network (DDDQN) algorithm to play a game.
    It uses a convolutional neural network (CNN) as a function approximator for the Q-values.
    The agent receives the game information, makes a decision on the next action, and updates the CNN parameters using a batch of experiences sampled from its memory.
    The compressed game screen image is used as input to the CNN model. The agent uses an epsilon-greedy policy for exploration-exploitation trade-off.
    The epsilon value is reduced over time during training. The trained model can be saved periodically.
    The agent operates on either CPU or GPU depending on the availability of CUDA.
    """

    def __init__(self, learningRate: Optional[float] = 0.001, gamma: Optional[float] = 0.9,
                 stepWithoutLearn: Optional[int] = 77000, batchSize: Optional[int] = 128,
                 memorySize: Optional[int] = 500000, startEpsilon: Optional[float] = 1.0,
                 stopEpsilon: Optional[float] = 0.001, reductionEpsilon: Optional[float] = 0.000001,
                 sizeResize: Optional[int] = 12, fileName: Optional[str] = 'model', clipByNorm: Optional[float] = None,
                 saveModelAfterGamesNumber: Optional[int] = 1000, tau: Optional[float] = 0.01) -> None:

        """
        Initializes the DQNAgent object with the specified hyperparameters and creates the convolutional neural network model, training function and memory.

        Args:
            learningRate (float): The learning rate for the optimizer.
            gamma (float): The discount factor for future rewards.
            stepWithoutLearn (int): The number of steps before the agent starts learning.
            batchSize (int): The size of the batches used for training.
            memorySize (int): The maximum size of the memory buffer.
            startEpsilon (float): The starting value for epsilon.
            stopEpsilon (float): The minimum value for epsilon.
            reductionEpsilon (float): The reduction rate for epsilon.
            sizeResize (int): The size to which the game screen images are resized (default 12).
            fileName (str): The name of the file to save the model weights (default 'model').
            clipByNorm (float): Parameter used to clip gradients during training. (default None, it means disabled).
            saveModelAfterGamesNumber (int): The number of games after which to save the model (default 1000).
            tau (float): The interpolation parameter used for updating the target network. Only needed when using Double DQN.

        Returns:
            None
        """

        self.__device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Device: ", self.__device)

        self.__learningRate: float = learningRate
        self.__gamma: float = gamma
        self.__stepWithoutLearn: int = stepWithoutLearn
        self.__batchSize: int = batchSize
        self.__epsilon: float = startEpsilon
        self.__stopEpsilon: float = stopEpsilon
        self.__reductionEpsilon: float = reductionEpsilon
        self.__sizeResize: int = sizeResize
        self.__fileName: str = fileName
        self.__clipByNorm: float = clipByNorm
        self.__saveModelAfterGamesNumber: int = saveModelAfterGamesNumber
        self.__tau: float = tau

        self.__lastScore: int = 0
        self.__lastNumberGame: int = 1
        self.__award: int = 0
        self.__lastPicture: List = None
        self.__lastDirection: int = None

        self.__memory: Memory = Memory(memorySize)
        self.__model: torch.nn.Module = CNNDDQN().to(self.__device)
        self.__trainingFunction: DDQN = DDQN(self.__model, self.__learningRate, self.__gamma, self.__clipByNorm, self.__tau)

        """
        model = CNNDQN and trainingFunction = DQN -> DQN
        model = CNNDDQN and trainingFunction = DQN -> Dueling DQN
        model = CNNDQN and trainingFunction = DDQN -> Double DQN
        model = CNNDDQN and trainingFunction = DDQN -> Dueling Double DQN
        """

    def getNewDirection(self, gameInfo: GameInfo) -> int:
        """
        Gets the new direction for the agent based on the game information and the current state.

        Args:
            gameInfo (GameInfo): An object containing information about the current game state.

        Returns:
            int: An integer representing the new direction for the agent to take.
        """

        if gameInfo.getNumberAllStep():
            if self.__lastNumberGame < gameInfo.getNumberGame():
                self.__award = -1.0

                if gameInfo.getNumberGame() % self.__saveModelAfterGamesNumber == 0:
                    print("Epsilon: ", self.__epsilon)
                    self.__model.save(self.__fileName + str(gameInfo.getNumberGame()//self.__saveModelAfterGamesNumber))

            elif self.__lastScore < gameInfo.getGameScore():
                self.__award = 1.0

            else:
                self.__award = -0.05

            self.__memory.add(self.__lastPicture, self.__lastDirection, self.__award, self.__compressionPicture(gameInfo.getGameScreenWithoutHUB()))

        self.__lastScore = gameInfo.getGameScore()
        self.__lastNumberGame = gameInfo.getNumberGame()
        self.__lastPicture = self.__compressionPicture(gameInfo.getGameScreenWithoutHUB())

        if gameInfo.getNumberAllStep() < self.__stepWithoutLearn:
            self.__lastDirection = randint(0, 3)
            return self.__lastDirection

        else:
            self.__trainBatch(self.__batchSize)

            self.__epsilon -= self.__reductionEpsilon

            if self.__epsilon < self.__stopEpsilon:
                self.__epsilon = self.__stopEpsilon

            p = randint(0, 10000) / 10000.0

            if p > self.__epsilon:
                state = torch.tensor(self.__lastPicture, dtype=torch.float).to(self.__device)
                state = torch.unsqueeze(state, 0).to(self.__device)

                self.__model.eval()
                with torch.no_grad():
                    prediction = self.__model(state).to(self.__device)
                self.__model.train()

                self.__lastDirection = torch.argmax(prediction).item()
                return self.__lastDirection

            else:
                self.__lastDirection = randint(0, 3)
                return self.__lastDirection

    def __compressionPicture(self, screen: ndarray) -> List:
        """
        Compresses the game screen image to a format that can be input into the CNN model.

        Args:
            screen (ndarray): A numpy array representing the game screen image.

        Returns:
            List: A list containing the compressed game screen image.
        """

        cvImage = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(cvImage, (self.__sizeResize, self.__sizeResize), interpolation=cv2.INTER_NEAREST)
        return [(resized.transpose()[2] / 255).tolist()]

    def __trainBatch(self, batchSize: int) -> None:
        """
        Trains model using a batch of samples from the memory buffer.

        Args:
            batchSize (int): The size of the batch to use for training.

        Returns:
            None
        """

        samples = self.__memory.getSamples(batchSize)
        states, actions, rewards, nextStates = zip(*samples)
        self.__trainingFunction.train(states, actions, rewards, nextStates)
