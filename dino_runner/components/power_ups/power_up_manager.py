import pygame
import random

from dino_runner.components.power_ups.power_up import PowerUp
from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer

class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0

    def generate_power_up(self, score):
        if len(self.power_ups) == 0 and self.when_appears == score:
            power_ups_random = random.randint(0,1)
            if power_ups_random == 0:
                self.when_appears += random.randint(700, 800)
                self.power_ups.append(Shield())
            elif power_ups_random == 1:
                self.when_appears += random.randint(500, 600)
                self.power_ups.append(Hammer())

    def update(self, score, game_speed, player):
        self.generate_power_up(score)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if player.dino_rect.colliderect(power_up):
                power_up.start_time = pygame.time.get_ticks()
                player.shield = True
                player.hammer = True
                player.has_power_up = True
                player.type = power_up.type
                player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(200, 300)
        PowerUp.reset_time(self)