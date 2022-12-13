import pygame
from dino_runner.utils.constants import RUNNING, JUMPING

X_POS = 80
Y_POS = 310

class Dinossauro:
    def __init__(self):
        self.image = RUNNING[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS
        self.step_index = 0
        self.dino_run = True
        self.dino_jump = False
        self.jump_vel = 8.5

    def update(self):
        if self.dino_run:
            self.run()
        
        if self.dino_jump:
            self.jump()
            
        if self.step_index >= 10:
            self.step_index = 0

    def jump(self):
        self.image = JUMPING
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4

    def run(self):
        self.image = RUNNING[0] if self.step_index < 5 else RUNNING[1]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS
        self.step_index += 1

    def draw(self, scream: pygame.Surface):
        scream.blit(self.image, (self.dino_rect.x, self.dino_rect.y))