import agentRandom
import game

def main():
    newAgent = agentRandom.AgentRandom()
    newGame = game.Game(newAgent, 200)
    newGame.setShowScore(True)
    newGame.setShowStep(True)
    newGame.setSnakeSpeed(1000)
    newGame.startGame()

if __name__ == '__main__':
    main()