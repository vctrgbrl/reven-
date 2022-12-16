import pygame
from actors.Actor import Actor
from maps.map import Map
from camera import Camera
from ui.UIElement import UIElement
from typing import List

class Renderer:
	def __init__(self, surface: pygame.surface.Surface):
		# self.window = window
		self.surface = pygame.Surface(surface.get_size())
		self.end_surf = surface
		self.block_size = 16
		self.win_size = pygame.display.get_window_size()
		self.w = self.win_size[0] // (self.block_size * 2)
		self.h = self.win_size[1] // (self.block_size * 2)
		self.ui_list: List[UIElement] = []

	def fill(self):
		self.surface.fill((0, 0, 0))

	def blit(self, camera: Camera):
		a = pygame.transform.scale(self.surface, (self.end_surf.get_width() * camera.zoom, self.end_surf.get_height() * camera.zoom))
		s = a.get_size()
		self.end_surf.blit(a, (0,0), 
			pygame.rect.Rect(
				(s[0] - s[0]/(camera.zoom))/2, 
				(s[1] - s[1]/(camera.zoom))/2, 
				s[0]/camera.zoom,
				s[1]/camera.zoom
				)
			)
		for element in self.ui_list:
			if not element.visible:
				continue
			if element.center:
				self.end_surf.blit(element.surface, 
				(self.end_surf.get_width()/2 - element.surface.get_width()/2, self.end_surf.get_height()/2 - element.surface.get_height()/2))
				continue
			self.end_surf.blit(element.surface, element.position)
		pygame.display.flip()

	def update(self):
		self.surface = pygame.Surface(pygame.display.get_window_size())
		self.win_size = pygame.display.get_window_size()
		self.w = self.win_size[0] // (self.block_size * 2)
		self.h = self.win_size[1] // (self.block_size * 2)

	def draw_actor(self, actor: Actor, camera: Camera):
		if actor.hidden:
			return
		s = actor.get_rect()
		r = s.get_rect()
		self.surface.blit(
				s,
				(
					(actor.position[0] - camera.position[0] + self.w) * self.block_size, 
					(- actor.position[1] + camera.position[1] + self.h) * self.block_size+ r.height//2),
			)

	def draw_map(self, camera: Camera, map: Map):
		w = self.w/camera.zoom
		h = self.h/camera.zoom

		min_w = int(camera.position[0] - w) - 1
		max_w = int(camera.position[0] + w) + 2

		min_h = int(camera.position[1] - h) - 1
		max_h = int(camera.position[1] + h) + 2

		for y in range(min_h, max_h):
			y =  int(y - map.position[1] + map.height/2)
			for x in range(min_w, max_w):
				x = int(x - map.position[0] + map.width/2)
				t = map.get_tile(x,y)
				if t != None:
					self.surface.blit(
						map.sprite_atlas, (
							(x + map.position[0] - camera.position[0] + w*camera.zoom - map.width/2) * self.block_size, 
							(- y - map.position[1] + camera.position[1] + h*camera.zoom + map.height/2) * self.block_size),
						area=t.rect
					)