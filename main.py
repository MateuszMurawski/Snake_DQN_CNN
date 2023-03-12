import agent
import agentDQN
import agentLoadModel
import agentRandom

import game

def main():
    newAgent: agent.Agent = agentDQN.AgentDQN(0.002, 0.99, 100000, 32, 500000, 0.000001, 12, 0.8, 0.01, "modele\model")
    #newAgent: agent.Agent = agentLoadModel.AgentLoadModel("1.pth")
    newGame: game.Game = game.Game(newAgent, 1000000, False)
    newGame.setSnakeSpeed(100000000)
    newGame.setShowPlot(True)
    newGame.setShowScore(True)
    newGame.setShowStep(True)
    newGame.startGame()

if __name__ == '__main__':
    main()