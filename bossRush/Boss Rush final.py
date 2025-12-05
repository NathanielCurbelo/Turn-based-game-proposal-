import pygame
import random
import os

pygame.init()

clock = pygame.time.Clock()
fps = 50

# WINDOW SETUP
bottomMenu = 350
screenWidth = 2000
screenHeight = 1000 + bottomMenu

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('battlel')

# GAME VARIABLES
currentTurn = 1
totalFighter = 2
actionCooldown = 0
actionWaitTime = 90
clicked = False
currentMob="no one"

# FONT
font = pygame.font.SysFont('Times New Roman', 50)

# COLORS
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# IMAGES
battle1 = pygame.image.load('img/backgrounds/graveyard.jpg').convert_alpha()
battle1 = pygame.transform.scale(battle1, (screenWidth, screenHeight - bottomMenu))

battle2 = pygame.image.load('img/backgrounds/gamble.png').convert_alpha()
battle2 = pygame.transform.scale(battle2, (screenWidth, screenHeight - bottomMenu))

menuPic = pygame.image.load('img/menu/battleMenu.png').convert_alpha()
menuPic = pygame.transform.scale(menuPic, (screenWidth, bottomMenu))

attack_icon = pygame.image.load('img/skill/physical.png').convert_alpha()
attack_icon = pygame.transform.scale(attack_icon, (200, 200))

heal_icon   = pygame.image.load('img/skill/heal.png').convert_alpha()
heal_icon = pygame.transform.scale(heal_icon, (200, 200))

magic_icon  = pygame.image.load('img/skill/magic.png').convert_alpha()
magic_icon = pygame.transform.scale(magic_icon, (200, 200))

shield_icon  = pygame.image.load('img/skill/shield.png').convert_alpha()
shield_icon = pygame.transform.scale(shield_icon, (200, 200))

# TEXT DRAWING
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# BACKGROUNDS
def draw_b1():
    screen.blit(battle1, (0, 0))
def draw_b2():
    screen.blit(battle2, (0, 0))
    

# BOTTOM MENU
def draw_botMenu():
    screen.blit(menuPic, (0, screenHeight - bottomMenu))
    draw_text(f'{healer.name} HP: {healer.hp}', font, white, 100, 0)
    draw_text(f'{skully.name} HP: {skully.hp}', font, red, 1600, 0)

def drawround2():
    draw_text(f'{healer.name} HP: {healer.hp}', font, white, 100, 0)
    draw_text(f'{skully.name} HP: {Allyskully.hp}', font, green, 100, 50)
    draw_text(f'{mobMagican.name} HP: {mobMagican.hp}', font, red, 1600, 0)

# BUTTON CLASS
class Button():
    def __init__(self, x, y, image, scale, action=None):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.action = action

    def draw(self, surface):
        action_triggered = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action_triggered = True
                if self.action:
                    self.action()

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action_triggered

# HEALER CLASS
class healer():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.shielded = False

        # idle animation
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/{self.name}/idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # attack animation
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/{self.name}/physical/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # magic animation
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/{self.name}/magic/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 200
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # Check shield
        if target.shielded:
            dmg = (self.strength + random.randint(10, 20)) // 2
            target.shielded = False
        else:
            dmg = self.strength + random.randint(10, 20)

        # Apply damage
        target.hp -= dmg
        if target.hp <= 0:
            target.hp = 0
            target.alive = False

        # Play attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def magic(self, target):
        # Check shield
        if target.shielded:
            dmg = (self.strength + random.randint(10, 20)) // 2
            target.shielded = False
        else:
            dmg = self.strength + random.randint(10, 20)

        # Apply damage
        target.hp -= dmg
        if target.hp <= 0:
            target.hp = 0
            target.alive = False

        # Play magic animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def heal(self, target):
        heal_amount = self.strength + random.randint(50, 100)
        target.hp += heal_amount

        if target.hp > self.max_hp:
            target.hp = self.max_hp
        if target.hp <= 0:
            target.hp = 1

        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def shield(self, target):
        # Set a shield flag on the target
        target.shielded = True  # this must exist on the target
        # Play shield/magic animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def draw(self):
        screen.blit(self.image, self.rect)

# SKULLY CLASS
class skully():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.shielded = False

        # idle animation
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'img/{self.name}/idle/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width()*1.5), int(img.get_height()*1.5)))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # attack animation
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'img/{self.name}/Atk/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width()*1.5), int(img.get_height()*1.5)))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 200
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # Check shield
        if target.shielded:
            dmg = (self.strength + random.randint(10, 20)) // 2
            target.shielded = False
        else:
            dmg = self.strength + random.randint(10, 20)

        # Apply damage
        target.hp -= dmg
        if target.hp <= 0:
            target.hp = 0
            target.alive = False

        # Play attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)

