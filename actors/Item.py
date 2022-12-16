from actors.Actor import *

class Item(Actor):
	surface = pygame.image.load('assets/items.png')
	def __init__(self, position: Tuple[float, float], sprites: Dict[str, Animation], init: str, type: str, secret = 0) -> None:
		super().__init__(position, Item.surface, sprites, init)
		self.box[0] = 16
		self.box[1] = 16
		self.secret = secret
		self.type = type

	def effect(self):
		pass