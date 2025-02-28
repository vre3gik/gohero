import pygame
import sys
import random

pygame.init()
width = 800
height = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Перемещение героя")

background_image = pygame.image.load("fon.jpg").convert()
background_image = pygame.transform.scale(background_image, (width, height))
player_image = pygame.image.load("mar.png").convert_alpha()
box_image = pygame.image.load("box.png").convert_alpha()
grass_image = pygame.image.load("grass.png").convert_alpha()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(center=(x, y))
        self.cell_x = x // 50
        self.cell_y = y // 50

    def move(self, dx, dy, box, grass):
        new_cell_x = self.cell_x + dx
        new_cell_y = self.cell_y + dy
        new_x = new_cell_x * 50 + 25
        new_y = new_cell_y * 50 + 25
        if new_x < 0 or new_x > width or new_y < 0 or new_y > height:
            return
        for boxx in box:
            if boxx.rect.collidepoint(new_x, new_y):
                return
        self.rect.center = (new_x, new_y)
        self.cell_x = new_cell_x
        self.cell_y = new_cell_y


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = box_image
        self.rect = self.image.get_rect(topleft=(x, y))


class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = grass_image
        self.rect = self.image.get_rect(topleft=(x, y))


def level(name):
    with open(name, "r") as file:
        lines = file.readlines()
        boxes = pygame.sprite.Group()
        grasses = pygame.sprite.Group()
        pos = []
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "#":
                    box = Box(x * 50, y * 50)
                    boxes.add(box)
                elif char == ".":
                    grass = Grass(x * 50, y * 50)
                    grasses.add(grass)
                    pos.append((x * 50 + 25, y * 50 + 25))
    return boxes, grasses, pos


if __name__ == "__main__":
    clock = pygame.time.Clock()
    boxs, grasss, pos = level("level.txt")
    start_position = random.choice(pos)
    player = Player(start_position[0], start_position[1])
    all_boxs = pygame.sprite.Group()
    all_boxs.add(boxs.sprites())
    all_boxs.add(grasss.sprites())
    all_player = pygame.sprite.Group()
    all_player.add(player)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-1, 0, boxs, grasss)
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0, boxs, grasss)
                elif event.key == pygame.K_UP:
                    player.move(0, -1, boxs, grasss)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1, boxs, grasss)
        screen.blit(background_image, (0, 0))
        all_boxs.draw(screen)
        all_player.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()
