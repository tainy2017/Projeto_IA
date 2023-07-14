import pygame
import queue
import labirintos
from button import Button

# Dimensões da janela e do labirinto
largura_janela = 1280
altura_janela = 720
tamanho_celula = 60
largura_labirinto = largura_janela // tamanho_celula
altura_labirinto = altura_janela // tamanho_celula

# Cores
COR_FUNDO = (255, 255, 255)
COR_PAREDE = (0, 0, 0)
COR_CAMINHO = (0, 255, 0)
COR_INICIO = (155, 0, 155)
COR_OBJETIVO = (0, 0, 255)


def calcular_heuristica(pos_atual, pos_objetivo):
    return abs(pos_atual[0] - pos_objetivo[0]) + abs(pos_atual[1] - pos_objetivo[1])


def a_estrela(labirinto, inicio, objetivo):
    def dentro_limites(pos):
        return 0 <= pos[0] < altura_labirinto and 0 <= pos[1] < largura_labirinto

    def obter_vizinhos(pos):
        vizinhos = [(pos[0]-1, pos[1]), (pos[0]+1, pos[1]),
                    (pos[0], pos[1]-1), (pos[0], pos[1]+1)]
        return [vizinho for vizinho in vizinhos if dentro_limites(vizinho) and labirinto[vizinho[0]][vizinho[1]] != '#']

    custos = [[float('inf')] *
              largura_labirinto for _ in range(altura_labirinto)]
    custos[inicio[0]][inicio[1]] = 0
    pais = [[None] * largura_labirinto for _ in range(altura_labirinto)]
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

# Função para desenhar o labirinto na tela


def desenhar_labirinto(labirinto, janela):
    for i in range(12):
        for j in range(16):
            if labirinto[i][j] == '#':
                cor = COR_PAREDE
            elif labirinto[i][j] == ' ':
                cor = COR_FUNDO
            elif labirinto[i][j] == 'D':
                cor = COR_OBJETIVO
            elif labirinto[i][j] == '$':
                cor = COR_INICIO
            else:
                COR_FUNDO
            pygame.draw.rect(janela, cor, (j * tamanho_celula,
                                           i * tamanho_celula, tamanho_celula, tamanho_celula))

    pygame.display.flip()

# Função para desenhar o caminho na tela


def desenhar_caminho(caminho, janela):
    for pos in caminho:
        pygame.draw.rect(janela, COR_CAMINHO, (
            pos[1] * tamanho_celula, pos[0] * tamanho_celula, tamanho_celula, tamanho_celula))
        pygame.display.flip()
        pygame.time.wait(200)
        

def play():
    # Labirinto de exemplo

    labirinto = [
        ['$', '#', '#', '#', '#', '#', '#', '#',
            '#', '#', '#', '#', '#', '#', '#', '#'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
            ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', ' ', '#', ' ', '#', ' ', '#', '#',
            '#', ' ', '#', '#', '#', ' ', ' ', '#'],
        ['#', ' ', '#', ' ', '#', ' ', ' ', ' ',
            '#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', ' ', '#', '#', '#', '#', '#', '#',
            '#', ' ', '#', '#', ' ', '#', ' ', '#'],
        ['#', ' ', '#', ' ', ' ', ' ', ' ', ' ',
            ' ', ' ', ' ', ' ', ' ', '#', ' ', '#'],
        ['#', ' ', '#', '#', '#', '#', '#', '#',
            '#', '#', '#', '#', '#', '#', ' ', '#'],
        ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
            ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', '#', '#', '#', '#', '#', ' ', '#',
            '#', '#', '#', '#', '#', '#', ' ', '#'],
        ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
            ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', '#', ' ', '#', '#', '#', '#', '#',
            '#', '#', ' ', '#', '#', '#', ' ', '#'],
        ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
            ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'D'],
        ['#', '#', '#', '#', '#', '#', '#', '#',
            '#', '#', '#', '#', '#', '#', '#', '#'],

    ]

    inicio = (1, 0)
    objetivo = (11, 15)

    # Inicialização do Pygame
    pygame.init()
    janela = pygame.display.set_mode((largura_janela, altura_janela))
    pygame.display.set_caption('Labirinto')

    # Desenha o labirinto inicial
    desenhar_labirinto(labirinto,janela)

    # Executa o algoritmo A* e desenha o caminho encontrado
    caminho = a_estrela(labirinto, inicio, objetivo)
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
