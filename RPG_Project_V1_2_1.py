import pygame
import random
import button
import mainV1
import buttonM
from Enemy_Class import Enemy
from pygame.locals import *


pygame.init()

clock = pygame.time.Clock()
fps = 60


#game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

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
headingfont = pygame.font.SysFont("Verdana", 40)
regularfont = pygame.font.SysFont('Corbel',25)
smallerfont = pygame.font.SysFont('Corbel',16) 

#def colors
red = (255, 0, 0)
green = (0, 255, 0)
color_light = (170,170,170)
color_dark = (100,100,100)
color_white = (255,255,255)

#load images
#background image
background_img = pygame.image.load('RPG_Project_items/img/Background/background.png').convert_alpha()
#panel image
panel_img = pygame.image.load('RPG_Project_items/img/Icons/panel.png').convert_alpha()
#button images
potion_img = pygame.image.load('RPG_Project_items/img/Icons/potion.png').convert_alpha()
restart_img = pygame.image.load('RPG_Project_items/img/Icons/restart.png').convert_alpha()
main_menu_img = pygame.image.load('RPG_Project_items/img/Icons/quit_button.png').convert_alpha()
#load victory and defeat images
victory_img = pygame.image.load('RPG_Project_items/img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('RPG_Project_items/img/Icons/defeat.png').convert_alpha()
#sword image
sword_img = pygame.image.load('RPG_Project_items/img/Icons/sword.png').convert_alpha()
inventory_img = pygame.image.load('RPG_Project_items/img/Icons/start_btn.png').convert_alpha()


def main():
    Game_Loop()

if __name__ == "__main__":
    main()



#create function for drawing text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#function got drawing background
def draw_bg():
	screen.blit(background_img, (0, 0))

#function for drawing panel
def draw_panel():
	#draw panel rectangle
	screen.blit(panel_img, (0, screen_height - bottom_panel))

	#show player name and health
	draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panel + 10)
	
		#show enemy1 name and health
	draw_text(f'{enemy1.name} HP: {enemy1.hp}', font, red, 550, (screen_height - bottom_panel +10) + 0)
	
		#show enemy2 name and health
	draw_text(f'{enemy2.name} HP: {enemy2.hp}', font, red, 550, (screen_height - bottom_panel +10) + 60)




