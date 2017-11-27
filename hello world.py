import pygame, sys
from pygame.locals import *

# set up pygame
pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((300, 200), 0, 32)
pygame.display.set_caption('Hello world!')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 182, 193)

# set up fonts
basicFont = pygame.font.SysFont(None, 50)

# set up the text
text = basicFont.render('Hello world!', True, PINK)
textRect = text.get_rect()
textRect.centerx = windowSurface.get_rect().centerx
textRect.centery = windowSurface.get_rect().centery

# draw the white background onto the surface
windowSurface.fill(PINK)

# draw the text's background rectangle onto the surface
pygame.draw.rect(windowSurface, WHITE, (textRect.left - 20, textRect.top - 20, textRect.width + 40, textRect.height + 40))

# draw the text onto the surface
windowSurface.blit(text, textRect)

# draw the window onto the screen
pygame.display.update()

# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
