from typing import Optional
import torch
import torch.nn as nn
import torch.nn.functional as F


class cnnDDQN(nn.Module):
    def __init__(self) -> None:
        super(cnnDDQN, self).__init__()

        self.__device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.__conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=5, stride=1).to(self.__device)
        self.__conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=2).to(self.__device)
        self.__conv3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=2).to(self.__device)

        self.__norm1 = nn.BatchNorm2d(16)
        self.__norm2 = nn.BatchNorm2d(32)

        self.__fc1Value = nn.Linear(64, 512).to(self.__device)
        self.__fc2Value = nn.Linear(512, 512).to(self.__device)
        self.__fc3Value = nn.Linear(512, 1).to(self.__device)

        self.__fc1Advantage = nn.Linear(64, 512).to(self.__device)
        self.__fc2Advantage = nn.Linear(512, 512).to(self.__device)
        self.__fc3Advantage = nn.Linear(512, 4).to(self.__device)

    def forward(self, x):
        x = F.relu(self.__conv1(x)).to(self.__device)
        x = self.__norm1(x).to(self.__device)
        x = F.relu(self.__conv2(x)).to(self.__device)
        x = self.__norm2(x).to(self.__device)
        x = F.relu(self.__conv3(x)).to(self.__device)
        x = torch.flatten(x, 1).to(self.__device)

        v = F.relu(self.__fc1Value(x)).to(self.__device)
        v = F.relu(self.__fc2Value(v)).to(self.__device)
        v = self.__fc3Value(v)

        a = F.relu(self.__fc1Advantage(x)).to(self.__device)
        a = F.relu(self.__fc2Advantage(a)).to(self.__device)
        a = self.__fc3Advantage(a)

        return v + (a - a.mean().to(self.__device))

    def save(self, fileName: Optional[str] = 'model'):
        torch.save(self.state_dict(), fileName + ".pth")


