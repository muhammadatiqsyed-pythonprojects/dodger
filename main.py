import pygame
import asyncio

WIDTH = 400
HEIGHT = 600
FPS = 60


async def main():
    # ------------------------SETUP----------------------------
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption("Dodger")
    clock = pygame.time.Clock()

    # VARIABLES
    running = True

    # GAME LOOP
    while running:
        # ----------------------INPUT------------------
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --------------------------UPDATE------------------

        # --------------------------DRAW----------------------
        screen.fill("darkblue")
        pygame.display.flip()
        await asyncio.sleep(0)
    pygame.quit()


asyncio.run(main())
