from turtle import color, window_width
import pygame
import random
import math

pygame.init()
window=pygame.display.set_mode((750,750))
clock=pygame.time.Clock()

oldPositions=[]
dmgTaken=1


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.transform.scale(pygame.image.load("images/testomato.jpg"),(64,64))
        self.rect=self.image.get_rect()


    def move(self):


        self.rect.centerx=pygame.mouse.get_pos()[0]
        self.rect.centery=pygame.mouse.get_pos()[1]

        try: 
            if abs(pygame.mouse.get_pos()[0]-oldPositions[0][0])>20 or abs(pygame.mouse.get_pos()[1]-oldPositions[0][1])>20:
                oldPositions.insert(0,pygame.mouse.get_pos())
        except IndexError: oldPositions.insert(0,pygame.mouse.get_pos())

class PlayerFollower(pygame.sprite.Sprite):

    def __init__(self,index):
        super().__init__()
        self.image=pygame.transform.scale(pygame.image.load("images/testomato.jpg"),(64,64))
        self.rect=self.image.get_rect()
        self.index=index


    def move(self):
        
        try:
            self.rect.centerx=oldPositions[self.index][0]
            self.rect.centery=oldPositions[self.index][1]
        except IndexError: 
            self.rect.centerx=pygame.mouse.get_pos()[0]
            self.rect.centery=pygame.mouse.get_pos()[1]


enemyImages=["images/banban.jpg","images/cherift.jpg","images/keewee.webp","images/brocoi.jpg"]
class Enemy(pygame.sprite.Sprite):
    def __init__(self,type,x,y):
        super().__init__()

        if type==0:
            self.w=80
            self.h=50

        if type==1:
            self.w=32
            self.h=32
        if type==2:
            self.w=64
            self.h=70
        if type==3:
            self.w=100
            self.h=100

        self.trueimage=pygame.transform.scale(pygame.image.load(enemyImages[type]),(self.w,self.h))

        self.image=pygame.transform.scale(pygame.image.load("images/red.jpg"),(self.w,self.h))
        self.rect=self.image.get_rect()
        self.rect.move_ip(x,y)
        self.type=type
        self.dir=random.uniform(0,math.pi*2.0)
        self.speed=0.5
        self.x=x
        self.y=y
        self.timer=180

    def update(self):

        if self.timer>0:
            self.timer-=1
            return 0
        self.image=self.trueimage

        if pygame.sprite.groupcollide(pygame.sprite.GroupSingle(self),playerGroup,1,0):
            print("Collison")
            global dmgTaken
            for i in range(dmgTaken):
                for sprite in playerGroup:
                    try:
                        if sprite.index>=len(playerGroup.sprites())-2:
                            dmgTaken+=1
                            playerGroup.remove(sprite)
                    except AttributeError: ""
            
        

        if self.type==0:

            self.x+=math.cos(self.dir)*1.3
            self.y+=math.sin(self.dir)*1.3

            self.rect.center=[self.x,self.y]

        if self.type==1:
            self.x+=math.cos(self.dir)*2.2
            self.y+=math.sin(self.dir)*2.2
            self.rect.center=[self.x,self.y]

            if self.timer>-5 and (self.rect.left<0 or self.rect.top<0 or self.rect.bottom>window.get_height() or self.rect.right>window.get_width()):
                self.rect.clamp_ip(window.get_rect())
                self.timer-=1
                self.dir+=math.pi/2

        if self.type==2:
            if self.timer==-1 or self.timer%200==0:
                self.dir=math.atan2(self.rect.centery-pygame.mouse.get_pos()[1],self.rect.centerx-pygame.mouse.get_pos()[0])+math.pi
                self.speed+=0.5
            self.timer-=1
            self.x+=math.cos(self.dir)*self.speed
            self.y+=math.sin(self.dir)*self.speed
            self.rect.center=[self.x,self.y]
        
        if self.type==3:
            self.timer-=1
            if self.timer<-1500:
                self.x+=math.cos(self.dir)
                self.y+=math.sin(self.dir)
                self.rect.center=[self.x,self.y]
            

        if self.rect.x<-100 or self.rect.y<-100 or self.rect.x>window.get_width()+100 or self.rect.y>window.get_height()+100:
            enemyGroup.remove(self)
        
class Collectible(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.transform.scale(pygame.image.load("images/seed.jpg"),(self.w,self.h))



    
player=Player()

playerGroup=pygame.sprite.Group()
enemyGroup=pygame.sprite.Group()
collectibleGroup=pygame.sprite.Group()


playerGroup.add(player)

for i in range(4):
    playerGroup.add(PlayerFollower(i))

enemyGroup.add(Enemy(3,random.uniform(0,window.get_width()),random.uniform(0,window.get_height())))



game_loop=True
framespassed=0
while game_loop:
    clock.tick(60)
    framespassed+=1

    window.fill((100,100,100))

    if framespassed % int(120-(framespassed/500))==0:
        enemyToAdd=0
        if random.random()<0.07: enemyToAdd=2
        elif random.random()<0.12: enemyToAdd=1
        elif random.random()<0.15: enemyToAdd=3
        enemyGroup.add(Enemy(enemyToAdd,random.uniform(0,window.get_width()),random.uniform(0,window.get_height())))

    for sprite in playerGroup:
        sprite.move()
    
    for sprite in enemyGroup:
        sprite.update()

    playerGroup.draw(window)
    enemyGroup.draw(window)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_loop=False

pygame.quit()