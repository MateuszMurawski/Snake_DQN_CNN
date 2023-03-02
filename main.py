import agent
import agentDQN
import agentLoadModel
import agentRandom

import game

def main():
    newAgent: agent.Agent = agentDQN.AgentDQN(0.001, 0.99, 100000, 256, 1000000, 0.000001, 12, 0.8, 0.01)
    #newAgent: agent.Agent = agentLoadModel.AgentLoadModel("1.pth")
    newGame: game.Game = game.Game(newAgent, 1000000)
    newGame.setSnakeSpeed(1)
    newGame.setShowGame(True)
    newGame.setShowPlot(True)
    newGame.setShowScore(True)
    newGame.setShowStep(True)
    newGame.startGame()

if __name__ == '__main__':
    main()