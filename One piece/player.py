import pygame
from settings import *
from os.path import join, dirname, abspath
from os import walk
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, max_health):
        super().__init__(groups)
        self.script_dir = dirname(abspath(__file__))
        self.load_images()

        self.state = 'idle'
        self.frame_index = 0
        self.animation_speed = 10

        
        try:
            self.image = pygame.image.load(join(self.script_dir, 'images', 'player', 'Left', '0.png')).convert_alpha()
        except FileNotFoundError:
            
            print("Error: Default player image 'Left/0.png' not found. Using a placeholder surface.")
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE)) 
            self.image.fill((255, 0, 255)) 

        self.rect = self.image.get_rect(center=pos)

        scale_factor = 2
        
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale_factor), int(self.image.get_height() * scale_factor)))
        self.rect = self.image.get_rect(center=pos) 

        self.hitbox_rect = self.rect.inflate(-60 * scale_factor, 0)
        self.hitbox_rect.center = self.rect.center

        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

        self.max_health = max_health
        self.current_health = max_health

    def load_images(self):
        self.frames = {
            'idle': [],
            'Left': [],
            'Right': []
        }

        
        idle_frame_path = join(self.script_dir, 'images', 'player', 'Left', '0.png')
        if os.path.exists(idle_frame_path):
            surf = pygame.image.load(idle_frame_path).convert_alpha()
            scale_factor = 1.75
            scaled_surf = pygame.transform.scale(surf, (int(surf.get_width() * scale_factor), int(surf.get_height() * scale_factor)))
            self.frames['idle'].append(scaled_surf)
        else:
            
            print(f"Warning: Idle animation frame 'Left/0.png' not found at {os.path.abspath(idle_frame_path)}")
           

        
        base_animation_path = join(self.script_dir, 'images', 'player')

        left_path = join(base_animation_path, 'Left')
        if os.path.exists(left_path):
            for _, _, files in walk(left_path):
                sorted_files = sorted(files, key=lambda name: int(name.split('.')[0]) if name.split('.')[0].isdigit() else -1)
                for file_name in sorted_files:
                    if file_name.endswith('.png'):
                        full_image_path = join(left_path, file_name)
                        try:
                            surf = pygame.image.load(full_image_path).convert_alpha()
                            scale_factor = 1.75
                            scaled_surf = pygame.transform.scale(surf, (int(surf.get_width() * scale_factor), int(surf.get_height() * scale_factor)))
                            self.frames['Left'].append(scaled_surf)
                        except pygame.error as e:
                            print(f"Error loading image {full_image_path}: {e}")
        else:
            print(f"Warning: 'Left' animation folder not found at {os.path.abspath(left_path)}")

        right_path = join(base_animation_path, 'Right')
        if os.path.exists(right_path):
            for _, _, files in walk(right_path):
                sorted_files = sorted(files, key=lambda name: int(name.split('.')[0]) if name.split('.')[0].isdigit() else -1)
                for file_name in sorted_files:
                    if file_name.endswith('.png'):
                        full_image_path = join(right_path, file_name)
                        try:
                            surf = pygame.image.load(full_image_path).convert_alpha()
                            scale_factor = 1.75
                            scaled_surf = pygame.transform.scale(surf, (int(surf.get_width() * scale_factor), int(surf.get_height() * scale_factor)))
                            self.frames['Right'].append(scaled_surf)
                        except pygame.error as e:
                            print(f"Error loading image {full_image_path}: {e}")
        else:
            print(f"Warning: 'Right' animation folder not found at {os.path.abspath(right_path)}")

    def get_state(self):
        
        if self.direction.x == 0 and self.direction.y == 0:
            return 'idle'
        elif self.direction.x < 0:
            return 'Left'
        elif self.direction.x > 0:
            return 'Right'
        return 'idle' 

    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        if keys[pygame.K_a]:
            self.direction.x = -1

        if keys[pygame.K_s]:
            self.direction.y = 1
        if keys[pygame.K_w]:
            self.direction.y = -1

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        previous_state = self.state
        self.state = self.get_state()

        if self.state != previous_state:
            self.frame_index = 0

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')

        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top

    def animate(self, dt):
        current_animation_frames = self.frames.get(self.state, [])
        if current_animation_frames:
            self.frame_index += self.animation_speed * dt
            self.image = current_animation_frames[int(self.frame_index) % len(current_animation_frames)]
        elif self.state == 'idle' and not self.frames['idle']:
           
            pass


    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)