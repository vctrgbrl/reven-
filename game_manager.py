import pygame

from actors.Actor import Actor, Animation
from actors.enemies.Morcego import Morcego
from actors.enemies.Enemy import Enemy
from actors.enemies.Esqueleto import Esqueleto
from actors.Item import Item
from actors.enemies.Ratazana import Ratazana
from actors.Player import Player
from camera import Camera
from maps.map import Map, Tile

from typing import List

ca = pygame.image.load('./assets/cilada_do_diabo.png')

enemy_list: List[Enemy] = [Ratazana((1,1)), Morcego((-1,-1))]
player = Player((0,3))
cd = Actor((-1,-1), ca, {'def': Animation(0,0,32,32,1,0)}, 'def')

size = 16
camera = Camera((0,0), player)
item_list: List[Item] = [
	Item((-24, -18), {'key': Animation(0,0,16,16,1,0)}, 'key', 'keys')
]
map_s = pygame.image.load('./assets/tiles0.png')
map = Map(map_s, {
	'0': Tile(0,0),
	'.': Tile(1,0),
	'#': Tile(0,1, True),
},
	(
		"############################"
		"#........#...##...#........#"
		"#........#........#........#"
		"#........#........#........#"
		"#..........................#"
		"#..........................#"
		"#........#........#........#"
		"#........#........#........#"
		"#........#........#........#"
		"####..#######..#######..####"
		"#........#.....#..#........#"
		"#........#........#........#"
		"#........#........#........#"
		"#..........................#"
		"#..........................#"
		"#........#........#........#"
		"#........#........#........#"
		"#........#........#........#"
		"############################"
	), (6*4+4, 48-29), (0, 0))

font = pygame.font.SysFont('monospace', 24)
player.hp_ui.surface = font.render(f"HP: {1000}:{1000}", True,(255,255,255))



# Zoom em mapa - v
# Olhar para onde mouse apontar - v
# Animações de Ataque e Andar - v
# Criar o mapa, não gerado processualmente - v	
# Colidir com o mapa - v
# Lançar magia simples, estilo "auto attack" do League of Legends - v
# IA Monstros, Andar, Perseguir, Atacar, Correr - v
# Colisão projéteis e monstros - v
# Fazer um Main Menu, New Game, Load Game, Settings, Quit

# Colisão jogador e monstros - ?
# Construir um Mapa Inteiro
# Fazer uma Boss Fight
# Adicionar Save e Load