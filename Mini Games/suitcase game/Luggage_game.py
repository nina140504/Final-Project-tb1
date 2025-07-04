# This is a game where you sort suitcases - red goes on the conveyor belt, blue goes in the bin.
# If you sort correctly, you get a point. Once the timer hit 0, you have your final score.
# You can use the arrow keys to move the suitcase and then launch it with space.
# AI was used to create parts of this game.


import pygame
import random
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Luggage Launch")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Load background
background = pygame.image.load("background_airport.PNG")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Conveyor belt setup
belt_width = 600
belt_height = 80
belt_rect = pygame.Rect(50, HEIGHT // 2 + 50, belt_width, belt_height)

# The bin
bin_img = pygame.image.load("bin.png")
bin_img = pygame.transform.scale(bin_img, (200, 200))
bin_rect = bin_img.get_rect(topleft=(belt_rect.right + 85, belt_rect.top - 80))

# Load suitcase images and scale
suitcase_red_img = pygame.image.load("suitcase_red.png")
suitcase_blue_img = pygame.image.load("suitcase_blue.png")
suitcase_red_img = pygame.transform.scale(suitcase_red_img, (150, 150))
suitcase_blue_img = pygame.transform.scale(suitcase_blue_img, (150, 150))

# Game state
score = 0
launch_ready = True
launch_speed = -8
game_time = 30_000  # milliseconds
start_time = pygame.time.get_ticks()

def create_suitcase():
    color = random.choice(["red", "blue"])
    image = suitcase_red_img if color == "red" else suitcase_blue_img
    x_pos = random.randint(50, WIDTH - 50)
    rect = image.get_rect(center=(x_pos, HEIGHT - 60))
    return {"image": image, "rect": rect, "color": color, "fired": False}


suitcase = create_suitcase()

# finish the conveyor belt
def draw_conveyor(surface, rect):
    pygame.draw.rect(surface, (80, 80, 80), rect, border_radius=20)
    roller_radius = 12
    spacing = 40
    x = rect.x + 20
    y = rect.centery
    while x <= rect.right - 20:
        pygame.draw.circle(surface, (60, 60, 60), (x, y), roller_radius)
        pygame.draw.circle(surface, (30, 30, 30), (x, y), roller_radius, 2)
        x += spacing

# Main game loop
running = True
while running:
    elapsed = pygame.time.get_ticks() - start_time
    time_left = max(0, (game_time - elapsed) // 1000)
    if elapsed > game_time:
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if not suitcase["fired"]:
        if keys[pygame.K_LEFT]:
            suitcase["rect"].x -= 5
        if keys[pygame.K_RIGHT]:
            suitcase["rect"].x += 5
        if keys[pygame.K_SPACE] and launch_ready:
            suitcase["fired"] = True
            launch_ready = False
    else:
        suitcase["rect"].y += launch_speed

    if not keys[pygame.K_SPACE]:
        launch_ready = True

    # Collision logic
    if suitcase["fired"]:
        hit_red = suitcase["rect"].colliderect(belt_rect) and suitcase["color"] == "red"
        hit_blue = suitcase["rect"].colliderect(bin_rect) and suitcase["color"] == "blue"
        if hit_red or hit_blue:
            score += 1
            suitcase = create_suitcase()

    if suitcase["rect"].bottom < 0:
        suitcase = create_suitcase()

    # Drawing
    screen.blit(background, (0, 0))
    draw_conveyor(screen, belt_rect)
    screen.blit(bin_img, bin_rect)
    screen.blit(suitcase["image"], suitcase["rect"])

    timer_text = font.render(f"Time Left: {time_left}", True, (0, 0, 0))
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(timer_text, (10, 10))
    screen.blit(score_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)

# Game Over
screen.fill((255, 255, 255))
end_text = font.render(f"Time's up! Final Score: {score}", True, (0, 0, 0))
screen.blit(end_text, (WIDTH // 2 - 180, HEIGHT // 2))
pygame.display.flip()
pygame.time.delay(3000)
pygame.quit()
