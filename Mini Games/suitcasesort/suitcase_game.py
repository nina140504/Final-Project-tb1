import pygame
import random
import sys
import os

# initialize pygame
pygame.init()
pygame.mixer.init()

# screen setup
screen_width, screen_height = 960,720
max_time = 45

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("suitcase sort")
clock = pygame.time.Clock()

# paths
current_folder = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_folder))
sound_folder = os.path.join(project_root, "sounds")
image_folder = os.path.join(project_root, "Images", "minigame_suitcase")
music_path = os.path.join(sound_folder, "music", "terminalsong.wav")

# add music
pygame.mixer.music.load(music_path)
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)

# load sounds
whoosh_sound = pygame.mixer.Sound(os.path.join(sound_folder, "whoosh.wav"))
score_sound = pygame.mixer.Sound(os.path.join(sound_folder, "score.wav"))
wrong_sound = pygame.mixer.Sound(os.path.join(sound_folder, "wrong.wav"))

# load images and scale
background = pygame.image.load(os.path.join(image_folder, "luggage_bg.png"))
background = pygame.transform.scale(background, (screen_width, screen_height))

bin_img = pygame.image.load(os.path.join(image_folder, "bin.png"))
bin_img = pygame.transform.scale(bin_img, (200, 200))

belt_img = pygame.image.load(os.path.join(image_folder, "luggage_conveyour.png"))
belt_img = pygame.transform.scale(belt_img, (500, 400))

suitcase_red_img = pygame.image.load(os.path.join(image_folder, "suitcase_red.png"))
suitcase_red_img = pygame.transform.scale(suitcase_red_img, (180, 180))

suitcase_blue_img = pygame.image.load(os.path.join(image_folder, "suitcase_blue.png"))
suitcase_blue_img = pygame.transform.scale(suitcase_blue_img, (180, 180))

# rects for belt and bin
belt_rect = belt_img.get_rect(topleft=(100, 150))
bin_rect = bin_img.get_rect(topleft=(belt_rect.right + 90, belt_rect.top + 110))

# fonts
score_font = pygame.font.SysFont("Courier New", 27, bold=True)
end_font = pygame.font.SysFont("Courier New", 36, bold=True)

# create a suitcase dict
def create_suitcase():
    color = random.choice(["red", "blue"])
    image = suitcase_red_img if color == "red" else suitcase_blue_img
    x_pos = random.randint(50,screen_width - 100)
    rect = image.get_rect(center=(x_pos, screen_height - 120))
    return {"image": image, "rect": rect, "color": color, "fired": False}

suitcase = create_suitcase()

# draw conveyor belt
def draw_conveyor(surface, rect):
    surface.blit(belt_img, rect)

# draw score and timer
def draw_score_and_timer():
    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
    time_left = max(0, int(max_time - seconds_passed))

    score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
    timer_text = score_font.render(f"Time: {time_left}", True, (0, 0, 0))

    screen.blit(timer_text, (630, 7))
    screen.blit(score_text, (630, 27))

# game variables
score = 0
launch_ready = True
launch_speed = -8
start_ticks = pygame.time.get_ticks()
game_over = False

# main loop
while True:
    dt = clock.tick(60)
    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
    time_left = max(0, int(max_time - seconds_passed))

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        keys = pygame.key.get_pressed()

        # move suitcase left/right or launch it
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

        # check collisions and scoring
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

        # spawn new suitcase if no collision
        if suitcase["rect"].bottom < 0 and suitcase["fired"]:
            wrong_sound.play()
            suitcase = create_suitcase()

        # draw
        screen.blit(background, (0, 0))
        dark_overlay = pygame.Surface((screen_width, screen_height))
        dark_overlay.set_alpha(100)
        dark_overlay.fill((0, 0, 0))
        screen.blit(dark_overlay, (0, 0))

        draw_conveyor(screen, belt_rect)
        screen.blit(bin_img, bin_rect)
        screen.blit(suitcase["image"], suitcase["rect"])
        draw_score_and_timer()

        if time_left <= 0:
            game_over = True

    else:
        # endscreen
        dark_overlay = pygame.Surface((screen_width, screen_height))
        dark_overlay.set_alpha(220)
        dark_overlay.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(dark_overlay, (0, 0))

        end_text = end_font.render("Successfully Sorted!", True, (0, 220, 100))
        final_score_text = end_font.render(f"Final Score: {score}", True, (255, 220, 0))

        screen.blit(end_text, (screen_width // 2 - end_text.get_width() // 2, screen_height // 2 - 40))
        screen.blit(final_score_text, (screen_width // 2 - final_score_text.get_width() // 2, screen_height // 2 + 10))
        pygame.display.flip()
        pygame.time.wait(2000)
        break

    pygame.display.flip()

print(score)
pygame.quit()
sys.exit()