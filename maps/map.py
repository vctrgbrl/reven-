from typing import Dict, List, Tuple
import pygame
import random as rng
import numpy as np

class Tile:
	def __init__(
		self, 
		# tileset: pygame.surface.Surface, 
		x: int, 
		y: int,
		blocking: bool = False,
		secret: int = 0,
		door: bool = False
		) -> None:
		# self.sprite = tileset
		self.rect = pygame.Rect(x * 16, y * 16, 16, 16)
		self.blocking = blocking
		self.secret = secret
		self.door = door
	
	def retile(self, x, y):
		self.rect = pygame.Rect(x * 16, y * 16, 16, 16)

class Map:
	def __init__(self, atlas: pygame.surface.Surface, tile_dict: Dict[str, Tile], matrix: str, size: Tuple[int, int], position: Tuple[int, int] = (0,0)):
		self.sprite_atlas = atlas
		self.position = position
		self.width = size[0]
		self.height = size[1]
		self.matrix = matrix
		self.tile_dict = tile_dict

	def get_tile(self, x: int, y: int) -> Tile:
		if 0 <= x < self.width and 0 <= y < self.height:
			return self.tile_dict[self.matrix[(self.height - y -1) * self.width + x]]
		return None

	# A* Path finding Algorythm
	def path_from_to(self, start: Tuple[float, float], end: Tuple[float, float]) -> None:

		fx, fy = (int(self.width/2 + start[0] 	- self.position[0]), 	int(self.height/2 + start[1] - self.position[1]))
		tx, ty = (int(self.width/2 + end[0] 	- self.position[0]), 	int(self.height/2 + end[1] 	- self.position[1]))

		cx, cy = fx, fy
		matrix = np.zeros((self.width, self.height, 3), dtype=np.float64) # 0 = dist from start, 1 = pythagoream dist to end, 2 = has been there
		
		neighbors = []

		best_f_cost = 100000000
		i = 0
		while cx != tx or cy != ty:
			i += 1
			if i > 100:
				return None
			matrix[cx][cy][2] = 1

			top = 	self.get_tile( (cx + 0),(cy + 1) ).blocking
			bot = 	self.get_tile( (cx + 0),(cy - 1) ).blocking
			left = 	self.get_tile( (cx - 1),(cy + 0) ).blocking
			right =	self.get_tile( (cx + 1),(cy + 0) ).blocking
			tp_lf = top or left 	or self.get_tile( (cx - 1), (cy + 1) ).blocking
			tp_rt = top or right 	or self.get_tile( (cx + 1), (cy + 1) ).blocking
			bt_lf = bot or left 	or self.get_tile( (cx - 1), (cy - 1) ).blocking
			bt_rt = bot or right 	or self.get_tile( (cx + 1), (cy - 1) ).blocking

			n = []

			if not top:
				n.append((+0, +1))
			if not tp_lf:
				n.append((-1, +1))
			if not tp_rt:
				n.append((+1, +1))
			if not bot:
				n.append((+0, -1))
			if not bt_lf:
				n.append((-1, -1))
			if not bt_rt:
				n.append((+1, -1))
			if not left:
				n.append((-1, +0))
			if not right:
				n.append((+1, +0))

			for a, b in n:
				if matrix[cx + a][cy + b][2] == 1:
					continue
				dist = (a**2 + b**2)**(1/2) + matrix[cx][cy][0]
				matrix[cx + a][cy + b][1] = ((cx + a - tx)**(2) + (cy + b - ty)**(2))**(1/2)
				if matrix[cx + a][cy + b][0] > dist:
					matrix[cx + a][cy + b][0] = dist
				if matrix[cx + a][cy + b][0] == 0:
					matrix[cx + a][cy + b][0] = dist
					neighbors.append((cx + a, cy + b))

			best_f_cost = 1_000_000
			for x, y in neighbors:
				f_cost = matrix[x][y][0] + matrix[x][y][1]
				if f_cost < best_f_cost and matrix[x][y][2] != 1:
					best_f_cost = f_cost
					cx, cy = x, y

			# for a in range(self.height - 1, 0, -1):
			# 	print('|', end='')
			# 	for b in range(self.width):
			# 		c = matrix[b][a][0] + matrix[b][a][1]
			# 		i = f'{c:.2f}'
			# 		i = (5 - len(i))*'0' + i
			# 		print(i, end='|')
			# 	print('')
			# print('')

		path = []
		min_f_cost = 1000000000
		# cx, cy = tx, ty
		point = end
		wx, wy = end

		while cx != fx or cy != fy:
			path.append(point)
			min_f_cost = 1000000000
			matrix[cx][cy][2] = 2

			top = 	self.get_tile( (cx + 0),(cy + 1) ).blocking
			bot = 	self.get_tile( (cx + 0),(cy - 1) ).blocking
			left = 	self.get_tile( (cx - 1),(cy + 0) ).blocking
			right =	self.get_tile( (cx + 1),(cy + 0) ).blocking
			tp_lf = top or left 	or self.get_tile( (cx - 1), (cy + 1) ).blocking
			tp_rt = top or right 	or self.get_tile( (cx + 1), (cy + 1) ).blocking
			bt_lf = bot or left 	or self.get_tile( (cx - 1), (cy - 1) ).blocking
			bt_rt = bot or right 	or self.get_tile( (cx + 1), (cy - 1) ).blocking

			n = []

			if not top:
				n.append((+0, +1))
			if not tp_lf:
				n.append((-1, +1))
			if not tp_rt:
				n.append((+1, +1))
			if not bot:
				n.append((+0, -1))
			if not bt_lf:
				n.append((-1, -1))
			if not bt_rt:
				n.append((+1, -1))
			if not left:
				n.append((-1, +0))
			if not right:
				n.append((+1, +0))

			for i,j in n:
				f_cost = matrix[cx + i][cy + j][0] + matrix[cx + i][cy + j][1]
				if f_cost != 0 and f_cost < min_f_cost and  matrix[cx + i][cy + j][2] != 2:
					min_f_cost = f_cost
					p = (cx + i, cy + j)
					point = (wx + i, wy + j)
				if cx + i == fx and cy + j == fy:
					p = (cx + i, cy + j)
					point = (wx + i, wy + j)
					break
			cx, cy = p
			wx, wy = point
		return path[::-1]

		# checar vizinhos da célula
		# dar valores aos vizinhos da célula
		# adicionar vizinhos da célula aos  vizinhos gerais
		# ir para o vizinho geral de menor valor