import pygame
import numpy as np
from typing import Tuple

class UIElement:
	def __init__(self, position: Tuple[float, float], surface: pygame.Surface) -> None:
		self.position = position
		self.surface = surface
		self.center = False
		self.visible = True