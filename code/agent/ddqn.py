from copy import deepcopy
from typing import List, Optional
import torch


class DDQN:
    """
    Double DQN class for training and evaluating reinforcement learning agents.
    """

    def __init__(self, model: torch.nn.Module, learningRate: Optional[float] = 0.001, gamma: Optional[float] = 0.99,
                 clipByNorm: Optional[float] = None, tau: Optional[float] = 0.01) -> None:
        """
        Initializes a new instance of the DDQN class.

        Args:
            model (torch.nn.Module): The neural network model to use for the agent.
            learningRate (float): The learning rate to use for optimizer.
            gamma (float): The discount factor to use for future rewards.
            clipByNorm (float): Parameter used to clip gradients during training. (default None, it means disabled).
            tau (float): The soft update parameter to use for updating the target network.

        Returns:
            None
        """

        self.__gamma: float = gamma
        self.__tau: float = tau
        self.__clipByNorm: float = clipByNorm
        self.__model: torch.nn.Module = model
        self.__modelTarget: torch.nn.Module = deepcopy(model)
        self.__modelTarget.eval()

        self.__optimer: torch.optim = torch.optim.Adam(self.__model.parameters(), lr=learningRate)
        self.__criterion = torch.nn.MSELoss()

        self.__device = 'cuda' if torch.cuda.is_available() else 'cpu'

    def train(self, state: List, action: List, reward: List, nextState: List) -> None:
        """
        Trains the agent using the provided batch of data.

        Args:
            state (List): The list of current states.
            action (List): The list of actions taken.
            reward (List): The list of rewards received.
            nextState (List): The list of next states.

        Returns:
            None
        """

        state = torch.tensor(state, dtype=torch.float).to(self.__device)
        nextState = torch.tensor(nextState, dtype=torch.float).to(self.__device)
        action = torch.tensor(action, dtype=torch.long).to(self.__device)
        reward = torch.tensor(reward, dtype=torch.float).to(self.__device)

        if len(state.shape) == 3:
            state = torch.unsqueeze(state, 0).to(self.__device)
            nextState = torch.unsqueeze(nextState, 0).to(self.__device)

        predict = self.__model(state).to(self.__device)
        target = predict.clone().to(self.__device)
        maxNextActions = torch.argmax(self.__model(nextState).to(self.__device), 1)
        nextTarget = self.__modelTarget(nextState).to(self.__device)

        for idx in range(len(state)):
            Qnew = reward[idx]
            if reward[idx] != -1.0 and reward[idx] != 1.0:
                Qnew = reward[idx] + self.__gamma * nextTarget[idx][maxNextActions[idx]]
            target[idx][action[idx]] = Qnew

        self.__optimer.zero_grad()
        loss = self.__criterion(target, predict).to(self.__device)
        loss.backward()

        if self.__clipByNorm is not None:
            torch.nn.utils.clip_grad_norm_(self.__model.parameters(), self.__clipByNorm)

        self.__optimer.step()

        for targetParam, param in zip(self.__modelTarget.parameters(), self.__model.parameters()):
            targetParam.data.copy_(self.__tau * param.data + (1.0 - self.__tau) * targetParam.data)
