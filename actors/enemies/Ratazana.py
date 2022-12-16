from actors.enemies import Enemy
from actors import Actor
from actors.Player import Map, Player
import pygame
import random
import numpy as np

class Ratazana(Enemy.Enemy):

	atlas = pygame.image.load('./assets/rat.png')

	def __init__(self, position) -> None:
		is_white = random.choice((0,0,0,16))
		super().__init__(
			position=position,
			sprites={
				'idle':	Actor.Animation(0   ,is_white, 16, 16, 3, 0.3),
				'atk':	Actor.Animation(16*3,is_white, 16, 16, 3, 0.2, False),
				'walk':	Actor.Animation(16*5,is_white, 16, 16, 6, 0.1),
				'die':	Actor.Animation(16*11,is_white, 16, 16, 5, 0.1, True),
			},
			surface=Ratazana.atlas,
			init='idle'
		)
		self.box[0] = 16
		self.box[1] = 16
		self.counter = 2.0
		self.attack_points = 50
		self.speed = 5
		self.dying_counter = 0.5
		self.health_points = 200

	# def update(self, delta_time: float, player: Player, map: Map ):
	# 	# self.counter -= delta_time
	# 	# self.position += self.velocity * delta_time
	# 	# if self.get_anim() != 'walk' and self.counter < 0:
	# 	# 	self.anim_stack.append('walk')
	# 	# 	pos = self.position + np.array((1,0))
	# 	# 	self.velocity = pos - self.position
	# 	return super().update(delta_time, player, map)

	def pursuit(self, delta_time: float, player: Player, map: Map):
		if self.get_anim() != 'walk' and self.get_anim() != 'atk':
			self.push_anim('walk')
		return super().pursuit(delta_time, player, map)
	
	def attack(self, player: Player):
		self.push_anim('atk')
		return super().attack(player)

	def passive(self, delta_time: float, map: Map):
		if self.get_anim() != 'idle':
			self.push_anim('idle')
		return super().passive(delta_time, map)

	def on_die(self):
		super().on_die()
		self.push_anim('die')