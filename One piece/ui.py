import pygame
from settings import *
from os.path import join

class Bar:
    def __init__(self, display_surface):
        self.display_surface = display_surface

    def draw_health_bar(self, current_health, max_health):
        bar_width = 200
        bar_height = 20
        bar_x = WINDOW_WIDTH - bar_width - 20
        bar_y = 20

        health_percentage = current_health / max_health
        current_bar_width = bar_width * health_percentage

        background_color = (50, 50, 50)
        border_color = (200, 200, 200)
        health_color = (255, 0, 0)

        background_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.display_surface, background_color, background_rect, border_radius=5)

        health_rect = pygame.Rect(bar_x, bar_y, current_bar_width, bar_height)
        pygame.draw.rect(self.display_surface, health_color, health_rect, border_radius=5)

        pygame.draw.rect(self.display_surface, border_color, background_rect, 3, border_radius=5)

class Menu:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        
        
        self.font_title = pygame.font.Font(None, 80)  
        self.font_main = pygame.font.Font(None, 50)  
        self.font_controls = pygame.font.Font(None, 36)  
        
        
        self.game_title = "ONE PIECE"
        self.menu_title = "Adventure"
        self.instructions = "Press SPACE to Start"
        self.controls = "WASD to Move | Mouse to Aim | Left Click to Shoot"
        
        
        self.title_color = (255, 215, 0)  
        self.text_color = (255, 255, 255)  
        self.controls_color = (200, 200, 200)  
        
        
        self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background.fill((0, 0, 0))  
        
        
        try:
            self.logo = pygame.image.load(join('One piece/images/Logo/One.png')).convert_alpha()
            self.logo = pygame.transform.scale(self.logo, (200, 200))
            self.logo_rect = self.logo.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//5))  
        except:
            self.logo = None
            print("Logo image not found, continuing without it")
        
        
        self.game_over = False
        self.final_score = 0

    def set_game_over(self, score):
        self.game_over = True
        self.final_score = score
        self.instructions = "Press SPACE to Play Again"

    def reset(self):
        self.game_over = False
        self.instructions = "Press SPACE to Start"

    def draw(self):
        
        self.display_surface.blit(self.background, (0, 0))
        
        
        if self.logo:
            self.display_surface.blit(self.logo, self.logo_rect)
        
        
        current_y = self.logo_rect.bottom + 30 if self.logo else WINDOW_HEIGHT//4
        
       
        title_surf = self.font_title.render(self.game_title, True, self.title_color)
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH//2, current_y))
        self.display_surface.blit(title_surf, title_rect)
        current_y = title_rect.bottom + 10
        
        
        menu_surf = self.font_main.render(self.menu_title, True, self.text_color)
        menu_rect = menu_surf.get_rect(center=(WINDOW_WIDTH//2, current_y))
        self.display_surface.blit(menu_surf, menu_rect)
        current_y = menu_rect.bottom + 40
        
        
        if self.game_over:
            
            game_over_surf = self.font_main.render("Game Over", True, (255, 0, 0))
            game_over_rect = game_over_surf.get_rect(center=(WINDOW_WIDTH//2, current_y))
            self.display_surface.blit(game_over_surf, game_over_rect)
            current_y = game_over_rect.bottom + 20
            
            
            score_surf = self.font_controls.render(f"Final Score: {self.final_score}", True, self.text_color)
            score_rect = score_surf.get_rect(center=(WINDOW_WIDTH//2, current_y))
            self.display_surface.blit(score_surf, score_rect)
            current_y = score_rect.bottom + 40
        
        
        instr_surf = self.font_main.render(self.instructions, True, self.text_color)
        instr_rect = instr_surf.get_rect(center=(WINDOW_WIDTH//2, current_y))
        self.display_surface.blit(instr_surf, instr_rect)
        current_y = instr_rect.bottom + 60
        
        
        ctrl_surf = self.font_controls.render(self.controls, True, self.controls_color)
        ctrl_rect = ctrl_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 50))
        self.display_surface.blit(ctrl_surf, ctrl_rect)

    def update(self):
        keys = pygame.key.get_pressed()
        return keys[pygame.K_SPACE]