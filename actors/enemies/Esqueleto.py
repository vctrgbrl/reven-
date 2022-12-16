from actors.Actor import Animation
from actors.enemies.Enemy import Enemy
from actors.Player import Map, Player
import pygame
from typing import Dict

class Esqueleto(Enemy):
	surface = pygame.image.load('assets/skeleton.png')
	def __init__(self, position) -> None:
		super().__init__(position, Esqueleto.surface, {
			'idle':	Animation(0   ,  0, 12, 16, 4, 0.3),
			'walk':	Animation(12*4,  0, 12, 16, 6, 0.1),
			'die':	Animation(12*10, 0, 12, 16, 4, 0.1, True),
			'atk':	Animation(12*14, 0, 12, 16, 3, 0.2, False),
		}, 'idle')

		self.box[0] = 12
		self.box[1] = 16
		self.attack_points = 200
		self.attack_cooldown = 3
		self.speed = 6
		self.dying_counter = 0.5
		self.health_points = 200

	def pursuit(self, delta_time: float, player: Player, map: Map):
		self.radius = 20
		if self.get_anim() != 'walk' and self.get_anim() != 'atk':
			self.push_anim('walk')
		return super().pursuit(delta_time, player, map)
	
	def attack(self, player: Player):
		self.push_anim('atk')
		return super().attack(player)

	def passive(self, delta_time: float, map: Map):
		self.radius = 7
		if self.get_anim() != 'idle':
			self.push_anim('idle')
		return super().passive(delta_time, map)

	def on_die(self):
		super().on_die()
		self.push_anim('die')