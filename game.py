"""the ninth life."""

import pygame
import sys
import random
import os

print(os.getcwd())

from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2

font = pygame.font.SysFont("Arial", 14)

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
r = 255
g = 255
b = 255
gamestate = False
ending_start_time = None
ending_delay = False
background_m = pygame.mixer.Sound("/Users/jakemajor/HACK 110/hack110-super-awesome-team-name/hack110-super-awesome-team-name/assets/lavendar.mp3")
blackout_m = pygame.mixer.Sound("/Users/jakemajor/HACK 110/hack110-super-awesome-team-name/hack110-super-awesome-team-name/assets/fnaf-power-outage-gaming-sound-effect-(hd)-made-with-Voicemod.mp3")
shake_m = pygame.mixer.Sound("/Users/jakemajor/HACK 110/hack110-super-awesome-team-name/hack110-super-awesome-team-name/assets/something-sound-effect-omori.mp3")
score = 0
FramePerSec = pygame.time.Clock()
score_explode = False

pygame.mixer.music.load("/Users/jakemajor/HACK 110/hack110-super-awesome-team-name/hack110-super-awesome-team-name/assets/lavendar.mp3")
pygame.mixer.music.play(-1)


displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("the ninth life.")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load('assets/images/idle.png').convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (35, 35))
        self.rect = self.surf.get_rect()
        self.jumping = False
        self.speed = 5

        self.pos = vec((10, 325))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        self.prev_pos_y = self.pos.y #helps store previous v position
    
    def move(self):
        self.prev_pos_y = self.pos.y
        
        self.acc = vec(0,0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
        
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

# ensures player can't go off screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        
        self.rect.midbottom = self.pos

# collision + gravity in relation to platforms
    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        # eleminates infinite jumping
        if P1.vel.y > 0:
            if hits:
                self.surf = pygame.image.load('assets/images/idle.png').convert_alpha()
                self.surf = pygame.transform.scale(self.surf, (35, 35))
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0
        # only collide when moving DOWN, 
        # prevents jumping through platforms
        if self.vel.y > 0:
            # checks if player's feet were above platform before fall
            for plat in hits:
                if self.rect.bottom <= plat.rect.top + self.vel.y:
                    self.pos.y = plat.rect.top + 1
                    self.vel.y = 0

    
    def jump(self):
        global score
        hits = pygame.sprite.spritecollide(self,platforms, False)
        # eleminates infinite jumping
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -20
            self.surf = pygame.image.load("assets/images/jump.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (35, 35))
            update_background()
            score += 30
        
    
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
        self.jumping = False
    

class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.surf = pygame.Surface((random.randint(50,100), 15))
        #self.surf.fill((0,0,0))
        rock1 = pygame.image.load("assets/images/rock_1.png").convert_alpha()
        rock2 = pygame.image.load("assets/images/rock_2.png").convert_alpha()
        deadcat = pygame.image.load("assets/images/dead_cat.png").convert_alpha()

        rock1 = pygame.transform.smoothscale_by(rock1, 0.4)
        rock2 = pygame.transform.smoothscale_by(rock2, 0.4)
        deadcat = pygame.transform.smoothscale_by(deadcat, 0.3)

        platform_assets = [rock1, rock2, deadcat]
        weights = [6, 6, 1]
        self.surf = random.choices(platform_assets, weights=weights, k=1)[0]
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10),random.randint(0, HEIGHT-30)))
    
def plat_gen():
    attempts = 0
    while len(platforms) < 5:
        width = random.randrange(50,100)
        p = platform()
        C = True

        while C and attempts < 10:
            p = platform()
            p.rect.center = (random.randrange(0, WIDTH - width), random.randrange(-50,0))
            C = check(p, platforms)
            attempts += 1
        platforms.add(p)
        all_sprites.add(p)

def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 105) and (abs(platform.rect.bottom - entity.rect.top) < 105):
                return True
        return False   # <-- IMPORTANT

