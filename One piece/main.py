import pygame
from os.path import join
import os
from os import walk
from settings import *
from player import Player
from Sprites import CollisionSprite, Sprite, Gun, Bullet, Enemy
from groups import AllSprites
from pytmx.util_pygame import load_pygame
from random import choice
from ui import Bar, Menu

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.mouse.set_visible(True)

        self.clock = pygame.time.Clock()
        self.running = True
        self.game_active = False

        self.menu = Menu(self.display_surface)
        self.load_assets()
        self.set_window_properties()

        self.all_sprites = None
        self.collision_sprites = None
        self.bullet_sprites = None
        self.enemy_sprites = None

        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 200

        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)
        self.spawn_positions = []

        self.player_max_health = 100
        self.player_current_health = self.player_max_health
        self.player_hit_cooldown = 1000
        self.last_hit_time = 0

        self.score = 0
        pygame.font.init()
        self.font = pygame.font.Font(None, 40)

    def set_window_properties(self):
        icon_path = os.path.join('One piece/images/Logo/One.png')
        try:
            icon = pygame.image.load(icon_path)
            pygame.display.set_icon(icon)
            pygame.display.set_caption('One Piece')
        except pygame.error as e:
            print(f"Warning: Could not load icon at {os.path.abspath(icon_path)}: {e}")
            pygame.display.set_caption('One Piece (No Icon)')

    def load_assets(self):
        self.load_images()
        self.load_audio()

    def load_audio(self):
        self.shoot_sound = pygame.mixer.Sound(join('One piece/audio/shoot.wav'))
        self.shoot_sound.set_volume(0.4)
        self.impact_sound = pygame.mixer.Sound(join('One piece/audio/impact.ogg'))
        self.music = pygame.mixer.Sound(join('One piece/audio/1.ogg'))
        self.music.set_volume(0.3)
        self.music.play(loops=-1)

    def load_images(self):
        bullet_image_path = os.path.join('One piece', 'images', 'gun', 'bullet.png')
        try:
            self.bullet_surf = pygame.image.load(bullet_image_path).convert_alpha()
        except pygame.error as e:
            print(f"Error: Could not load bullet image at {os.path.abspath(bullet_image_path)}: {e}")
            self.bullet_surf = pygame.Surface((10, 5)).convert_alpha()
            self.bullet_surf.fill('red')

        folders = list(walk(join('One piece', 'images', 'enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            folder_path = join('One piece', 'images', 'enemies', folder)
            self.enemy_frames[folder] = []
            for file_name in sorted(os.listdir(folder_path), key=lambda name: int(name.split('.')[0])):
                if file_name.endswith('.png'):
                    full_path = join(folder_path, file_name)
                    try:
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.enemy_frames[folder].append(surf)
                    except pygame.error as e:
                        print(f"Warning: Could not load enemy image {file_name} from {folder_path}: {e}")

    def start_game(self):
        self.game_active = True
        pygame.mouse.set_visible(False)

        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        self.can_shoot = True
        self.shoot_time = 0
        self.score = 0
        self.player_current_health = self.player_max_health
        self.last_hit_time = 0

        self.setup_level()
        self.ui = Bar(self.display_surface)

    def process_input(self):
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and self.can_shoot:
            self.shoot_sound.play()
            if self.gun and hasattr(self.gun, 'player_direction'):
                bullet_spawn_pos = self.gun.rect.center
                bullet_direction = self.gun.player_direction

                if hasattr(self, 'bullet_surf') and self.bullet_surf:
                    Bullet(self.bullet_surf, bullet_spawn_pos, bullet_direction, (self.all_sprites, self.bullet_sprites))
                    self.can_shoot = False
                    self.shoot_time = pygame.time.get_ticks()

    def handle_gun_cooldown(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

    def setup_level(self):
        map_path = os.path.join(os.path.dirname(__file__), 'data', 'maps', 'world.tmx')
        try:
            self.tmx_data = load_pygame(map_path)
        except Exception as e:
            print(f"CRITICAL ERROR: Could not load TMX map: {e}")
            self.running = False
            return

        if not hasattr(self, 'tmx_data') or self.tmx_data is None:
            return

        for x, y, image in self.tmx_data.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in self.tmx_data.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in self.tmx_data.get_layer_by_name('Collisions'):
            collision_surf = pygame.Surface((obj.width, obj.height), pygame.SRCALPHA)
            CollisionSprite((obj.x, obj.y), collision_surf, self.collision_sprites)

        for obj in self.tmx_data.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player_max_health)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x, obj.y))

    def handle_bullet_collision(self):
        if self.bullet_sprites and self.enemy_sprites:
            for bullet in self.bullet_sprites:
                hit_enemies = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if hit_enemies:
                    self.impact_sound.play()
                    for enemy in hit_enemies:
                        if enemy.death_time == 0:
                            enemy.destroy()
                            self.score += 10
                    bullet.kill()

    def handle_player_collision(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > self.player_hit_cooldown:
            colliding_enemies = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask)
            active_colliding_enemies = [enemy for enemy in colliding_enemies if enemy.death_time == 0]

            if active_colliding_enemies:
                self.player_current_health -= 10
                self.last_hit_time = current_time

                if self.player_current_health <= 0:
                    self.menu.set_game_over(self.score)
                    self.game_active = False
                    pygame.mouse.set_visible(True)

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event and self.game_active:
                    if self.enemy_frames and self.spawn_positions:
                        Enemy(choice(self.spawn_positions), choice(list(self.enemy_frames.values())),
                              (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)

            if not self.game_active:
                self.menu.draw()
                pygame.display.update()

                if self.menu.update():
                    self.start_game()
            else:
                self.handle_gun_cooldown()
                self.process_input()
                self.all_sprites.update(dt)
                self.handle_bullet_collision()
                self.handle_player_collision()

                self.display_surface.fill('black')
                if self.player:
                    self.all_sprites.draw(self.player.rect.center)
                else:
                    self.all_sprites.draw(pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

                if self.player:
                    self.ui.draw_health_bar(self.player_current_health, self.player_max_health)

                score_text_surf = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
                score_text_rect = score_text_surf.get_rect(topleft=(20, 20))
                self.display_surface.blit(score_text_surf, score_text_rect)

                pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()