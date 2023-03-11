import agent
import agentDQN
import agentLoadModel
import agentRandom

import game

def main():
    newAgent: agent.Agent = agentDQN.AgentDQN(0.002, 0.9, 20000, 32, 20000, 0.000002, 84, 0.01, "modele\model")
    #newAgent: agent.Agent = agentLoadModel.AgentLoadModel("1.pth")
    newGame: game.Game = game.Game(newAgent, 1000000, False)
    newGame.setSnakeSpeed(100000000)
    newGame.setShowPlot(True)
    newGame.setShowScore(True)
    newGame.setShowStep(True)
    newGame.startGame()

if __name__ == '__main__':
    main()