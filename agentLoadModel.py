from typing import Optional, List
import cv2
import numpy
import torch
from torch import nn

import agent
import gameInfo
from cnnDDQN import cnnDDQN


class AgentLoadModel(agent.Agent):
    def __init__(self, fileName: Optional[str] = 'model.pth') -> None:
        self.__model: nn.Module = cnnDDQN.cnnDDQN()
        self.__model.load_state_dict(torch.load(fileName))
    def getNewDirection(self, gameInfo: gameInfo.GameInfo) -> int:
        state = torch.tensor(self.__compresionPicture(gameInfo.getGameScreenWithoutHUB()),
                             dtype=torch.float).to(self.__device)
        state = torch.unsqueeze(state, 0).to(self.__device)
        prediction = self.__model(state).to(self.__device)
        return torch.argmax(prediction).item()
    def __compresionPicture(self, screen: numpy.ndarray) -> List:
        cvImage = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(cvImage, (self.__sizeResize, self.__sizeResize), interpolation=cv2.INTER_NEAREST)
        return [(resized.transpose()[2] / 255).tolist()]

