import pygame
import sys
import random


def game_physics(ball: pygame.Rect, player: pygame.Rect, opponent: pygame.Rect, ball_speed_x: int,
                 ball_speed_y: int, screen_width: int, screen_height: int,
                 player_score: int, opponent_score: int, score_time: int):

    # Ball movement and collisions
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # To make the ball go in the other direction
    # Multily the speed by -1, to reverse the speeed
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    # Determines whos wins and score
    if ball.left <= 0:
        player_score += 1
        score_time = pygame.time.get_ticks()

        ball.center = (screen_width/2, screen_height/2)
        reset_paddles(player, opponent, screen_height)

        ball_speed_x, ball_speed_y = 0, 0

    elif ball.right >= screen_width:
        opponent_score += 1
        score_time = pygame.time.get_ticks()

        ball.center = (screen_width/2, screen_height/2)
        reset_paddles(player, opponent, screen_height)

        ball_speed_x, ball_speed_y = 0, 0

    # Handled the ball getting caught inside a paddle
    if ball.colliderect(player) and ball_speed_x > 0:
        ball_speed_x *= -1
        ball.right = player.left
    elif ball.colliderect(opponent) and ball_speed_x < 0:
        ball_speed_x *= -1
        ball.left = opponent.right

    return ball_speed_x, ball_speed_y, player_score, opponent_score, score_time


def player_movement(player: pygame.Rect, player_speed: int, screen_height: int):
    player.y += player_speed
    # Handles the player from going out of bounds
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_ai(opponent: pygame.Rect, opponent_speed: int, screen_height: int, ball: pygame.Rect):
    if opponent.centery < ball.centery:
        opponent.centery += opponent_speed
    elif opponent.centery > ball.centery:
        opponent.centery -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_restart(ball: pygame.Rect, screen_width: int, screen_height: int,
                 ball_speed_x: int, ball_speed_y: int):
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))

    return ball_speed_x, ball_speed_y

def reset_paddles(player: pygame.Rect, opponent: pygame.Rect, screen_height: int):
    player.centery = screen_height // 2
    opponent.centery = screen_height // 2
    
# General setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 1280
screen_height = 960

# Returns surface display object
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)
timer_color = pygame.Color('indianred3')

ball_speed_x = 7
ball_speed_y = 7
player_speed = 0
opponent_speed = 7

# Text Variables
prev_player_score = 0
prev_opponent_score = 0
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)
game_font_timer = pygame.font.Font("freesansbold.ttf", 64)

# Pre-rendering countdown numbers
countdown_text = {
    "3": game_font_timer.render("3", True, timer_color),
    "2": game_font_timer.render("2", True, timer_color),
    "1": game_font_timer.render("1", True, timer_color),
}

# Initially render score text
player_text: pygame.Surface = game_font.render(
    f"{player_score}", True, light_grey)
opponent_text: pygame.Surface = game_font.render(
    f"{opponent_score}", True, light_grey)

# Score Timer
score_time = -1


while True:
    # Handling input
    # event = all user actions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7
    
    # Only updates when the ball is in play
    if score_time == -1:
        ball_speed_x, ball_speed_y, player_score, opponent_score, score_time = game_physics(
            ball, player, opponent,
            ball_speed_x, ball_speed_y,
            screen_width, screen_height,
            player_score, opponent_score,
            score_time
        )
    if score_time == -1:
        player_movement(player, player_speed, screen_height)
        opponent_ai(opponent, opponent_speed, screen_height, ball)

    # Visuals, Elements are drawn bottom to top
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.rect(screen, light_grey, ball)
    pygame.draw.aaline(
        screen, light_grey,
        (screen_width / 2, 0),
        (screen_width / 2, screen_height)
    )

    # Only assign score on condition
    if player_score != prev_player_score:
        prev_player_score = player_score
        player_text: pygame.Surface = game_font.render(
            f"{player_score}", True, light_grey)
    if opponent_score != prev_opponent_score:
        prev_opponent_score = opponent_score
        opponent_text: pygame.Surface = game_font.render(
            f"{opponent_score}", True, light_grey)

    screen.blit(player_text, (960, 96))
    screen.blit(opponent_text, (320, 96))

    # Count down timer for the serve
    if score_time != -1:
        time_elapsed = pygame.time.get_ticks() - score_time
        
        if time_elapsed < 2100:
            if time_elapsed < 700:
                timer_num = "3"
            elif time_elapsed < 1400:
                timer_num = "2"
            else:
                timer_num = "1"

            screen.blit(countdown_text[timer_num], (screen_width/2 - 15, 78))
        else:
            ball_speed_x, ball_speed_y = ball_restart(ball, screen_width, screen_height, 7, 7)
            score_time = -1

    # Updating the window
    pygame.display.flip()
    clock.tick(60)
