import pygame
import random
import RPG_Project_V1_2_1


pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')

#define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 15
clicked = False
game_over = 0

#define fonts
font = pygame.font.Font('Menu_assets/runescape_uf.ttf', 26)

#def colors
red = (255, 0, 0)
green = (0, 255, 0)

#Enemy class settings

class Enemy():
	def __init__(self, x, y, name, max_hp, strength, dexterity, crit_chance, crit_damage, armor, magic_resist, potions, idle, attack, hurt, death):
		self.name = name
		self.max_hp = max_hp
		self.hp = max_hp
		self.strength = strength
		self.dexterity = dexterity
		self.crit_chance = crit_chance
		self.crit_damage = crit_damage
		self.armor = armor
		self.magic_resist = magic_resist
		self.start_potions = potions
		self.potions = potions
		self.alive = True
		self.animation_list = []
		self.frame_index = 0
		self.action = 0 #0:idle, 1:attack, 2:hurt, 3:dead
		self.update_time = pygame.time.get_ticks()
		self.frame_range_idle = idle
		self.frame_range_attack = attack
		self.frame_range_hurt = hurt
		self.frame_range_death = death
		self.mana = random.randint(1, 3) #Randomized amount of mana obtained after each kill

		#self.height_scale = 0
		#self.width_scale = 0

		#Load animation images

		#load idle images
		temp_list = []
		for i in range(self.frame_range_idle):
			img = pygame.image.load(f'RPG_Project_items/img/{self.name}/Idle/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * (3), img.get_height() * (3)))
			temp_list.append(img)
		self.animation_list.append(temp_list)

		#load attack images
		temp_list = []
		for i in range(self.frame_range_attack):
			img = pygame.image.load(f'RPG_Project_items/img/{self.name}/Attack/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * (3), img.get_height() * (3)))
			temp_list.append(img)
		self.animation_list.append(temp_list)

		#load hurt images
		temp_list = []
		for i in range(self.frame_range_hurt):
			img = pygame.image.load(f'RPG_Project_items/img/{self.name}/Hurt/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * (3), img.get_height() * (3)))
			temp_list.append(img)
		self.animation_list.append(temp_list)

		#load death images
		temp_list = []
		for i in range(self.frame_range_death):
			img = pygame.image.load(f'RPG_Project_items/img/{self.name}/Death/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * (3), img.get_height() * (3)))
			temp_list.append(img)
		self.animation_list.append(temp_list)

		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def update(self):
		animation_cooldown = 100
		#handle animation
		#update image
		self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#if the animation has run out then reset back to the start
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.idle()

	def idle(self):
		#set variables to idle animation
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def attack(self, target):
		#deal damage to enemy
		rand = random.randint(-5, 5)
		damage = self.strength + rand
		target.hp -= damage
		#run enemy hurt animation
		target.hurt()
		#check if target has died
		if target.hp < 1:
			target.hp = 0 
			target.alive = False
			target.death()
		damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
		damage_text_group.add(damage_text)

		#set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def hurt(self):
		#set variables to hurt animation
		self.action = 2
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def death(self):
		#set variables to death animation
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()


	def reset(self):
		self.alive = True
		self.potions = self.start_potions
		self.hp = self.max_hp
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()



	def draw(self):
		screen.blit(self.image, self.rect)

class DamageText(pygame.sprite.Sprite):
	def __init__(self, x, y, damage, color):
		pygame.sprite.Sprite.__init__(self)
		self.image = font.render(damage, True, color)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.counter = 0

	def update(self):
		#move damage text up
		self.rect.y -= 1
		#delete the text after a few seconds
		self.counter =+ 1
		if self.counter > 30:
			self.kill()

damage_text_group = pygame.sprite.Group()

#Define the Enemy characters


bandit1 = Enemy(550,			## x-coordinate location ##
				  270, 			## y-coordinate location ##
				  'Bandit', 	##         Name          ##
				  20,           ##          HP           ##
				  6, 			##       Strength        ##
				  6,			##       Dexterity		 ##
				  0.1,			##    	Crit_chance		 ##
				  1.5,			## 		Crit_damage		 ##
				  4,			##         Armor         ##
				  4,			##		magic_resist     ##
				  1, 			##        Potion         ##
				  8, 			##         Idle          ##
				  8, 			##        Attack         ##
				  3,            ##         Hurt          ##
				  10)			##		   Dead          ##

bandit2 = Enemy(700,			## x-coordinate location ##
				  270, 			## y-coordinate location ##	
				  'Bandit', 	##         Name          ##
				  20,           ##          HP           ##
				  6, 			##       Strength        ##
				  6,			##       Dexterity		 ##
				  0.1,			##    	Crit_chance		 ##
				  1.5,			## 		Crit_damage		 ##
				  4,			##         Armor         ##
				  4,			##		magic_resist     ##
				  1, 			##        Potion         ##
				  8, 			##         Idle          ##
				  8, 			##        Attack         ##
				  3,            ##         Hurt          ##
				  10)			##		   Dead          ##

skeleton1 = Enemy(550,			## x-coordinate location ##
				  270, 			## y-coordinate location ##
				  'Skeleton', 	##         Name          ##
				  15,           ##          HP           ##
				  6, 			##       Strength        ##
				  6,			##       Dexterity		 ##
				  0.1,			##    	Crit_chance		 ##
				  1.5,			## 		Crit_damage		 ##
				  4,			##         Armor         ##
				  4,			##		magic_resist     ##
				  1, 			##        Potion         ##
				  11, 			##         Idle          ##
				  18, 			##        Attack         ##
				  8,            ##         Hurt          ##
				  14)			##		   Dead          ##

skeleton2 = Enemy(700,			## x-coordinate location ##
				  270, 			## y-coordinate location ##	
				  'Skeleton', 	##         Name          ##
				  15,           ##          HP           ##
				  6, 			##       Strength        ##
				  6,			##       Dexterity		 ##
				  0.1,			##    	Crit_chance		 ##
				  1.5,			## 		Crit_damage		 ##
				  4,			##         Armor         ##
				  4,			##		magic_resist     ##
				  1, 			##        Potion         ##
				  11, 			##         Idle          ##
				  18, 			##        Attack         ##
				  8,            ##         Hurt          ##
				  14)			##		   Dead          ##

mushroom1 = Enemy(550,			## x-coordinate location ##
				  270, 			## y-coordinate location ##	
				  'Mushroom', 	##         Name          ##
				  15,           ##          HP           ##
				  6, 			##       Strength        ##
				  6,			##       Dexterity		 ##
				  0.1,			##    	Crit_chance		 ##
				  1.5,			## 		Crit_damage		 ##
				  4,			##         Armor         ##
				  4,			##		magic_resist     ##
				  1, 			##        Potion         ##
				  4, 			##         Idle          ##
				  13, 			##        Attack         ##
				  4,            ##         Hurt          ##
				  4)			##		   Dead          ##

mushroom2 = Enemy(700,			## x-coordinate location ##
				  270, 			## y-coordinate location ##	
				  'Mushroom', 	##         Name          ##
				  15,           ##          HP           ##
				  6, 			##       Strength        ##
				  6,			##       Dexterity		 ##
				  0.1,			##    	Crit_chance		 ##
				  1.5,			## 		Crit_damage		 ##
				  4,			##         Armor         ##
				  4,			##		magic_resist     ##
				  1, 			##        Potion         ##
				  4, 			##         Idle          ##
				  13, 			##        Attack         ##
				  4,            ##         Hurt          ##
				  4)			##		   Dead          ##