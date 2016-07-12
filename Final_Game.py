# Pygame template
import pygame
import random
import time

# Window size and frames per second
WIDTH = 600
HEIGHT = 352
FPS = 30


# Define colors that will be used in game
BLACK = (0, 0, 0)


# Game objects
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # The sprites basic attributes go here
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('heavyarms2.png')
        self.image = pygame.transform.scale(self.image, (95, 85))
        self.rect = self.image.get_rect()
        #  The sprites starting position
        self.rect.x = 0
        self.rect.y = 0

    def handle_keys(self):
        """ process input for character """
        key = pygame.key.get_pressed()
        distance = 15  # distance moved in 1 frame, try changing it to 10
        if key[pygame.K_DOWN] and self.rect.y < (352 - 44):    # down key
            self.rect.y += distance    # move down
        elif key[pygame.K_UP] and self.rect.y > 0:    # up key
            self.rect.y -= distance    # move up
        if key[pygame.K_RIGHT] and self.rect.x < (600 - 44):   # right key
            self.rect.x += distance    # move right
        elif key[pygame.K_LEFT] and self.rect.x > 0:  # left key
            self.rect.x -= distance    # move left

    def shoot(self):
        bullet = Bullet((self.rect.x - 70, self.rect.y + 15))
        bullet2 = Bullet((self.rect.x - 65, self.rect.y + 35))
        all_sprites.add(bullet, bullet2)
        bullets.add(bullet, bullet2)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, (x, y)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('laser.png')
        self.image = pygame.transform.scale(self.image, (200, 25))
        self.rect = self.image.get_rect()
        (self.rect.x, self.rect.y) = (x, y)
        self.speed_x = 150

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.x > 600:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('aries.png')
        self.image = pygame.transform.scale(self.image, (75, 35))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(600, WIDTH + self.rect.width)
        self.rect.y = random.randrange(0, HEIGHT)
        self.speed_x = random.randrange(3, 6)

    def update(self):
        self.rect.x -= self.speed_x
        if self.rect.x < 0:
            self.rect.x = random.randrange(600, WIDTH + self.rect.width)
            self.rect.y = random.randrange(0, HEIGHT)
            self.speed_x = random.randrange(3, 6)

    def mob_generate(self):
        for i in range(random.randrange(5, 15)):
            enemy = Enemy()
            all_sprites.add(enemy)
            mobs.add(enemy)


class Background():
    def __init__(self):
        # The sprites basic attributes go here
        # scrolling background
        self.background = pygame.image.load('bg3.jpg').convert()
        self.background1 = pygame.image.load('bg3.jpg')
        self.background2 = pygame.image.load('bg3.jpg')
        self.background1_x = 0
        self.background2_x = self.background1.get_width()
        screen.blit(self.background, (0, 0))

    def bg_position(self):
        # This will adjust the backgrounds position and blit accordingly.
        screen.blit(self.background1, (self.background1_x, 0))
        screen.blit(self.background2, (self.background2_x, 0))

        self.background1_x -= 1
        self.background2_x -= 1

        if self.background1_x == -1 * self.background1.get_width():
            self.background1_x = self.background2_x + self.background2.get_width()
        if self.background2_x == -1 * self.background2.get_width():
            self.background2_x = self.background1_x + self.background1.get_width()


# Ask for users name and list instructions
user_name = raw_input("***** GAME INSTRUCTIONS *****\n"
                      "PRESS THE SPACE BAR TO SHOOT\n"
                      "USE THE ARROW KEYS TO MOVE AROUND\n"
                      "DON'T GET HIT\n"
                      "\n"
                      "Please type in your name and press enter: "
                      ).capitalize()


# Initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mobile Suit Shooter")


# Initialize all objects and create appropriate sprite groups
city = Background()
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
bullets = pygame.sprite.Group()
enemies = Enemy()
enemies.mob_generate()
dead_enemies = 0


# Set the game speed
clock = pygame.time.Clock()


# Countdown
print "\nADJUST THE GAME WINDOW IF NECESSARY\n"
print "THE GAME WILL BEGIN IN :"

for i in xrange(10, 0, -1):
    time.sleep(1)
    print i
pygame.time.delay(1000)


################## Main Game loop ##################

running = True
while running:
    # Keep loop running at the correct speed
    clock.tick(FPS)

    # Process input (events/ keys pressed)
    for event in pygame.event.get():  # Call to the 'event' class
        # check for closing the game window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    player.handle_keys()  # handle the key input

    # Update (sprites and drawings go in the following two groups)
    mob_hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in mob_hits:
        e = Enemy()
        all_sprites.add(e)
        mobs.add(e)
        dead_enemies += 1

    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False

    city.bg_position()
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()


############ CALCULATING RESULTS ############


# Read from the high scores file.
scores_file = open("highscores.txt", "r")
champion = scores_file.readline().strip()
champs_score = int(scores_file.readline().strip())
scores_file.close()


# Check to see if the current player is the new champion:
print "you eliminated {0} mobile suits".format(dead_enemies)


if dead_enemies > champs_score:
    # OPEN THE FILE **AGAIN**, WRITE NEW DATA
    print "*************** WE HAVE A NEW HIGH SCORE ***************"
    scores_file = open("highscores.txt", "w")
    scores_file.write(user_name + "\n")
    scores_file.write(str(dead_enemies) + "\n")
    scores_file.close()

    # OPEN THE FILE **AGAIN**, Read and report the new champs scores
    scores_file = open("highscores.txt", "r")
    new_champion = scores_file.readline().strip()
    new_champs_score = int(scores_file.readline().strip())
    print "Players name: ***** {0} ******".format(new_champion)
    print "Players score: ***** {0} *****".format(new_champs_score)
    scores_file.close()

# Print the defending champions score
else:
    print "The current champion is: **{0}**".format(champion)
    print "With a score of: **{0}**".format(champs_score)
