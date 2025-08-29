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

background_path = os.path.join(project_root, "Images", "main_menu_title.png")
arrow_path = os.path.join(project_root, "Images", "arrow_button.png")

background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

arrow_img = pygame.image.load(arrow_path)
arrow_img = pygame.transform.scale(arrow_img, (150, 150))
arrow_rect = arrow_img.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))

# font for rules text
font = pygame.font.SysFont("Courier New", 20, bold=True)

# rules text lines
rules = [
    "HELP! IT'S RAINING COCONUTS!",
    "CATCH all the coconuts.",
    "BEWARE of the palm leaves.",
    "Coconut = +1 point",
    "Golden coconut = +3 point",
    "Palm leaves = -1 point",
    "Use the arrow keys to NAVIGATE",
    "Press the arrow button to continue!",
]