import pygame
from random import randint, uniform
from os.path import join


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WIDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2(1, 1)
        self.speed = 500
        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def update(self, dt):
        self.fire_lazer_setup()
        self.laser_timer_setup()
        (x, y) = self.get_key_movement()
        self.direction.x = x
        self.direction.y = y
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )
        if self.rect:
            self.rect.center += self.direction * self.speed * dt
        self.check_boundary()

    def laser_timer_setup(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def get_key_movement(self):
        keys = pygame.key.get_pressed()
        x = int(keys[pygame.K_f]) - int(keys[pygame.K_s])
        y = int(keys[pygame.K_d]) - int(keys[pygame.K_e])

        return (x, y)

    def fire_lazer_setup(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.can_shoot and self.rect:
            Laser(laser_surface, self.rect.midtop, all_sprites)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

    def check_boundary(self):
        if self.rect:
            if self.rect.bottom > WIDOW_HEIGHT:
                self.rect.bottom = WIDOW_HEIGHT
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.right > WINDOW_WIDTH:
                self.rect.right = WINDOW_WIDTH
            if self.rect.left < 0:
                self.rect.left = 0


class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(
            center=(randint(0, WINDOW_WIDTH), randint(0, WIDOW_HEIGHT))
        )


class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)

    def update(self, dt):
        if self.rect:
            self.rect.centery -= 400 * dt
            if self.rect.bottom < 0:
                self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=(randint(0, WINDOW_WIDTH), 0))
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 3 * 1000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)

    def update(self, dt):
        if pygame.time.get_ticks() - self.creation_time >= self.lifetime:
            self.kill()
        if self.rect:
            self.rect.center += self.direction * self.speed * dt


# setup
WINDOW_WIDTH, WIDOW_HEIGHT = 1280, 720
pygame.init()
surface = pygame.Surface((100, 200))
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WIDOW_HEIGHT))
pygame.display.set_caption("Space shooter")
running = True
clock = pygame.time.Clock()

# import assets
star_surf = pygame.image.load(join("images", "star.png")).convert_alpha()
meteor_surface = pygame.image.load(join("images", "meteor.png")).convert_alpha()
laser_surface = pygame.image.load(join("images", "laser.png")).convert_alpha()

# asset generation
all_sprites = pygame.sprite.Group()
for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)


# custom events => meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)


while running:
    dt = clock.tick() / 1000

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surface, all_sprites)

    # update
    all_sprites.update(dt)

    # draw the game
    display_surface.fill("darkgray")
    all_sprites.draw(display_surface)
    pygame.display.update()

pygame.quit()
