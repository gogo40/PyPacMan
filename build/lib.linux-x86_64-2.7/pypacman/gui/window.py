# -*- coding: utf-8 -*-

"""
PyPacMan
Copyright (c) 2013 - Péricles Lopes Machado

This file is distributed under the MIT license. See LICENSE for details.
"""

import sys, pygame
from pypacman.ai import *

"""
Implementação da janela de visualização do jogo
"""
class Window:
	def __init__(self, G, ai):
		self.ai = ai
		self.delay  = 100
		#dimensao da celula
		self.dim_cell = 15

		#velocidade da celula
		self.speed = self.dim_cell

		#dimensao da tela
		self.n_cell = len(G);
		self.m_cell = len(G[0]);

		self.size = self.width, self.height = self.dim_cell * len(G[0]), self.dim_cell * len(G)

		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption('PyPacMan')
		
		#cor do fundo
		self.color = 0, 0, 0


		#elementos do jogo
		self.empty = pygame.Surface((self.dim_cell, self.dim_cell))
		self.empty.fill(self.color)

		self.pacmano = pygame.image.load("imgs/pacman.png")
		self.pacman = self.pacmano = pygame.transform.smoothscale(self.pacmano, (self.dim_cell, self.dim_cell))

		self.fruta = pygame.image.load("imgs/fruta.png")
		self.fruta = pygame.transform.smoothscale(self.fruta, (self.dim_cell, self.dim_cell))
		
		self.fantasma = [
			pygame.image.load("imgs/fantasma1.png"),
			pygame.image.load("imgs/fantasma2.png"),
			pygame.image.load("imgs/fantasma3.png"),
			pygame.image.load("imgs/fantasma4.png")
		]

		self.fantasma[0] = pygame.transform.smoothscale(self.fantasma[0], (self.dim_cell, self.dim_cell))
		self.fantasma[1] = pygame.transform.smoothscale(self.fantasma[1], (self.dim_cell, self.dim_cell))
		self.fantasma[2] = pygame.transform.smoothscale(self.fantasma[2], (self.dim_cell, self.dim_cell))
		self.fantasma[3] = pygame.transform.smoothscale(self.fantasma[3], (self.dim_cell, self.dim_cell))

		self.parede = pygame.image.load("imgs/parede.png")
		self.parede = pygame.transform.smoothscale(self.parede, (self.dim_cell, self.dim_cell))

		self.position = self.pacmano.get_rect()
		self.real_pos_pac_man = [0, 0] 
		self.d = [0, 0]
		self.dr = [0, 0]
		self.addGrid(G)

	"""
	Adiciona grade do jogo
	"""
	def addGrid(self, G):
		self.G = G

	"""
	Pinta a tela do jogo
	"""
	def paintGrid(self):	
		for x in range(0, len(self.G[0])):
			for y in range(0, len(self.G)):
				if self.G[y][x] == '#':
					self.position = self.parede.get_rect()
					self.position = self.position.move(x * self.dim_cell, y * self.dim_cell)
					self.screen.blit(self.parede, self.position)
				elif self.G[y][x] == '+':
					self.position = self.pacman.get_rect()
					self.real_pos_pac_man = [y, x]
					self.position_pac_man = self.position.move(x * self.dim_cell, y * self.dim_cell)
					self.screen.blit(self.pacman, self.position_pac_man)
				elif self.G[y][x] == 'x' or self.G[y][x] == '*':
					self.position = self.fantasma[(x+y)%4].get_rect()
					self.position = self.position.move(x * self.dim_cell, y * self.dim_cell)
					self.screen.blit(self.fantasma[(x+y)%4], self.position)
				elif self.G[y][x] == 'o':
					self.position = self.fruta.get_rect()
					self.position = self.position.move(x * self.dim_cell, y * self.dim_cell)
					self.screen.blit(self.fruta, self.position)

	"""
	Atualiza posicao do pacman
	"""
	def move_pac_man(self):		
		self.position = self.position_pac_man 
		real_pos = self.real_pos_pac_man

		x = (real_pos[0] + self.dr[0] + self.n_cell) % self.n_cell;
		y = (real_pos[1] + self.dr[1] + self.m_cell) % self.m_cell;
		
		if self.G[x][y] == '.' or self.G[x][y] == 'o':
			self.real_pos_pac_man = [x, y]
			self.screen.blit(self.empty, self.position)
			
			l = list(self.G[real_pos[0]]);
			l[real_pos[1]]='.';
			self.G[real_pos[0]]="".join(l);

			l = list(self.G[x]);
			l[y]='+';
			self.G[x]="".join(l);

			N = self.dim_cell * self.n_cell
			M = self.dim_cell * self.m_cell

			self.position_pac_man[0] = (self.position[0] + self.d[0] + M) % M
			self.position_pac_man[1] = (self.position[1] + self.d[1] + N) % N

			self.screen.blit(self.pacman, self.position_pac_man)

			pygame.display.flip()

	"""
	Roda renderização do jogo e captura de movimentos do jogador e da AI
	"""
	def run(self):
		self.screen.fill(self.color)
		self.paintGrid()
		pygame.display.flip()
		
		is_running = True
		while is_running:
			for event in pygame.event.get():
				#Fecha janela
				if event.type == pygame.QUIT: 
					is_running = False
					break

				#Trata eventos da AI
				elif event.type == pygame.USEREVENT:

					#imprime grade
					if event.action == ai_control.PRINT_G:
						G = event.value
						for x in range(0, len(G)):
							print G[x]

					#imprime fantasmas
					elif event.action == ai_control.PRINT_P:
						print "Phatoms:"
						print event.value

					#move fantasma
					elif event.action == ai_control.MOVE_P:
						mov = event.value
						orig = event.origin
						dest = event.dest

						print "Move:"
						print mov
						print "orig:"
						print orig
						print "dest:"
						print dest

				#Trata Entrada de usuario
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						is_running = False
						break
					elif event.key == pygame.K_LEFT:
						self.d[0] = -self.speed
						self.d[1] = 0

						self.dr[1] = -1
						self.dr[0] = 0

						self.pacman = pygame.transform.rotate(self.pacmano, 360)
					elif event.key == pygame.K_RIGHT:
						self.d[0] = self.speed
						self.d[1] = 0

						self.dr[1] = 1
						self.dr[0] = 0

						self.pacman = pygame.transform.rotate(self.pacmano, 180)
					elif event.key == pygame.K_UP:
						self.d[0] = 0
						self.d[1] = -self.speed

						self.dr[1] = 0
						self.dr[0] = -1

						self.pacman = pygame.transform.rotate(self.pacmano, 270)
					elif event.key == pygame.K_DOWN:
						self.d[0] = 0
						self.d[1] = self.speed

						self.dr[1] = 0
						self.dr[0] = 1

						self.pacman = pygame.transform.rotate(self.pacmano, 90)
				
			
			#Move o pac man
			self.move_pac_man()

			#Dorme um pouco
			pygame.time.delay(self.delay)

		#Desliga AI
		self.ai.call_exit()
			



