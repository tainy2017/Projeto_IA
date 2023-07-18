import pygame
import queue
import mapas
from button import Button

# Dimensões da janela e do mapa
largura_janela = 950
altura_janela = 720
tamanho_celula = 50
largura_mapa = largura_janela // tamanho_celula
altura_mapa = altura_janela // tamanho_celula

# Cores
COR_FUNDO = (255, 255, 255)
COR_PAREDE = (0, 0, 0)
COR_CAMINHO = (0, 255, 0)
COR_INICIO = (255, 0, 0)
COR_OBJETIVO = (0, 0, 255)

# Função para fazer o cálculo da heuristica usada no algoritmo A*
def calcular_heuristica(pos_atual, pos_objetivo):
    return abs(pos_atual[0] - pos_objetivo[0]) + abs(pos_atual[1] - pos_objetivo[1])

# Código referente ao algoritmo A*
def a_estrela(mapa, inicio, objetivo):
    def dentro_limites(pos):
        return 0 <= pos[0] < altura_mapa and 0 <= pos[1] < largura_mapa

    def obter_vizinhos(pos):
        vizinhos = [(pos[0]-1, pos[1]), (pos[0]+1, pos[1]),
                    (pos[0], pos[1]-1), (pos[0], pos[1]+1)]
        return [vizinho for vizinho in vizinhos if dentro_limites(vizinho) and mapa[vizinho[0]][vizinho[1]] != '#']

    custos = [[float('inf')] *
              largura_mapa for _ in range(altura_mapa)]
    custos[inicio[0]][inicio[1]] = 0
    pais = [[None] * largura_mapa for _ in range(altura_mapa)]
    pais[inicio[0]][inicio[1]] = inicio

    fila_prioridade = queue.PriorityQueue()
    fila_prioridade.put((0, inicio))

    while not fila_prioridade.empty():
        _, pos_atual = fila_prioridade.get()

        if pos_atual == objetivo:
            caminho = []
            pos = objetivo
            while pos != inicio:
                caminho.append(pos)
                pos = pais[pos[0]][pos[1]]
            caminho.append(inicio)
            caminho.reverse()
            return caminho

        for vizinho in obter_vizinhos(pos_atual):
            novo_custo = custos[pos_atual[0]][pos_atual[1]] + 1

            if novo_custo < custos[vizinho[0]][vizinho[1]]:
                custos[vizinho[0]][vizinho[1]] = novo_custo
                prioridade = novo_custo + \
                    calcular_heuristica(vizinho, objetivo)
                fila_prioridade.put((prioridade, vizinho))
                pais[vizinho[0]][vizinho[1]] = pos_atual

    return None

# Função para desenhar o mapa na tela
def desenhar_mapa(mapa, janela):
    for i in range(12): # Altura da matriz (mapa)
        for j in range(18): # Largura da matriz (mapa)
            if mapa[i][j] == '#':
                cor = COR_PAREDE
            elif mapa[i][j] == '$':
                cor = COR_INICIO
            elif mapa[i][j] == ' ':
                cor = COR_FUNDO
            elif mapa[i][j] == 'D':
                cor = COR_OBJETIVO
            else:
                COR_FUNDO
            pygame.draw.rect(janela, cor, (j * tamanho_celula, i * tamanho_celula, tamanho_celula, tamanho_celula))

    pygame.display.flip()

# Função para desenhar o caminho na tela
def desenhar_caminho(caminho, janela):
    for pos in caminho:
        pygame.draw.rect(janela, COR_CAMINHO, (
            pos[1] * tamanho_celula, pos[0] * tamanho_celula, tamanho_celula, tamanho_celula))
        pygame.display.flip()
        pygame.time.wait(400)
        

def play():
   # Mapa
    mapa = [
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['$', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    [' ', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#', '#', '#', '#', '#', ' ', '#', '#', ' ', '#'],
    [' ', ' ', ' ', ' ', ' ', '#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', '#', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#'],
    ['#', '#', '#', '#', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', '#', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', '#', '#', '#', ' ', ' ', ' ', '#', '#', '#', '#', '#', ' ', '#', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', '#', '#', '#', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'D', ' ', ' ', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
]

    inicio = (1, 1)
    objetivo = (11, 15)

    # Inicialização do Pygame
    pygame.init()
    janela = pygame.display.set_mode((largura_janela, altura_janela))
    pygame.display.set_caption('Mapa')

    # Desenha o mapa
    desenhar_mapa(mapa,janela)

    # Executa o algoritmo A* e desenha o caminho até o objetivo
    caminho = a_estrela(mapa, inicio, objetivo)
    if caminho:
        desenhar_caminho(caminho, janela)
    else:
        print("Não foi possível encontrar um caminho válido.")

    # Loop principal do jogo
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
