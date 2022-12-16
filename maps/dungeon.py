import pygame
from typing import Dict, List
from map import Map

# class Dungeon(Map):

# 	def __init__(self, atlas: pygame.surface.Surface, rect_map: Dict, rand_list: List[int]):
# 		super().__init__(atlas, rect_map, rand_list)

# 	def __init__(self, matrix: List[str] = []):
# 		self.matrix: List[str] = matrix
# 		self.tileset = pygame.image.load("assets/tiles0.png")
# 		self.tile_dict: Dict[str, Tile] = {
# 			'#': Tile(self.tileset, 0, 1),
# 			'.': Tile(self.tileset, 1, 0),
# 			'H': Tile(self.tileset, 5, 0),
# 		}
# 		a = (
# 			"#####5####"
# 			"#........#"
# 			"#........#"
# 			"#........#"
# 			"#........#"
# 			"##########"
# 			)

# 	def get_rect(self, x: int, y: int) -> pygame.Rect:
# 		pass