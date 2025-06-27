# Arquivo: setup.py (VERSÃO COM CARTAS MAIORES)

import pygame
import os

# --- INICIALIZAÇÃO BÁSICA ---
pygame.init()
pygame.font.init()

# --- CONFIGURAÇÕES DA TELA ---
LARGURA_TELA, ALTURA_TELA = 800, 600
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Coup")
TELA_RECT = TELA.get_rect()

# --- CORES ---
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (200, 200, 200)
AZUL_ATIVO = (100, 149, 237)


# --- FONTES ---
FONTE_TITULO = pygame.font.Font(None, 50)
FONTE_GERAL = pygame.font.Font(None, 32)

# --- CONSTANTES DE LAYOUT ---
MARGEM = 20
ESPACAMENTO_CARTAS = 60 # AJUSTE: Um pouco mais de espaço para as cartas maiores

# --- CONFIGURAÇÃO DE RECURSOS (IMAGENS) ---
PASTA_IMAGENS = "cartas"
# AJUSTE: Novo tamanho para as cartas (10% maiores)
LARGURA_CARTA, ALTURA_CARTA = 110, 165
# AJUSTE: Tamanho das cartas reveladas também aumentado proporcionalmente
LARGURA_CARTA_REVELADA, ALTURA_CARTA_REVELADA = int(LARGURA_CARTA * 0.6), int(ALTURA_CARTA * 0.6)

def carregar_imagens_cartas():
    frente, reveladas, verso = {}, {}, None
    try:
        caminho_verso = os.path.join(PASTA_IMAGENS, 'carta_verso.png')
        verso_img = pygame.image.load(caminho_verso).convert_alpha()
        verso = pygame.transform.scale(verso_img, (LARGURA_CARTA, ALTURA_CARTA))
        
        nomes_cartas = ["duque", "assassino", "condessa", "capitao", "embaixador"]
        for nome in nomes_cartas:
            caminho_frente = os.path.join(PASTA_IMAGENS, f'{nome}.png')
            img = pygame.image.load(caminho_frente).convert_alpha()
            frente[nome] = pygame.transform.scale(img, (LARGURA_CARTA, ALTURA_CARTA))
            reveladas[nome] = pygame.transform.scale(img, (LARGURA_CARTA_REVELADA, ALTURA_CARTA_REVELADA))
    except pygame.error as e:
        print(f"ERRO ao carregar imagem: {e}")
        return None, {}, {}
    return verso, frente, reveladas

# --- RECURSOS CARREGADOS ---
CARTA_VERSO_IMG, CARTAS_FRENTE_IMGS, CARTAS_REVELADAS_IMGS = carregar_imagens_cartas()