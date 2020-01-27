# PYGAME.TRANSFORM.ROTATE
import sys, pygame, random, math
import time
from pygame import *
from pygame.locals import *
from pygame.sprite import *

# Color setup
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 155, 255)
BROWN = (181, 101, 29)
LIGHTGRAY = (160, 160, 160)
LIGHTYELLOW = (250, 218, 94)


# NOT RECURSIVE
def snakeMovement(direction, screenList, xHead, yHead, frameSpeed):
    gameOver = False
    eatsFood = False

    if direction == "LEFT":
        if screenList[xHead - 1][yHead] == 0 and xHead != 0:
            xHead -= 1
        elif screenList[xHead - 1][yHead] == 2 and xHead != 0:
            xHead -= 1
            eatsFood = True
        elif (screenList[xHead - 1][yHead] == 1 or screenList[xHead - 1][yHead] == 3) and xHead != 0:
            gameOver = True
        elif xHead == 0:
            gameOver = True

    if direction == "RIGHT":
        if screenList[xHead + 1][yHead] == 0 and xHead != 15:
            xHead += 1
        elif screenList[xHead + 1][yHead] == 2 and xHead != 15:
            xHead += 1
            eatsFood = True
        elif (screenList[xHead + 1][yHead] == 1 or screenList[xHead + 1][yHead] == 3) and xHead != 15:
            gameOver = True
        elif xHead == 15:
            gameOver = True

    if direction == "UP":
        if screenList[xHead][yHead - 1] == 0 and yHead != 0:
            yHead -= 1
        elif screenList[xHead][yHead - 1] == 2 and yHead != 0:
            yHead -= 1
            eatsFood = True
        elif (screenList[xHead][yHead - 1] == 1 or screenList[xHead][yHead - 1] == 3) and yHead != 0:
            gameOver = True
        elif yHead == 0:
            gameOver = True

    if direction == "DOWN":
        if screenList[xHead][yHead + 1] == 0 and yHead != 19:
            yHead += 1
        elif screenList[xHead][yHead + 1] == 2 and yHead != 19:
            yHead += 1
            eatsFood = True
        elif (screenList[xHead][yHead + 1] == 1 or screenList[xHead][yHead + 1] == 3) and yHead != 19:
            gameOver = True
        elif yHead == 19:
            gameOver = True

    return xHead, yHead, gameOver, eatsFood


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def main():
    pygame.init()
    # Create the window, saving it to a variable. EFFECTIVE BOARD WILL BE 200 X 200. EACH BOX WILL BE 10 X 10 pixels
    DISPLAYSURF = pygame.display.set_mode((250, 250), pygame.RESIZABLE)
    # Aspect ratio is 1 x 1 (Square)
    pygame.display.set_caption("Snake/Wormy Clone")

    screenWidth = DISPLAYSURF.get_width()
    screenHeight = DISPLAYSURF.get_height()

    # INITIAL SCREEN SETUP - 22 x 22 grid (effectively 20 x 20, but need end identifiers)
    # 0 = empty screen, 1 = snake part, 2 = food part
    screenList = []

    for j in range(20):
        column = []
        for i in range(21):
            column.append(0)
        screenList.append(column)

    # Initial starting position of snake
    startPositionX = random.randint(0, 15)
    startPositionY = random.randint(0, 15)

    screenList[startPositionX][startPositionY] = 1  # head

    # Initialization of snake food
    foodPositionX = random.randint(0, 15)
    foodPositionY = random.randint(0, 15)

    screenList[foodPositionX][foodPositionY] = 2

    # PAUSE setup (including button) - NEED TO WORK ON PRESSEDPAUSE FUNCTION
    pressedPause = False

    # Sets up initial frames
    frames = 0

    # Initializing framespeed (rate at which frames grow)
    frameSpeed = (1 / 64)

    # Initializes timeTemp to ensure that the snake moves every time frame reaches a new whole number
    timeTemp = 0

    # Sets up START booleans (Space for start, pressedStart for ongoing
    pressedSpace = False
    pressedStart = False

    # For first runthrough that determines random initial direction
    runThrough = 0
    direction = 'RIGHT'
    direction2 = "RIGHT"

    # Initializing first and last colored tiles - these are the only ones that need to be updated each time
    xHead = startPositionX
    yHead = startPositionY

    # Initializes snakeHeadsX and snakeHeadsY arrays that keep track of X's and Y's of the head
    snakeHeadsX = []
    snakeHeadsY = []

    snakeHeadsX.append(xHead)  # Point 1
    snakeHeadsY.append(yHead)

    snakeHeadsXTrack = 0
    snakeHeadsYTrack = 0

    # HERE
    # Initial starting position of snake # 2
    startPositionX2 = 0
    startPositionY2 = 0

    # Initializing first and last colored tiles - these are the only ones that need to be updated each time
    xHead2 = startPositionX2
    yHead2 = startPositionY2

    # Initializes snakeHeadsX and snakeHeadsY arrays that keep track of X's and Y's of the head
    snakeHeadsX2 = []
    snakeHeadsY2 = []

    snakeHeadsXTrack2 = 0
    snakeHeadsYTrack2 = 0

    # Initializes GAME OVER boolean (Snake 1)
    gameOver = False

    # Initializes GAME OVER boolean (Snake 2)
    gameOver2 = False

    # Initialize booleans for identifying which game mode is active
    standardGame = True
    fastGame = False
    twoPlayerGame = False

    while True:
        # Font and text size setup - TEXT RATIO IS (10 / 250)
        if pressedStart is True:
            frames += frameSpeed
        textSize = int(screenWidth / 20)
        smallTextSize = int(screenWidth / 30)
        BASICFONTLarge = pygame.font.Font('freesansbold.ttf', textSize)
        BASICFONTSmall = pygame.font.Font('freesansbold.ttf', smallTextSize)

        DISPLAYSURF.fill(WHITE)

        # Sets up menu area
        pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, (
        DISPLAYSURF.get_width() * (4 / 5), 0, DISPLAYSURF.get_width() * (1 / 5), DISPLAYSURF.get_height()))
        # pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, (
        # 0, DISPLAYSURF.get_width() * (4 / 5), DISPLAYSURF.get_width(), DISPLAYSURF.get_height() * (1 / 5)))

        # Game Over text
        if gameOver is True or gameOver2 is True:
            pressedStart = False
            youDiedText = "DEATH"
            gameOverText = "GAME OVER"
            theYouDiedText = BASICFONTSmall.render(youDiedText, True, BLACK)
            theGameOverText = BASICFONTSmall.render(gameOverText, True, BLACK)
            pygame.draw.rect(DISPLAYSURF, WHITE, (0, 0, DISPLAYSURF.get_width(), DISPLAYSURF.get_height()))
            DISPLAYSURF.blit(theYouDiedText, (DISPLAYSURF.get_width() * (4 / 10), DISPLAYSURF.get_height() * (4 / 10)))
            DISPLAYSURF.blit(theGameOverText, (DISPLAYSURF.get_width() * (4 / 10), DISPLAYSURF.get_height() * (5 / 10)))

        # Starting text
        if pressedStart is False and (gameOver is False and gameOver2 is False):
            startingText1 = "PRESS ANY KEY"
            startingText2 = "TO GO"
            theStartingText1 = BASICFONTLarge.render(startingText1, True, BLACK)
            theStartingText2 = BASICFONTLarge.render(startingText2, True, BLACK)
            DISPLAYSURF.blit(theStartingText1, (55, 55))
            DISPLAYSURF.blit(theStartingText2, (55, 55 + textSize))

        # Runs at first start to determine snake movement
        if pressedStart is True and runThrough == 0:
            runThrough += 1
            temp = random.randint(0, 3)
            if temp == 0:
                direction = "LEFT"
            elif temp == 1:
                direction = "RIGHT"
            elif temp == 2:
                direction = "UP"
            elif temp == 3:
                direction = "DOWN"

            if twoPlayerGame is True:
                temp2 = random.randint(0, 3)
                if temp2 == 0:
                    direction2 = "LEFT"
                elif temp2 == 1:
                    direction2 = "RIGHT"
                elif temp2 == 2:
                    direction2 = "UP"
                elif temp2 == 3:
                    direction2 = "DOWN"

        # STUFF THAT RUNS WHEN THE GAME IS RUNNING AFTER THE FIRST RUN
        if pressedStart is True and runThrough != 0:
            ongoingText1 = "PRESS"
            ongoingText2 = "SPACE"
            ongoingText3 = "TO PAUSE"
            theOngoingText1 = BASICFONTSmall.render(ongoingText1, True, BLACK)
            theOngoingText2 = BASICFONTSmall.render(ongoingText2, True, BLACK)
            theOngoingText3 = BASICFONTSmall.render(ongoingText3, True, BLACK)
            DISPLAYSURF.blit(theOngoingText1, (screenWidth * (81 / 100), screenWidth * (40 / 100)))
            DISPLAYSURF.blit(theOngoingText2, (screenWidth * (81 / 100), screenWidth * (50 / 100)))
            DISPLAYSURF.blit(theOngoingText3, (screenWidth * (81 / 100), screenWidth * (60 / 100)))

            # Makes snake move in current direction
            if truncate(frames) == timeTemp:
                tempX = snakeHeadsX[snakeHeadsXTrack]
                tempY = snakeHeadsY[snakeHeadsYTrack]

                print(frames)
                timeTemp += 1
                xHead, yHead, gameOver, eatsFood = snakeMovement(direction, screenList, xHead, yHead, frameSpeed)
                screenList[snakeHeadsX[snakeHeadsXTrack]][snakeHeadsY[snakeHeadsYTrack]] = 0  # Removes old tail
                snakeHeadsX.append(xHead)  # adds new snake head x to head array
                snakeHeadsXTrack += 1  # iterates snake head x tracker
                snakeHeadsY.append(yHead)  # adds new snake head y to head array
                snakeHeadsYTrack += 1  # iterates snake head y tracker
                print(direction)
                pygame.draw.rect(DISPLAYSURF, WHITE,
                                 (0, 0, DISPLAYSURF.get_width() * (4 / 5), DISPLAYSURF.get_height()))
                screenList[xHead][yHead] = 1

                # If a piece of food is eaten, add one more part to snake. Then creates a new piece
                if eatsFood is True:
                    if fastGame is True:
                        frameSpeed = (frameSpeed * 1.2)
                    screenList[tempX][tempY] = 1  # restore old tail
                    snakeHeadsXTrack -= 1
                    snakeHeadsYTrack -= 1

                    foodPositionX = random.randint(0, 15)
                    foodPositionY = random.randint(0, 15)

                    # Makes sure that food doesn't spawn on snake
                    while screenList[foodPositionX][foodPositionY] == 1 or screenList[foodPositionX][foodPositionY] == 3:
                        foodPositionX = random.randint(0, 15)
                        foodPositionY = random.randint(0, 15)

                    screenList[foodPositionX][foodPositionY] = 2

                # Movement for snake 2 if two player mode is active
                if twoPlayerGame is True:
                    tempX2 = snakeHeadsX2[snakeHeadsXTrack2]
                    tempY2 = snakeHeadsY2[snakeHeadsYTrack2]

                    print(frames)
                    xHead2, yHead2, gameOver2, eatsFood2 = snakeMovement(direction2, screenList, xHead2, yHead2, frameSpeed)
                    screenList[snakeHeadsX2[snakeHeadsXTrack2]][snakeHeadsY2[snakeHeadsYTrack2]] = 0  # Removes old tail
                    snakeHeadsX2.append(xHead2)  # adds new snake head x to head array
                    snakeHeadsXTrack2 += 1  # iterates snake head x tracker
                    snakeHeadsY2.append(yHead2)  # adds new snake head y to head array
                    snakeHeadsYTrack2 += 1  # iterates snake head y tracker
                    print(direction2)
                    pygame.draw.rect(DISPLAYSURF, WHITE,
                                     (0, 0, DISPLAYSURF.get_width() * (4 / 5), DISPLAYSURF.get_height()))
                    screenList[xHead2][yHead2] = 3

                    # If a piece of food is eaten, add one more part to snake. Then creates a new piece
                    if eatsFood2 is True:
                        screenList[tempX2][tempY2] = 3  # restore old tail
                        snakeHeadsXTrack2 -= 1
                        snakeHeadsYTrack2 -= 1

                        foodPositionX = random.randint(0, 15)
                        foodPositionY = random.randint(0, 15)

                        # Makes sure that food doesn't spawn on snake
                        while screenList[foodPositionX][foodPositionY] == 1 or screenList[foodPositionX][foodPositionY] == 3:
                            foodPositionX = random.randint(0, 15)
                            foodPositionY = random.randint(0, 15)

                        screenList[foodPositionX][foodPositionY] = 2

        if gameOver is False and gameOver2 is False:

            # Sets up Standard Mode (1 Player, No Speed Boost)
            standardModeButton = pygame.draw.rect(DISPLAYSURF, WHITE, (
                screenWidth * (81 / 100), screenWidth * (1 / 4), screenWidth * (9 / 50), screenHeight * (1 / 18)))
            restartText = "STANDARD"
            theRestartText = BASICFONTSmall.render(restartText, True, BLACK)
            DISPLAYSURF.blit(theRestartText, (screenWidth * (81 / 100), screenWidth * (1 / 4)))

            # Sets up Acceleration Mode (1 Player, Speed Boost with food eaten)
            speedModeButton = pygame.draw.rect(DISPLAYSURF, WHITE, (
                screenWidth * (81 / 100), screenWidth * (5 / 16), screenWidth * (9 / 50), screenHeight * (1 / 18)))
            restartText = "SPEED-UP"
            theRestartText = BASICFONTSmall.render(restartText, True, BLACK)
            DISPLAYSURF.blit(theRestartText, (screenWidth * (81 / 100), screenWidth * (5 / 16)))

            # Sets up 2 Player Mode (2 Players, Speed Boost with food eaten)
            twoPlayerModeButton = pygame.draw.rect(DISPLAYSURF, WHITE, (
                screenWidth * (81 / 100), screenWidth * (6 / 16), screenWidth * (9 / 50), screenHeight * (1 / 18)))
            restartText = "2-PLAYERS"
            theRestartText = BASICFONTSmall.render(restartText, True, BLACK)
            DISPLAYSURF.blit(theRestartText, (screenWidth * (81 / 100), screenWidth * (6 / 16)))

        # Identify and draw location(s) of snake part(s) as indicated in screenList array
        for a in range(20):
            for b in range(20):
                if screenList[a][b] == 1:
                    # CREATE A SPRITE FOR THIS?
                    pygame.draw.rect(DISPLAYSURF, BLUE, (
                    a * (screenWidth / 20), b * (screenHeight / 20), screenWidth / 20, screenHeight / 20))
                elif screenList[a][b] == 2:
                    pygame.draw.rect(DISPLAYSURF, GREEN, (
                        a * (screenWidth / 20), b * (screenHeight / 20), screenWidth / 20, screenHeight / 20))
                elif screenList[a][b] == 3: # Snake 2
                    # CREATE A SPRITE FOR THIS?
                    pygame.draw.rect(DISPLAYSURF, BLACK, (
                    a * (screenWidth / 20), b * (screenHeight / 20), screenWidth / 20, screenHeight / 20))

        pygame.display.update()

        # EVENT CHECKER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # PAUSE AND GO FUNCTIONALITY
                if event.key == pygame.K_SPACE and pressedStart is False:
                    pressedStart = True
                elif event.key == pygame.K_SPACE and pressedStart is True:
                    pressedStart = False

                # CHANGE DIRECTION FUNCTIONALITY FOR SNAKE 1
                if event.key == pygame.K_RIGHT and pressedStart is True and direction != "LEFT":
                    direction = "RIGHT"
                if event.key == pygame.K_LEFT and pressedStart is True and direction != "RIGHT":
                    direction = "LEFT"
                if event.key == pygame.K_UP and pressedStart is True and direction != "DOWN":
                    direction = "UP"
                if event.key == pygame.K_DOWN and pressedStart is True and direction != "UP":
                    direction = "DOWN"

                # CHANGE DIRECTION FUNCTIONALITY FOR SNAKE 2
                if event.key == pygame.K_d and pressedStart is True and twoPlayerGame is True and direction2 != "LEFT":
                    direction2 = "RIGHT"
                if event.key == pygame.K_a and pressedStart is True and twoPlayerGame is True and direction2 != "RIGHT":
                    direction2 = "LEFT"
                if event.key == pygame.K_w and pressedStart is True and twoPlayerGame is True and direction2 != "DOWN":
                    direction2 = "UP"
                if event.key == pygame.K_s and pressedStart is True and twoPlayerGame is True and direction2 != "UP":
                    direction2 = "DOWN"

            # Detects if Standard Mode Button is clicked.
            if pygame.mouse.get_pressed()[0] and standardModeButton.collidepoint(pygame.mouse.get_pos()):
                standardGame = True
                fastGame = False
                twoPlayerGame = False

                # Reset frames
                frames = 0
                timeTemp = 0

                # Reset runthrough
                runThrough = 0

                # Reset visual "board"
                for a in range(20):
                    for b in range(21):
                        screenList[a][b] = 0

                # Initial starting position of snake
                startPositionX = random.randint(0, 15)
                startPositionY = random.randint(0, 15)

                screenList[startPositionX][startPositionY] = 1  # head

                # Initialization of snake food
                foodPositionX = random.randint(0, 15)
                foodPositionY = random.randint(0, 15)

                screenList[foodPositionX][foodPositionY] = 2

                # Initializing first and last colored tiles - these are the only ones that need to be updated each time
                xHead = startPositionX
                yHead = startPositionY

                # Initializes snakeHeadsX and snakeHeadsY arrays that keep track of X's and Y's of the head
                del snakeHeadsX[0: len(snakeHeadsX)]
                del snakeHeadsY[0: len(snakeHeadsY)]

                snakeHeadsX.append(xHead)  # Point 1
                snakeHeadsY.append(yHead)

                snakeHeadsXTrack = 0
                snakeHeadsYTrack = 0

            # Detects if Speed Button is clicked.
            if pygame.mouse.get_pressed()[0] and speedModeButton.collidepoint(pygame.mouse.get_pos()):
                standardGame = False
                fastGame = True
                twoPlayerGame = False

                # Reset frames
                frames = 0
                timeTemp = 0

                # Reset runthrough
                runThrough = 0

                # Reset visual "board"
                for a in range(20):
                    for b in range(21):
                        screenList[a][b] = 0

                # Initial starting position of snake # 1
                startPositionX = random.randint(0, 15)
                startPositionY = random.randint(0, 15)

                screenList[startPositionX][startPositionY] = 1  # 1 head

                # Initialization of snake food
                foodPositionX = random.randint(0, 15)
                foodPositionY = random.randint(0, 15)

                screenList[foodPositionX][foodPositionY] = 2

                # Initializing first and last colored tiles - these are the only ones that need to be updated each time
                xHead = startPositionX
                yHead = startPositionY

                # Initializes snakeHeadsX and snakeHeadsY arrays that keep track of X's and Y's of the head
                del snakeHeadsX[0: len(snakeHeadsX)]
                del snakeHeadsY[0: len(snakeHeadsY)]

                snakeHeadsX.append(xHead)  # Point 1
                snakeHeadsY.append(yHead)

                snakeHeadsXTrack = 0
                snakeHeadsYTrack = 0

            # Detects if Two Player Mode Button is clicked.
            if pygame.mouse.get_pressed()[0] and twoPlayerModeButton.collidepoint(pygame.mouse.get_pos()):
                standardGame = False
                fastGame = False
                twoPlayerGame = True

                # Reset frames
                frames = 0
                timeTemp = 0

                # Reset runthrough
                runThrough = 0

                # Reset visual "board"
                for a in range(20):
                    for b in range(21):
                        screenList[a][b] = 0

                # Initial starting position of snake 1
                startPositionX = random.randint(0, 15)
                startPositionY = random.randint(0, 15)

                # Initial starting position of snake 2
                startPositionX2 = random.randint(0, 15)
                startPositionY2 = random.randint(0, 15)

                if startPositionX2 == startPositionX and startPositionY2 == startPositionY:
                    startPositionX2 = random.randint(0, 15)
                    startPositionY2 = random.randint(0, 15)

                screenList[startPositionX][startPositionY] = 1  # head 1
                screenList[startPositionX2][startPositionY2] = 3  # head 2

                # Initialization of snake food
                foodPositionX = random.randint(0, 15)
                foodPositionY = random.randint(0, 15)

                while (startPositionX == foodPositionX and startPositionY == foodPositionY) or (startPositionX2 == foodPositionX and startPositionY2 == foodPositionY):
                    foodPositionX = random.randint(0, 15)
                    foodPositionY = random.randint(0, 15)

                screenList[foodPositionX][foodPositionY] = 2

                # Initializing first and last colored tiles - these are the only ones that need to be updated each time
                xHead = startPositionX
                yHead = startPositionY
                xHead2 = startPositionX2
                yHead2 = startPositionY2

                # Initializes snakeHeadsX and snakeHeadsY arrays that keep track of X's and Y's of the head
                del snakeHeadsX[0: len(snakeHeadsX)]
                del snakeHeadsY[0: len(snakeHeadsY)]
                del snakeHeadsX2[0: len(snakeHeadsX2)]
                del snakeHeadsY2[0: len(snakeHeadsY2)]

                snakeHeadsX.append(xHead)  # Point 1
                snakeHeadsY.append(yHead)
                snakeHeadsX2.append(xHead2)  # Point 2
                snakeHeadsY2.append(yHead2)

                snakeHeadsXTrack = 0
                snakeHeadsYTrack = 0
                snakeHeadsXTrack2 = 0
                snakeHeadsYTrack2 = 0

            if event.type == pygame.VIDEORESIZE:
                # There's some code to add back window content here.
                DISPLAYSURF = pygame.display.set_mode((event.w, event.h),
                                                      pygame.RESIZABLE)
                if DISPLAYSURF.get_width() < DISPLAYSURF.get_height():
                    DISPLAYSURF = pygame.display.set_mode((DISPLAYSURF.get_width(), DISPLAYSURF.get_width()),
                                                          pygame.RESIZABLE)
                    screenWidth = DISPLAYSURF.get_width()
                    screenHeight = DISPLAYSURF.get_width()
                elif DISPLAYSURF.get_height() < DISPLAYSURF.get_width():
                    DISPLAYSURF = pygame.display.set_mode((DISPLAYSURF.get_height(), DISPLAYSURF.get_height()),
                                                          pygame.RESIZABLE)
                    screenWidth = DISPLAYSURF.get_height()
                    screenHeight = DISPLAYSURF.get_height()

                print(DISPLAYSURF.get_width())
                print(DISPLAYSURF.get_height())


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
    sys.exit()
