# Actor são todos os elementos que se movem no jogo
# sejam eles: projéteis, criaturas, itens(enquanto estão no mapa)

import numpy
import pygame
from typing import Dict, Tuple

class Animation():
	def __init__(
			self, 
			pos_x: int,
			pos_y: int,
			sprite_w: int,
			sprite_h: int,
			number: int,
			duration: float,
			is_loop = True
		) -> None:
		self.playing = True
		self.timer = duration
		self.number = number
		self.duration = duration
		self.index = 0
		self.x = pos_x
		self.y = pos_y
		self.w = sprite_w
		self.h = sprite_h
		self.is_loop = is_loop
		self.clip_rect = pygame.rect.Rect(
				self.x + self.index * self.w, 
				self.y, 
				self.w, 
				self.h
			)

	def update(self, delta_time: float):
		self.timer -= delta_time
		if (self.timer <= 0):
			self.index += 1
			self.timer = self.duration
			if not self.is_loop and self.index == self.number:
				return True
			self.index %= self.number
			self.clip_rect = pygame.rect.Rect(
				self.x + self.index * self.w, 
				self.y, 
				self.w, 
				self.h
			)
		return False

class Actor:
	def __init__(self, position: Tuple[float, float], surface: pygame.surface.Surface, sprites: Dict[str, Animation], init: str) -> None:
		self.position = numpy.array(position, dtype=numpy.float64)
		self.velocity = numpy.array((0,0), dtype=numpy.float64)
		self.box = numpy.array((0,0))
		self.hidden = False
		self.anim_stack = [init]
		self.is_playing = True
		self.is_flipped = False
		self.surface = surface
		self.sprites = sprites

	def get_anim(self) -> str:
		return self.anim_stack[len(self.anim_stack) - 1]

	def update(self, delta_time: float):
		if not self.is_playing:
			return
		should_pop = self.sprites[self.get_anim()].update(delta_time)
		if should_pop:
			self.anim_stack.pop()

	def reset_anim(self):
		self.sprites[self.get_anim()].timer = 0.0
		self.sprites[self.get_anim()].index = 0

	def push_anim(self, name: str):
		if self.get_anim() == name:
			self.reset_anim()
		else:
			self.anim_stack.append(name)
	
	def get_rect(self):
		an = self.sprites[self.get_anim()]
		return 	pygame.transform.flip(self.surface.subsurface(an.clip_rect), self.is_flipped, False)


# OK Computer
# Kid A
# Amnesiac
# In Rainbows
# A Moon Shaped Pool
# Hail To The King
# The Bends
# Pablo Honey
# The King of Limbs
