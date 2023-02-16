import agent
import agentRandom
import game

def main():
    newAgent: agent.Agent = agentRandom.AgentRandom()
    newGame: game.Game = game.Game(newAgent, 100)
    newGame.setSnakeSpeed(50)
    newGame.setShowGame(True)
    newGame.setShowPlot(True)
    newGame.setShowScore(True)
    newGame.setShowStep(True)
    newGame.startGame()

if __name__ == '__main__':
    main()