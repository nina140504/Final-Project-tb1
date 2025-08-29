import pygame
import sys
import subprocess
import os

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MADEIRA PARTY - Menu")
clock = pygame.time.Clock()

# load images
current_folder = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_folder))

base_path = os.path.dirname(os.path.abspath(__file__))
maingame_path = os.path.join(base_path, "main_game_loop.py")

background_path = os.path.join("Images", "main_menu_title.png")
arrow_path = os.path.join("Images", "arrow_button.png")

background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

arrow_img = pygame.image.load(arrow_path)
arrow_img = pygame.transform.scale(arrow_img, (150, 150))
arrow_rect = arrow_img.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))

# font for rules text
font = pygame.font.SysFont("Courier New", 16, bold=True)

# rules text lines
rules = [
    "After a long and stressful semester you've finally decided to take a break.",
    "The goal is to score as many points as possible before the game is over.",
    "When you land on a blue field you get -3 points,",
    "the pink one is +2 and the yellow starts a minigame.",
    "The points from the minigame will be added to the total score.",
    "To move forward click the dice image in the left top corner.",
    "The yellow frame shows who`s turn it is.",
    "The game is over when each player played 5 minigames.",
    "Are you guys ready for a fun adventure all over the island?"
]

# box size and position
BOX_WIDTH, BOX_HEIGHT = 800, 320
BOX_X, BOX_Y = (SCREEN_WIDTH - BOX_WIDTH) // 2, 250

running = True
while running:
    # draw background image
    screen.blit(background, (0, 0))

    # create transparent black box to put text on
    box = pygame.Surface((BOX_WIDTH, BOX_HEIGHT), pygame.SRCALPHA)
    box.fill((0, 0, 0, 140))  # black with transparency
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
                proc = subprocess.Popen([sys.executable, maingame_path])
                proc.wait()
                pygame.quit()
                sys.exit()

    pygame.display.flip()
    clock.tick(30)