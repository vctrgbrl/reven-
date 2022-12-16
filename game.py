from renderer import Renderer
from game_manager import *
from actors.projectiles.Projectile import Projectile

def reset():
	global enemy_list, player, map, camera, ca, cd, size, font, item_list

	ca = pygame.image.load('./assets/cilada_do_diabo.png')
	enemy_list = [
		Ratazana((1,1)), 
		Ratazana((6,3)), 
		Ratazana((9,4)), 
		Ratazana((6, 6)), 
		Ratazana((9, 5)), 
		Morcego((-2,-2)),
		Morcego((-10,-15)),
		Esqueleto((0,5)),
		]
	player = Player((-22,-15))
	cd = Actor((-1,5), ca, {'def': Animation(0,0,32,32,1,0)}, 'def')
	
	item_list = [
		Item((-24, -17), {'key': Animation(16,16,16,16,1,0)}, 'key', 'keys', secret=0),
		Item((-23, -17), {'life': Animation(16*0,16*7,16,16,1,0)}, 'life', 'life', secret=0),
		Item((-21, -17), {'mana': Animation(16*1,16*7,16,16,1,0)}, 'mana', 'mana', secret=0),
	]

	player.hp_ui.surface = font.render(f"HP: {player.health_points}/{player.health_points}", True,(255,255,255))
	player.mp_ui.surface = font.render(f"MP: {player.mana_points}/{player.mana_points}", True,(255,255,255))

	player.po_hp_ui.surface = font.render(f"Health Pot: {player.items['life']}", True,(255,255,255))
	player.po_mp_ui.surface = font.render(f"Mana Pot: {player.items['mana']}", True,(255,255,255))


	player.dead_ui.surface = font.render(f" Você Morreu ", True, (255,50,50), (0,0,0))
	size = 16
	camera = Camera((0,0), player)

	map_s = pygame.image.load('./assets/tiles0.png')
	mur = (
			"0000000000000000000############################0000000000000000000"
			"0000000000000000000#........#...##...#........#0000000000000000000"
			"0000000000000000000#........#........#........#0000000000000000000"
			"0000000000000000000#........#........#........#0000000000000000000"
			"0000000000000000000#..........................#0000000000000000000"
			"0000000000000000000#..........................#0000000000000000000"
			"0000000000000000000#........#........#........#0000000000000000000"
			"0000000000000000000#........#........#........#0000000000000000000"
			"0000000000000000000#........#........#........#0000000000000000000"
			"0000000000000000000####..#######..#######..#######################"
			"0000000#############........#.....#..#........#A................A#"
			"0000000#...........#........#........#........#..................#"
			"0000000#...........#........#........#........#..................#"
			"0000000#.........................................................#"
			"0000000#.........................................................#"
			"0000000#...........#........#........#........#..................#"
			"0000000#...........#........#........#........#..................#"
			"0000000#...........#........#........#........#A................A#"
			"0000000#########################.....#############################"
			"0000000000000000000#........#..####..#........#0000000000000000000"
			"0000000000000000000#........#....##..#........#0000000000000000000"
			"0000000000000000000#........#....##..#........#0000000000000000000"
			"0000000000000000000#..........................#0000000000000000000"
			"0000000000000000000#..........................#0000000000000000000"
			"0000000000000000000#........#........#........#0000000000000000000"
			"0000000000000000000#........#........#........#0000000000000000000"
			"0000000000000000000#........#........#........#0000000000000000000"
			"0000000000000000000####..#######..#######..####0000000000000000000"
			"0000000#############,.......#.....#..#........#0000000000000000000"
			"0000000#A.........A#,.......#........#........#0000000000000000000"
			"0000000#..........,#........#........#........#0000000000000000000"
			"0000000#...........#..........................#0000000000000000000"
			"0000000#...........D..........................#0000000000000000000"
			"0000000#...........#........#........#........#0000000000000000000"
			"0000000#...........#........#........#........#0000000000000000000"
			"0000000#A.........A#........#........#........#0000000000000000000"
			"0000000########################################0000000000000000000"
		)
	map = Map(map_s, {
		'0': Tile(0,0),
		'.': Tile(1,0),
		',': Tile(8,1),
		'D': Tile(5,0, True, door=True),
		'#': Tile(0,1, True),
		'A': Tile(3,2, True),
	}, mur, (len(mur) // (1 + 54 - 18), 1 + 54 - 18), (0, 0))

def loop():
	surface = pygame.display.get_surface()

	r = Renderer(surface)
	r.ui_list.append(player.hp_ui)
	r.ui_list.append(player.mp_ui)
	r.ui_list.append(player.dead_ui)
	r.ui_list.append(player.po_hp_ui)
	r.ui_list.append(player.po_mp_ui)

	size = 16
	c = pygame.time.Clock()
	v = 1
	running = True

	while running:
		r.fill()
		t = c.tick()/1000
		v -= t
		pressed = pygame.key.get_pressed()
		mouse_pos = pygame.mouse.get_pos()
		r.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEWHEEL:
				camera.zoom_in(event.y)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
				player.on_keydown(event)

		camera.update(mouse_pos, t, pressed)
		if v < 0:
			v = 1
			print(1/t) 
		r.draw_map(camera, map)

		for enemy in enemy_list:
			enemy.update(t, player, map)

		player.check_collision_item(item_list, t)
		player.update(t, pressed, 
			(mouse_pos[0] - r.win_size[0]/2)/(16*camera.zoom) + camera.position[0], 
			(- mouse_pos[1] + r.win_size[1]/2)/(16*camera.zoom) + camera.position[1], map)
		Projectile.update_projectiles(t, map, enemy_list)
		r.draw_actor(cd, camera)
		
		for item in item_list:
			r.draw_actor(item, camera)

		for enemy in enemy_list:
			r.draw_actor(enemy, camera)

		r.draw_actor(player, camera)
		Projectile.render_projectiles(r, camera)
		r.blit(camera)