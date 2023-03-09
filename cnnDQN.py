from typing import Optional
import torch
import torch.nn as nn
import torch.nn.functional as F


class cnnDQN(nn.Module):
    def __init__(self) -> None:
        super(cnnDQN, self).__init__()

        self.__device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.__conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=5, stride=2, padding=2).to(self.__device)
        self.__conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1).to(self.__device)
        self.__conv3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1).to(self.__device)

        self.__batchNorm1 = nn.BatchNorm2d(32)
        self.__batchNorm2 = nn.BatchNorm2d(64)

        self.__fc1 = nn.Linear(256, 512).to(self.__device)
        self.__fc2 = nn.Linear(512, 512).to(self.__device)
        self.__fc3 = nn.Linear(512, 4).to(self.__device)

    def forward(self, x):
        x = F.relu(self.__conv1(x)).to(self.__device)
        x = F.relu(self.__conv2(x)).to(self.__device)
        x = self.__batchNorm1(x).to(self.__device)
        x = F.relu(self.__conv3(x)).to(self.__device)
        x = self.__batchNorm2(x).to(self.__device)
        x = torch.flatten(x, 1).to(self.__device)

        x = F.relu(self.__fc1(x)).to(self.__device)
        x = F.relu(self.__fc2(x)).to(self.__device)
        x = self.__fc3(x)

        return x

    def save(self, fileName: Optional[str] = 'model'):
        torch.save(self.state_dict(), fileName + ".pth")


