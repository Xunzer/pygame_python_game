import pygame
from pygame.locals import *

pygame.init()

# game window display
screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Python Game")

# define initial game variables
cell_size = 10
direction = 1 # 1 is up, 2 is right, 3 is down, 4 is left

# define python
python_pos = [[int(screen_width / 2), int(screen_height / 2)]]
python_pos.append([int(screen_width / 2), int(screen_height / 2) + cell_size])
python_pos.append([int(screen_width / 2), int(screen_height / 2) + cell_size * 2])
python_pos.append([int(screen_width / 2), int(screen_height / 2) + cell_size * 3])

# define colors
bg_color = (255, 255, 204)
body_inner_color = (50, 175, 25)
body_outer_color = (100, 100, 200)
red = (255, 0, 0)

def draw_screen():
    screen.fill(bg_color)


# set game loop
run = True
while run:
    draw_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 3:
                direction = 1
            if event.key == pygame.K_RIGHT and direction != 4:
                direction = 2
            if event.key == pygame.K_DOWN and direction != 1:
                direction = 3
            if event.key == pygame.K_LEFT and direction != 2:
                direction = 4

    
    # draw python
    head = 1
    for x in python_pos:
        if head == 0:
            pygame.draw.rect(screen, body_outer_color, (x[0], x[1], cell_size, cell_size))
            pygame.draw.rect(screen, body_inner_color, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
        if head == 1:
            pygame.draw.rect(screen, body_outer_color, (x[0], x[1], cell_size, cell_size))
            pygame.draw.rect(screen, red, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
            head = 0
    # display update
    pygame.display.update()

pygame.quit()