# ALLYSKULLY CLASS
class Allyskully():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.potions = potions
        self.alive = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.shielded = False

        # idle animation
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'img/{self.name}/idle/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width()*1.5), int(img.get_height()*1.5)))
            img= pygame.transform.flip(img, True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # attack animation
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'img/{self.name}/Atk/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width()*1.5), int(img.get_height()*1.5)))
            img= pygame.transform.flip(img, True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 200
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # Check shield
        if target.shielded:
            dmg = (self.strength + random.randint(10, 20)) // 2
            target.shielded = False
        else:
            dmg = self.strength + random.randint(10, 20)

        # Apply damage
        target.hp -= dmg
        if target.hp <= 0:
            target.hp = 0
            target.alive = False

        # Play attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)

# MAGICAN CLASS
class Magican():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.shielded = False

        # idle animation
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/{self.name}/idle/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width()*1.5), int(img.get_height()*1.5)))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # attack animation
        #temp_list = []
        #for i in range(5):
           # img = pygame.image.load(f'img/{self.name}/Atk/{i}.png')
            #img = pygame.transform.scale(img, (int(img.get_width()*1.5), int(img.get_height()*1.5)))
           # temp_list.append(img)
        #self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 200
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # Check shield
        if target.shielded:
            dmg = (self.strength + random.randint(10, 20)) // 2
            target.shielded = False
        else:
            dmg = self.strength + random.randint(10, 20)

        # Apply damage
        target.hp -= dmg
        if target.hp <= 0:
            target.hp = 0
            target.alive = False

        # Play attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)

# MOBMAGICAN CLASS
class MobMagican():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.potions = potions
        self.alive = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.shielded = False

        # idle animation
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/{self.name}/idle/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width()*1.5), int(img.get_height()*1.5)))
            img= pygame.transform.flip(img, True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # attack animation
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'img/{self.name}/magic/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width()*1.5), int(img.get_height()*1.5)))
            temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 200
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # Check shield
        if target.shielded:
            dmg = (self.strength + random.randint(10, 20)) // 2
            target.shielded = False
        else:
            dmg = self.strength + random.randint(10, 20)

        # Apply damage
        target.hp -= dmg
        if target.hp <= 0:
            target.hp = 0
            target.alive = False

        # Play attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)


# HEALTH BAR CLASS
class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        self.hp = hp
        ratio = self.hp / self.max_hp

        pygame.draw.rect(screen, red,   (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))

#CREATE CHARACTERS
healer = healer(200, 740, 'Healer', 100, 6, 1)
skully = skully(700, 710, 'skully', 100, 6, 1)
Allyskully= Allyskully(700, 710, 'Allyskully', 100, 6, 1)
magican= Magican(700,710, 'magican',100,6,1)
mobMagican= MobMagican(1250,600, 'magican',100,6,1)

healer_health_bar = HealthBar(425, 20, healer.hp, healer.max_hp)
skully_health_bar = HealthBar(1440, 20, skully.hp, skully.max_hp)
Allyskully_health_bar = HealthBar(425, 70, Allyskully.hp, Allyskully.max_hp)
mobMagican_healthBar = HealthBar(1440, 20, mobMagican.hp, skully.max_hp)

# CREATE SKILL BUTTONS 

# Attack button
def attack_action():
    healer.attack(currentMob)

attack_button = Button(200, screenHeight - bottomMenu + 40, attack_icon, 1, attack_action)

# Heal button
def heal_action():
    healer.heal(healer)

heal_button = Button(450, screenHeight - bottomMenu + 40, heal_icon, 1, heal_action)

# Magic button
def magic_action():
    healer.magic(currentMob)

magic_button = Button(700, screenHeight - bottomMenu + 40, magic_icon, 1, magic_action)

# Magic button
def shield_action():
    healer.shield(healer)

shield_button = Button(950, screenHeight - bottomMenu + 40, shield_icon, 1, shield_action)

currentMob= skully

# GAME LOOP

run = True
while run:
    clock.tick(fps)

    draw_b1()
    draw_botMenu()

    healer_health_bar.draw(healer.hp)
    skully_health_bar.draw(skully.hp)

    healer.update()
    healer.draw()

    skully.update()
    skully.draw()

    if skully.hp== 0:
        skully.hp = 0
        Allyskully.alive= True
        mobMagican.alive = True

        currentMob= mobMagican
        draw_b2()

        healer.hp= 100
        healer_health_bar.draw(healer.hp)
        Allyskully_health_bar.draw(Allyskully.hp)
        mobMagican_healthBar.draw(mobMagican.hp)
        
        mobMagican.update()
        mobMagican.draw()
        
        healer.rect.center = (500, 900)
        Allyskully.rect.center = (625, 750)

        healer.update()
        healer.draw()

        Allyskully.update()
        Allyskully.draw()
        drawround2()
        
    # PLAYER TURN (BUTTON ACTIONS)
    if healer.alive and currentTurn == 1:
        actionCooldown += 1
        if actionCooldown >= actionWaitTime:
            
            attack_button.draw(screen)
            heal_button.draw(screen)
            magic_button.draw(screen)
            shield_button.draw(screen)
            
        if pygame.mouse.get_pressed()[0] == 1:
            if currentMob== skully:
                currentTurn=3
                actionCooldown =0

            if currentMob== magican:
                currentTurn=4
                actionCooldown =0

    if currentTurn == 2:
        if Allyskully.alive:
            actionCooldown += 1
            if actionCooldown >= actionWaitTime:
                Allyskully.attack(currentMob)
                currentTurn=1
                actionCooldown= 0
        else:
            currentTurn= 1


    # ENEMY TURN
    if currentTurn == 3:
        if skully.alive:
            actionCooldown += 1
            if actionCooldown >= actionWaitTime:
                currentMob.attack(healer)
                currentTurn = 1
                actionCooldown = 0
        else:
            currentTurn = 1  
            
    if currentTurn == 4:
        if mobMagican.alive:
            actionCooldown +=1
            if actionCooldown >= actionWaitTime:
                target = random.choice([healer, Allyskully])
                mobMagican.attack(target)
                currentTurn = 2
                actionCooldown = 0
        else:
            currentTurn = 2
            
    # QUIT EVENT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
