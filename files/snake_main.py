import pygame
import random

pygame.init()

#define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#this is kinda the fps clock
clock = pygame.time.Clock()

#4 line boundries
lines = [((0, 5), (SCREEN_WIDTH, 5)), 
         ((SCREEN_WIDTH-5, 0), (SCREEN_WIDTH-5, SCREEN_HEIGHT)), 
         ((0, SCREEN_HEIGHT-5), (SCREEN_WIDTH, SCREEN_HEIGHT-5)),
         ((5, 0), (5, SCREEN_HEIGHT))]

#player attributes n stuff
player_x = 300
player_y = 250
#I put player in a list to allow new segments to be appended and rendered in as 1 whole thing, called player.
player = [pygame.Rect((player_x, player_y, 40, 40))]
#I use random.choice which chooses a random element from a list and here it chooses a random direction
player_direction = random.choice([UP, DOWN, LEFT, RIGHT])
#number of pixels the player moves per frame
player_speed = 5

#food attributes n stuff
obst_x = random.randint(35, int(SCREEN_WIDTH)-35)
obst_y = random.randint(35, int(SCREEN_HEIGHT)-35)
obst = pygame.Rect((obst_x, obst_y, 30, 30))

#my font variable to define how the font will look like for when I render the score
myfont = pygame.font.SysFont('monospace', 30, True)

def move():
    
    player[0].move_ip(player_direction[0] * player_speed, player_direction[1] * player_speed)


score = 0
run = True
while run:

    clock.tick(60)
    screen.fill((0,0,0))

    #draw food
    pygame.draw.rect(screen, (245, 255, 34), obst)

    #draw the 4 boundries
    for line in lines:
        pygame.draw.line(screen, 'white', *line, 3)
            
        #if player collides with any of the 4 lines, reset the player position
        if player[0].clipline(*line):
            score = 0
            player_speed = 5
            player_x = 300
            player_y = 250
            player = [pygame.Rect((player_x, player_y, 40, 40))]
            player_direction = random.choice([UP, DOWN, LEFT, RIGHT])
    
    #draw every segment of the snake
    for segment in player:
        pygame.draw.rect(screen, (0, 255, 34), segment)
    
    # functional code for chekcing self-collision, except it checks if the head is in the same position as any segment
    if len(player) > 3:
         #I do this because I want all the segments of the snake except for the head
        for segment in player[1:]:
            if (player[0].x, player[0].y) == (segment.x, segment.y):
                score = 0
                player_speed = 5
                player_x = 300
                player_y = 250
                player = [pygame.Rect((player_x, player_y, 40, 40))]
                player_direction = random.choice([UP, DOWN, LEFT, RIGHT])
    
    #for every segment in the snake excpet for the head had the last segement follow the topleft of the other last segment
    for i in range(len(player)-1, 0, -1):
        player[i].topleft = player[i-1].topleft

    
    #move function to allow player to move
    move()

    #if the player collides with the food then randomize its position on the screen and add 1 to the score
    if player[0].colliderect(obst):
        score += 1
        obst_x = random.randint(35, int(SCREEN_WIDTH)-35)
        obst_y = random.randint(35, int(SCREEN_HEIGHT)-35)
        obst = pygame.Rect((obst_x, obst_y, 30, 30))
        
        #add a new segment after colliding with the food
        tail = player[-1]
        new_segment = pygame.Rect(tail.x, tail.y, tail.width, tail.height)
        player.append(new_segment)
        
        #every multiple of 5 increase speed by 1
        if score % 5 == 0:
            player_speed += 1
    

    
    for event in pygame.event.get():
         #exits out of game when you press the x on the window
        if event.type == pygame.QUIT:
            run = False
        
        elif event.type == pygame.KEYDOWN:
         #I do the extra and statement to not allow the snake to reverse because I do not want the snake reversing into itself
            if event.key == pygame.K_UP and player_direction != DOWN:
                player_direction = UP
            elif event.key == pygame.K_DOWN and player_direction != UP:
                player_direction = DOWN
            elif event.key == pygame.K_LEFT and player_direction != RIGHT:
                player_direction = LEFT
            elif event.key == pygame.K_RIGHT and player_direction != LEFT:
                player_direction = RIGHT

    #render the score   
    text = myfont.render('Score {0}'.format(score), 5, (255, 255, 255))
    screen.blit(text, (20, 10))

    pygame.display.update()

pygame.quit()
