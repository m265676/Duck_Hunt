import pygame
import sys
from constants import *
from duck import green_ducks, blue_ducks, red_ducks
from crosshair import Crosshair
import os
import math
import random
from spawn_duck import spawn_duck
import time

# Initialize the high score variable
high_score = 0

# Difficulty level
diff_level = -1
amp = 0

# Initialize Pygame
pygame.init()

running = True
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create Pygame clock
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = screen.copy()
background_image = pygame.transform.scale(pygame.image.load(f'assets/sprites/background.png'),
                                          (SCREEN_WIDTH, SCREEN_HEIGHT))
# Load the target image
target_image = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'sprites', 'target.png')), (40, 40))

# Create the background on the screen
screen.blit(background_image, (0, 0))

# Constant modifies the rate at which the ducks spawn in
spawn_delay_green = 3
spawn_delay_blue = 5
spawn_delay_red = 7

# Time Starting Points for the spawning of the ducks
current_time = pygame.time.get_ticks()
last = current_time - spawn_delay_green * 250
last1 = current_time - spawn_delay_blue * 250
last2 = current_time - spawn_delay_red * 250

# Creating an instance of crosshair that I'll call
crosshair = Crosshair(target_image)

# Creating my font and initializing the things I'll need for my score box
score = 0
font = pygame.font.Font('Assets/Pixellettersfull-BnJ5.ttf', 36)

# Setting up the timer
game_duration = 10
start_time = None

# All the sounds I need for the game and making the background music play
duck_sound = pygame.mixer.Sound('Assets/quack.wav')
pygame.mixer.music.load('Assets/background_music.mp3')
pygame.mixer.music.play(-1)  # -1 means it loops the whole time the game is running.


def draw_loading_screen():
    loading_font1 = pygame.font.Font('Assets/Pixellettersfull-BnJ5.ttf', 50)
    loading_font2 = pygame.font.Font('Assets/Pixellettersfull-BnJ5.ttf', 32)
    loading_font3 = pygame.font.Font('Assets/Pixellettersfull-BnJ5.ttf', 32)
    loading_font4 = pygame.font.Font('Assets/Pixellettersfull-BnJ5.ttf', 32)
    loading_font5 = pygame.font.Font('Assets/Pixellettersfull-BnJ5.ttf', 32)
    loading_text1 = loading_font1.render('DUCK HUNT', True, (255, 255, 255))
    loading_text2 = loading_font2.render('Choose Level of Difficulty', True, (255, 255, 255))
    loading_text3 = loading_font3.render("Type '1' for Easy", True, (255, 255, 255))
    loading_text4 = loading_font4.render("Type '2' for Medium", True, (255, 255, 255))
    loading_text5 = loading_font5.render("Type '3' for Hard", True, (255, 255, 255))

    try:
        with open('high_score.txt', 'r') as file:
            high_score = int(file.read())
    except FileNotFoundError:
        # Handle the case where the file doesn't exist (first-time play)
        high_score = 0
    high_score_text = loading_font5.render(f'High Score: {high_score}', True, (255, 255, 255))

    screen.blit(loading_text1, (SCREEN_WIDTH // 2 - loading_text1.get_width() // 2, 80))
    screen.blit(loading_text2, (SCREEN_WIDTH // 2 - loading_text2.get_width() // 2, 140))
    screen.blit(loading_text3, (SCREEN_WIDTH // 2 - loading_text3.get_width() // 2, 180))
    screen.blit(loading_text4, (SCREEN_WIDTH // 2 - loading_text4.get_width() // 2, 220))
    screen.blit(loading_text5, (SCREEN_WIDTH // 2 - loading_text5.get_width() // 2, 260))
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 300))


def draw_score():
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, SCREEN_HEIGHT - 50))


def draw_time():
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Convert to seconds
    remaining_time = max(0, game_duration - elapsed_time)
    time_text = font.render(f'Time: {int(remaining_time)}s', True, (255, 255, 255))
    screen.blit(time_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 50))


def draw_end_screen(score):
    end_font = pygame.font.Font('Assets/Pixellettersfull-BnJ5.ttf', 50)
    text1 = end_font.render(f'Game Over!', True, (255, 255, 255))
    text2 = end_font.render(f'Your Score: {score}', True, (255, 255, 255))
    screen.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, 80))
    screen.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, 130))


def draw_gun():
    gun = pygame.transform.scale(pygame.image.load(f'assets/sprites/gun.png'), (35, 55))
    mouse_pos = pygame.mouse.get_pos()
    gun_point = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 120)

    # Calculates slope for an imaginary line leading from the gun and ensures that there isn't an error when the
    # mouse is directly above.
    if mouse_pos[0] != gun_point[0]:
        slope = (mouse_pos[1] - gun_point[1]) / (mouse_pos[0] - gun_point[0])
    else:
        slope = -100000
    angle = math.atan(slope)
    # Needs the angle in degrees
    rotation = math.degrees(angle)

    # Flips if you pass 180 degrees of rotation for Left Side of the Screen
    if mouse_pos[0] < SCREEN_WIDTH / 2:
        gunn = pygame.transform.flip(gun, True, False)
        if mouse_pos[1] < 600:
            screen.blit(pygame.transform.rotate(gun, 90 - rotation), (SCREEN_WIDTH / 2 - 35, SCREEN_HEIGHT - 220))


    # For the right side of the Screen
    else:
        if mouse_pos[1] < 600:
            screen.blit(pygame.transform.rotate(gun, 270 - rotation), (SCREEN_WIDTH / 2 - 20, SCREEN_HEIGHT - 220))


