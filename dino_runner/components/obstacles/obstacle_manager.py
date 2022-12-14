import pygame
import random

from dino_runner.components.obstacles.birds import Birds
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD


class ObstacleManager:
    def __init__(self):
        self.step_index = 0
        self.image = BIRD
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            self.number = random.randrange(0,3)
#self.image = self.obstacles.append(Cactus(SMALL_CACTUS)) if self.step_index < 2 else self.obstacles.append(Cactus(LARGE_CACTUS))
            if self.number == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif self.number == 1:
                self.obstacles.append(Cactus(LARGE_CACTUS))
            elif self.number == 2:
                self.obstacles.append(Birds(BIRD))
                #self.image = self.obstacles.append(Birds(BIRD[0])) if self.step_index < 5 else self.obstacles.append(Birds(BIRD[1]))
        if self.step_index >= 10:
            self.step_index = 0
            

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(1000)
                game.playing = False
                break

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)