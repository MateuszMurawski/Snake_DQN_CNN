import copy
from typing import List, Optional
import torch
from torch import optim, nn

class DDQN:
    def __init__(self, model: nn.Module, learningRate: Optional[float] = 0.001, gamma: Optional[float] = 0.99, tau: Optional[float] = 0.01) -> None:
        self.__gamma: float = gamma
        self.__model: nn.Module = model
        self.__modelTarget: nn.Module = model
        self.__tau = tau

        self.__optimer: optim = optim.Adam(self.__model.parameters(), lr=learningRate)
        self.__criterion = nn.MSELoss()

        self.__device = 'cuda' if torch.cuda.is_available() else 'cpu'

    def train(self, state: List, action: List, reward: List, nextState: List) -> None:
        state = torch.tensor(state, dtype=torch.float).to(self.__device)
        nextState = torch.tensor(nextState, dtype=torch.float).to(self.__device)
        action = torch.tensor(action, dtype=torch.int).to(self.__device)
        reward = torch.tensor(reward, dtype=torch.float).to(self.__device)

        if len(state.shape) == 3:
            state = torch.unsqueeze(state, 0).to(self.__device)
            nextState = torch.unsqueeze(nextState, 0).to(self.__device)

        predict = self.__model(state).to(self.__device)
        maxNextActions = torch.argmax(self.__model(nextState).to(self.__device), 1)
        nextTarget = self.__modelTarget(nextState).to(self.__device)
        target = predict.clone().to(self.__device)

        for idx in range(len(state)):
            Qnew = reward[idx]
            if reward[idx] != -1.0:
                Qnew = reward[idx] + self.__gamma * nextTarget[idx][maxNextActions[idx]]
            target[idx][action[idx]] = Qnew

        self.__optimer.zero_grad()
        loss = self.__criterion(target, predict).to(self.__device)
        loss.backward()
        nn.utils.clip_grad_norm_(self.__model.parameters(), max_norm=1.0)
        self.__optimer.step()

        for targetParam, param in zip(self.__modelTarget.parameters(), self.__model.parameters()):
            targetParam.data.copy_(self.__tau * param + (1 - self.__tau) * targetParam)
