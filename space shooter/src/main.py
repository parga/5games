import pygame
from random import randint
from os.path import join


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WIDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2(1, 1)
        self.speed = 300

    def update(self):
        (x, y) = self.get_key_movement();
        self.direction.x = x
        self.direction.y = y
        self.direction= self.direction.normalize() if self.direction else self.direction 
        if self.rect:
            self.rect.center += self.direction * self.speed * dt
        self.check_boundary()

    def get_key_movement(self):
        keys = pygame.key.get_pressed()
        x = int(keys[pygame.K_f]) - int(keys[pygame.K_s])
        y = int(keys[pygame.K_d]) - int(keys[pygame.K_e])

        return (x, y)

    def fire_lazer_setup(self):
        keys = pygame.key.get_just_pressed()

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
        self.rect = self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WIDOW_HEIGHT))) 

# setup
WINDOW_WIDTH, WIDOW_HEIGHT = 1280, 720
pygame.init()
surface = pygame.Surface((100, 200))
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WIDOW_HEIGHT))
pygame.display.set_caption("Space shooter")
running = True
clock = pygame.time.Clock()


# asset generation 
all_sprites = pygame.sprite.Group()
star_surf = pygame.image.load(join("images", "star.png")).convert_alpha()
for i in range(20):
   Star(all_sprites, star_surf) 
player = Player(all_sprites)

meteor_surface = pygame.image.load(join("images", "meteor.png")).convert_alpha()
meteor_rectangle = meteor_surface.get_frect(center=(WINDOW_WIDTH / 2, WIDOW_HEIGHT / 2))

laser_surface = pygame.image.load(join("images", "laser.png")).convert_alpha()
laser_rectangle = laser_surface.get_frect(center=(WINDOW_WIDTH / 2, WIDOW_HEIGHT / 2))


while running:
    dt = clock.tick() / 1000

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update
    all_sprites.update()

    # draw the game
    display_surface.fill("darkgray")
    all_sprites.draw(display_surface)
    pygame.display.update()

pygame.quit()
