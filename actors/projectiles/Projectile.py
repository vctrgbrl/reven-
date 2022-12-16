from actors.Actor import *
from actors.Creature import Creature
import numpy as np
from utils.queue import Queue
from typing import List
from maps.map import Map

class Projectile(Actor):

	queue: Queue = Queue(20)
	speed = 15
	player_attack_surface = pygame.image.load('assets/player_common_attack.png')

	def __init__(self, position, velocity, surface: pygame.surface.Surface, sprites: Dict[str, Animation], init: str) -> None:
		super().__init__(position, surface, sprites, init)
		self.velocity = np.array(velocity)
		self.life_time = 2
		self.damage = 10
	
	@staticmethod
	def create_projectile(position, velocity):
		Projectile.queue.add(
			Projectile(
				position,
				velocity,
				Projectile.player_attack_surface,
				{
					'idle': Animation(0, 0, 16, 16, 2, 0.1, True),
				},
				'idle'
			)
		)

	def check_collision_creature(self, actors: List[Creature]) -> bool:
		has_col = False
		if self.hidden:
			return True
		for ac in actors:
			if ac.is_dead:
				continue
			a = (ac.position[0], ac.position[1])
			b = (ac.position[0] + ac.box[0], ac.position[1])
			c = (ac.position[0], ac.position[1] + ac.box[1])
			d = (ac.position[0] + ac.box[0], ac.position[1] + ac.box[1])

			for p in [a,b,c,d]:
				if ((p[0] - self.position[0] )**2 + (p[1] - self.position[1] )**2)**(1/2) <= 0.5:
					ac.on_hit(self.damage)
					has_col = True
					break
		return has_col

	def check_collision_map(self, map: Map, delta_time: float) -> bool:
		new_pos = self.position + self.velocity * delta_time
		has_col = False
		a = 0.05
		b = 0.05
		if self.velocity[0] < 0:
			a = -0.1
		if self.velocity[1] < 0:
			b = -0.1
		
		x = int(new_pos[0] - map.position[0] + map.width  //2 + a + 0.5)
		y = int(new_pos[1] - map.position[1] + map.height //2 + b + 0.5)
		
		t = map.get_tile(x, y)

		if t != None:
			if t.blocking:
				has_col = True
		return has_col

	def update(self, delta_time: float):
		self.life_time -= delta_time
		if self.life_time <= 0:
			self.on_destroy()
		return super().update(delta_time)

	def on_destroy(self): pass

	@staticmethod
	def update_projectiles(delta_time: float, map: Map, enemies: List[Creature]):
		for proj in Projectile.queue:
			proj.update(delta_time)
			proj.hidden = proj.check_collision_map(map, delta_time) or proj.check_collision_creature(enemies)
			if not proj.hidden:
				proj.position += proj.velocity * delta_time * Projectile.speed

	@staticmethod
	def render_projectiles(renderer, camera):
		for proj in Projectile.queue:
			renderer.draw_actor(proj, camera)