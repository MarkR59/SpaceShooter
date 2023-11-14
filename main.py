import pygame
import random
import math
from pygame import mixer

mixer.init()
pygame.init()

mixer.music.load('Sound/journey-end.mp3')
mixer.music.play(-1)

screen = pygame.display.set_mode((800,600))

#set title of game window
pygame.display.set_caption('Space Shooter')

font = pygame.font.SysFont('Impact', 32)
font_description = pygame.font.SysFont('Impact', 24)
font_game_over = pygame.font.SysFont('Impact', 64)

#set image for window
ship = pygame.image.load('Images/space-ship.png')
pygame.display.set_icon(ship)

background = pygame.image.load('Images/background.jpg')
#values to make background move vertically
background_y1 = 0
background_y2 = 600

shipImg = pygame.image.load('Images/player-ship.png')
shipX = 370 #value to move ship left/right
shipY = 480 #value to move ship up/down
changeX = 0 #used to adjust shipX

meteor_leftImg = pygame.image.load('Images/diagonal_left.png')
meteor_rightImg = pygame.image.load('Images/diagonal_right.png')
meteor_leftX = 0
meteor_leftY = 0
meteor_leftchangeX = 0
meteor_leftchangeY = 0
meteor_rightX = 800
meteor_rightY = 0
meteor_rightchangeX = 0
meteor_rightchangeY = 0
meteor = False

side = 0

enemyImg = []
enemyX = []
enemyY = []
enemyspeedX = []
no_of_enemies = 6

for i in range (no_of_enemies):
    enemyImg.append(pygame.image.load('Images/enemy.png'))
    #random loaction for enemys to spawn
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(30,150))
    enemyspeedX.append(4)

laserImg = pygame.image.load('Images/laser.png')
tri_laser1Img = pygame.image.load('Images/laser.png')
tri_laser2Img = pygame.image.load('Images/laser.png')
laserX = 370
laserY = 490
tri_laser1X = 370
tri_laser1Y = 490
tri_laser2X = 370
tri_laser2Y = 490
shooting = False

triple_shotImg = pygame.image.load('Images/three.png')
powerUp = False

score = 0

clock = pygame.time.Clock()
SPAWNMETEOR = pygame.USEREVENT + 1  #event to spawn meteor every 5 seconds
SPAWNENEMIES = pygame.USEREVENT + 2 #event to spawn more eneimes every minute
spawn_counter = 0 #keeps track of how many times more enemies have spawned
pygame.time.set_timer(SPAWNMETEOR, 5000)
pygame.time.set_timer(SPAWNENEMIES, 60000)

#variable used to open or close the game window
running = True
running_gameover = False
running_gamestart = True
    
def show_score():
    scoreImg = font.render(f'Score: {score}', True, 'white')
    screen.blit(scoreImg, (10, 10))

def game_over():
    game_overImg = font_game_over.render('GAME OVER', True, 'white')
    screen.blit(game_overImg, (250, 250))
    restart_optionImg = font.render('Press space key to restart', True, 'white')
    screen.blit(restart_optionImg, (225, 350))

