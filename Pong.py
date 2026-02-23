import pygame, sys
import random

def ballPhysics(ball, player, opponent, ballspeedX, 
                ballspeedY, screenWidth, screenHeight,
                playerScore, opponentScore):
    
    # Ball movement and collisions
    ball.x += ballspeedX
    ball.y += ballspeedY

    # To make the ball go in the other direction
    # Multily the speed by -1, to reverse the speeed
    if ball.top <= 0 or ball.bottom >= screenHeight:
        ballspeedY *= -1

    # Determines whos wins and score
    if ball.left <= 0: 
        ballspeedX, ballspeedY = ballRestart(ball, screenWidth, screenHeight,
                                                ballspeedX, ballspeedY)
        playerScore += 1              
    elif ball.right >= screenWidth:
        ballspeedX, ballspeedY = ballRestart(ball, screenWidth, screenHeight,
                                                ballspeedX, ballspeedY)
        opponentScore += 1  
        
    # Handled the ball getting caught inside a paddle
    if ball.colliderect(player) and ballspeedX > 0:
        ballspeedX *= -1
        ball.right = player.left
    elif ball.colliderect(opponent) and ballspeedX < 0:
        ballspeedX *= -1
        ball.left = opponent.right
    
    return ballspeedX, ballspeedY, playerScore, opponentScore

def playerMovement(player, playerSpeed, screenHeight):
    player.y += playerSpeed 
    # Handles the player from going out of bounds
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screenHeight:
        player.bottom = screenHeight

def opponentAI(opponent, opponentSpeed, screenHeight, ball):
    if opponent.centery < ball.centery:
        opponent.centery += opponentSpeed
    elif opponent.centery > ball.centery:
        opponent.centery -= opponentSpeed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screenHeight:
        opponent.bottom = screenHeight
    
def ballRestart(ball, screenWidth, screenHeight,
                ballspeedX, ballspeedY):
    ball.center = (screenWidth/2, screenHeight/2)
    ballspeedY *= random.choice((1,-1))
    ballspeedX *= random.choice((1,-1))

    return ballspeedX, ballspeedY

# General setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screenWidth = 1280
screenHeight = 960

# Returns surface display object
screen = pygame.display.set_mode((screenWidth, screenHeight)) 
pygame.display.set_caption('Pong')

# Game Rectangles
ball = pygame.Rect(screenWidth/2 - 15, screenHeight/2 - 15, 30, 30)
player = pygame.Rect(screenWidth - 20, screenHeight/2 - 70, 10, 140)
opponent = pygame.Rect(10, screenHeight/2 - 70, 10, 140)

bgColor = pygame.Color('grey12')
lightGrey = (200, 200, 200)

ballspeedX = 7
ballspeedY= 7
playerSpeed = 0
opponentSpeed = 7

# Text Variables
prevPlayerScore = -1
prevOpponentScore = -1
playerScore = 0
opponentScore = 0
gameFont = pygame.font.Font("freesansbold.ttf", 32)


while True:
    # Handling input
    # event = all user actions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                playerSpeed += 7
            if event.key == pygame.K_UP:
                playerSpeed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                playerSpeed -= 7
            if event.key == pygame.K_UP:
                playerSpeed += 7
                

    ballspeedX, ballspeedY, playerScore, opponentScore = ballPhysics(
        ball, player, opponent,
        ballspeedX, ballspeedY,
        screenWidth, screenHeight,
        playerScore, opponentScore
    )

    playerMovement(player, playerSpeed, screenHeight)
    opponentAI(opponent, opponentSpeed, screenHeight, ball)

    # Visuals, Elements are drawn bottom to top
    screen.fill(bgColor)
    pygame.draw.rect(screen, lightGrey, player)
    pygame.draw.rect(screen, lightGrey, opponent)
    pygame.draw.rect(screen, lightGrey, ball)
    pygame.draw.aaline(screen, lightGrey, 
                       (screenWidth/2,0), 
                       (screenWidth/2, screenHeight))
    
    # Keeps from rendering every frame, only renders when score is changed
    if playerScore != prevPlayerScore:
        playerText = gameFont.render(f"{playerScore}", True, lightGrey)
        prevPlayerScore = playerScore
    if opponentScore != prevOpponentScore:
        opponentText = gameFont.render(f"{opponentScore}", True, lightGrey)
        prevOpponentScore = opponentScore

    screen.blit(playerText, (960, 96))
    screen.blit(opponentText, (320, 96))

    # Updating the window
    pygame.display.flip()
    clock.tick(60)

