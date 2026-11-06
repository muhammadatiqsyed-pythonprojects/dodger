import pygame
import asyncio


# WINDOW WIDTH, HEIGHT AND FRAME RATE PER SECOND
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
FPS = 60


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

    # SCREEN_RECT
    screen_rect = screen.get_rect()

    # Player class OBJECT
    player_width = 50
    player_height = 20
    player_color = "orange"
    player_speed = 300
    player_x = WINDOW_WIDTH // 2
    player_y = WINDOW_HEIGHT - 50
    player1 = Player(
        player_x, player_y, player_width, player_height, player_color, player_speed
    )

    # GAME LOOP
    while running:
        # ----------------------INPUT------------------
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --------------------------UPDATE------------------

        player1.update(dt, screen_rect)

        # --------------------------DRAW----------------------
        screen.fill("darkblue")

        player1.draw(screen)

        pygame.display.flip()
        await asyncio.sleep(0)
    pygame.quit()


asyncio.run(main())
