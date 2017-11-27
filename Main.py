#LUNAR JUMP!
import pygame as pg
import random
import os
from Settings import *
from Sprites import *
from os import path

class Game:
    def __init__(self):
        #initialze game window
        pg.init()
        pg.mixer.init() #sound
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("LUNAR JUMP!")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        #load high score
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        #load sounds
        self.sound_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.sound_dir, 'jump.wav'))
        self.boost_sound = pg.mixer.Sound(path.join(self.sound_dir, 'boost.wav'))
        self.bow_sound = pg.mixer.Sound(path.join(self.sound_dir, 'yelp.wav'))
        self.hurt_sound = pg.mixer.Sound(path.join(self.sound_dir, 'ow.wav'))
                
    def new(self):
        #start a new game
        self.score = 0
        self.bow_score = 100
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.bows = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.enemy = pg.sprite.Group()
        self.stars = pg.sprite.Group()
        self.life = pg.sprite.Group()
        self.player = Player(self)
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
        self.enemy_timer = 0
        pg.mixer.music.load(path.join(self.sound_dir, 'intro.ogg'))
        for i in range(10):
            s = Star(self)
            s.rect.y += 500
        self.run()

    def run(self):
        #game loop
        pg.mixer.music.play(loops = -1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        #game loop - update
        self.all_sprites.update()

        #spawn an enemy?
        now = pg.time.get_ticks()
        if now - self.enemy_timer > ENEMY_FREQ + random.choice([-1000,500, 0, 500, 1000]):
            self.enemy_timer = now
            Enemy(self)

        #scrolling the window
        if self.player.rect.top <= (HEIGHT / 4):
            if random.randrange(100) < 25:
                Star(self)
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for star in self.stars:
                star.rect.y += max(abs(self.player.vel.y / 2), 2)
            for enem in self.enemy:
                enem.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
                    
        #new platforms to keep same avg
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30))
            
        #check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
                        
        #if player hits boost
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            self.boost_sound.play()
            self.player.vel.y = -BOOST_POWER
            self.player.jumping = False
            
        #if player hits bow
        bow_hits = pg.sprite.spritecollide(self.player, self.bows, True)
        for bows in bow_hits:
            self.bow_sound.play()
            self.score += self.bow_score
            self.draw_text("+ " + str(self.bow_score) + "!", 45, YELLOW, WIDTH / 2, 60)
            pg.display.flip()

        #if player hits life
        life_hits = pg.sprite.spritecollide(self.player, self.life, True)
        for l in life_hits:
            self.bow_sound.play()
            if self.player.lives < 3:
                self.player.lives += 1
            elif self.player.lives == 3:
                self.score += 50
        
        #if player hits enemies
        enem_hits = pg.sprite.spritecollide(self.player, self.enemy, True, pg.sprite.collide_mask)
        if enem_hits:
            self.hurt_sound.play()
            self.player.hide()
            self.player.lives -= 1
                        
        # Death
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
                    
        if len(self.platforms) == 0 or self.player.lives < 0:
            self.playing = False

    def events(self):
        #game loop - events
        for event in pg.event.get():
            #check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        #game loop - draw
        self.screen.fill(MIDNIGHT)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 40, YELLOW, WIDTH / 2, 15)
        self.draw_lives(self.screen, WIDTH - 100, 5, self.player.lives, self.player.life_image)
        # *after* drawing everything
        pg.display.flip()

    def show_start_screen(self):
        # game start screen
        pg.mixer.music.load(path.join(self.sound_dir, 'musicbox.ogg'))
        pg.mixer.music.play(loops = -1)
        self.screen.fill(MIDNIGHT)
        self.draw_text(TITLE, 90, HPINK, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Use  arrows  to  move  and  space  bar  to  jump.", 40, YELLOW, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Watch  out  for  items  that  will  help  your  score!", 40, YELLOW, WIDTH / 2, HEIGHT / 2 + 40)
        self.draw_text("Press  any  key  to  begin!", 40, YELLOW, WIDTH / 2, HEIGHT / 2 +80)
        self.draw_text("High  Score: " + str(self.highscore), 40, YELLOW, WIDTH / 2, 15)
        pg.display.flip()
        self.wait()
        pg.mixer.music.fadeout(500)

    def wait(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def show_go_screen(self):
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.sound_dir, 'musicbox.ogg'))
        pg.mixer.music.play(loops = -1)
        self.screen.fill(MIDNIGHT)
        self.draw_text("Game  Over!", 90, HPINK, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 40, YELLOW, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key  to  play  again!", 40, YELLOW, WIDTH / 2, HEIGHT / 2 + 80)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("New  High  Score!", 40, YELLOW, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High  Score: " + str(self.highscore), 40, YELLOW, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait()
        pg.mixer.music.fadeout(800)


    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_lives(self, surf, x, y, lives, img):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 25 * i
            img_rect.y = y
            self.screen.blit(img, img_rect)
        

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
