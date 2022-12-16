from ui.UIElement import UIElement
import pygame
from typing import Tuple

font = pygame.font.SysFont('monospace', 24)

class Button(UIElement):
	def __init__(self, position: Tuple[float, float], text: str, color: Tuple[int, int ,int], bg_color: Tuple[int, int, int], on_click) -> None:
		super().__init__(position, font.render(text, True, color, bg_color))
		self.background_color = bg_color
		self.color = color
		self.text = text
		self.size = (self.surface.get_width(), self.surface.get_height())
		self.invert = False
		self.on_click = on_click

	def update(self, mouse_pos: Tuple[float, float], click: bool):
		toggle = False
		if (
			(self.position[0] - self.size[0]/2 < mouse_pos[0] < self.position[0] + self.size[0]/2) 
			and 
			(self.position[1] - self.size[1]/2 < mouse_pos[1] < self.position[1] + self.size[1]/2)):
			if click:
				self.on_click(self)
			if not self.invert:
				toggle = True
				self.invert = True
		else:
			if self.invert:
				toggle = True
				self.invert = False
		if toggle:
			c = self.color
			b = self.background_color
			if self.invert:
				c = self.background_color
				b = self.color
			self.surface = font.render(self.text, True, c, b)
	
	def draw(self, surface: pygame.Surface):
		w, h = surface.get_size()
		surface.blit(self.surface, (self.position[0] + w/2 - self.size[0]/2, self.position[1] + h/2 - self.size[1]/2))