def update_background():
    global r, g, b, gamestate, ending_start_time, ending_delay, score_explode
    if r - 5.1 >= 0 and g - 9.46 >= 0 and b - 9.37 >=0:
        r -= 6.1
        g -= 8.46
        b -= 8.37
    else:
        r = 0
        b = 0
        g = 0
        pygame.mixer.music.stop()
        if not gamestate:
            score_explode = True
            pygame.mixer.music.load("/Users/jakemajor/HACK 110/hack110-super-awesome-team-name/hack110-super-awesome-team-name/assets/fnaf-power-outage-gaming-sound-effect-(hd)-made-with-Voicemod.mp3")
            pygame.mixer.music.play(-1)
            gamestate = True
            ending_start_time = pygame.time.get_ticks()
            ending_delay = True

    displaysurface.fill((r,g,b))
    pygame.display.update()

def ending():
    shake_m.play()
    target = pygame.math.Vector2(400/2, 450/2)
    direction = target - P1.pos

    for plat in platforms:
        plat.kill()

    if direction.length() != 0:
        direction = direction.normalize()  # unit vector
        P1.pos += direction * P1.speed
        P1.rect.center = P1.pos



            

PT1 = platform()
P1 = Player()

PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((0,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))


all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

for x in range(random.randint(4,6)):
    pl = platform()
    platforms.add(pl)
    all_sprites.add(pl)



while True:
    
    score_text = font.render(f"Score: {score}", True, (255,255,255))
    displaysurface.blit(score_text, (10,10))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_UP:
                P1.jump()
            if event.key == K_LEFT:
                P1.surf = pygame.image.load("/Users/jakemajor/HACK 110/hack110-super-awesome-team-name/hack110-super-awesome-team-name/assets/images/left.png").convert_alpha()
                P1.surf = pygame.transform.scale(P1.surf, (35, 35))
            if event.key == K_RIGHT:
                P1.surf = pygame.image.load("/Users/jakemajor/HACK 110/hack110-super-awesome-team-name/hack110-super-awesome-team-name/assets/images/right.png").convert_alpha()
                P1.surf = pygame.transform.scale(P1.surf, (35, 35))
                

        if event.type == KEYUP:
            if event.key == pygame.K_UP:
                P1.cancel_jump()
            if event.key == K_LEFT:
                P1.surf = pygame.image.load("/Users/jakemajor/HACK 110/hack110-super-awesome-team-name/hack110-super-awesome-team-name/assets/images/left.png").convert_alpha()
                P1.surf = pygame.transform.scale(P1.surf, (35, 35))
            if event.key == K_RIGHT:
                P1.surf = pygame.image.load("/Users/jakemajor/HACK 110/hack110-super-awesome-team-name/hack110-super-awesome-team-name/assets/images/left.png").convert_alpha()
                P1.surf = pygame.transform.scale(P1.surf, (35, 35))


            
    
    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
    
    if gamestate:
       
        if score_explode:
            score = random.randint(0,1000)
            shake = random.randint(-3,3)
            score_text = font.render(f"Score: {score}", True, (255,255,255))
            displaysurface.blit(score_text, (10 + shake, 10 + shake))

        time_passed = pygame.time.get_ticks() - ending_start_time 
        if ending_delay and time_passed >= 5000:
            ending_delay = False
        if not ending_delay:
            ending()

            if pygame.time.get_ticks() - ending_start_time >= 10000:
                pygame.quit()
                sys.exit
    else:
        P1.move()
        P1.update()
        plat_gen()
    
    if P1.rect.top > HEIGHT:
        for n in range(0,20):
            displaysurface.fill((45,9,18))
            pygame.display.update()
            displaysurface.fill((0,0,0))
            pygame.display.update()
        pygame.quit()
    pygame.display.flip()
    

    displaysurface.fill((r,g,b))

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
    
    pygame.display.update()
    FramePerSec.tick(FPS)


