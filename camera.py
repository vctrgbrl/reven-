import numpy as np
import pygame
from actors.Player import Player
from typing import Tuple, Sequence

class Camera:
	def __init__(self, position: Tuple[float, float], player: Player) -> None:
		self.position = np.array(position, dtype=np.float64)
		self.zoom = 2.0
		self.camera_box_ratio = 0.75
		self.speed = 15
		self.player = player
		self.fixed = True

	def update(self, mouse_pos: Tuple[float, float], delta_time: float, pressed: Sequence[bool]):

		if self.fixed:
			self.position = self.player.position * 1.0
		if pressed[pygame.K_SPACE]:
			d = self.player.position - self.position
			self.position += d * delta_time * self.speed * 0.6
			return
	
		m_pos = np.array(mouse_pos, dtype=np.float64)
		size = np.array(pygame.display.get_surface().get_size(), dtype=np.float64)
		camera_box = size * self.camera_box_ratio
		top_left = (size - camera_box)/2
		if (
			self.fixed or
			(top_left[0] < mouse_pos[0] < top_left[0] + camera_box[0]) and
			(top_left[1] < mouse_pos[1] < top_left[1] + camera_box[1])
			): pass
		else:
			m_pos[1] = size[1] - m_pos[1]
			direction = m_pos - size/2
			direction /= np.linalg.norm(direction)
			self.position += direction * delta_time * self.speed

	def zoom_in(self, value: int):
		s = 10
		return
		if self.zoom > 1:
			s = 5
		value /= s
		self.zoom += value
		if self.zoom > 4:
			self.zoom = 4
		elif self.zoom < 1:
			self.zoom = 1