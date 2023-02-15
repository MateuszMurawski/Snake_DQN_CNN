import agent
import agentRandom
import game

def main():
    newAgent: agent.Agent = agentRandom.AgentRandom()
    newGame: game.Game = game.Game(newAgent, 10)
    newGame.setShowScore(True)
    newGame.setShowStep(True)
    newGame.setSnakeSpeed(20)
    newGame.setShowGame(True)
    newGame.startGame()

if __name__ == '__main__':
    main()