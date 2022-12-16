from actors import Creature
from actors.Player import Player, Map
import pygame
import numpy as np
from typing import Dict
import random
import math

class Enemy(Creature.Creature):

	behaviour_states = [
		'passive', 	# Modo passivo, sem atacar
		'pursuit', 	# Perseguindo um alvo, se dentro do alcance, ataca
		'flee', 	# Correndo do inimigo
		]

	def __init__(self, position, surface: pygame.surface.Surface, sprites: Dict[str, Creature.Actor.Animation], init: str) -> None:
		super().__init__(position, surface, sprites, init)
		self.is_servant = False
		self.radius = 5
		self.attack_cooldown = 2
		self.attack_timer = 0
		self.walk_timer = 3
		self.walking = False

	def attack(self, player: Player):
		player.on_hit(self.attack_points)

	def passive(self, delta_time: float, map: Map): pass


	def pursuit(self, delta_time: float, player: Player, map: Map):
		if self.attack_timer > 0:
			self.attack_timer -= delta_time
		if np.linalg.norm(self.position - player.position) <= 1.5:
			if self.attack_timer <= 0:
				self.attack(player)
				self.attack_timer = self.attack_cooldown
		else:
			path = map.path_from_to((*self.position,), (*player.position,))
			if path == None:
				return
			p = np.array(path[0])
			self.position += (p - self.position)/np.linalg.norm(p - self.position) * delta_time * self.speed

	def update(self, delta_time: float, player: Player, map: Map):
		super().update(delta_time)
		if self.is_dead:
			return
		# check if player is in some radius
		# it is, change behaviour to pursuit
		# it is not, passive

		if np.linalg.norm(player.position - self.position) < self.radius:
			self.is_flipped = False
			if player.position[0] < self.position[0]:
				self.is_flipped = True
			self.pursuit(delta_time, player, map)
		else:
			self.passive(delta_time, map)

		# pursuit
		#		find path

	def on_die(self):
		super().on_die()
		print('enemy dead')