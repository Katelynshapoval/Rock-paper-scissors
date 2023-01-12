import pygame
import time
from random import randint
pygame.init()

red = (128, 27, 27)
black = (0, 0, 0)
white = (255, 255, 255)
green = (111, 247, 87)

clock = pygame.time.Clock()
win = pygame.display.set_mode((500,500))

#importing pictures

paper_pic = pygame.image.load("Rock paper scissors\paper.png")
scissors_pic = pygame.image.load("Rock paper scissors\scissor.png")
rock_pic = pygame.image.load("Rock paper scissors\stone.png")
loading_pic = pygame.image.load("Rock paper scissors\loading.png")
bg = pygame.image.load("Rock paper scissors\scene.jpg")

clock.tick(40)

class Picks():
    def __init__(self, x, y, width, height, pic):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.display = True
        self.pic = pic
        self.chosen = False
        self.notclicked = True
        self.pick_comp = False

    def draw(self):
        # Saves the copy so the image's quality won't get worse
        copy = self.pic
        if self.chosen:
            copy = pygame.transform.scale(copy, (self.width + 20, self.height + 20)) 
            win.blit(copy, (self.x - 10, self.y - 10))
        else:
            self.pic = pygame.transform.scale(self.pic, (self.width, self.height)) 
            win.blit(self.pic, (self.x, self.y))

    # Checks if the mouse pointer is on one of the picks
    def checkpos(self):
        x_len = self.width
        y_len = self.height
        mos_x, mos_y = pygame.mouse.get_pos()
        if mos_x > self.x and mos_x < self.x + self.width and mos_y > self.y and mos_y < self.y + self.height:
            self.chosen = True
        else:
            self.chosen = False

    # Moves the pick to the center with a little animation
    def move(self):
        while self.x != 215:
            if self.x > 215:
                self.x -= 1
            else:
                self.x += 1
            self.draw()
            pygame.display.update()

class Loading():
    def __init__(self, x, y, width, height, pic):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.display = True
        self.pic = pygame.transform.scale(pic, (self.width, self.height)) 
        self.angle = 0
    
    def draw(self):
        self.blitRotate()

    # Makes the loading picture rotate an image around its center
    def blitRotate(self):
        copy = pygame.transform.rotate(self.pic, self.angle)
        win.blit(copy, (self.x + 37 - int(copy.get_width() / 2), self.y + 33 - int(copy.get_height() / 2)))
        self.angle += 1.5

def redrawGameWindow():
    global winner, score_player, score_computer
    win.blit(bg, (0,0))
    for pick in picks:
        if pick.notclicked:
            pick.draw()
    if loading_show:
        loading.draw()
    for pick_comp in comp_picks:
        if pick_comp.pick_comp == True:
            pick_comp.draw()
    if winner:
        # Rock paper scissors rules
        if index_p == random_pick:
            score_player += 1
            score_computer += 1
        elif (index_p == 1 and random_pick == 0) or (index_p == 0 and random_pick == 2) or (index_p == 2 and random_pick == 1):
            score_player += 1
        else:
            score_computer += 1
        winner = False
    person = font.render("Your score: " + str(score_player), 1, (255,255,255))
    win.blit(person, (180, 230))
    person = font.render("Computer's score: " + str(score_computer), 1, (255,255,255))
    win.blit(person, (130, 260))
    pygame.display.update()

# Waits for a few seconds so the unnecessary picks' dissappearence is seen 
def wait():
    i = 0
    while i < 100:
        pygame.time.delay(10)
        i += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                i = 301
                pygame.quit()

# Characters
scissors = Picks(125, 70, 70, 70, scissors_pic)
paper = Picks(215, 70, 70, 70, paper_pic)
rock = Picks(305, 70, 70, 70, rock_pic)
loading = Loading(215, 350, 70, 70, loading_pic)

paper_comp = Picks(215, 350, 70, 70, paper_pic)
scissors_comp = Picks(215, 350, 70, 70, scissors_pic)
rock_comp = Picks(215, 350, 70, 70, rock_pic)

# Variables

font = pygame.font.SysFont("comicsans", 30, True)
# If it's True, the program is running
run = True
# Makes the pick a normal size after clicking on it
normal_size = True
# Activates the check of the winner
winner = False
loading_show = True
# Activates a loop to hide unnecessary picks
hide_bool = False
start_ticks = pygame.time.get_ticks()
picks = [rock, paper, scissors]
comp_picks = [rock_comp, paper_comp, scissors_comp]
# List of picks to hide
hide = []
# The index of a player's pick in list of picks
index_p = 0
score_player = 0
score_computer = 0
restart = False
while run:
    # Restarts the program (keeping the score), deletes everything from the screen and moves picks to the right positions
    if restart:
        wait()
        scissors.x = 125
        scissors.y = 70
        paper.x = 215
        paper.y = 70
        rock.x = 305
        rock.y = 70
        normal_size = True
        winner = False
        loading_show = True
        hide_bool = False
        hide = []
        for pick in picks:
            pick.notclicked = True
        for pick_comp in comp_picks:
            pick_comp.pick_comp = False
        restart = False

    # If a user clicks on a "X", the program stops without displaying an error
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            hide = []
            for pick in picks:
                if normal_size:
                    if pick.chosen:
                        index_p = picks.index(pick)
                        # Keeps the pick on the screen
                        pick.notclicked = True
                        # Activates the process of hiding the other picks
                        hide_bool = True
                        pick.move()
                    else: 
                        # A list of picks to hide
                        hide.append(pick)
            if hide_bool and normal_size:
                for pick in hide:
                    # Picks in list hide will not be displayed
                    pick.notclicked = False
                normal_size = False
                loading_show = False
                random_pick = randint(0, 2)
                comp_picks[random_pick].pick_comp = True
                winner = True
                restart = True
                
    for pick in picks:
        if normal_size:
            pick.checkpos()
        else:
            pick.chosen = False
    redrawGameWindow()
pygame.quit()