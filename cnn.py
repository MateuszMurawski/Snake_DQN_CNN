import os

import torch
import torch.nn as nn
import torch.nn.functional as F


class CNN(nn.Module):
    def __init__(self) -> None:
        super(CNN, self).__init__()

        self.__device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.__conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=5, stride=2, padding=2).to(self.__device)
        self.__conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=2, padding=1).to(self.__device)
        self.__conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=2, padding=1).to(self.__device)
        self.__fc1 = nn.Linear(512, 512).to(self.__device)
        self.__fc2 = nn.Linear(512, 4).to(self.__device)

    def forward(self, x):
        x = F.relu(self.__conv1(x))
        x = F.relu(self.__conv2(x))
        x = F.relu(self.__conv3(x))
        x = torch.flatten(x, 1)
        x = F.relu(self.__fc1(x))
        x = self.__fc2(x)

        return x

    def save(self, fileName='model_name.pth'):
        modelFolderPpath = 'Path'
        fileName = os.path.join(modelFolderPpath, fileName)
        torch.save(self.state_dict(), fileName)