# -----------------------------------------------------------------------------------------------------------------
while True:

    # This is the loop that puts the title screen and once the player chooses a level of difficulty, the game starts.
    running = False
    loading_screen = True
    while loading_screen:

        for event in pygame.event.get():
            print(event.type)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                print('I AM HERE!!!!')
                loading_screen = False
                start_time = pygame.time.get_ticks()  # Starts the Game
                diff_level = 1
                running = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                loading_screen = False
                start_time = pygame.time.get_ticks()  # Starts the Game
                diff_level = 2
                running = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                loading_screen = False
                start_time = pygame.time.get_ticks()  # Starts the Game
                diff_level = 3
                running = True

        screen.blit(background_image, (0, 0))
        draw_loading_screen()
        pygame.display.flip()
        clock.tick(60)

    # Determine duck speed based on difficulty level.
    if diff_level == 1:
        g_spd = 3
        b_spd = 5
        r_spd = 7
        amp = 0

    elif diff_level == 2:
        g_spd = 3
        b_spd = 5
        r_spd = 7
        amp = 1

    elif diff_level == 3:
        g_spd = 8
        b_spd = 10
        r_spd = 12
        amp = 1.5

    # This is the main loop that starts after the loading screen is false and this is when the ducks spawn and you can
    # start shooting.
    game_over_screen = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # Reset relevant variables
                start_time = None
                score = 0
                in_game = False
            # Get the mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Update the crosshair position
            crosshair.update(mouse_x, mouse_y)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                # Check for collisions with green ducks
                # print(crosshair.rect.center)
                # print(green_ducks.sprites()[0].rect.center)
                for ducks in [green_ducks, blue_ducks, red_ducks]:
                    ducks_sprites = ducks.sprites()
                    for duck_sprite in ducks_sprites:
                        if pygame.sprite.collide_rect(crosshair, duck_sprite):
                            print("hahaha")
                            duck_sound.play()
                            # print(duck_sprite.speed)
                            score = score + 100 * duck_sprite.speed
                            duck_sprite.kill()
                            if score > high_score:
                                high_score = score
        green_ducks.update()
        blue_ducks.update()
        red_ducks.update()
        screen.blit(background_image, (0, 0))
        # Spawn new ducks as needed

        last = spawn_duck(green_ducks, 'assets/sprites/green.png', g_spd, last, spawn_delay_green, random.randint(200, 250),
                          amp)

        last1 = spawn_duck(blue_ducks, 'assets/sprites/blue.png', b_spd, last1, spawn_delay_blue, random.randint(150, 200),
                           amp)
        last2 = spawn_duck(red_ducks, 'assets/sprites/red.png', r_spd, last2, spawn_delay_red, random.randint(100, 150),
                           amp)
        green_ducks.draw(screen)
        blue_ducks.draw(screen)
        red_ducks.draw(screen)

        screen.blit(crosshair.image, crosshair.rect.topleft)
        draw_gun()
        draw_score()
        draw_time()

        # Check if the game time has elapsed
        if start_time is not None:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Convert to seconds
            if elapsed_time >= game_duration:
                running = False  # End the game when the time is up
                game_over_screen = True

        pygame.display.flip()

        clock.tick(60)

    # This is the loop that puts the game over screen up once the timer has run out.

    t0 = time.time()
    t = 0
    while game_over_screen and t < 5:
        # Update time.
        t = time.time() - t0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Saves the highscore if the Player achieves one
                with open('high_score.txt', 'w') as file:
                    file.write(str(high_score))

                pygame.quit()
                sys.exit()

        screen.blit(background_image, (0, 0))
        draw_end_screen(score)
        pygame.display.flip()

