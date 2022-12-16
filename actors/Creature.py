# Criaturas são todos objetos que possuem
# Vida, podem morrer
from actors import Actor
import pygame
from typing import Dict

class Creature(Actor.Actor):
	def __init__(self, position, surface: pygame.surface.Surface, sprites: Dict[str, Actor.Animation], init: str, ) -> None:
		super().__init__(position, surface, sprites, init)
		self.health_points = 0
		self.mana_points = 0
		self.attack_points = 0
		self.speed = 1
		self.is_dead = False
		self.dying_counter = 0

	def on_hit(self, damage: float):
		if self.is_dead:
			return
		self.health_points -= damage
		if self.health_points <= 0:
			self.is_dead = True
			self.on_die()

	def on_die(self): pass

	def update(self, delta_time: float):
		super().update(delta_time)
		if self.is_dead and self.dying_counter > 0:
			self.dying_counter -= delta_time
		if self.is_dead and self.dying_counter <= 0:
			self.hidden = True