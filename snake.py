import pygame
import random
import os
pygame.init()

# Setting the values for colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Creating the window
window_width = 600
window_height = 500
gameWindow = pygame.display.set_mode((window_width, window_height))

# Changing the title of the window
pygame.display.set_caption('Snake game')
pygame.display.update()

# ------------------Setting the game variables-----------------------
game_on = True
game_over = False
begin_game = False
# Co-ordinates for the snake
snake_x = 50
snake_y = 50
snake_size = 15
# To increase the size of the snake
snake_length = 1
snake_list = [[snake_x, snake_y]]
# For calculating the score
score = 0
# For moving the snake with the specified velocity
init_velocity = 5
velocity_x = init_velocity
velocity_y = 0
# For setting the fps of the game
fps = 30
clock = pygame.time.Clock()
# For setting the font to be displayed on the screen
font = pygame.font.SysFont(None, 40)
# For keeping track of the high-score
# Create the highscore file if it does not exist
try:
	with open('highscore.txt') as f:
	    high_score = int(f.read())
	    
except:
	with open('highscore.txt', 'r+') as f:
		f.write('0')
		high_score = int(f.read())
# -------------------------------------------------------------------

# Function to check if the snake has reached the borders
def border_check():
    global snake_x, snake_y, window_width, window_height, game_over
    # For x-axis
    if snake_x == 0 or snake_y == 0 or snake_x == window_width or snake_y == window_height:
        game_over = True


# Function to get the co-ordinates for food
def get_food():
    global window_width, window_height, snake_list
    while True:
        food_x = random.randint(10, window_width-5)
        food_y = random.randint(10, window_height-5)
        food_coordinates = [food_x, food_y]
        if food_coordinates not in snake_list:
            break
    return food_x, food_y


# Function to print text on the screen
def print_text(text_string, color, x, y):
    text = font.render(text_string, True, color)
    gameWindow.blit(text, [x, y])


# Function to plot the snake
def plot_snake(gameWindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])
    
    
# Function to display the home screen
def welcome():
    gameWindow.fill(white)
    positions = [[135, window_height//2.4], [50, window_height//2.07], [190, window_height//1.8]]
    text_list = ['Welcome to Snake Game', 'Press the spacebar to start the game', 
                 'High-Score: ' + str(high_score)]
    i = 0
    for position in positions:
        color = black
        print_text(text_list[i], color, position[0], position[1])
        i += 1
    pygame.display.update()
    
    
# Function to display the game-over screen when the snake dies
def print_game_over():
    global game_over, score, high_score
    # Updating the high score
    if score > high_score:
        high_score = score
        with open('highscore.txt', 'w') as f:
            f.write(str(high_score))
    # Displaying the game-over screen
    game_over = True
    gameWindow.fill(white)
    positions = [[15, window_height//2.4], [150, window_height//2.07], [200, window_height//1.8]]
    text_list = ['Game over! Press Enter to start new game.', 'Your final score is: ' + str(score), 
                 'High-Score: ' + str(high_score)]
    i = 0
    for position in positions:
        color = black
        if i == 0:
            color = red
        print_text(text_list[i], color, position[0], position[1])
        i += 1
    pygame.display.update()
    
    
# Function to plot everything in the window
def plot_window(velocity_x, velocity_y):
    global snake_x, snake_y, food_x, food_y, score, snake_length, snake_list, game_over
    # Checking if the snake has eaten the food
    if abs(snake_x - food_x) < 8 and abs(snake_y - food_y) < 8:
        food_x, food_y = get_food()
        score += 1
        snake_length += 5
        
    # Moving the snake in the required direction
    snake_x += velocity_x
    snake_y += velocity_y
    
    # Increasing the size of the snake 
    new_head = [snake_x, snake_y]
    if new_head in snake_list:
        game_over = True
        
    snake_list.append(new_head)
    if len(snake_list) >= snake_length:
        snake_list.pop(0)
        
    # Checking if the snake has reached the borders
    border_check()

    # Draw the snake and food on the window
    if begin_game == False:
        welcome()
    elif game_over:
        print_game_over()
    else:
        gameWindow.fill(white)
        print_text('Score: ' + str(score), blue, 5, 5)
        pygame.draw.rect(gameWindow, red, [food_x, food_y, (snake_size//1.3), (snake_size//1.3)])
        plot_snake(gameWindow, black, snake_list, snake_size)
        pygame.display.update()
    

# Function to set all the values back to default
def set_default_values():
    global snake_x, snake_y, snake_length, snake_list, score, game_over
    global food_x, food_y, velocity_x, velocity_y, begin_game
    score = 0
    snake_x = 50
    snake_y = 50
    snake_length = 1
    snake_list = [[snake_x, snake_y]]
    game_over = False
    begin_game = False
    velocity_x = 5
    velocity_y = 0
    food_x, food_y = get_food()
    
    
# Playing the game
food_x, food_y = get_food()

def play_game():
    global game_on, game_over, begin_game, velocity_x, velocity_y, init_velocity
    
    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
        
            if begin_game == False:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        begin_game = True
        
            elif game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        set_default_values()
                        break
                    
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_UP:
                        velocity_x = 0
                        velocity_y = -init_velocity
                    elif event.key == pygame.K_DOWN:
                        velocity_x = 0
                        velocity_y = init_velocity

        plot_window(velocity_x, velocity_y)
        clock.tick(fps)  
            
    pygame.quit()
    

# Start the game
play_game()
