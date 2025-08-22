import pygame
import random
from objetos import GameObject
from particula import Particula

# Inicia o jogo (necessário para rodar)
pygame.init()


# Fonte padrão com tamanha 30
fonte = pygame.font.Font(None, 25)

# Definindo as dimensões da tela
largura_tela = 500
altura_tela = 500
altura_painel = 60

# Velocidade do Jogo
velocidade_inicial = 1

# Definindo propriedades do BOTÃO (START)
botao_largura = 60
botao_altura = 25
# Posiciona o botão no centro do painel, na horizontal
botao_x = (largura_tela / 2) - (botao_largura / 2)
botao_y = 30 # 30 pixels a partir do topo
botao_rect = pygame.Rect(botao_x, botao_y, botao_largura, botao_altura)

# Definindo propriedades do BOTÃO (FAST) RAPIDO
botao2_largura = 60
botao2_altura = 25
# Posiciona o botão na lateral do painel, na horizontal
botao2_x = (largura_tela / 60) - (botao2_largura / 60)
botao2_y = 30 # 30 pixels a partir do tpo
botao2_rect = pygame.Rect(botao2_x, botao2_y,botao2_largura, botao2_altura)

# Definindo propriedades do BOTÃO (SLOW) LENTO
button_slow_largura = 60
button_slow_altura = 25
# Posiciona o botão na lateral do painel, na horizontal
button_slow_x = (largura_tela / 50) + (button_slow_largura / 1)
button_slow_y = 30
button_slow_rect = pygame.Rect(button_slow_x, button_slow_y, button_slow_largura, button_slow_altura)

# Definindo propriedades do BOTÃO (RESET)
reset_button_largura = 60
reset_button_altura = 25
# Posiciona o botão na lateral direita do painel, na horizontal
reset_button_x = (largura_tela) + (reset_button_altura/ -0.4)
reset_button_y = 30 # 30 pixels a partir do topo
reset_button_rect = pygame.Rect(reset_button_x, reset_button_y, reset_button_largura, reset_button_altura)

# MAPA DE CORES 
MAPA_DE_CORES = {
    "pedra": (200, 200, 200),   # Cinza
    "papel": (0, 180, 0),       # Verde
    "tesoura": (200, 0, 0)      # Vermelho
}

# CARREGAR IMAGENS
tamanho_imagem = (25, 25) # Define o tamanhão padrão das imagens

try:
    imagem_pedra = pygame.transform.scale(pygame.image.load('D:\GitHub\projeto-jogo\Raiz\image\pedra.png'), tamanho_imagem)
    imagem_papel = pygame.transform.scale(pygame.image.load('D:\GitHub\projeto-jogo\Raiz\image\papel.png'), tamanho_imagem)
    imagem_tesoura = pygame.transform.scale(pygame.image.load('D:\GitHub\projeto-jogo\Raiz\image\\tesoura.png'), tamanho_imagem)

    mapa_de_imagens = {
        'pedra': imagem_pedra,
        'papel': imagem_papel,
        'tesoura': imagem_tesoura
    }
    usar_imagens = True
except FileNotFoundError:
    print("Aviso: Ficheiros de imagem não encontrados.")
    usar_imagens = False
 
# Criando a tela
tela = pygame.display.set_mode((largura_tela, altura_tela))

# titulo do jogo (da tela)
pygame.display.set_caption("Simulação de Pedra, Papel e Tesoura")

# CRIAÇÃO DOS OBJETOS
# Lista onde os objetos serão guardados
num_objetos = 30
def criar_objetos_iniciais():
    objetos = []
    for _ in range(num_objetos): # O _, significa que não importa o número de volta
        # Adiciona uma Pedra em posição  Canto inferior esquerdo
        objetos.append(GameObject(random.randint(0, 150), random.randint(altura_tela - 150, altura_tela - tamanho_imagem[1]), "pedra"))
        # Adiciona um Papel em posição Canto inferior direito
        objetos.append(GameObject(random.randint(largura_tela - 150, largura_tela- tamanho_imagem[0]), 
        random.randint(altura_tela - 150, altura_tela - tamanho_imagem[1]), "papel"))
        # Adiciona uma Tesooura em posição Abaixo do painel
        objetos.append(GameObject(random.randint(int(largura_tela / 2 - 75), int(largura_tela / 2 + 75)),
        random.randint(altura_painel, altura_painel + 100), "tesoura"))
    return objetos
