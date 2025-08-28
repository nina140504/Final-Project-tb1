import pygame
import random
import os
import sys

# initialize pygame
pygame.init()
pygame.mixer.init()

#screen setup
screen_width, screen_height = 960, 720
max_time = 60

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Coconut Catch")
clock = pygame.time.Clock()

# paths
current_folder = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_folder))
sound_folder = os.path.join(project_root, "sounds")
image_folder = os.path.join(project_root, "Images", "minigame_coconutcatch")

# load sounds
score_sound = pygame.mixer.Sound(os.path.join(sound_folder, "score.wav"))
whoosh_sound = pygame.mixer.Sound(os.path.join(sound_folder, "whoosh.wav"))

# load background
background = pygame.transform.scale(
    pygame.image.load(os.path.join(image_folder, "background.png")),
    (screen_width, screen_height)
)

# helper: scale image by height
def scale_height(img, target_height):
    ratio = target_height / img.get_height()
    new_width = int(img.get_width() * ratio)
    return pygame.transform.scale(img, (new_width, target_height))

# player setup
player_img = pygame.image.load(os.path.join(image_folder, "tami_coconutcatcher.png")).convert_alpha()
player_img = scale_height(player_img, 200)
player_rect = player_img.get_rect()
player_rect.centerx = screen_width // 2
player_rect.bottom = screen_height - 20
player_speed = 7

# coconuts
coconut_img = scale_height(
    pygame.image.load(os.path.join(image_folder, "coconut.png")).convert_alpha(),
    100)
pink_coconut_img = scale_height(
    pygame.image.load(os.path.join(image_folder, "pink_coconut.png")).convert_alpha(),
    100)
leaf_coconut_img = scale_height(
    pygame.image.load(os.path.join(image_folder, "leaf_coconut.png")).convert_alpha(),
    100)

# fonts
score_font = pygame.font.SysFont("Courier New", 30, bold=True)
end_font = pygame.font.SysFont("Courier New", 30, bold=True)

# coconut object
class FallingCoconut:
    def __init__(self, x, img, value):
        self.img = img
        self.value = value
        self.rect = img.get_rect()
        self.rect.x = x
        self.rect.y = -50
        self.speed = 4

    def fall(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.img, self.rect)

# spawn coconut
def spawn_coconut():
    x_pos = random.randint(0, screen_width - coconut_img.get_width())
    r = random.random()
    if r < 0.20: # 20% chance
        coconut = FallingCoconut(x_pos, pink_coconut_img, 3)
    elif r < 0.65: #45% chance
        coconut = FallingCoconut(x_pos, coconut_img, 1)
    else: # 35% chance
        coconut = FallingCoconut(x_pos, leaf_coconut_img, -1)
    coconuts.append(coconut)

# draw score and timer
def draw_score_and_timer(score, time_left):
    rect_w, rect_h = 180, 80
    rect_surf = pygame.Surface((rect_w, rect_h), pygame.SRCALPHA)
    rect_surf.fill((0, 0, 0, 150))
    rect_x = screen_width // 2 - rect_w // 2
    rect_y = 20
    screen.blit(rect_surf, (rect_x, rect_y))

    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    timer_text = score_font.render(f"Time: {time_left}", True, (255, 255, 255))

    screen.blit(score_text, (rect_x + rect_w // 2 - score_text.get_width() // 2, rect_y + 8))
    screen.blit(timer_text, (rect_x + rect_w // 2 - timer_text.get_width() // 2, rect_y + 40))

# game variables
coconuts = []
spawn_delay = 1000
spawn_timer = 0
score = 0
start_ticks = pygame.time.get_ticks()
game_over = False

# main loop
while True:
    dt = clock.tick(60)
    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
    time_left = max(0, int(max_time - seconds_passed))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < screen_width:
            player_rect.x += player_speed

        # spawn coconuts
        spawn_timer += dt
        if spawn_timer >= spawn_delay:
            spawn_coconut()
            spawn_timer = 0

        # update coconuts
        for c in coconuts[:]:
            c.fall()
            if c.rect.colliderect(player_rect):
                score += c.value
                if c.value == -1:
                    whoosh_sound.play()
                else:
                    score_sound.play()
                coconuts.remove(c)
            elif c.rect.top > screen_height:
                coconuts.remove(c)

        # draw
        screen.blit(background, (0, 0))
        for c in coconuts:
            c.draw(screen)
        screen.blit(player_img, player_rect)
        draw_score_and_timer(score, time_left)

        # end game after 60s
        if time_left <= 0:
            game_over = True

    else:
        # endscreen
        dark_overlay = pygame.Surface((screen_width, screen_height))
        dark_overlay.set_alpha(220)
        dark_overlay.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(dark_overlay, (0, 0))

        end_text = end_font.render("You caught so many coconuts!", True, (255, 220, 0))
        final_score_text = end_font.render(f"Final Score: {score}", True, (255, 220, 0))

        screen.blit(end_text, (screen_width // 2 - end_text.get_width() // 2, screen_height // 2 - 30))
        screen.blit(final_score_text, (screen_width // 2 - final_score_text.get_width() // 2, screen_height // 2 + 20))
    pygame.display.flip()

    print(score)
    pygame.quit()
    sys.exit()