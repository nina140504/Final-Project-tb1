import pygame
import random
import sys
import os

# screen setup
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Luggage Launch")

clock = pygame.time.Clock()

# initialize pygame
pygame.init()
pygame.mixer.init()

# path setup
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
IMG_DIR = os.path.join(BASE_DIR, "Images", "minigame_suitcase")
SND_DIR = os.path.join(BASE_DIR, "sounds")

# load images
background = pygame.image.load(os.path.join(IMG_DIR, "luggage_bg.png"))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

bin_img = pygame.image.load(os.path.join(IMG_DIR, "bin.png"))
bin_img = pygame.transform.scale(bin_img, (200, 200))
belt_img = pygame.image.load(os.path.join(IMG_DIR, "luggage_conveyour.png"))
belt_img = pygame.transform.scale(belt_img, (500, 400))

suitcase_red_img = pygame.image.load(os.path.join(IMG_DIR, "suitcase_red.png"))
suitcase_red_img = pygame.transform.scale(suitcase_red_img, (150, 150))
suitcase_blue_img = pygame.image.load(os.path.join(IMG_DIR, "suitcase_blue.png"))
suitcase_blue_img = pygame.transform.scale(suitcase_blue_img, (150, 150))

# define suitcase rects
belt_rect = belt_img.get_rect(topleft=(80, 80))
bin_rect = bin_img.get_rect(topleft=(belt_rect.right + 90, belt_rect.top + 110))

# load sounds
whoosh_sound = pygame.mixer.Sound(os.path.join(SND_DIR, "whoosh.wav"))
score_sound = pygame.mixer.Sound(os.path.join(SND_DIR, "score.wav"))
wrong_sound = pygame.mixer.Sound(os.path.join(SND_DIR, "wrong.wav"))

# font
font = pygame.font.SysFont("Courier New", 24, bold=True)
end_font = pygame.font.SysFont("Courier New", 36, bold=True)

# game stats
score = 0
launch_ready = True
launch_speed = -8
game_time = 45_000
start_time = pygame.time.get_ticks()

def create_suitcase():
    color = random.choice(["red", "blue"])
    image = suitcase_red_img if color == "red" else suitcase_blue_img
    x_pos = random.randint(50, WIDTH - 50)
    rect = image.get_rect(center=(x_pos, HEIGHT - 60))
    return {"image": image, "rect": rect, "color": color, "fired": False}

suitcase = create_suitcase()

def draw_conveyor(surface, rect):
    surface.blit(belt_img, rect)

def draw_score_and_timer(time_left, score):
    timer_text = font.render(f"Time Left: {time_left}", True, (0, 0, 0))
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    surface = screen
    surface.blit(timer_text, (650, 5))
    surface.blit(score_text, (650, 25))

# main game loop
running = True
while running:
    # time control -> AI was used to clean up my try of coding this
    dt = clock.tick(60)
    elapsed = pygame.time.get_ticks() - start_time
    time_left = max(0, (game_time - elapsed) // 1000)
    if elapsed > game_time:
        running = False

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # control suitcase movement
    keys = pygame.key.get_pressed()

    if not suitcase["fired"]:
        if keys[pygame.K_LEFT]:
            suitcase["rect"].x -= 5
        if keys[pygame.K_RIGHT]:
            suitcase["rect"].x += 5
        if keys[pygame.K_SPACE] and launch_ready:
            suitcase["fired"] = True
            launch_ready = False
            whoosh_sound.play()
    else:
        suitcase["rect"].y += launch_speed

    if not keys[pygame.K_SPACE]:
        launch_ready = True

    # check collisions and handle scores
    if suitcase["fired"]:
        hit_red = suitcase["rect"].colliderect(belt_rect) and suitcase["color"] == "red"
        hit_blue = suitcase["rect"].colliderect(bin_rect) and suitcase["color"] == "blue"
        if hit_red or hit_blue:
            score += 1
            score_sound.play()
            suitcase = create_suitcase()
        elif suitcase["rect"].bottom < 0:
            wrong_sound.play()
            suitcase = create_suitcase()

    if suitcase["rect"].bottom < 0 and suitcase["fired"]:
        wrong_sound.play()
        suitcase = create_suitcase()

    # draw game
    screen.blit(background, (0, 0))
    draw_conveyor(screen, belt_rect)
    screen.blit(bin_img, bin_rect)
    screen.blit(suitcase["image"], suitcase["rect"])

    draw_score_and_timer(time_left, score)

    pygame.display.flip()

# endscreen
dark_overlay = pygame.Surface((WIDTH, HEIGHT))
dark_overlay.set_alpha(220)
dark_overlay.fill((0, 0, 0))

screen.blit(background, (0, 0))
screen.blit(dark_overlay, (0, 0))

end_text = end_font.render("Successfully sorted!", True, (0, 220, 100))
final_score_text = end_font.render(f"Final Score: {score}", True, (255, 220, 0))

screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - 40))
screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 10))

pygame.display.flip()
pygame.time.delay(3000)
pygame.quit()
