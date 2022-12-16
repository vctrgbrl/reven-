from typing import Dict, List
import pygame
import random as rng

class Map:
	def __init__(self, atlas: pygame.surface.Surface, rect_map: Dict, rand_list: List[int]):
		self.sprite_atlas = atlas
		self.width = 100
		self.height = 100

		self.matrix = [ rng.choice(rand_list) for x in range(self.width * self.height)]
		self.rect_map = {}
		for k, v in rect_map.items():
			self.rect_map[k] = pygame.Rect(v[0] * 16, v[1] * 16, 16, 16)

	def noise(self):
		for y in range(self.width):
			for x in range(self.height):
				a = self.get_neighbors(x, y, 1)
				v = self.matrix[y * self.width + x]	
				if a < 4:
					v = 0
				if a > 4:
					v = 1
				self.matrix[y * self.width + x] = v

	def get_neighbors(self, i_x: int, i_y: int, comp: int) -> int:
		n = 0
		m = self.matrix
		for y in range(i_y - 1, i_y + 2):
			for x in range(i_x - 1, i_x + 2):
				if (y >= 0 and x >= 0 and y < self.width and x < self.width and not (x==i_x and y == i_y)):
					if m[y * self.width + x] == comp:
						n += 1
		return n

	def get_rect(self, x: int, y: int) -> pygame.Rect:
		return self.rect_map[self.matrix[y * self.width + x]]