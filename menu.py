from ui.Button import Button
import pygame
import game
import sys

def on_newgame(button: Button):
	print(button.text)
	game.reset()
	game.loop()

def on_continue(button: Button):
	print(button.text)
	game.loop()

def on_quit(button: Button):
	sys.exit()

def loop():

	btn_list = [
		Button((0, -200), 'Revenã', (255, 255, 255), (0,0,0), lambda x: x),
		Button((0,-50), 'New Game', (255, 255, 255), (0,0,0), on_newgame), 
		Button((0,0), 'Continue', (255, 255, 255), (0,0,0), on_continue),
		Button((0,50), 'Quit', (255, 255, 255), (0,0,0), on_quit)
		]
	surf = pygame.display.get_surface()
	running = True
	while running:
		w, h = pygame.display.get_window_size()
		surf.fill((0,0,0))
		left, right, middle = False, False, False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				left, right, middle = pygame.mouse.get_pressed()
			
		mx, my = pygame.mouse.get_pos()
		mouse_pos = (mx - w/2, my - h/2)
		for b in btn_list:
			b.update(mouse_pos, left)
			b.draw(surf)
		pygame.display.flip()
