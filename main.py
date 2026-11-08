import asyncio
import random

import pygame

# WINDOW WIDTH, HEIGHT AND FRAME RATE PER SECOND
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
FPS = 60
RESTART_DELAY = 500

# rock global CONSTANTS
ROCK_MIN_SIZE = 10
ROCK_MAX_SIZE = 20
ROCK_MIN_SPEED = 300
ROCK_MAX_SPEED = 500


# --------------------------PLAYER CLASS------------------------
class Player:
    def __init__(self, x, y, width, height, color, speed):
        self.rect = pygame.FRect(0, 0, width, height)
        self.rect.center = (x, y)
        self.color = color
        self.speed = speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def update(self, dt, screen_rect, ignore_mouse):
        move_by_key = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_by_key = True
            self.rect.x -= self.speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_by_key = True
            self.rect.x += self.speed * dt
        if not move_by_key and not ignore_mouse and pygame.mouse.get_pressed()[0]:
            self.rect.centerx = pygame.mouse.get_pos()[0]

        self.rect.clamp_ip(screen_rect)


# ---------------------------ROCK CLASS-------------------------
class Rock:
    def __init__(self, x, y, width, height, color, speed):
        self.rect = pygame.FRect(0, 0, width, height)
        self.rect.centerx = x
        self.rect.bottom = y
        self.color = color
        self.speed = speed

    def update(self, dt):
        self.rect.y += self.speed * dt

    def is_off_the_screen(self, surface_height):
        return self.rect.top >= surface_height

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


# ----------------------------BUTTON CLASS------------------------
class Button:
    def __init__(self, x, y, width, height, bg_color):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.bg_color = bg_color

    def draw_text(self, surface, text_color, message, font):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        button_text_img = font.render(message, True, text_color)
        button_text_rect = button_text_img.get_rect(center=self.rect.center)
        surface.blit(button_text_img, button_text_rect)


async def main():
    # ------------------------SETUP----------------------------
    pygame.init()
    screen = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SCALED | pygame.RESIZABLE
    )
    pygame.display.set_caption("Dodger")
    clock = pygame.time.Clock()

    # VARIABLES
    running = True
    last_spawn_time = pygame.time.get_ticks()  # start time
    spawn_interval = 700
    rock_list = []
    game_state = "menu"  # other states are playing and gameover
    state_font = pygame.font.Font(None, 28)
    ignore_mouse = False
    gameover_time = 0

    # Score Variables
    run_start_time = 0
    current_score = 0
    best_score = 0

    # SCREEN_RECT
    screen_rect = screen.get_rect()

    # Player class OBJECT
    player_width = 50
    player_height = 20
    player_color = "orange"
    player_speed = 300  # pixels per second
    player_x = WINDOW_WIDTH // 2
    player_y = WINDOW_HEIGHT - 50
    player1 = Player(
        player_x, player_y, player_width, player_height, player_color, player_speed
    )

    # Button class OBJECTS
    menu_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 260, 50, "grey")
    gameover_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 300, 50, "grey")
    buttons = {
        "menu": menu_button,
        "gameover": gameover_button,
    }  # a dictionary used for merging repetitive if statements in the event loop

    # GAME LOOP
    while running:
        # ----------------------INPUT------------------
        dt = clock.tick(FPS) / 1000
        now = pygame.time.get_ticks()
        can_click = game_state == "menu" or now - gameover_time > RESTART_DELAY
        for event in pygame.event.get():
            active_button = buttons.get(game_state)
            if event.type == pygame.QUIT:
                running = False
            if (
                active_button is not None
                and can_click
                and event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and active_button.rect.collidepoint(event.pos)
            ):
                game_state = "playing"
                rock_list.clear()
                player1.rect.center = (player_x, player_y)
                ignore_mouse = True
                last_spawn_time = now
                run_start_time = now
                current_score = 0
        # --------------------------UPDATE------------------
        if game_state == "playing":
            current_score = (now - run_start_time) // 1000
            if not pygame.mouse.get_pressed()[0]:
                ignore_mouse = False
            player1.update(dt, screen_rect, ignore_mouse)
            if now - last_spawn_time >= spawn_interval:
                width = random.randint(ROCK_MIN_SIZE, ROCK_MAX_SIZE)
                height = random.randint(ROCK_MIN_SIZE, ROCK_MAX_SIZE)
                rock_x = random.randint(width // 2, WINDOW_WIDTH - width // 2)
                rock_speed = random.randint(ROCK_MIN_SPEED, ROCK_MAX_SPEED)
                rock = Rock(rock_x, 0, width, height, "grey", rock_speed)
                rock_list.append(rock)
                last_spawn_time = now
            for rock in rock_list:
                rock.update(dt)
                if rock.rect.colliderect(player1.rect):
                    game_state = "gameover"
                    gameover_time = now
                    best_score = max(best_score, current_score)
                    break

            for rock in rock_list[:]:
                off_the_screen = rock.is_off_the_screen(WINDOW_HEIGHT)
                if off_the_screen:
                    rock_list.remove(rock)
        # --------------------------DRAW----------------------
        screen.fill("darkblue")
        if game_state == "menu":
            menu_button.draw_text(
                screen, "black", "Welcome! Click to Play.", state_font
            )
        elif game_state in ("playing", "gameover"):
            player1.draw(screen)
            for rock in rock_list:
                rock.draw(screen)
            score_img = state_font.render(f"Score: {current_score}", True, "white")
            score_rect = score_img.get_rect(midtop=(WINDOW_WIDTH // 2, 10))
            screen.blit(score_img, score_rect)
            if game_state == "gameover":
                gameover_button.draw_text(
                    screen, "black", "Gameover! Click to play again.", state_font
                )
                best_img = state_font.render(f"Best Score: {best_score}", True, "white")
                best_rect = best_img.get_rect(
                    midtop=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
                )
                screen.blit(best_img, best_rect)

        pygame.display.flip()
        await asyncio.sleep(0)
    pygame.quit()


asyncio.run(main())
