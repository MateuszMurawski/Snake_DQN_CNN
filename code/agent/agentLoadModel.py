from typing import Optional, List
import cv2
import torch
from numpy import ndarray

from game.agent import Agent
from game.gameInfo import GameInfo
from agent.cnnDDQN import CNNDDQN
from agent.cnnDQN import CNNDQN


class AgentLoadModel(Agent):
    """
    A class representing an agent that loads a pre-trained convolutional neural network model for making decisions in a game.
    """

    def __init__(self, fileName: Optional[str] = 'model.pth', algorithm: Optional[int] = 1, sizeResize: Optional[int] = 12) -> None:
        """
        Initializes an AgentLoadModel object that loads a pre-trained CNN model from a file.

        Args:
            fileName (string): The name of the file that contains the pre-trained model parameters. Defaults to 'model.pth'.
            algorithm (int): Flag indicating which algorithm to use for a given model.
                1 - DQN and Double DQN.
                2 - Dueling DQN and Dueling Double DQN. Defaults to 1.
            sizeResize (int): The size to which the game screen should be resized before inputting it into the model. Defaults to 12.

        Returns:
            None
        """

        self.__device = 'cuda' if torch.cuda.is_available() else 'cpu'

        if algorithm == 1:
            self.__model: torch.nn.Module = CNNDQN().to(self.__device)
        elif algorithm == 2:
            self.__model: torch.nn.Module = CNNDDQN().to(self.__device)
        else:
            print("Incorrect option")
            exit()

        self.__model.load_state_dict(torch.load(fileName))
        self.__model.eval()
        self.__sizeResize = sizeResize

    def getNewDirection(self, gameInfo: GameInfo) -> int:
        """
        Gets a new direction prediction from the pre-trained CNN model based on the current game screen.

        Args:
            gameInfo (GameInfo): An object containing the current game state information.

        Returns:
            int: the predicted direction as a value:
                0: up
                1: right
                2: down
                3: left.
        """

        state = torch.tensor(self.__compressionPicture(gameInfo.getGameScreenWithoutHUB()), dtype=torch.float).to(self.__device)
        state = torch.unsqueeze(state, 0).to(self.__device)

        with torch.no_grad():
            prediction = self.__model(state).to(self.__device)

        return torch.argmax(prediction).item()

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

