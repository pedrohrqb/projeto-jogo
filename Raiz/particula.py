import pygame
import random

class Particula:
    def __init__(self, x, y):
        """
        Função chamada quando uma nova faísca é criada.
        """
        # Posição inicial ( O centro da explosão )
        self.x = x
        self.y = y

        # Cria uma velocidade aleatória para a explosão
        # Um valor entra -3 e 3 para a direação X
        self.vx = random.uniform(-3, 3)
        # Um valor negativo forte para a direção Y, para a explosão ir para cima
        self.vy = random.uniform(-7, -1)

        # "Vida" da particula em frames (ex: 120 frams = 2 segundos a 60fps)
        self.vida = 120
        self.tamanho = random.randint(2, 5) # Tamanho akeatório para faísca
        self.cor = (255, random.randint(150, 255), 0) # Cor aleatória entre amarelo e laranja

    def update(self):
        """
        Esta função atualiza a posição e a vida da faísca a cada frame
        """
        # Aplica uma "Gravidade" simples, puxando a partícula para baixo
        self.vy += 0.1

        # Move a partícula com base na sua velocidade
        self.x += self.vx
        self.y += self.vy

        # D iminui a vida da partícula
        self.vida -= 1

    def draw(self, tela):
        """
        Esta função desenha a faísca na tela
        """
        # Desenha a partícula como um pequeno círculo
        pygame.draw.circle(tela, self.cor, (self.x, self.y), self.tamanho)