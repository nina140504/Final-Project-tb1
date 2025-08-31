import pygame
import sys
import subprocess
import os
import time


def run_end_screen(scores):
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("MADEIRA PARTY - Endscreen")
    clock = pygame.time.Clock()
    background_path = os.path.join("Images", "main_menu_title.png")
    arrow_path = os.path.join("Images", "arrow_button.png")
    background = pygame.image.load(background_path)
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    arrow_img = pygame.image.load(arrow_path)
    arrow_img = pygame.transform.scale(arrow_img, (150, 150))
    arrow_rect = arrow_img.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))

    font = pygame.font.SysFont("Courier New", 16, bold=True)
    large_font = pygame.font.SysFont("Courier New", 40, bold=True)

    rules = [
        "CONGRATULATIONS!",
        "You have finished your adventure all over the island of Madeira.",
        "Hopefully you enjoyed your vacation and had a lot of fun.",
        "Let's see who of you conquered the adventures of island the best.",
        "Click the arrow button to see the FINAL RESULTS.",
        "Come back soon for your next holiday! :)"
    ]

    BOX_WIDTH, BOX_HEIGHT = 800, 330
    BOX_X, BOX_Y = (SCREEN_WIDTH - BOX_WIDTH) // 2, 250

    show_scores = False
    running = True

    while running:
        screen.blit(background, (0, 0))
        box = pygame.Surface((BOX_WIDTH, BOX_HEIGHT), pygame.SRCALPHA)
        box.fill((0, 0, 0, 140))
        screen.blit(box, (BOX_X, BOX_Y))

        if not show_scores:
            line_height = 35
            for i, line in enumerate(rules):
                text_surface = font.render(line, True, (255, 255, 255))
                text_x = BOX_X + (BOX_WIDTH - text_surface.get_width()) // 2
                text_y = BOX_Y + 30 + i * line_height
                screen.blit(text_surface, (text_x, text_y))
            screen.blit(arrow_img, arrow_rect)
        else:
            title = large_font.render("FINAL RESULTS", True, (255, 255, 80))
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, BOX_Y + 30))
            for i, (name, score) in enumerate(scores):
                result = font.render(f"{i + 1}. {name}: {score} Points", True, (255, 230, 120))
                screen.blit(result, (BOX_X + 70, BOX_Y + 100 + i * 35))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not show_scores and arrow_rect.collidepoint(event.pos):
                    show_scores = True

        pygame.display.flip()
        clock.tick(30)


