import pygame
import random
import math

# Velocidade do objeto
def alterar():
    velocidade = 0.02
    return velocidade

velocidade = alterar()

class GameObject:
    def __init__(self, x, y, tipo):
        self.tipo = tipo
        # Guarda a posição exata (com casas decimais)
        self.x = float(x)
        self.y = float(y)

        # Usado para desenho e coliões
        self.rect = pygame.Rect(x, y, 10, 10)

        # Sorteia um ângulo aletório num circulo completo
        angulo = random.uniform(0, 2 * math.pi) # 2*pi é 360 graus

        # Usa seno e coseno para converter o angulo da direcao_x e direcao_y
        self.direcao_x = math.cos(angulo)
        self.direcao_y = math.sin(angulo)

        # Garante que os objetos não fique totalmente parado
        # Sorteia a direção positiva ou negativa
        self.direcao_x = random.choice([-1, 1])
        self.direcao_y = random.choice([-1, 1])

    # Definindo as movimentações dos objetos
    def mover(self, largura_tela, altura_tela, altura_painel, velocidade_atual):
        # Define a velocidade com direção sorteada
        self.x += self.direcao_x * velocidade_atual
        self.y += self.direcao_y * velocidade_atual
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        margem = 10
            # A lógica de ricochete com a margem
        if self.rect.left <= margem or self.rect.right >= largura_tela - margem:
            self.direcao_x *= -1
        if self.rect.top <= altura_painel + margem or self.rect.bottom >= altura_tela - margem:
            self.direcao_y *= -1
        

        # Lógica de ricochete com correção de posição
        if self.rect.left <= 0:
            self.direcao_x *= -1
            self.rect.left = 1 # Empurra de volta para a posição 1
        elif self.rect.right >= largura_tela:
            self.direcao_x *= -1
            self.rect.right = largura_tela - 1 # Empurra de volta
            
        if self.rect.top <= altura_painel:
            self.direcao_y *= -1
            self.rect.top = altura_painel + 1 # Empurra para baixo
        elif self.rect.bottom >= altura_tela:
            self.direcao_y *= -1
            self.rect.bottom = altura_tela - 1 # Empurra para cima
        
    # Fazendo as figuras na tela (por enquanto será quadrados brancos)
    def desenhar(self, tela, mapa_de_cores, mapa_de_imagens, imagens_disponiveis):
        if imagens_disponiveis:
            # Se houver imagens, desenha a imagem
            imagem = mapa_de_imagens[self.tipo]
            tela.blit(imagem, self.rect)
        else:
            # Senão, desenha o quadrado colorido
            cor = mapa_de_cores[self.tipo]
            pygame.draw.rect(tela, cor, self.rect)

    # Novo método 
    def mudar_tipo(self, novo_tipo):
        self.tipo = novo_tipo