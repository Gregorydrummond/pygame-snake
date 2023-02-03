import pygame
import random
from sys import exit
from pygame.math import Vector2


class Snake:
    def __init__(self):
        # Start with a body of 3 blocks
        self.body = [Vector2(cell_number/2 + 1, cell_number/2), Vector2(
            cell_number/2, cell_number/2), Vector2(cell_number/2 - 1, cell_number/2)]
        # Direction (right)
        self.direction = Vector2(1, 0)
        # Adding a new block or not
        self.new_block = False

    def draw(self):
        for block in self.body:
            xpos = block.x * cell_size
            ypos = block.y * cell_size
            block_rect = pygame.Rect(xpos, ypos, cell_size, cell_size)
            pygame.draw.rect(screen, (232, 90, 213), block_rect)

    def move(self):
        new_body = []
        if self.new_block:
            # Copy the body
            new_body = self.body[:]
            self.new_block = False
        else:
            # Copy the body
            new_body = self.body[:-1]    # Won't copy the last element

        # Insert the new head
        new_body.insert(0, new_body[0] + self.direction)

        # Copy the new body into the old one
        self.body = new_body.copy()

    def ateFruit(self):
        self.new_block = True


class Fruit:
    def __init__(self):
        self.setRandomFruitLocation()

    def draw(self):
        fruit_rect = pygame.Rect(
            self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (147, 250, 2), fruit_rect)

    def setRandomFruitLocation(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class Game:
    def __init__(self):
        # Snake and fruit objects
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move()
        self.checkSnackEaten()
        self.checkLoss()

    def draw_elements(self):
        self.fruit.draw()
        self.snake.draw()

    def checkSnackEaten(self):
        if self.snake.body[0] == self.fruit.pos:
            # Move fruit
            self.fruit.setRandomFruitLocation()
            self.snake.ateFruit()

    def checkLoss(self):
        # Wall collision
        if not (0 <= self.snake.body[0].x < cell_number and 0 <= self.snake.body[0].y < cell_number):
            self.endGame()

        # Self collision
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.endGame()

    def endGame(self):
        pygame.quit()
        exit()


# Initialize pygame
pygame.init()

# Create a screen with dimensions
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode(
    (cell_size * cell_number, cell_size * cell_number))

# Clock object
clock = pygame.time.Clock()

# Game object
game = Game()

# Custom event (timer to move snake)
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get():
        # Exit game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == SCREEN_UPDATE:
            game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if game.snake.direction.y != 1:
                    game.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN:
                 if game.snake.direction.y != -1:
                    game.snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_LEFT:
                if game.snake.direction.x != 1:
                    game.snake.direction = Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT:
                if game.snake.direction.x != -1:
                    game.snake.direction = Vector2(1, 0)

    # Screen color
    screen.fill((215, 252, 3))

    # Draw game elements
    game.draw_elements()


    # Update graphics
    pygame.display.update()

    # FPS -> 60 Frames per second
    clock.tick(60)
