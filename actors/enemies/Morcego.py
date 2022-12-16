from actors.enemies import Enemy
from actors import Actor
from actors.Player import Map, Player
import pygame

class Morcego(Enemy.Enemy):

	atlas = pygame.image.load('./assets/bat.png')

	def __init__(self, position) -> None:
		super().__init__(
			position=position,
			sprites={
				'fly': Actor.Animation(0   ,0, 15, 16, 2, 0.1),
				'atk': Actor.Animation(16*2,0, 15, 16, 2, 0.2, False),
				'die': Actor.Animation(16*4,0, 15, 16, 3, 0.1, False)
			},
			surface=Morcego.atlas,
			init='fly'
		)
		self.box[0] = 15
		self.box[1] = 16
		self.attack_points = 50
		self.speed = 7
		self.dying_counter = 0.3
		self.health_points = 100

	def pursuit(self, delta_time: float, player: Player, map: Map):
		self.radius = 10
		if self.get_anim() != 'fly' and self.get_anim() != 'atk':
			self.push_anim('fly')
		return super().pursuit(delta_time, player, map)
	
	def attack(self, player: Player):
		self.push_anim('atk')
		return super().attack(player)

	def passive(self, delta_time: float, map: Map):
		self.radius = 5
		if self.get_anim() != 'fly':
			self.push_anim('fly')
		return super().passive(delta_time, map)

	def on_die(self):
		super().on_die()
		self.push_anim('die')