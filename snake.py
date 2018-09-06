# snake.py
#
# Original design by Justin Hendrick http://code.google.com/p/colorful-snake
#
# This program is free software. You can redistribute and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, using either version 3 of the License, or 
# any later version.
#
# This program is distributed WITHOUT ANY WARRANTY, including, but not 
# limited to, the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import pygame, pygame.mixer, os.path
from random import randint

def cdetect():
    global leng, x, y, xcors, ycors, running
    gameover = pygame.mixer.Sound("sounds/WilhelmScream.wav")
    for i in range(1, leng):
        if x == xcors[len(xcors) - i] and y == ycors[len(ycors) - i]:
            gameover.play()
            clock.tick(1)
            running = False

def draw(x, y, col):
    if col == "sn":
        r = randint(100, 200)
        g = randint(100, 200)
        b = randint(100, 200)
    if col == "tr":
        r = randint(3, 18)
        g = randint(3, 18)
        b = randint(3, 18)
    if col == "ap":
        r = randint(200, 255)
        g = randint(200, 255)
        b = randint(200, 255)
    l = range(-radius + 1,radius)
    for ix in l:
        for iy in l:
            if (ix == radius - 1 or ix == -radius + 1) and (iy == radius - 1 or iy == -radius + 1):
                pass
            else:
                screen.set_at((x + ix, y + iy), (r, g, b))

pygame.init()
#chomp audio file from soundjay http://www.soundjay.com/tos.html
#wilhelm audio file from hollywoodlostandfound.net
#I don't think I broke copyright law but if I did, notify me and I will remove any offending material.
chomp = pygame.mixer.Sound("sounds/chomp.wav")
clock = pygame.time.Clock()

#Grabs the difficulty selected in the menu and changes the setting accordingly
# diff = open(".dif.txt")
# dif = diff.read()
# diff.close()
# os.remove(".dif.txt")
dif = "Medium"
spd = 20
apl = 10
difi = 1


#sets up screen, snake, and caption
size = 705
#size must be a multiple of width
screen = pygame.display.set_mode((size,size))
score = 0
pygame.display.set_caption("%s\tScore: %d" %(dif, score))
#width must be odd. 
width = 15
if width % 2 == 0:
    print "Invalid snake width. width must be odd."
    quit()
if size % width != 0:
    print "Invalid snake width or screen size. size must be a multiple of width."
    quit()

#initial conditions
radius = (width - 1) / 2
x = radius + 1
y = radius + 1
a = 0
b = 0
direction = "right"
leng = 4
lenguntil = 4
xcors = [0, 0, 0, 0]
ycors = [0, 0, 0, 0]
running = True

#draw first apple
while (a + radius) % width != 0 or (b + radius) % width != 0 or a == x or b == y:
    a = randint(radius + 1, size - width - 1)
    b = randint(radius + 1, size - width - 1)
draw(a, b, "ap")
pygame.display.flip()

#main loop
while running:
    #get input
    inp = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and inp == False:
                if direction != "right":
                    direction = "left"
                    inp = True
            elif event.key == pygame.K_UP and inp == False:
                if direction != "down":
                    direction = "up"
                    inp = True
            elif event.key == pygame.K_RIGHT and inp == False:
                if direction != "left":
                    direction = "right"
                    inp = True
            elif event.key == pygame.K_DOWN and inp == False:
                if direction != "up":
                    direction = "down"
                    inp = True

    #add current position to coordinate lists
    xcors.append(x)
    ycors.append(y)

    #draw trail behind snake
    draw(xcors[len(xcors) - leng], ycors[len(ycors) - leng], "tr")
    
    #snake growth control
    if leng != lenguntil:
        leng += 1

    #movement value change
    if direction == "left":
        x -= width
    if direction == "up":
        y -= width
    if direction == "right":
        x += width
    if direction == "down":
        y += width

    #teleport from edge to other side
    if x == -radius:
        x = size - radius
    elif x == size + radius + 1:
        x = radius + 1
    elif y == -radius:
        y = size - radius
    elif y == size + radius + 1:
        y = radius + 1
    
    #draw new point and check for collision
    draw(x, y, "sn")
    cdetect()

    #running into apple
    if x == a and y == b:
        chomp.play()
        olda = a
        oldb = b
        while (a + radius) % width != 0 or (b + radius) % width != 0 or a == olda or b == oldb:
            a = randint(radius + 1, size - width - 1)
            b = randint(radius + 1, size - width - 1)
            for i in range(1, leng):
                if a == xcors[len(xcors) - i] and b == ycors[len(ycors) - i]:
                    a = olda
                    b = oldb
        lenguntil = leng + apl
        score = lenguntil / apl
        pygame.display.set_caption("%s\tScore: %d" %(dif, score))
        draw(a, b, "ap")
    clock.tick(spd)
    pygame.display.flip()

#high score control
if os.path.exists(".hiscore.txt") == False:
    hsf = open(".hiscore.txt", "w")
    hsf.write("0\n0\n0")
    hsf.close()
hsfa = open(".hiscore.txt", "r")
chs = hsfa.read()
hsfa.close()
chs = chs.split("\n")
for i in range(0,3):
    chs[i] = eval(chs[i])
if score > chs[difi]:
    arial = pygame.font.SysFont("arial", 30)
    nhs = arial.render("%d is a new high score!" %score, True, (255, 255, 255))
    screen.blit(nhs, (250, 320))
    pygame.display.flip()
    for i in range(3):
        clock.tick(1)
    hsfb = open(".hiscore.txt", "w")
    chs[difi] = score
    for i in chs:
        hsfb.write("%s\n" %i)
    hsfb.close()

# vim: set ts=2 sts=2 sw=2 et:
