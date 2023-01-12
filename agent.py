import threading
import cv2
import gameAI
import random

class Agent:
    def __init__(self, snakeSpeed=1, windowX=240, windowY=240, unitSize=20):
        Agent.snakeSpeed = snakeSpeed
        Agent.windowX = windowX
        Agent.windowY = windowY
        Agent.unitSize = unitSize
        Agent.step = 0
        Agent.lastScore = 0
        Agent.pathDir = "D:\\test\\"
        Agent.numberPicture = 0
        Agent.newGame = True

    def start():
        Agent.newGame = gameAI.Game(Agent.snakeSpeed, Agent.windowX, Agent.windowY, Agent.unitSize)
        Agent.newGame.startGame()

    def getNewDirection():
        Agent.step += 1
        print(Agent.step)
        temp = random.randint(0,3)

        if temp == 0:
            return 'UP'
        elif temp == 1:
            return 'DOWN'
        elif temp == 2:
            return 'RIGHT'
        else:
            return 'LEFT'

    def newDataAboutGame(direction, screen, score):
        if Agent.newGame:
            Agent.newGame = False
            return

        if score == -1:
            award = -1
            Agent.lastScore = 1
            Agent.newGame = True

        elif score > Agent.lastScore:
            award = 1
            Agent.lastScore = score

        else:
            award = 0.1
            Agent.lastScore = score

        Agent.numberPicture += 1
        threading.Thread(target=Agent.compresionAndSaveImage, args=(direction, screen, award, Agent.numberPicture,)).start()

    def compresionAndSaveImage(direction, screen, award, numberPicture):
        cvImage = cv2.cvtColor(screen.transpose([1, 0, 2]), cv2.COLOR_BGR2RGB)

        #resized = cv2.resize(cvImage, (int(Agent.windowX / Agent.unitSize), int(Agent.windowY / Agent.unitSize)), interpolation=cv2.INTER_NEAREST)

        resized = cvImage
        grayImage = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

        (row, col) = resized.shape[0:2]

        for i in range(row):
            for j in range(col):
                grayImage[i, j] = resized[i, j][2]

        cv2.imwrite(Agent.pathDir + str(numberPicture) + "_" + direction + "_" + str(award) + ".png", grayImage)


