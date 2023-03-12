from typing import Optional
import torch
import torch.nn as nn
import torch.nn.functional as F


class cnnDDQN(nn.Module):
    def __init__(self) -> None:
        super(cnnDDQN, self).__init__()

        self.__device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.__conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=5, stride=2, padding=2).to(self.__device)
        self.__conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=2, padding=1).to(self.__device)
        self.__conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=2, padding=1).to(self.__device)

        self.__fc1Value = nn.Linear(512, 512).to(self.__device)
        self.__fc1Advantage = nn.Linear(512, 512).to(self.__device)

        self.__fc2Value = nn.Linear(512, 1).to(self.__device)
        self.__fc2Advantage = nn.Linear(512, 4).to(self.__device)

    def forward(self, x):
        x = F.relu(self.__conv1(x)).to(self.__device)
        x = F.relu(self.__conv2(x)).to(self.__device)
        x = F.relu(self.__conv3(x)).to(self.__device)
        x = torch.flatten(x, 1).to(self.__device)

        v = F.relu(self.__fc1Value(x)).to(self.__device)
        a = F.relu(self.__fc1Advantage(x)).to(self.__device)

        v = self.__fc2Value(v)
        a = self.__fc2Advantage(a)

        return v + (a - a.mean().to(self.__device))

    def save(self, fileName: Optional[str] = 'model'):
        torch.save(self.state_dict(), fileName + ".pth")


