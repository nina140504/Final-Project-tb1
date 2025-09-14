import pygame
import os
import sys

# initialize pygame
pygame.init()
pygame.mixer.init()

# screen setup
screen_width, screen_height = 960, 720
max_time = 60

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ananas Pong")
clock = pygame.time.Clock()

# paths
current_folder = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_folder))
sound_folder = os.path.join(project_root, "sounds")
image_folder = os.path.join(project_root, "Images", "minigame_ananaspong")
music_path = os.path.join(sound_folder, "music", "AP_StockTune-Sunshine Rhythm Ride_1756649176.mp3")

# add music
pygame.mixer.music.load(music_path)
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

# load sounds
score_sound = pygame.mixer.Sound(os.path.join(sound_folder, "score.wav"))
miss_sound = pygame.mixer.Sound(os.path.join(sound_folder, "wrong.wav"))

# load background
background = pygame.image.load(os.path.join(image_folder, "ananas_bg.png"))
background = pygame.transform.scale(background, (screen_width, screen_height))

# helper: scale image by height
def scale_height(img, target_height):
    ratio = target_height / img.get_height()
    new_width = int(img.get_width() * ratio)
    return pygame.transform.scale(img, (new_width, target_height))

# surfboard setup
surfboard_img = pygame.image.load(os.path.join(image_folder, "surfboard.png")).convert_alpha()
surfboard_img = scale_height(surfboard_img, 300)

surfboard_rect_left = surfboard_img.get_rect(center=(50, screen_height // 2))
surfboard_rect_right = surfboard_img.get_rect(center=(screen_width - 50, screen_height // 2))
surfboard_mask = pygame.mask.from_surface(surfboard_img)

# pineapple ball setup
ananas_img_original = pygame.image.load(os.path.join(image_folder, "ananas.png")).convert_alpha()
ananas_img_original = scale_height(ananas_img_original, 100)
ananas_rect = ananas_img_original.get_rect(center=(screen_width // 2, screen_height // 2))

ball_speed = [5, 5]
rotation_angle = 0

# fonts
score_font = pygame.font.SysFont("Courier New", 30, bold=True)
end_font = pygame.font.SysFont("Courier New", 30, bold=True)

# draw score and timer
def draw_score_and_timer():
    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
    time_left = max(0, max_time - int(seconds_passed))

    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    timer_text = score_font.render(f"Time: {time_left}", True, (255, 255, 255))

    score_x = screen_width // 2 - score_text.get_width() // 2
    timer_x = screen_width // 2 - timer_text.get_width() // 2

    screen.blit(score_text, (score_x, 10))
    screen.blit(timer_text, (timer_x, 40))

# game variables
score = 0
ball_reset_cooldown = 0
start_ticks = pygame.time.get_ticks()
game_over = False

# main loop
while True:
    dt = clock.tick(60)
    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
    time_left = max(0, int(max_time - seconds_passed))

    # cooldown to avoid repeated sounds -> used AI to come up with this
    if ball_reset_cooldown > 0:
        ball_reset_cooldown -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and surfboard_rect_left.top > 0:
            surfboard_rect_left.y -= 6
        if keys[pygame.K_s] and surfboard_rect_left.bottom < screen_height:
            surfboard_rect_left.y += 6
        if keys[pygame.K_UP] and surfboard_rect_right.top > 0:
            surfboard_rect_right.y -= 6
        if keys[pygame.K_DOWN] and surfboard_rect_right.bottom < screen_height:
            surfboard_rect_right.y += 6

        # move pineapple
        ananas_rect.x += ball_speed[0]
        ananas_rect.y += ball_speed[1]

        # spin pineapple
        rotation_angle = (rotation_angle + 5) % 360
        ananas_img = pygame.transform.rotate(ananas_img_original, rotation_angle)
        ananas_mask = pygame.mask.from_surface(ananas_img)
        rotated_rect = ananas_img.get_rect(center=ananas_rect.center)

        # bounce off top/bottom
        if rotated_rect.top <= 0 or rotated_rect.bottom >= screen_height:
            ball_speed[1] *= -1

        # pixel perfect collision -> used AI to fix my use of masks
        offset_left = (rotated_rect.left - surfboard_rect_left.left, rotated_rect.top - surfboard_rect_left.top)
        if surfboard_mask.overlap(ananas_mask, offset_left):
            ball_speed[0] = abs(ball_speed[0])
            score += 1
            score_sound.play()

        offset_right = (rotated_rect.left - surfboard_rect_right.left, rotated_rect.top - surfboard_rect_right.top)
        if surfboard_mask.overlap(ananas_mask, offset_right):
            ball_speed[0] = -abs(ball_speed[0])
            score += 1
            score_sound.play()

        # missed pineapple
        if rotated_rect.left <= 0 or rotated_rect.right >= screen_width:
            if ball_reset_cooldown == 0:  # only when cooldown is over
                score -= 3
                miss_sound.play()
                ball_reset_cooldown = 60

            # reset ball
            ananas_rect.center = (screen_width // 2, screen_height // 2)
            ball_speed[0] = 5 if rotated_rect.left <= 0 else -5
            ball_speed[1] = 5
            rotation_angle = 0

        # draw
        screen.blit(background, (0, 0))
        screen.blit(surfboard_img, surfboard_rect_left)
        screen.blit(surfboard_img, surfboard_rect_right)
        screen.blit(ananas_img, rotated_rect)
        draw_score_and_timer()

        # end game ater 60s
        if time_left <= 0:
            game_over = True
    else:
        # endscreen
        dark_overlay = pygame.Surface((screen_width, screen_height))
        dark_overlay.set_alpha(220)
        dark_overlay.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(dark_overlay, (0, 0))

        end_text = end_font.render("You really are a Pong Pro!", True, (255, 220, 0))
        final_score_text = end_font.render(f"Final Score: {score}", True, (255, 220, 0))

        screen.blit(end_text, (screen_width // 2 - end_text.get_width() // 2, screen_height // 2 - 30))
        screen.blit(final_score_text, (screen_width // 2 - final_score_text.get_width() // 2, screen_height // 2 + 20))
        pygame.display.flip()
        pygame.time.wait(2000)
        break

    pygame.display.flip()

print(score)
pygame.quit()
sys.exit()