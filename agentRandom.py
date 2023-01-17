import random
import agent
import threading
import cv2

class AgentRandom(agent.Agent):
    def __init__(self):
        self.__pathDirPicture = "D:\\test\\"
        self.__pathDirCounter = "D:\\counter.txt"
        self.__lastScore = 0
        self.__lastNumberGame = 1
        self.__award = 0
        self.__numberPicture = 0
        self.__lastPicture = None
        self.__sizeResize = 12

        f = open(self.__pathDirCounter, "r")
        self.__numberPicture = int(f.read())
        f.close()
    def getNewDirection(self, gameInfo):
        if gameInfo.getNumberAllStep():
            if self.__lastNumberGame < gameInfo.getNumberGame():
                self.__award = -1

                f = open(self.__pathDirCounter, "w")
                f.write(str(self.__numberPicture+1))
                f.close()

            elif self.__lastScore < gameInfo.getGameScore():
                self.__award = 1
            else:
                self.__award = 0.1

            self.__numberPicture += 1
            threading.Thread(target=self.__compresionAndSaveImage, args=(gameInfo.getLastDirection(), self.__lastPicture, self.__award, self.__numberPicture, self.__pathDirPicture,)).start()

        self.__lastScore = gameInfo.getGameScore()
        self.__lastNumberGame = gameInfo.getNumberGame()
        self.__lastPicture = gameInfo.getGameScreenWithoutHUB()

        temp = random.randint(0, 3)

        if temp == 0:
            return 'UP'
        elif temp == 1:
            return 'DOWN'
        elif temp == 2:
            return 'RIGHT'
        else:
            return 'LEFT'

    def __compresionAndSaveImage(self, direction, screen, award, numberPicture, pathDir):
        cvImage = cv2.cvtColor(screen.transpose([1, 0, 2]), cv2.COLOR_BGR2RGB)
        resized = cv2.resize(cvImage, (self.__sizeResize, self.__sizeResize), interpolation=cv2.INTER_NEAREST)

        #resized = cvImage
        grayImage = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

        (row, col) = resized.shape[0:2]

        for i in range(row):
            for j in range(col):
                grayImage[i, j] = resized[i, j][2]

        cv2.imwrite(pathDir + str(numberPicture) + "_" + direction + "_" + str(award) + ".png", grayImage)
