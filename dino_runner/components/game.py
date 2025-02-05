import pygame

from dino_runner.components.dinosaur import Dinossauro
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DINO_START, DEFAULT_TYPE
from dino_runner.utils.text_utils import draw_message_component
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

FONT_STYLE = "freesansbold.ttf"

class Game:

    SPEED = 20
    SCORE = 0

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = self.SPEED
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.score = self.SCORE
        self.score_list = []
        self.death_count = 0
        self.player = Dinossauro()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.half_scream_width = SCREEN_HEIGHT // 2
        self.half_scream_height = SCREEN_WIDTH // 3
        
    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.playing = True
        self.score = self.SCORE
        self.game_speed = self.SPEED 
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.clear_score_final()
        while self.playing:
            self.events()
            self.update()
            self.draw()   

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.update_score()
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.score, self.game_speed, self.player)

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 1
        
    def update_score1(self):
        self.score += 100
        if self.score % 100 == 0:
            self.game_speed += 1

    def score_final(self):
        self.score_list.append(self.score)

    def clear_score_final(self):
        self.score_list = []

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255)) #Também aceita código hexadecimal "#FFFFFF"
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render(f'Pontos: {self.score}', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect_center = (950, 50)
        self.screen.blit(text, text_rect_center)

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                draw_message_component(
                    f"{self.player.type.capitalize()} habilitado para {time_to_show} segundos", self.screen, font_size = 18, pos_x_center = 500, pos_y_center = 40)
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def formatted_text(self, texto: str, posi_x: int, posi_y: int):
        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render(texto, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect_center = (self.half_scream_width - posi_x, self.half_scream_height - posi_y)
        self.screen.blit(text, text_rect_center)

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        if self.death_count == 0:
            self.formatted_text('Pressione qualquer tecla para jogar', -50, 150)
            self.screen.blit(DINO_START, (self.half_scream_width - -200, self.half_scream_height - 0))
        else:
            self.screen.blit(ICON, (self.half_scream_width - -200, self.half_scream_height - 250))
            self.formatted_text('Pressione qualquer tecla para jogar novamente', 0, 50)
            self.formatted_text(f'Quantidade de mortes: {self.death_count}', -115, -100)
            self.formatted_text(f'Sua pontuação foi de: {self.score_list[0]}', -110, -200)

        pygame.display.update()
        self.handle_events_on_menu()