#fighter class
class Fighter():
	def __init__(self, x, y, name, max_hp, strength, potions, idle, attack, hurt, death):
		self.name = name
		self.max_hp = max_hp
		self.hp = max_hp
		self.strength = strength
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
		self.mana = 0
		self.experience = 0
		self.gp = 0

		#Load animation images

		#load idle images
		temp_list = []
		for i in range(self.frame_range_idle):
			img = pygame.image.load(f'RPG_Project_items/img/{self.name}/Base_mesh/Idle/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)

		#load attack images
		temp_list = []
		for i in range(self.frame_range_attack):
			img = pygame.image.load(f'RPG_Project_items/img/{self.name}/Attack/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)

		#load hurt images
		temp_list = []
		for i in range(self.frame_range_hurt):
			img = pygame.image.load(f'RPG_Project_items/img/{self.name}/Hurt/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)

		#load death images
		temp_list = []
		for i in range(self.frame_range_death):
			img = pygame.image.load(f'RPG_Project_items/img/{self.name}/Death/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
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


class HealthBar():
	def __init__(self, x, y, hp, max_hp):
		self.x = x 
		self.y = y 
		self.hp = hp 
		self.max_hp = max_hp

	def draw(self, hp):
		#update bar with new HP
		self.hp = hp
		#calculate HP ratio
		ratio = self.hp / self.max_hp
		pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


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




knight = Fighter(200, 260, 'Knight', 30, 10, 3, 8, 8, 3, 10)



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

enemy_list1 = []
enemy_list2 = []
enemy_list1.append(bandit1)
enemy_list2.append(bandit2)
enemy_list1.append(mushroom1)
enemy_list2.append(mushroom2)

random_enemy1 = random.randint(0, (len(enemy_list1) - 1))
random_enemy2 = random.randint(0, (len(enemy_list2) - 1))

enemy1 = (enemy_list1[random_enemy1])
enemy2 = (enemy_list1[random_enemy2])

#print(enemy1)


knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
enemy1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, enemy1.hp, enemy1.max_hp)
enemy2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, enemy2.hp, enemy2.max_hp)

#create buttons
potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)
main_menu_button = button.Button(screen, 200, screen_height - bottom_panel + 70, main_menu_img, 128, 64)
inventory_button = button.Button(screen, 415, screen_height - bottom_panel + 70, main_menu_img, 128, 64)



#Game loop calls

def Game_Loop():

	current_fighter = 1
	total_fighters = 3
	action_cooldown = 0
	action_wait_time = 90
	attack = False
	potion = False
	potion_effect = 15
	clicked = False
	game_over = 0
	run = True
	main_menu = False
	inventory = False
	enemy1 = (enemy_list1[random_enemy1])
	enemy2 = (enemy_list2[random_enemy2])
	while run:

		clock.tick(fps)

		if main_menu == True:
			mainV1.main_menu()

		if inventory == True:
			mainV1.inventory()


		#draw background
		draw_bg()

		#draw panel
		draw_panel()
		knight_health_bar.draw(knight.hp)
		enemy1_health_bar.draw(enemy1.hp)
		enemy2_health_bar.draw(enemy2.hp)


		#draw fighters
		knight.update()
		knight.draw()
		enemy1.update()
		enemy1.draw()
		enemy2.update()
		enemy2.draw()

		#for enemy in enemy_list1:
		#	random.choice(enemy_list1)
		#	enemy.update()
		#	enemy.draw()
		#for enemy in enemy_list2:
		#	random.choice(enemy_list2)
		#	enemy.update()
		#	enemy.draw()


		#draw the damage text
		damage_text_group.update()
		damage_text_group.draw(screen)

		#control player actions
		#reset action variables
		attack = False
		potion = False
		target = None
		#make sure mouse is visible
		pygame.mouse.set_visible(True)
		pos = pygame.mouse.get_pos()

		if enemy1.rect.collidepoint(pos):
				#hide mouse
			pygame.mouse.set_visible(False)
				#show sword in place of mouse cursor
			screen.blit(sword_img, pos)
			if clicked == True and enemy1.alive == True:
				attack = True
				target = enemy1


		if enemy2.rect.collidepoint(pos):
				#hide mouse
			pygame.mouse.set_visible(False)
				#show sword in place of mouse cursor
			screen.blit(sword_img, pos)
			if clicked == True and enemy2.alive == True:
				attack = True
				target = enemy2
		
		if potion_button.draw():
			potion = True
		if main_menu_button.draw():
			main_menu = True
		if inventory_button.draw():
			inventory = True


		#show number of potions remaining
		draw_text(str(knight.potions), font, red, 150, screen_height - bottom_panel + 70)


		if game_over == 0:
			#player action
			if knight.alive == True:
				if current_fighter == 1:
					action_cooldown += 1
					if action_cooldown >= action_wait_time:
						#look for player action
						#attack
						if attack == True and target != None:
							knight.attack(target)
							current_fighter += 1
							action_cooldown = 0
						#potion
						if potion == True:
							if knight.potions > 0:
								#check if the potion would heal the player beyond max health
								if knight.max_hp - knight.hp > potion_effect:
									heal_amount = potion_effect
								else:
									heal_amount = knight.max_hp - knight.hp
								knight.hp += heal_amount
								knight.potions -= 1
								damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
								damage_text_group.add(damage_text)
								current_fighter += 1
								action_cooldown = 0
						#Quit
						#if main_menu == True:
						#	mainV1.menu()


			else:
				game_over = -1


			#enemy action
			#for count, enemy1 in enumerate(enemy_list1):
			if current_fighter == 2:
				if enemy1.alive == True:
					action_cooldown += 1
					if action_cooldown >= action_wait_time:
							#check if enemy needs to heal first
						if (enemy1.hp / enemy1.max_hp) < 0.5 and enemy1.potions > 0:
								#check if the potion would heal the enemy beyond max health
							if enemy1.max_hp - enemy1.hp > potion_effect:
								heal_amount = potion_effect
							else:
								heal_amount = enemy1.max_hp - enemy1.hp
							enemy1.hp += heal_amount
							enemy1.potions -= 1
							damage_text = DamageText(enemy1.rect.centerx, enemy1.rect.y, str(heal_amount), green)
							damage_text_group.add(damage_text)
							current_fighter += 1
							action_cooldown = 0

							#attack
						else:	
							enemy1.attack(knight)
							current_fighter += 1
							action_cooldown = 0
				else:
					current_fighter += 1

			#for count, enemy2 in enumerate(enemy_list2):
			if current_fighter == 3:
				if enemy2.alive == True:
					action_cooldown += 1
					if action_cooldown >= action_wait_time:
							#check if enemy needs to heal first
						if (enemy2.hp / enemy2.max_hp) < 0.5 and enemy2.potions > 0:
								#check if the potion would heal the enemy beyond max health
							if enemy2.max_hp - enemy2.hp > potion_effect:
								heal_amount = potion_effect
							else:
								heal_amount = enemy2.max_hp - enemy2.hp
							enemy2.hp += heal_amount
							enemy2.potions -= 1
							damage_text = DamageText(enemy2.rect.centerx, enemy2.rect.y, str(heal_amount), green)
							damage_text_group.add(damage_text)
							current_fighter += 1
							action_cooldown = 0

							#attack
						else:	
							enemy2.attack(knight)
							current_fighter += 1
							action_cooldown = 0
				else:
					current_fighter += 1


			#if all fighters take their turn then reset
			if current_fighter > total_fighters:
				current_fighter = 1

		#check if all enemies are dead
		alive_enemies = 0
		#for enemy1 in enemy_list1:
		if enemy1.alive == True:
			alive_enemies += 1
		#if alive_enemies == 0:
		#	game_over = 1
		#for enemy2 in enemy_list2:
		if enemy2.alive == True:
			alive_enemies += 1
		if alive_enemies == 0:
			if knight.mana < 100:
				knight.mana += knight.mana
			knight.experience += 1
			knight.gp += 1
			game_over = 1

		#check if game is over
		if game_over != 0:
			if game_over == 1:
				screen.blit(victory_img, (250, 50))
			if game_over == -1:
				screen.blit(defeat_img, (290, 50))
			if restart_button.draw():
				knight.reset()
				#for enemy in enemy_list1:
				enemy1.reset()
				current_fighter = 1
				action_cooldown
				game_over = 0
				#for enemy in enemy_list2:
				enemy2.reset()
				current_fighter = 1
				action_cooldown
				game_over = 0


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				clicked = True
			else:
				clicked = False

		pygame.display.update()

	pygame.quit()

#Game_Loop()
