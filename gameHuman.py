import random
import time
import pygame
import cv2

class Game:
    def __init__(self, snakeSpeed=10, windowX=240, windowY=240, unitSize=20):
        self.colorBlack = pygame.Color(0, 0, 0)
        self.colorWhite = pygame.Color(0, 255, 255)
        self.colorRed = pygame.Color(255, 0, 0)
        self.colorGreen = pygame.Color(85, 255, 0)
        self.colorViolet = pygame.Color(170, 0, 200)

        self.snakeSpeed = snakeSpeed
        self.windowX = windowX
        self.windowY = windowY
        self.unitSize = unitSize
        self.bestScore = 0

        pygame.init()
        pygame.display.set_caption('Snake Game')
        self.gameWindow = pygame.display.set_mode((self.windowX, self.windowY))
        self.fps = pygame.time.Clock()

        self.snakePosition = [self.windowX / 4, self.windowY / 2]
        self.snakeBody = [[self.windowX / 4, self.windowY / 2], [self.windowX / 4 - self.unitSize, self.windowY / 2], [self.windowX / 4 - self.unitSize * 2, self.windowY / 2]]
        self.fruitPosition = [random.randrange(1, (self.windowX // self.unitSize)) * self.unitSize, random.randrange(1, (self.windowY // self.unitSize)) * self.unitSize]

    def showScore(self, color, font, size):
        scoreFont = pygame.font.SysFont(font, size)
        scoreSurface = scoreFont.render('Score : ' + str(self.score), True, color)
        scoreRect = scoreSurface.get_rect()
        self.gameWindow.blit(scoreSurface, scoreRect)

        bestScoreFont = pygame.font.SysFont(font, size)
        bestScoreSurface = bestScoreFont.render('Best score : ' + str(self.bestScore), True, color)
        bestScoreRect = bestScoreSurface.get_rect()
        bestScoreRect.topright = (self.windowX, 0)
        self.gameWindow.blit(bestScoreSurface, bestScoreRect)

    def gameOver(self):
        myFont = pygame.font.SysFont('times new roman', 20)
        gameOverSurface = myFont.render('Your Score is : ' + str(self.score), True, self.colorRed)
        gameOverRect = gameOverSurface.get_rect()
        gameOverRect.midtop = (self.windowX / 2, self.windowX / 4)
        self.gameWindow.blit(gameOverSurface, gameOverRect)
        pygame.display.flip()
        time.sleep(2)

        if self.score > self.bestScore:
            self.bestScore = self.score

        self.newGame()

    def newGame(self):
        self.snakePosition = [self.windowX / 4, self.windowY / 2]
        self.snakeBody = [[self.windowX / 4, self.windowY / 2], [self.windowX / 4 - self.unitSize, self.windowY / 2], [self.windowX / 4 - self.unitSize * 2, self.windowY / 2]]
        self.fruitPosition = [random.randrange(1, (self.windowX // self.unitSize)) * self.unitSize, random.randrange(1, (self.windowY // self.unitSize)) * self.unitSize]

        self.fruitSpawn = True
        self.direction = 'RIGHT'
        self.changeTo = self.direction
        self.score = 0

    def startGame(self):
        self.newGame()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.changeTo = 'UP'
                    if event.key == pygame.K_DOWN:
                        self.changeTo = 'DOWN'
                    if event.key == pygame.K_LEFT:
                        self.changeTo = 'LEFT'
                    if event.key == pygame.K_RIGHT:
                        self.changeTo = 'RIGHT'

            if self.changeTo == 'UP' and self.direction != 'DOWN':
                self.direction = 'UP'
            if self.changeTo == 'DOWN' and self.direction != 'UP':
                self.direction = 'DOWN'
            if self.changeTo == 'LEFT' and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            if self.changeTo == 'RIGHT' and self.direction != 'LEFT':
                self.direction = 'RIGHT'

            if self.direction == 'UP':
                self.snakePosition[1] -= self.unitSize
            if self.direction == 'DOWN':
                self.snakePosition[1] += self.unitSize
            if self.direction == 'LEFT':
                self.snakePosition[0] -= self.unitSize
            if self.direction == 'RIGHT':
                self.snakePosition[0] += self.unitSize

            self.snakeBody.insert(0, list(self.snakePosition))
            if self.snakePosition[0] == self.fruitPosition[0] and self.snakePosition[1] == self.fruitPosition[1]:
                self.score += 1
                self.fruitSpawn = False
            else:
                self.snakeBody.pop()

            if not self.fruitSpawn:
                while not self.fruitSpawn:
                    self.fruitPosition = [random.randrange(1, (self.windowX // self.unitSize)) * self.unitSize, random.randrange(1, (self.windowY // self.unitSize)) * self.unitSize]
                    self.fruitSpawn = True

                    for pos in self.snakeBody:
                        if pos == self.fruitPosition:
                            break
                            self.fruitSpawn = False

            self.gameWindow.fill(self.colorBlack)

            for pos in self.snakeBody:
                pygame.draw.rect(self.gameWindow, self.colorGreen, pygame.Rect(pos[0], pos[1], self.unitSize, self.unitSize))

            pygame.draw.rect(self.gameWindow, self.colorViolet, pygame.Rect(self.snakeBody[0][0], self.snakeBody[0][1], self.unitSize, self.unitSize))
            pygame.draw.rect(self.gameWindow, self.colorRed, pygame.Rect(self.fruitPosition[0], self.fruitPosition[1], self.unitSize, self.unitSize))

            if self.snakePosition[0] < 0 or self.snakePosition[0] > self.windowX - self.unitSize:
                self.gameOver()
                continue

            if self.snakePosition[1] < 0 or self.snakePosition[1] > self.windowY - self.unitSize:
                self.gameOver()
                continue

            for block in self.snakeBody[1:]:
                if self.snakePosition[0] == block[0] and self.snakePosition[1] == block[1]:
                    self.gameOver()
                    continue

            self.showScore(self.colorWhite, 'times new roman', 20)
            pygame.display.update()
            self.fps.tick(self.snakeSpeed)

    def getScreenOnGame(self):
        np_image = pygame.surfarray.array3d(self.gameWindow)
        return cv2.cvtColor(np_image.transpose([1, 0, 2]), cv2.COLOR_BGR2RGB)

    def getScore(self):
        return self.score



