import pygame
import sys
import random
import os

# screen setup
screen_width, screen_height = 960, 720
player_speed = 5
fish_speed = 5
max_time = 60  # max time in seconds

# initialize pygame
pygame.init()
pygame.mixer.init()

# path setup
current_folder = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_folder))
sound_folder = os.path.join(project_root, "sounds")
image_folder = os.path.join(project_root, "Images", "minigame_catfishfever")

bubble_sound_path = os.path.join(sound_folder, "bubble.wav")

# set up diplay
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Catfish Fever")
clock = pygame.time.Clock()

# load and loop sound
bubble_sound = pygame.mixer.Sound(bubble_sound_path)
bubble_sound.play(loops=-1)

# load background
background = pygame.transform.scale(
    pygame.image.load(os.path.join(image_folder, "Welsfieber_bg.png")),
    (screen_width, screen_height)
)

# scale image
def scale_height(img, target_height):
    ratio = target_height / img.get_height()
    new_width = int(img.get_width() * ratio)
    return pygame.transform.scale(img, (new_width, target_height))

# load player image + mask -> used AI to correct my use of masks
player_img = pygame.image.load(os.path.join(image_folder, "tami_taucher.png")).convert_alpha()
player_img = scale_height(player_img, 100)
player_mask = pygame.mask.from_surface(player_img)
player_rect = player_img.get_rect()
player_rect.x = 50
player_rect.centery = screen_height // 2

# load fish images + masks -> used AI to correct my use of masks
fish_images = []
fish_masks = []
fish_files = ["catfish.png", "fish.png", "shark.png"]
for fish_file in fish_files:
    img = pygame.image.load(os.path.join(image_folder, fish_file)).convert_alpha()
    img = scale_height(img, 140)
    fish_images.append(img)
    fish_masks.append(pygame.mask.from_surface(img))

# fonts
score_font = pygame.font.SysFont("Courier New", 30, bold=True)
end_font = pygame.font.SysFont("Courier New", 30, bold=True)

# game variables
fishes = []
spawn_delay = 1000 # -> ms
spawn_timer = 0
score = 0
start_ticks = pygame.time.get_ticks()
game_over = False
success = False

def spawn_fish():
    index = random.randint(0, len(fish_images) - 1)
    fish_img = fish_images[index]
    fish_mask = fish_masks[index] # mask so collision is pixel perfect
    fish_rect = fish_img.get_rect()
    fish_rect.x = screen_width + random.randint(0, 50)
    fish_rect.y = random.randint(0, screen_height - fish_rect.height)
    fishes.append((fish_img, fish_rect, fish_mask))

def draw_score_and_timer():
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
    time_left = max(0, max_time - int(seconds_passed))
    timer_text = score_font.render(f"Time left: {time_left}s", True, (255, 255, 255))
    screen.blit(timer_text, (10, 40))

def reset_game():
    global fishes, spawn_timer, score, start_ticks, game_over, success
    fishes = []
    spawn_timer = 0
    score = 0
    start_ticks = pygame.time.get_ticks()
    player_rect.centery = screen_height // 2
    game_over = False
    success = False

reset_game()

# main game loop -> used AI to format and polish my code
while True:
    dt = clock.tick(60)

    # draw background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < screen_height:
            player_rect.y += player_speed

        # spawn fish
        spawn_timer += dt
        if spawn_timer >= spawn_delay:
            spawn_fish()
            spawn_timer = 0

        # move fish + check collision
        for fish in fishes[:]:
            fish_img, fish_rect, fish_mask = fish
            fish_rect.x -= fish_speed
            if fish_rect.right < 0:
                fishes.remove(fish)

            offset = (fish_rect.x - player_rect.x, fish_rect.y - player_rect.y)
            if player_mask.overlap(fish_mask, offset):
                game_over = True
                success = False

        # update score
        seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
        score = int(seconds_passed)

        # draw everything
        screen.blit(player_img, player_rect)
        for fish_img, fish_rect, _ in fishes:
            screen.blit(fish_img, fish_rect)
        draw_score_and_timer()

        # end game after 60s
        if seconds_passed >= max_time:
            score = max_time  # 60
            game_over = True
            success = True

    else:
        # endscreen
        dark_overlay = pygame.Surface((screen_width, screen_height))
        dark_overlay.set_alpha(220)
        dark_overlay.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(dark_overlay, (0, 0))

        if success:
            success_text = end_font.render("SUCCESS!", True, (0, 220, 100))
        else:
            success_text = end_font.render("GAME OVER", True, (255, 0, 0))
        final_score_text = end_font.render(f"Final Score: {score}", True, (255, 220, 0))

        screen.blit(success_text, (screen_width // 2 - success_text.get_width() // 2, screen_height // 2 - 100))
        screen.blit(final_score_text, (screen_width // 2 - final_score_text.get_width() // 2, screen_height // 2 + 10))

    pygame.display.flip()
