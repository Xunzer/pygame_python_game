import pygame
from pygame.locals import *
import random

pygame.init()

# game window display
screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Python Game")

# define initial game variables
cell_size = 10 # size of python body cell
direction = 1 # 1 is up, 2 is right, 3 is down, 4 is left
update_python = 0 # a timer for the movement of python
food = [0, 0]
new_food = True
new_cell = [0, 0]
score = 0
game_over = False
clicked = False

# define python
python_pos = [[int(screen_width / 2), int(screen_height / 2)]]
python_pos.append([int(screen_width / 2), int(screen_height / 2) + cell_size])
python_pos.append([int(screen_width / 2), int(screen_height / 2) + cell_size * 2])
python_pos.append([int(screen_width / 2), int(screen_height / 2) + cell_size * 3])

# define colors
bg_color = (255, 255, 204)
body_inner_color = (50, 175, 25)
body_outer_color = (100, 100, 200)
food_color = (255, 80, 80)
red = (255, 0, 0)
blue = (0, 0, 255)

# a rectangle for play again
again_rect = Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)

# define font
font = pygame.font.SysFont(None, 40)


def draw_screen():
    screen.fill(bg_color)

def draw_score():
    score_text = "Score: " + str(score)
    score_image = font.render(score_text, True, blue)
    screen.blit(score_image, (0, 0))

def check_game_over(game_over: bool):
    # check if python has eaten itself
    for cell in python_pos[1:]:
        if python_pos[0] == cell:
            game_over = True
    
    # # check if python has gone out of the bounds
    # if python_pos[0][0] < 0 or python_pos[0][0] > screen_width or python_pos[0][1] < 0 or python_pos[0][1] > screen_height:
    #     game_over = True
    
    return game_over

def draw_game_over():
    game_over_text = "Game Over!"
    game_over_image = font.render(game_over_text, True, blue)
    pygame.draw.rect(screen, red, (screen_width // 2 - 80, screen_height // 2 - 60, 160, 50))
    screen.blit(game_over_image, (screen_width // 2 - 80, screen_height // 2 - 50))

    again_text = "Play again?"
    again_image = font.render(again_text, True, blue)
    pygame.draw.rect(screen, red, again_rect)
    screen.blit(again_image, (screen_width // 2 - 80, screen_height // 2 + 10))

# set game loop
run = True
while run:

    draw_screen()
    draw_score()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            # moving up
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != 3:
                direction = 1
            # moving right
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != 4:
                direction = 2
            # moving down
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != 1:
                direction = 3
            # moving left
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != 2:
                direction = 4

    # create food
    if new_food == True:
        new_food = False
        food[0] = cell_size * random.randint(0, (screen_width // cell_size) - 1)
        food[1] = cell_size * random.randint(0, (screen_height // cell_size) - 1)

    # draw food
    pygame.draw.rect(screen, food_color, (food[0], food[1], cell_size, cell_size))

    # check if food has been eaten
    if python_pos[0] == food:
        new_food = True
        # create a new cell at the tail of python
        new_cell = list(python_pos[-1])
        # when python is moving up
        if direction == 1:
            new_cell[1] += cell_size
        # when python is moving down
        if direction == 3:
            new_cell[1] -= cell_size
        # when python is moving right
        if direction == 2:
            new_cell[0] -= cell_size
        # when python is moving left
        if direction == 4:
            new_cell[0] += cell_size
        
        # attach the new cell to the tail of python
        python_pos.append(new_cell)

        # increase the score
        score += 1

    if game_over == False:
    # only update the animation of python when the timer has been met
        if update_python > 99:
            update_python = 0
            # shift up the position of last body cell to the front, shift back the rest of body cells by 1 to the back (so that the python will start to move)
            python_pos = python_pos[-1:] + python_pos[:-1]
            # heading up
            if direction == 1:
                # x coordinate doesn't change, y coordinate goes up so reduce the size of the cell (closer to origin)
                python_pos[0][0] = python_pos[1][0]
                python_pos[0][1] = python_pos[1][1] - cell_size
            if direction == 3:
                # x coordinate doesn't change, y coordinate goes down so increase the size of the cell (further from origin)
                python_pos[0][0] = python_pos[1][0]
                python_pos[0][1] = python_pos[1][1] + cell_size
            if direction == 2:
                # y coordinate doesn't change, x coordinate goes to right so increase the size of the cell (further to origin)
                python_pos[0][1] = python_pos[1][1]
                python_pos[0][0] = python_pos[1][0] + cell_size
            if direction == 4:
                # y coordinate doesn't change, x coordinate goes to left so reduce the size of the cell (closer to origin)
                python_pos[0][1] = python_pos[1][1]
                python_pos[0][0] = python_pos[1][0] - cell_size

            # screen wrapping so that the python cell could go to the other side of screen when going beyond
            for cell in python_pos:
                if cell[0] > screen_width:
                    cell[0] = 0
                elif cell[0] < 0:
                    cell[0] = screen_width
                elif cell[1] > screen_height:
                    cell[1] = 0
                elif cell[1] < 0:
                    cell[1] = screen_height

            game_over = check_game_over(game_over)

    if game_over == True:
        draw_game_over()
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
            mouse_pos = pygame.mouse.get_pos()
            if again_rect.collidepoint(mouse_pos):
                # reset game variables
                direction = 1 # 1 is up, 2 is right, 3 is down, 4 is left
                update_python = 0 # a timer for the movement of python
                food = [0, 0]
                new_food = True
                new_cell = [0, 0]
                score = 0
                game_over = False

                # reinitialize python
                python_pos = [[int(screen_width / 2), int(screen_height / 2)]]
                python_pos.append([int(screen_width / 2), int(screen_height / 2) + cell_size])
                python_pos.append([int(screen_width / 2), int(screen_height / 2) + cell_size * 2])
                python_pos.append([int(screen_width / 2), int(screen_height / 2) + cell_size * 3])


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

    update_python += 1

pygame.quit()