objetos = criar_objetos_iniciais()

# Criando o Loop do Jogo
rodando = True
jogo_iniciado = False #Chave geral, o Jogo começa desligado.
vencedor = None
velocidade_atual = velocidade_inicial
lista_particulas = []
explosao_iniciada = False

while rodando:
    # Este 'for' verifica todos os eventos que etão acontecendo
    for evento in pygame.event.get():
        # Se o evento for clicar no 'X' da janela, irá fechar o "jogo"(tela).
        if evento.type == pygame.QUIT:
            rodando = False

        # Lógica do clique do BOTÃO PLAY
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # ..e o jogo ainda não tiver começado
            if not jogo_iniciado:
                # ...e a posição do clique (evento.pos) estiver dentro do retângulo do botão...
                if botao_rect.collidepoint(evento.pos):
                    #... então, LIGUE A CHAVE GERAL!
                    jogo_iniciado = True
        
            # Lógica do BOTÃO RESET
            if reset_button_rect.collidepoint(evento.pos):
                # Chame a função parar criar os objetos de novo
                objetos = criar_objetos_iniciais()
                # E "desligue" as chaves do jogo para voltar ao estado inicial.
                jogo_iniciado = False
                vencedor = None
                lista_particulas = []
                explosao_iniciada = False

            # Lógica do BOTÃO SLOW        
            if button_slow_rect.collidepoint(evento.pos):
                velocidade_atual = 0.03
            
            # Lógica do BOTÃO FAST
            if botao2_rect.collidepoint(evento.pos):
                velocidade_atual = 0.08


    # Pinta o fundo da tela de preto
    tela.fill((0, 0, 0))

    # Desenha uma linha branca para separar o painel do jogo
    pygame.draw.line(tela, (255, 255, 255), (0, altura_painel), (largura_tela, altura_painel))

    if jogo_iniciado:
        # Lógica de Colisão
        for i in range(len(objetos)):
            # irá comparar com todos os outros objetos que vêm depois dele na lista
            for j in range(i +1, len(objetos)):
                obj1 = objetos[i]
                obj2 = objetos[j]

                # Se os retângulos (objetos) sse tocam E eles são de tipos diferentes...
                if obj1.rect.colliderect(obj2.rect) and obj1.tipo != obj2.tipo:
                    # aplicar as regras do jogo
                    if (obj1.tipo == 'pedra' and obj2.tipo == 'tesoura') or \
                    (obj1.tipo == 'tesoura' and obj2.tipo == 'papel') or \
                    (obj1.tipo == 'papel' and obj2.tipo == 'pedra'):
                        #obj1 ganha, então obj2 muda de tipo
                        obj2.mudar_tipo(obj1.tipo)
                    else:
                        # Se não, obj2 ganha, e obj1 muda de tipo
                        obj1.mudar_tipo(obj2.tipo)
        # Lógica de movimento, somente irá se movimentar se a variável "jogo_iniciado" virar TRUE
        for obj in objetos:
            obj.mover(largura_tela, altura_tela, altura_painel, velocidade_atual)
    
    # Desenho dos OBJETOS na TELA
    for obj in objetos:
        obj.desenhar(tela, MAPA_DE_CORES, mapa_de_imagens, usar_imagens)
    

    # PLACAR
    # Contagem
    contagem = {'pedra': 0, 'papel': 0, 'tesoura': 0}
    for obj in objetos:
        contagem[obj.tipo] +=1 # Adiciona +1 ao tipo correspondente
    
    # VERIFICAÇÃO DE VITÓRIA
    if not vencedor:
        total_objetos = num_objetos * 3
        if contagem['pedra'] == total_objetos:
            vencedor = 'PEDRA'
        elif contagem['papel'] == total_objetos:
            vencedor = 'PAPEL'
        elif contagem['tesoura'] == total_objetos:
            vencedor = 'TESOURA'

    # LÓGICA DA EXPLOSÃO DE VITÓRIA
    if vencedor and not explosao_iniciada:
        for _ in range(100):
            # A explosão acontece no centro da tela
            lista_particulas.append(Particula(largura_tela / 2, altura_tela / 2))
        
        # Avisamos que a explosão já foi iniciada ( para não criar mais)
        
    
    # MENSAGEM DE VITÓRIA
    if vencedor:
        # Fonte maior para mensagem
        fonte_grande = pygame.font.Font(None, 60)
        texto_vitoria = fonte_grande.render(f'{vencedor} VENCEU!', True, (255, 215, 0)) # Cor dourada

        # Centraliza o texto no meio da tela
        texto_rect = texto_vitoria.get_rect(center=(largura_tela/2, altura_tela/2))

        tela.blit(texto_vitoria, texto_rect)

    # Prepando o texto para ser desenhado
    # O metodo .render() cria uma "imagem" do texto
    texto_pedra = fonte.render(f'Pedra: {contagem['pedra']}', True, MAPA_DE_CORES['pedra'])
    texto_papel = fonte.render(f'Papel: {contagem['papel']}', True, MAPA_DE_CORES['papel'])
    texto_tesoura = fonte.render(f'Tesoura: {contagem['tesoura']}', True, MAPA_DE_CORES['tesoura'])

    # Desenha a "imagem" do texto na tela
    # O método .blit() cola uma imagem em cima da outra. Aqui, cola o texto na tela.
    tela.blit(texto_pedra, (10, 5)) # Posição (x, y) = (10, 5)
    tela.blit(texto_papel, (200, 5)) # Mais para o lado
    tela.blit(texto_tesoura, (400, 5)) # Mais para o lado

    # BOTÃO
    # Só desenha o botão se o jogo AINDA NÃO começou
    if not jogo_iniciado:
        # Deenha o retângulo do botão
        pygame.draw.rect(tela, (0, 200, 0), botao_rect) # Um retângulo verde

        # Prepara o texto "jogar"
        texto_botao = fonte.render("PLAY", True, (255, 255, 255)) # Texto branco

        # Pega o retângulo do text opara poder centralizá-lo
        texto_rect = texto_botao.get_rect(center=botao_rect.center)

        # Desenha o texto na tela
        tela.blit(texto_botao, texto_rect)

    # BOTÃO DE ACELERAR O JOGO
    # Desenha o retângulo do botão
    pygame.draw.rect(tela, (255, 200, 0), botao2_rect) # Um retângulo verde
    # Prepara o texto "jogar"
    texto_botao2 = fonte.render("FAST", True, (255, 255, 255)) # Texto branco
    # Pega o retângulo do text opara poder centralizá-lo
    texto_rect = texto_botao2.get_rect(center=botao2_rect.center)
    # Desenha o texto na tela
    tela.blit(texto_botao2, texto_rect)

    # BOTÃO DE DESACELERAR O JOGO
    # Desenha o retângulo do botão
    pygame.draw.rect(tela, (255, 200, 0), button_slow_rect) # Um retângulo verde
    # Prepara o texto "jogar"
    texto_button_slow = fonte.render("SLOW", True, (255, 255, 255)) # Texto branco
    # Pega o retângulo do text opara poder centralizá-lo
    texto_rect = texto_button_slow.get_rect(center=button_slow_rect.center)
    # Desenha o texto na tela
    tela.blit(texto_button_slow, texto_rect)

    # BOTÃO DE REINICIAR O JOGO
    # Desenha o retângulo do botão
    pygame.draw.rect(tela, (255, 200, 0), reset_button_rect) # Um retângulo verde
    # Prepara o texto "jogar"
    texto_reset_button = fonte.render("RESET", True, (255, 255, 255)) # Texto branco
    # Pega o retângulo do text opara poder centralizá-lo
    texto_rect = texto_reset_button.get_rect(center=reset_button_rect.center)
    # Desenha o texto na tela
    tela.blit(texto_reset_button, texto_rect)
    
    # Atualização e desenho das PARTICULAS
    # Percorre a lista de partículas que estão "vivas"
    for particula in lista_particulas[:]: # O [:] cria uma cópia segura da lista
        particula.update()
        particula.draw(tela)

        # Se a "vida" da particula acabou...
        if particula.vida <= 0:
            lista_particulas.remove(particula)

    # Atualiza a tela para mostrar o que foi desenhado
    pygame.display.flip()

# Finaliza o Jogo
pygame.quit()
