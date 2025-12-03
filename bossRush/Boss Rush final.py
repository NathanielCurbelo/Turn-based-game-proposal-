import pygame
import random

pygame.init()

clock = pygame.time.Clock()
fps= 50

#window
bottomMenu= 350
screenWidth = 2000
screenHeight= 1000+ bottomMenu

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('battlel')

#game variables
currentTurn=1
totalFighter=2
actionCooldown= 0
actionWaitTime=90
attack = False
potion = False
clicked = False

#font
font = pygame.font.SysFont('Times New Roman',50)

#colors
white= (255,255,255)
red= (255,0,0)
green= (0,255,0)

#images
battle1= pygame.image.load('img/backgrounds/graveyard.jpg').convert_alpha()
battle1= pygame.transform.scale(battle1, (screenWidth,screenHeight-bottomMenu))

#bottom menu
menuPic= pygame.image.load('img/menu/battleMenu.png').convert_alpha()
menuPic= pygame.transform.scale(menuPic, (screenWidth,bottomMenu))

#cursor
mousePic= pygame.image.load('img/menu/mouse.png').convert_alpha()

#draw text function
def draw_text(text,font,text_col,x,y):
    img= font.render(text,True,text_col)
    screen.blit(img,(x,y))
    
#function for backgrounds
def draw_b1():
    screen.blit(battle1,(0,0))
    
#function for drawing bottom menu
def draw_botMenu():
    #drawing menu
    screen.blit(menuPic,(0,screenHeight-bottomMenu))
    #healer stats
    draw_text(f'{healer.name} HP: {healer.hp}',font,white,100,0)
    #mob skully
    draw_text(f'{skully.name} HP: {skully.hp}',font,red,1600,0)
    
#healer class
class healer():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0#0:idle, 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()
        #load idle images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/{self.name}/idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load attack images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/{self.name}/physical/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/{self.name}/magic/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)


    def update(self):
        animation_cooldown = 200
	#handle animation
	#update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            #if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.idle()
            
    def idle(self):
        #set variables to attack animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

            
    def attack(self, target):
        #dmg
        ran= random.randint(-5,5)
        damage= self.strength + ran
        target.hp = target.hp - damage
        #check if death
        if target.hp<1:
            target.hp = 0
            target.alive =False
        #set variables to attack
        self.action=1
        self.frame_index=0
        self.update_time = pygame.time.get_ticks()
        
    def magic(self, target):
        #dmg
        ran= random.randint(-5,5)
        damage= self.strength + ran
        target.hp = target.hp - damage
        #check if death
        if target.hp<1:
            target.hp = 0
            target.alive =False
        #set variables to attack
        self.action=2
        self.frame_index=0
        self.update_time = pygame.time.get_ticks()
        
    def heal(self, target):
        #check if death
        if target.hp<=0:
            target.hp=1
        else:
            #dmg
            ran= random.randint(-5,5)
            damage= self.strength + ran
            target.hp = target.hp + damage
            if target.hp>self.max_hp:
                target.hp= self.max_hp
        
        #set variables to attack
        self.action=2
        self.frame_index=0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)
        

#skully class
class skully():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0#0:idle, 1:attack, 2:hurt, 3:magic
        self.update_time = pygame.time.get_ticks()
        #load idle images
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'img/{self.name}/idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.5, img.get_height() * 1.5))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load attack images
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'img/{self.name}/Atk/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.5, img.get_height() * 1.5))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update(self):
        animation_cooldown = 200
	#handle animation
	#update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            #if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            self.idle()
            
    def idle(self):
        #set variables to attack animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

            
    def attack(self, target):
        #dmg
        ran= random.randint(-5,5)
        damage= self.strength + ran
        target.hp = target.hp - damage
        #check if death
        if target.hp<1:
            target.hp = 0
            target.alive =False
        #set variables to attack
        self.action=1
        self.frame_index=0
        self.update_time = pygame.time.get_ticks()
        self.rect.x -=80
        self.rect.x +=80

    def draw(self):
        screen.blit(self.image, self.rect)

        
class HealthBar():
	def __init__(self, x, y, hp, max_hp):
		self.x = x
		self.y = y
		self.hp = hp
		self.max_hp = max_hp


	def draw(self, hp):
		#update with new health
		self.hp = hp
		#calculate health ratio
		ratio = self.hp / self.max_hp
		pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))

healer = healer(200, 740, 'Healer', 100, 10, 3)
skully = skully(700,710,'skully',100,6,1)

healer_health_bar = HealthBar(425, 20, healer.hp, healer.max_hp)
skully_health_bar = HealthBar(1440, 20, skully.hp, skully.max_hp)
    
#game loop
run= True
while run:
    
    #fps
    clock.tick(fps)
    
    #drawing background 
    draw_b1()
    #drawing bottom menu
    draw_botMenu()
    healer_health_bar.draw(healer.hp)
    skully_health_bar.draw(skully.hp)

    #unit drawing
    healer.update()
    healer.draw()
    
    skully.update()
    skully.draw()

    #control player actions 
    #reset action variables
    attack = False
    potion = False
    target = None
    pos = pygame.mouse.get_pos()

    #player action
    if healer.alive == True:
        if currentTurn == 1:
            menuPic= pygame.image.load('img/menu/healermenu.png').convert_alpha()
            menuPic= pygame.transform.scale(menuPic, (screenWidth,bottomMenu))
            
            actionCooldown += 1
            if actionCooldown >= actionWaitTime:
            #look for player action
            #attack
                healer.heal(healer)
                currentTurn += 1
                actionCooldown = 0


    if skully.alive == True:
        if currentTurn == 2:
            actionCooldown += 1
            if actionCooldown >= actionWaitTime:
            #look for player action
            #attack
                skully.attack(healer) 
                currentTurn += 1
                actionCooldown = 0

	#if all fighters have had a turn then reset
        if currentTurn > totalFighter:
            currentTurn = 1

    
    
    
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            run = False
    pygame.display.update()
        
pygame.quit()
