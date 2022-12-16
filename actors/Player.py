import pygame
from actors.Actor import *
import numpy as np
from typing import Sequence, Tuple
from maps.map import Map
from actors.projectiles.Projectile import Projectile
from actors.Item import Item
from ui.UIElement import UIElement
from typing import List

font = pygame.font.SysFont('monospace', 24)

class Player(Actor):

	surface = pygame.image.load("assets/mage.png")

	def __init__(self, position) -> None:
		super().__init__(position, Player.surface, {
			'idle': Animation(00, 0, 12, 15, 2, 1),
			'walk': Animation(24, 0, 12, 15, 6, 0.1),
			'atck': Animation(156, 0, 12, 15, 3, 0.08, is_loop=False),
		}, 'idle')
		self.is_walking = False
		self.speed = 10
		self.left_click = False
		self.cool_down = 0.1
		self.cool_down_timer = self.cool_down
		self.dist_matrix_size = (20,20,2)
		self.dist_matrix: np.zeros(self.dist_matrix_size)
		self.health_points = 1000
		self.max_hp = 1000
		self.mana_points = 1000
		self.max_mana = 1000
		self.hp_ui = UIElement((0,0), None)
		self.mp_ui = UIElement((0,20), None)
		self.po_hp_ui = UIElement((0,40), None)
		self.po_mp_ui = UIElement((0,60), None)
		self.dead_ui = UIElement((400, 300), None)
		self.dead_ui.center = True
		self.dead_ui.visible = False
		self.is_dead = False
		self.items = {
			'life':0,
			'mana':0,
			'keys':[]
		}

	def walking(self):
		if not self.is_walking and not self.get_anim() == 'walk':
			self.anim_stack.append('walk')
			self.is_walking = True

	def stop_walking(self):
		if self.is_walking and self.get_anim() == 'walk':
			self.anim_stack.pop()
			self.is_walking = False

	def atack(self, mouse_pos: Tuple[float, float]) -> Projectile:
		self.update_mana(-10)
		if self.mana_points == 0:
			return
		self.push_anim('atck')
		a = np.array(mouse_pos, dtype=np.float64) - self.position
		a /= np.linalg.norm(a)
		p = self.position
		Projectile.create_projectile((p[0], p[1]), (a[0],a[1]))

	def check_colision_map(self, map: Map, delta_time: float) -> bool:
		new_pos = self.position + self.velocity * delta_time
		new_pos_tl = np.copy(new_pos) + np.array((0.1, 0.1))
		new_pos_tr = new_pos + np.array((0.9,0))
		new_pos_bl = new_pos + np.array((0,0.9))
		new_pos_br = new_pos + np.array((0.9,0.9))
		
		new_positions = [new_pos_tl, new_pos_tr, new_pos_bl, new_pos_br]
		
		has_col = False
		a = 0.1
		b = 0.1
		if self.velocity[0] < 0:
			a = -0.1
		if self.velocity[1] < 0:
			b = -0.1
		
		for p in new_positions:
			x = int(p[0] - map.position[0] + map.width  //2 + a)
			y = int(p[1] - map.position[1] + map.height //2)
			
			t = map.get_tile(x, y)

			if t != None:
				if t.blocking:
					self.velocity[0] = 0
					has_col = True
				if t.door and t.blocking:
					for key in self.items['keys']:
						if key.secret == t.secret:
							t.blocking = False
							t.retile(6, 0)

			x = int(p[0] - map.position[0] + map.width  //2)
			y = int(p[1] - map.position[1] + map.height //2 + b)
			
			t = map.get_tile(x, y)

			if t != None:
				if t.blocking:
					self.velocity[1] = 0
					has_col = True
				if t.door and t.blocking:
					for key in self.items['keys']:
						if key.secret == t.secret:
							t.blocking = False
							t.retile(6, 0)
		return has_col

	def check_collision_item(self, items: List[Item], delta_time):
		new_pos = self.position + self.velocity * delta_time
		new_pos_tl = np.copy(new_pos)
		new_pos_tr = new_pos + np.array((1,0))
		new_pos_bl = new_pos + np.array((0,1))
		new_pos_br = new_pos + np.array((1,1))
		
		new_positions = [new_pos_tl, new_pos_tr, new_pos_bl, new_pos_br]

		for item in items:
			for pos in new_positions:
				if item.hidden:
					continue
				if np.linalg.norm(item.position + np.array((0.5,0.5)) - pos) < 1:
					item.hidden = True
					if item.type == 'keys':
						self.items[item.type].append(item)
					else:
						self.items[item.type]+=1
					if item.type == 'life':
						self.po_hp_ui.surface = font.render(f"Health Pot: {self.items['life']}", True,(255,255,255))
					if item.type == 'mana':
						self.po_mp_ui.surface = font.render(f"Mana Pot: {self.items['mana']}", True,(255,255,255))



	def update(self, delta_time: float, pressed: Sequence[bool], mouse_world_x: float, mouse_world_y: float, map: Map):

		self.velocity[0] = 0
		self.velocity[1] = 0
		self.update_mana(delta_time)
		
		if self.is_dead:
			return

		if mouse_world_x < self.position[0]:
			self.is_flipped = True
		else:
			self.is_flipped = False
		
		if pressed[pygame.K_w]:
			self.velocity[1] += 1
		elif pressed[pygame.K_s]:
			self.velocity[1] -= 1

		if pressed[pygame.K_a]:
			self.velocity[0] -= 1
		elif pressed[pygame.K_d]:
			self.velocity[0] += 1
		n = np.linalg.norm(self.velocity)

		if n > 0:
			self.walking()
			self.velocity /= n
		else:
			self.stop_walking()

		left_click, right_click, wheel_click = pygame.mouse.get_pressed()
		self.cool_down_timer -= delta_time
		if not self.left_click and left_click and self.cool_down_timer <= 0:
			self.cool_down_timer = self.cool_down
			self.atack((mouse_world_x,  mouse_world_y))
		self.left_click = left_click


		self.check_colision_map(map, delta_time)

		self.position += self.velocity * delta_time * self.speed
		return super().update(delta_time)

	def update_health(self, value):
		self.health_points += value
		if self.health_points <= 0:
			self.on_die()
			self.health_points = 0
		if self.health_points > self.max_hp:
			self.health_points = self.max_hp
		self.hp_ui.surface = font.render(f"HP: {int(self.health_points)}/{self.max_hp}", True,(255,255,255))

	def update_mana(self, value: float):
		self.mana_points += value
		if self.mana_points < 0:
			self.mana_points = 0
		if self.mana_points > self.max_hp:
			self.mana_points = self.max_hp
		self.mp_ui.surface = font.render(f"MP: {int(self.mana_points)}/{self.max_mana}", True,(255,255,255))


	def on_keydown(self, pressed):
		if pressed.key == pygame.K_1:
			if self.items['life'] > 0:
				self.items['life'] -= 1
				self.update_health(50)
				self.po_hp_ui.surface = font.render(f"Health Pot: {self.items['life']}", True,(255,255,255))

		if pressed.key == pygame.K_2:
			if self.items['mana'] > 0:
				self.items['mana'] -= 1
				self.update_mana(50)
				self.po_mp_ui.surface = font.render(f"Mana Pot: {self.items['mana']}", True,(255,255,255))
			

	def on_hit(self, damage: float):
		if self.is_dead:
			return
		self.update_health(-damage)

	def on_die(self):
		self.is_dead = True
		self.dead_ui.visible = True