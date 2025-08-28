import pygame
import sys
import subprocess
import os

# set up screen size to match the game window
SCREEN_WIDTH, SCREEN_HEIGHT = 960, 720

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catfish Fever - Rules")
clock = pygame.time.Clock()

# load images
current_folder = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_folder))

background_path = os.path.join(project_root, "Images", "minigame_ananaspong", "ananaspong_title.png")
arrow_path = os.path.join(project_root, "Images", "arrow_button.png")

background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

arrow_img = pygame.image.load(arrow_path)
arrow_img = pygame.transform.scale(arrow_img, (150, 150))
arrow_rect = arrow_img.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))

# font for rules text
font = pygame.font.SysFont("Courier New", 22, bold=True)

# rules text lines
rules = [
    "READY TO RIDE THE PINEAPPLE WAVE?",
    "WELCOME to Ananas Pong.",
    "AVOID letting the pineapple get past you!",
    "USE W/S and UP/DOWN keys to move the surfboards.",
    "EVERY successful hit = +1 point.",
    "MISS the pineapple = -3 points.",
    "SURVIVE 60 seconds -> Success!",
    "Press the arrow button to continue!",
]

# box size and position
BOX_WIDTH, BOX_HEIGHT = 700, 320
BOX_X, BOX_Y = (SCREEN_WIDTH - BOX_WIDTH) // 2, 250

running = True
while running:
    # draw background image
    screen.blit(background, (0, 0))

    # create transparent black box to put text on
    box = pygame.Surface((BOX_WIDTH, BOX_HEIGHT), pygame.SRCALPHA)
    box.fill((0, 0, 0, 180))  # black with transparency
    screen.blit(box, (BOX_X, BOX_Y))

    # draw each line of the rules centered in the box
    line_height = 35
    for i, line in enumerate(rules):
        text_surface = font.render(line, True, (255, 255, 255))
        text_x = BOX_X + (BOX_WIDTH - text_surface.get_width()) // 2
        text_y = BOX_Y + 30 + i * line_height
        screen.blit(text_surface, (text_x, text_y))

    # draw the arrow button
    screen.blit(arrow_img, arrow_rect)

    # handle events -> MIT AI VERSUCHT; GEHT NICHT; SPÄTER WEITERBEARTBEITEN
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if arrow_rect.collidepoint(event.pos):
                # start the actual game
                subprocess.Popen(["python", "Mini Games/ananaspong/ananas_game.py"])
                pygame.quit()
                sys.exit()

    pygame.display.flip()
    clock.tick(30)
