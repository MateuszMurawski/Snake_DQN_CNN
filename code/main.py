from game.agent import Agent
from game.game import Game
from agent.agentDQN import AgentDQN
from agent.agentLoadModel import AgentLoadModel
from game.agentRandom import AgentRandom


def main():
    newAgent: Agent = AgentDQN(0.0001, 0.9, 150000, 24, 500000, 1.0, 0.001, 0.00000055, 12, "models/model", 1.0, 1000, 0.0006)
    #newAgent: agent.Agent = AgentLoadModel("models\DoubleDQN\model180.pth", 1)
    #newAgent: game.agentRandom = AgentRandom()
    newGame: Game = Game(newAgent, 10000000, True)
    newGame.setSnakeSpeed(100000000)
    newGame.setShowPlot(True)
    newGame.setShowScore(True)
    newGame.setShowStep(True)
    newGame.startGame()


if __name__ == '__main__':
    main()
