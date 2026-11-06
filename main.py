import asyncio
import random

import pygame

# WINDOW WIDTH, HEIGHT AND FRAME RATE PER SECOND
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
FPS = 60

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

    def update(self, dt, screen_rect):
        move_by_key = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_by_key = True
            self.rect.x -= self.speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_by_key = True
            self.rect.x += self.speed * dt
        if not move_by_key and pygame.mouse.get_pressed()[0]:
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
    last_spawn_time = pygame.time.get_ticks()
    spawn_interval = 700
    rock_list = []

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

    # GAME LOOP
    while running:
        # ----------------------INPUT------------------
        dt = clock.tick(FPS) / 1000
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --------------------------UPDATE------------------
        player1.update(dt, screen_rect)
        if now - last_spawn_time >= spawn_interval:
            width = random.randint(ROCK_MIN_SIZE, ROCK_MAX_SIZE)
            height = random.randint(ROCK_MIN_SIZE, ROCK_MAX_SIZE)
            x = random.randint(width // 2, WINDOW_WIDTH - width // 2)
            speed = random.randint(ROCK_MIN_SPEED, ROCK_MAX_SPEED)
            rock = Rock(x, 0, width, height, "grey", speed)
            rock_list.append(rock)
            last_spawn_time = now
        for rock in rock_list:
            rock.update(dt)

        for rock in rock_list[:]:
            off_the_screen = rock.is_off_the_screen(WINDOW_HEIGHT)
            if off_the_screen:
                rock_list.remove(rock)

        # --------------------------DRAW----------------------
        screen.fill("darkblue")

        player1.draw(screen)
        for rock in rock_list:
            rock.draw(screen)

        pygame.display.flip()
        await asyncio.sleep(0)
    pygame.quit()


asyncio.run(main())
