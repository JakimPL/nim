import pygame, sys
from pygame.locals import*
pygame.init()

# GRA
nim = [1,3,5,7,11,15,18]
l = len(nim)
g = 0
name = ["Gracz pierwszy", "Gracz drugi"]
counter = 0
click = True
game = True
undo = []

# GUI
x_offset = 12
y_offset = 12*(l+2) + 4
w = 20
h = 140
r = 80
select = -1
game_width = max(2*x_offset + w*max(nim) + r, 280)
game_height = y_offset + h*l

DISPLAYSURF = pygame.display.set_mode((game_width,game_height),0,32)
font = pygame.font.SysFont("Lucida Console", 14)

match = pygame.image.load("match.png")
match_on = pygame.image.load("match_on.png")

def mouse_in(pos, j, i):
    if pos[0] > x_offset + i*w and pos[0] <= x_offset + (i+1)*w and pos[1] > y_offset + j*h and pos[1] <= y_offset + (j+1)*h:
        return True
    return False

def nimsum(nim):
    eq = 0
    for i in range(l):
        eq ^= nim[i]
    return eq

def nonzero(nim):
    k = 0
    for i in range(l):
        if nim[i] > 0:
            k += 1
    return k

def heaps(nim):
    k = 0
    for i in range(l):
        if nim[i] == 1:
            k += 1
    return k

def lose(nim):
    nim[nim.index(max(nim))] -= 1
    return nim

def move(nim):
    m = nimsum(nim)
    if sum(1 for x in nim if x > 1) <= 1:
        moves_left = sum(1 for x in nim if x > 0)
        is_odd = (moves_left % 2 == 1)
        M = max(nim)
        if M == 1 and is_odd:
            nim = lose(nim)
            return nim
        else:
            nim[nim.index(M)] -= max(nim) - int(is_odd)
            return nim
    if m != 0:
        for i in range(l):
            if nim[i]^m < nim[i]:
                nim[i] = nim[i]^m
                return nim
    else:
        nim = lose(nim)
        return nim

print(nim)
while True:
    pygame.draw.rect(DISPLAYSURF, (64,64,128), (0, 0, game_width, game_height))
    flag = False
    if not pygame.mouse.get_pressed()[0]:
        click = True
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            print(undo)
            if event.key == K_RETURN:
                if select == -1:
                    select = -1
                    counter = 0
                    flag = True
                else:
                    print(nim)
                    undo += [[nim[:], g]]
                    nim[select] -= counter
                    select = -1
                    counter = 0
                    g = 1 - g
            if event.key == K_BACKSPACE:
                if len(undo) > 0:
                    print(undo[-1][0])
                    nim = undo[-1][0]
                    g = undo[-1][1]
                    del undo[-1]
    if flag and sum(nim) > 0:
        undo += [[nim[:], g]]
        print(undo)
        nim = move(nim)
        print(name[g] + " wykonal ruch:")
        g = 1 - g
    if sum(nim) == 0 and game:
        print(name[g] + " wygral.")
        game = False
    if select != -1:
        pygame.draw.rect(DISPLAYSURF, (128,128,128), (x_offset, y_offset + select*h, nim[select]*w, h))
    m = nimsum(nim)
    DISPLAYSURF.blit(font.render("Ruch: " + name[g]+ ".", 1, (255,255,255)), (12, 12))
    DISPLAYSURF.blit(font.render("NIM: " + str("TAK" if m == 0 else "NIE"), 1, (255,255,255)), (208, 12))
    for i in range(l):
        DISPLAYSURF.blit(font.render("Rzad " + str(i) + ": " + str(nim[i]), 1, (255,255,255)), (12, 24+12*i))
        if pygame.mouse.get_pressed()[2]:
            select = -1
            counter = 0
        for j in range(nim[i]):
            if mouse_in(pygame.mouse.get_pos(),i,j):
                if pygame.mouse.get_pressed()[0]:
                    if click:
                        click = False
                        if select == -1 and nim[i] != 0:
                            counter += 1
                            select = i
                        elif select == i and counter < nim[i]:
                            counter += 1
            if i == select and j >= nim[i] - counter:
                DISPLAYSURF.blit(match_on, (x_offset + w*j, y_offset + h*i))
            else:
                DISPLAYSURF.blit(match, (x_offset + w*j, y_offset + h*i))
    pygame.display.update()
