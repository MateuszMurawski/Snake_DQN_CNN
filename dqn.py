from typing import List, Optional
import torch
from torch import optim, nn

class DQN:
    def __init__(self, model: nn.Module, learningRate: Optional[float] = 0.001, gamma: Optional[float] = 0.99) -> None:
        self.__learningRate: float = learningRate
        self.__gamma: float = gamma
        self.__model: nn.Module = model

        self.__optimer: optim = optim.Adam(model.parameters(), lr=self.__learningRate)
        self.__criterion = nn.MSELoss()

        self.__device = 'cuda' if torch.cuda.is_available() else 'cpu'

    def train(self, state: List, action: List, reward: List, nextState: List) -> None:
        state = torch.tensor(state, dtype=torch.float).to(self.__device)
        nextState = torch.tensor(nextState, dtype=torch.float).to(self.__device)
        action = torch.tensor(action, dtype=torch.int).to(self.__device)
        reward = torch.tensor(reward, dtype=torch.float).to(self.__device)

        nextState = torch.unsqueeze(nextState, 1).to(self.__device)

        if len(state.shape) == 3:
            state = torch.unsqueeze(state, 0).to(self.__device)
            nextState = torch.unsqueeze(nextState, 0).to(self.__device)

        predict = self.__model(state).to(self.__device)
        target = predict.clone().to(self.__device)

        for idx in range(len(state)):
            Qnew = reward[idx]
            if reward[idx] != -1.0 and reward[idx] != 1.0:
                Qnew = reward[idx] + self.__gamma * torch.max(self.__model(nextState[idx]).to(self.__device))
            target[idx][action[idx]] = Qnew

        self.__optimer.zero_grad()
        loss = self.__criterion(target, predict).to(self.__device)
        loss.backward()

        self.__optimer.step()