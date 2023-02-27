import agent
import agentDQN
import agentRandom

import game

def main():
    newAgent: agent.Agent = agentDQN.AgentDQN(0.001, 0.9, 200, 128, 500000, 0.000001, 12)
    newGame: game.Game = game.Game(newAgent, 100000)
    newGame.setSnakeSpeed(10000000)
    newGame.setShowGame(True)
    newGame.setShowPlot(True)
    newGame.setShowScore(True)
    newGame.setShowStep(True)
    newGame.startGame()

if __name__ == '__main__':
    main()