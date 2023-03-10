import agent
import agentDQN
import agentLoadModel
import agentRandom

import game

def main():
    newAgent: agent.Agent = agentDQN.AgentDQN(0.0025, 0.99, 50000, 32, 50000, 0.000002, 84, 0.01, "modele\model")
    #newAgent: agent.Agent = agentLoadModel.AgentLoadModel("1.pth")
    newGame: game.Game = game.Game(newAgent, 1000000)
    newGame.setSnakeSpeed(100000000)
    newGame.setShowGame(True)
    newGame.setShowPlot(True)
    newGame.setShowScore(True)
    newGame.setShowStep(True)
    newGame.startGame()

if __name__ == '__main__':
    main()