import pygame
from settings import *
from math import atan2, degrees 
from os.path import join 
import os 

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.ground = True

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        self.player = player 
        self.distance = 140
        self.player_direction = pygame.Vector2(0,1)

        super().__init__(groups)
        self.gun_surf = pygame.image.load(join('One piece', 'images', 'gun', 'gun.png')).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_rect(center = self.player.rect.center + self.player_direction * self.distance) 
    
    def get_direction(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pos = pygame.Vector2(mouse_x, mouse_y)
        
        player_screen_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        
        self.player_direction = (mouse_pos - player_screen_pos).normalize()
        
    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.y, self.player_direction.x)) 
        self.image = pygame.transform.rotozoom(self.gun_surf, -angle, 1)

    def shoot(self):
        print("shoot")
            
    def update(self, _):
        self.get_direction()
        self.rotate_gun() 
        self.rect.center = self.player.rect.center + self.player_direction * self.distance

class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_rect(center = pos)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000

        self.direction = direction.normalize() if direction.magnitude() > 0 else pygame.Vector2(0, -1) 
        self.speed = 1000 

        if self.direction.magnitude() > 0:
            angle = degrees(atan2(self.direction.y, self.direction.x))
            self.image = pygame.transform.rotozoom(self.image, -angle, 1)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt

        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill() 

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player

        self.frames = frames
        self.frame_index = 0
        
        self.image = self.frames[self.frame_index] 
        self.animation_speed = 6

        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-20,-40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 300

        self.death_time = 0
        self.death_duration = 400

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def move(self, dt):
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        
        direction_to_player = player_pos - enemy_pos

        if direction_to_player.magnitude() > 0:
            self.direction = direction_to_player.normalize()
        else:
            self.direction = pygame.Vector2(0, 0)
            
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    def destroy(self):
        self.death_time = pygame.time.get_ticks()
        surf = pygame.mask.from_surface(self.frames[0]).to_surface()
        surf.set_colorkey('black')
        self.image = surf

    def death_timer(self):
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill()

    def update(self, dt):
        if self.death_time == 0:
            self.move(dt)
            self.animate(dt)
        else:
            self.death_timer()