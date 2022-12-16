import pygame
import random

from dino_runner.components.obstacles.birds import Birds
from dino_runner.components.obstacles.cactus import Cactus, Large_Cactus
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

pygame.mixer.init()
morte = pygame.mixer.Sound('/Users/fruto/Desktop/Diogenes-Turma15/dino_runner/assets/Other/morte.mp3')

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            if random.randrange(0,3) == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif random.randrange(0,3) == 1:
                self.obstacles.append(Large_Cactus(LARGE_CACTUS))
            else:
                self.obstacles.append(Birds(BIRD))
            

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up:
                    morte.play()
                    pygame.time.delay(1000)
                    game.death_count += 1
                    game.score_final()
                    game.playing = False
                    break
                else:
                    self.obstacles.remove(obstacle)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []