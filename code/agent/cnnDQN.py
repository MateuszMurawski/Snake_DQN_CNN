from typing import Optional
import torch


class CNNDQN(torch.nn.Module):
    """
    Convolutional Neural Network with Deep Q-Network architecture for reinforcement learning.
    """

    def __init__(self) -> None:
        """
        Initializes the CNN model for DQN.

        Returns:
            None
        """

        super(CNNDQN, self).__init__()

        self.__conv1 = torch.nn.Conv2d(in_channels=1, out_channels=16, kernel_size=5, stride=1)
        self.__conv2 = torch.nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1)
        self.__conv3 = torch.nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1)

        self.__pool = torch.nn.MaxPool2d(kernel_size=2, stride=2)

        self.__fc1 = torch.nn.Linear(64, 128)
        self.__fc2 = torch.nn.Linear(128, 128)
        self.__fc3 = torch.nn.Linear(128, 128)
        self.__fc4 = torch.nn.Linear(128, 4)

    def forward(self, x):
        """
        Performs a forward pass through the network.

        Args:
            x (torch.Tensor): Input tensor with shape (batch_size, channels, height, width).

        Returns:
            torch.Tensor: Output tensor with shape (batch_size, num_actions).
        """

        x = torch.nn.functional.relu(self.__conv1(x))
        x = torch.nn.functional.relu(self.__conv2(x))
        x = self.__pool(x)
        x = torch.nn.functional.relu(self.__conv3(x))
        x = torch.flatten(x, 1)

        x = torch.nn.functional.relu(self.__fc1(x))
        x = torch.nn.functional.relu(self.__fc2(x))
        x = torch.nn.functional.relu(self.__fc3(x))
        x = self.__fc4(x)

        return x

    def save(self, fileName: Optional[str] = 'model'):
        """
        Saves the parameters of the convolutional neural network to a file.

        Args:
            fileName (string): The name of the file to save the parameters to. Defaults to 'model.pth'.

        Returns:
            None
        """

        torch.save(self.state_dict(), fileName + ".pth")


