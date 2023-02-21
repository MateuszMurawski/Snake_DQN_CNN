import torch
from torch import optim, nn


class DQN:
    def __init__(self, model, lr: float, gamma: float) -> None:
        self.__device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss().to(self.__device)

    def train(self, state, action, reward: float, nextState, sumSumples: int):
        state = torch.tensor(state, dtype=torch.float).to(self.__device)
        nextState = torch.tensor(nextState, dtype=torch.float).to(self.__device)
        action = torch.tensor(action, dtype=torch.int).to(self.__device)
        reward = torch.tensor(reward, dtype=torch.float).to(self.__device)

        nextState = torch.unsqueeze(nextState, 1).to(self.__device)

        if sumSumples == 1:
            state = torch.unsqueeze(state, 0).to(self.__device)
            nextState = torch.unsqueeze(nextState, 0).to(self.__device)
            reward = torch.unsqueeze(reward, 0).to(self.__device)

        pred = self.model(state).to(self.__device)
        target = pred.clone().to(self.__device)

        for idx in range(len(state)):
            Qnew = reward[idx]
            if reward[idx] != -1.0:
                Qnew = reward[idx] + self.gamma * torch.max(self.model(nextState[idx]).to(self.__device))
            target[idx][action[idx]] = Qnew

        self.optimer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimer.step()
