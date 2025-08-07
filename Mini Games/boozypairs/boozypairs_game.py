import pygame
import sys
import random
import os

# set up sizes
screen_width, screen_height = 960, 720
card_width, card_height = 120, 120
rows, cols = 3, 6  # grid of cards
start_y = 300

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Boozy Pairs")
clock = pygame.time.Clock()

# get images and sounds
current_folder = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_folder))

image_folder = os.path.join(project_root, "Images", "minigame_boozypairs")
sound_folder = os.path.join(project_root, "sounds")

# define pairs of cards: each pair has a fruit and a cocktail
pairs = [
    ("strawberry.png", "strawberry_daiquiri.png"),
    ("watermelon.png", "watermelon_cocktail.png"),
    ("passionfruit.png", "martini_pornstar.png"),
    ("mango.png", "mango_margarita.png"),
    ("lime.png", "margarita.png"),
    ("ananas.png", "pina_colada.png"),
    ("lemon.png", "citrus_cocktail.png"),
    ("cranberry.png", "cosmopolitain.png"),
    ("orange.png", "mai_thai.png"),
]

# load sounds
whoosh_sound = pygame.mixer.Sound(os.path.join(sound_folder, "whoosh.wav"))
score_sound = pygame.mixer.Sound(os.path.join(sound_folder, "score.wav"))
wrong_sound = pygame.mixer.Sound(os.path.join(sound_folder, "wrong.wav"))


# load background and leaf image
background = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, "background.jpg")), (screen_width, screen_height))
leaf_img = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, "leafs.png")), (card_width, card_height))

# helper function to load and scale card images by filename
def load_card_image(filename):
    return pygame.transform.scale(pygame.image.load(os.path.join(image_folder, filename)), (card_width, card_height))


# set up fonts for showing score and end game messages
score_font = pygame.font.SysFont("Courier New", 48, bold=True)
end_font = pygame.font.SysFont("Courier New", 64, bold=True)

# cards list: two cards per pair (fruit + drink) with same ID for matching -> used AI to come up with using ID and to understand how to use it
cards = []
for i, (fruit_img, drink_img) in enumerate(pairs[: (rows * cols) // 2]):
    cards.append({"id": i, "img": load_card_image(fruit_img)})
    cards.append({"id": i, "img": load_card_image(drink_img)})

# spread out cards
x_padding = (screen_width - (cols * card_width)) // (cols + 1)
positions = []
for row in range(rows):
    for col in range(cols):
        x = x_padding + col * (card_width + x_padding)  # x pos for each card
        y = start_y + row * (card_height + 20)          # y pos for each card, 20 px vertical gap
        positions.append((x, y))

# function to start or reset the game
def reset_game():
    random.shuffle(cards)  # shuffle the cards so they're in random order every game
    for index, card in enumerate(cards):
        # create a rectangle for each card, used for drawing and clicking
        card["rect"] = pygame.Rect(positions[index][0], positions[index][1], card_width, card_height)
        card["matched"] = False  # mark all cards as unmatched at the start
    global covered, first_choice, second_choice, score
    covered = [True] * len(cards)  # all cards start covered
    first_choice = second_choice = None  # no cards flipped yet
    score = 0  # reset score to zero

# initialize game variables before the main loop
covered = []
first_choice = None
second_choice = None
check_delay = 0  # timer for delaying match checking
score = 0

reset_game()
running = True

# main game loop - runs until player closes the window
while running:
    # draw background and add a dark overlay
    screen.blit(background, (0, 0))
    dark_overlay = pygame.Surface((screen_width, screen_height))
    dark_overlay.set_alpha(60)  # low opacity
    dark_overlay.fill((0, 0, 0))
    screen.blit(dark_overlay, (0, 0))

    # handle user interaction -> AI was used for formating and polishing this loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and check_delay == 0: # card can only be clicked after short wait time
            mouse_pos = pygame.mouse.get_pos()
            # check if clicked on a card that is covered and not matched
            for idx, card in enumerate(cards):
                if card["rect"].collidepoint(mouse_pos) and covered[idx] and not card["matched"]: # was the card clicked, covered and unmatched?
                    covered[idx] = False  # flip card face up
                    whoosh_sound.play()   # play flip sound
                    # set first or second choice and safe id
                    if first_choice is None:
                        first_choice = idx
                    elif second_choice is None and idx != first_choice:
                        second_choice = idx
                    break

    # check if two cards flipped and check if they match
    if first_choice is not None and second_choice is not None:
        check_delay += clock.get_time()
        if check_delay > 800:  # delay
            if cards[first_choice]["id"] == cards[second_choice]["id"]:
                # cards match! -> mark as matched, increase score, play success sound
                cards[first_choice]["matched"] = True
                cards[second_choice]["matched"] = True
                score += 5
                score_sound.play()
            else:
                # cards don't match! -> flip back over, deduct a point, play wrong sound
                covered[first_choice] = True
                covered[second_choice] = True
                score = max(score - 1, 0)  # score can't go below zero
                wrong_sound.play()
            # reset choices and delay timer for next turn
            first_choice = second_choice = None
            check_delay = 0

    # draw all cards, face up or covered with leaf image
    for i, card in enumerate(cards): # not covered
        screen.blit(card["img"], card["rect"].topleft)
        if covered[i]: # covered
            screen.blit(leaf_img, card["rect"].topleft)

    # draw the current score centered at the top
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 20))

    # if all cards matched, show success screen with final score
    if all(card["matched"] for card in cards):
        dark_overlay = pygame.Surface((screen_width, screen_height))
        dark_overlay.set_alpha(220)  # dark overlay
        dark_overlay.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(dark_overlay, (0, 0))

        success_text = end_font.render("SUCCESS!", True, (0, 220, 100))
        final_score_text = end_font.render(f"Final Score: {score}", True, (255, 220, 0))

        # center the success and final score messages
        screen.blit(success_text, (screen_width // 2 - success_text.get_width() // 2, screen_height // 2 - 100))
        screen.blit(final_score_text, (screen_width // 2 - final_score_text.get_width() // 2, screen_height // 2 + 10))

    pygame.display.flip()
    clock.tick(30)  # keep game running at 30 frames per second