class Button:
    def __init__(self, x, y, width, height, color, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        if self.text != '':
            text = font.render(self.text, 1, (0,0,0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False
    
    def center(self, screen_width):
        self.x = (screen_width - self.width) / 2
    
button = Button(0, 400, 220, 80, (255, 255, 255), 'Start Game')
button.center(800)

game_description_1 = font_description.render('Don\'t let the aliens reach your ship!', True, 'white')
game_description_2 = font_description.render('It is your mission to survive as long as possible and wipe out all enemies', True, 'white')
game_description_3 = font_description.render('You got this trooper!', True, 'white')

game_description_1_rect = game_description_1.get_rect()
game_description_2_rect = game_description_2.get_rect()
game_description_3_rect = game_description_3.get_rect()

game_description_1_rect.center = (screen.get_width() / 2, 200)
game_description_2_rect.center = (screen.get_width() / 2, 250)
game_description_3_rect.center = (screen.get_width() / 2, 300)

while running:
    if running_gamestart:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.is_over(pos):
                    running_gamestart = False
            if event.type == pygame.MOUSEMOTION:
                if button.is_over(pos):
                    button.color = (255, 215, 0)
                else:
                    button.color = (255, 255, 255)

        screen.fill((0,0,0))
        background_y1 -= 3
        background_y2 -= 3

        if background_y1 <= -600:
            background_y1 = 600
        if background_y2 <= -600:
            background_y2 = 600

        screen.blit(background, (0, background_y1))
        screen.blit(background, (0,background_y2))

        screen.blit(game_description_1, game_description_1_rect)
        screen.blit(game_description_2, game_description_2_rect)
        screen.blit(game_description_3, game_description_3_rect)

        button.draw(screen)

        pygame.time.Clock().tick(60)
        pygame.display.update()

    elif running_gameover:
        if spawn_counter > 0:
            for i in range(spawn_counter):
                enemyImg.pop()
                enemyX.pop()
                enemyY.pop()
                enemyspeedX.pop()
                
        spawn_counter = 0
        no_of_enemies = 6
        for i in range (no_of_enemies):
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(30,150)

        meteor_leftX = 0
        meteor_leftY = 0
        meteor_rightX = 800
        meteor_rightY = 0

        screen.fill((0,0,0))
        background_y1 -= 3
        background_y2 -= 3

        if background_y1 <= -600:
            background_y1 = 600
        if background_y2 <= -600:
            background_y2 = 600

        screen.blit(background, (0, background_y1))
        screen.blit(background, (0,background_y2))
        game_over()
        show_score()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                screen.fill((0,0,0))
                score = 0
                running_gameover = False              

        pygame.time.Clock().tick(60)
        pygame.display.update()

    elif not running_gameover:
        screen.fill((0,0,0))
        background_y1 -= 3
        background_y2 -= 3

        if background_y1 <= -600:
            background_y1 = 600
        if background_y2 <= -600:
            background_y2 = 600

        screen.blit(background, (0, background_y1))
        screen.blit(background, (0,background_y2))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == SPAWNMETEOR:
                if meteor is False:
                    meteor = True
                    side = random.randint(1,2)
                    if side == 1:
                        meteor_leftchangeX = random.uniform(3, 8)
                        meteor_leftchangeY = random.uniform(3, 8)
                    elif side == 2:
                        meteor_rightchangeX = random.uniform(-3, -8)
                        meteor_rightchangeY = random.uniform(3, 8)   
            if event.type == SPAWNENEMIES:  
                no_of_enemies += 2              
                for i in range(2):
                    enemyImg.append(pygame.image.load('Images/enemy.png'))
                    enemyX.append(random.randint(0,736))
                    enemyY.append(random.randint(30,150))
                    enemyspeedX.append(4)
                    spawn_counter += 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    changeX = -8
                if event.key == pygame.K_RIGHT:
                    changeX = 8
                if event.key == pygame.K_SPACE:
                    if not shooting:
                        laser_sound = mixer.Sound('Sound/laser.mp3')
                        laser_sound.set_volume(0.1)
                        laser_sound.play()
                        shooting = True
                        laserX = shipX + 16
                        tri_laser1X = shipX + 25
                        tri_laser2X = shipX + 7
                        
            if event.type == pygame.KEYUP:
                changeX = 0
  
        shipX += changeX
        #setting boundaries for player horizontal movement
        if shipX <= 0:
            shipX = 0
        elif shipX >= 736:
            shipX = 736

        for i in range (no_of_enemies):
            if enemyY[i] > 420:
                running_gameover = True
                break
            enemyX[i] += enemyspeedX[i]
            #setting boundaries for enemy horizontal movement
            if enemyX[i] <= 0:
                enemyspeedX[i] = 4
                enemyY[i] += 40
            elif enemyX[i] >= 736:
                enemyspeedX[i] = -4
                enemyY[i] += 40

            #handles collision between laser and enemy using the distance formula
            distance = math.sqrt(math.pow(laserX - enemyX[i],2) + math.pow(laserY - enemyY[i],2))
            distance_tri_laser1 = 10000
            distance_tri_laser2 = 10000
            if powerUp:
                distance_tri_laser1 = math.sqrt(math.pow(tri_laser1X - enemyX[i],2) + math.pow(tri_laser1Y - enemyY[i],2))
                distance_tri_laser2 = math.sqrt(math.pow(tri_laser2X - enemyX[i],2) + math.pow(tri_laser2Y - enemyY[i],2))
            if distance < 35 or distance_tri_laser1 < 35 or distance_tri_laser2 < 35:
                explosion_sound = mixer.Sound('Sound/explosion.wav')
                explosion_sound.set_volume(0.2)
                explosion_sound.play()
                laserY = 480
                tri_laser1Y = 480
                tri_laser2Y = 480
                shooting = False
                score += 1
                enemyX[i] = random.randint(0,736) 
                enemyY[i] = random.randint(30,150)
        
            screen.blit(enemyImg[i], (enemyX[i], enemyY[i]))

        if laserY <= 0:
            laserY = 490
            tri_laser1Y = 490
            tri_laser2Y = 490
            shooting = False

        if shooting:
            screen.blit(laserImg, (laserX, laserY))
            laserY -= 10
            if powerUp:
                screen.blit(tri_laser1Img, (tri_laser1X, tri_laser1Y))
                screen.blit(tri_laser2Img, (tri_laser2X, tri_laser2Y))
                tri_laser1Y -= 10
                tri_laser2Y -= 10
                
        if meteor and side == 1:
            screen.blit(meteor_leftImg, (meteor_leftX, meteor_leftY))
            meteor_leftX += meteor_leftchangeX
            meteor_leftY += meteor_leftchangeY

        if meteor and side == 2:
            screen.blit(meteor_rightImg, (meteor_rightX, meteor_rightY))
            meteor_rightX += meteor_rightchangeX
            meteor_rightY += meteor_rightchangeY
        
        meteor_distance_left = math.sqrt(math.pow(meteor_leftX - shipX, 2) + math.pow(meteor_leftY - shipY, 2))
        if meteor_distance_left < 36:
            meteor = False
            running_gameover = True

        meteor_distance_right = math.sqrt(math.pow(meteor_rightX - shipX, 2) + math.pow(meteor_rightY - shipY, 2))
        if meteor_distance_right < 35:
            meteor = False
            running_gameover = True

        if meteor_leftY > 530:
            meteor = False
            meteor_leftX = 0
            meteor_leftY = 0

        if meteor_rightY > 530:
            meteor = False
            meteor_rightX = 800
            meteor_rightY = 0    

        screen.blit(shipImg, (shipX, shipY)) 

        show_score() 

        pygame.time.Clock().tick(60)
        pygame.display.update()

