
from pygame import *
import random

width = 1000
height = 900
score = 0
max_score = 10
miss = 0
max_miss = 5


init()
window = display.set_mode((width,height))
backround = transform.scale(image.load('galaxy.jpg'), (width, height))

font.init()
font1 = font.Font(None,40)
bigfont = font.Font(None,100)


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

shootsound = mixer.Sound('fire.ogg')



clock= time.Clock()


class GameSprite(sprite.Sprite):
    def __init__ (self,player_image,x,y,width,height,speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(width,height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def update(self):
        window.blit(self.image,(self.rect.x,self.rect.y))


class Player(GameSprite):
    def movement(self):
        keys = key.get_pressed()
        if keys [K_a] and self.rect.x > self.speed: self.rect.x -= self.speed
        elif keys[K_d] and self.rect.x < width - self.rect.width: self.rect.x += self.speed


    def shoot(self):
        bullet = Bullet('bullet.png',self.rect.centerx, self.rect.top,30,30,20)
        Bullets.add(bullet)
player = Player('ufo.png',width/2,height-100,90,90,10)






class Bullet(GameSprite):
    def update(self):
        if self.rect.y <0: self.kill()
        else: self.rect.y -= self.speed
Bullets = sprite.Group()

class Enemy(GameSprite):
    def update(self):
        if self.rect.y > height:
            self.kill()
            global miss
            miss += 1
        else: self.rect.y += self.speed

Enemies = sprite.Group()


run = True
finish= False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
            quit()
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.shoot()
                shootsound.play()

    if not finish:

        window.blit(backround,(0,0))
        numScore=font1.render('Scores: '+str(score),True,(0,255,0))
        numMiss=font1.render('Misses:   '+str(miss),True,(255,0,0))
        window.blit(numMiss,(width-200,20))
        window.blit(numScore,(20,20))
        if random.randint(0,100)>98:
            enemy = Enemy('asteroid.png', random.randint(70,width)-70,-70,70,70,2)
            Enemies.add(enemy)


        player.movement()
        player.update()

        Enemies.update()
        Enemies.draw(window)

        Bullets.update()
        Bullets.draw(window)


        if sprite.groupcollide(Enemies,Bullets,True,True):
            score += 1

        if score >= max_score:
            finish = True
            win = bigfont_render('YOU WIN',True,(255,239,0))
            window.blit(win,(width/2,height/2))
        if sprite.spritecollide(player,Enemies,False) or miss > max_miss:
            finish = True
            lose = bigfont.render('YOU LOSE', True,(255,0,0))
            window.blit(lose,(width/2,height/2))

        display.update()
    else:
        for i in Bullets:
            i.kill()
        for i in Enemies:
            i.kill()
        score=0
        miss=0
        time.delay(3000)
        finish=False

    clock.tick(60)