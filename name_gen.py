import random as rng

vogais = list('aeiou')

# b, c, d, t, v, g | r + (a,i,o,u)
#  g, s, r, t, v, j | ão, on
def gera_tipo_0():
	global vogais
	a_0 = list('bcdtvg')
	d_0 = list('gsrtvjn')
	e_0 = ['ão','on', 'ém', 'inho', 'anha']

	name = ''
	name += rng.choice(a_0)
	if rng.random() < 0.5:
		name += 'r'
		name += rng.choice(vogais)
	else:
		name += rng.choice(vogais)
		name += 'r'
	name += rng.choice(d_0)
	name += rng.choice(e_0)
	return name

# c, d, t, b, m, n, s | a, e, i, o, u
# n, m, d, p, r | ilo, elo
def gera_tipo_1():
	global vogais

	nome = ''
	a_1 = list('cdtbmns')
	d_1 = list('nmdpr')
	for i in range(rng.randint(1,2)):
		nome += rng.choice(a_1)
		nome += rng.choice(vogais)
	nome += rng.choice(d_1)
	nome += rng.choice(['elo', 'ilo', 'ata', 'ato'])
	return nome

def gera_tipo_2():
	global vogais

	name = ''
	name += rng.choice(vogais)
	name += rng.choice(list('lvcst'))
	name += rng.choice(vogais)
	name += rng.choice(list('rscç'))
	name += rng.choice([*vogais])
	name += rng.choice(['monte', 'l', 'r', 'z', 'ã'])
	return name

def gera_tipo_2_5():
	global vogais

	name = ''
	name += rng.choice(vogais)
	name += rng.choice(list('zls'))
	name += rng.choice(list('rsct'))
	name += rng.choice(vogais)
	name += rng.choice([*vogais])
	name += rng.choice(['monte', 'l', 'r', 'z', 'ã','s'])
	return name

def gera_tipo_3():
	global vogais

	name = ''
	for i in range(2):
		name += rng.choice(list('vslcp'))
		if rng.random() < 0.5:
			name += rng.choice(list('aeio'))
			name += rng.choice(list('lr'))
		else:
			b = list('aeio')
			i = rng.randint(0, len(b) - 1)
			name += b.pop(i)
			name += rng.choice(b)
	return name

c = ['Castelo de', 'O Calabouço', 'Masmorras', 'Catabumbas']
geradores = [gera_tipo_0, gera_tipo_1, gera_tipo_2, gera_tipo_3]

for i in range(10):
	d = rng.choice(c)
	n = rng.choice(geradores)()
	print(d + " " + n.capitalize())