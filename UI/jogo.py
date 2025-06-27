import pygame
import os
from setup import * # Importa tudo do setup

# --- DADOS DO JOGO (Simulação) ---
estado_do_jogo = {
    "rodada": 1,
    "ultima_acao": "Sua vez. Escolha uma ação.",
    "cartas_reveladas": ["condessa", "capitao"],
    "jogador": { "moedas": 2, "cartas": ["duque", "assassino"] },
    "oponentes": {
        "topo": {"moedas": 2, "cartas": 2},
        "esquerda": {"moedas": 2, "cartas": 2},
        "direita": {"moedas": 2, "cartas": 2}
    }
}

# --- ELEMENTOS DA INTERFACE (Reorganizados) ---
info_rect = pygame.Rect(0, 0, 450, 60)
# NOVA ALTERAÇÃO 2: Caixa de informação movida para o centro vertical exato
info_rect.center = (TELA_RECT.centerx, TELA_RECT.centery)
FONTE_ACAO = pygame.font.Font(None, 28)

LARGURA_CARTA_JOGADOR = int(LARGURA_CARTA * 1.2)
ALTURA_CARTA_JOGADOR = int(ALTURA_CARTA * 1.2)
ESPACAMENTO_JOGADOR = int(ESPACAMENTO_CARTAS * 1.2)

CARTAS_JOGADOR_GRANDES = {
    nome: pygame.transform.scale(img, (LARGURA_CARTA_JOGADOR, ALTURA_CARTA_JOGADOR))
    for nome, img in CARTAS_FRENTE_IMGS.items()
}

botao_acao_rect = pygame.Rect(0, 0, 150, 60)
botao_acao_rect.bottomright = (TELA_RECT.right - MARGEM, TELA_RECT.bottom - MARGEM)
fundo_menu_rect = pygame.Rect(0, 0, 400, 400)
fundo_menu_rect.center = TELA_RECT.center
botoes_do_menu = {
    "Renda": pygame.Rect(0, 0, 300, 50), "Ajuda Externa": pygame.Rect(0, 0, 300, 50),
    "Golpear": pygame.Rect(0, 0, 300, 50)
}
botoes_do_menu["Renda"].center = (fundo_menu_rect.centerx, fundo_menu_rect.y + 100)
botoes_do_menu["Ajuda Externa"].center = (fundo_menu_rect.centerx, fundo_menu_rect.y + 160)
botoes_do_menu["Golpear"].center = (fundo_menu_rect.centerx, fundo_menu_rect.y + 220)


# --- FUNÇÕES DE DESENHO AUXILIARES (Refatoradas) ---

def desenhar_cartas_oponente(pos_base, quantidade, angulo=0):
    if not quantidade > 0: return
    imagens_cartas = [CARTA_VERSO_IMG] * quantidade
    total_largura = (quantidade - 1) * ESPACAMENTO_CARTAS + LARGURA_CARTA
    for i, imagem in enumerate(imagens_cartas):
        carta_rotacionada = pygame.transform.rotate(imagem, angulo)
        rect = carta_rotacionada.get_rect()
        if angulo == 180: rect.midtop = (pos_base[0] - total_largura/2 + LARGURA_CARTA/2 + i * ESPACAMENTO_CARTAS, pos_base[1])
        elif angulo == 90: rect.midleft = (pos_base[0], pos_base[1] - total_largura/2 + LARGURA_CARTA/2 + i * ESPACAMENTO_CARTAS)
        elif angulo == 270: rect.midright = (pos_base[0], pos_base[1] - total_largura/2 + LARGURA_CARTA/2 + i * ESPACAMENTO_CARTAS)
        TELA.blit(carta_rotacionada, rect)

def desenhar_cartas_jogador(pos_base, lista_cartas):
    if not lista_cartas: return
    quantidade = len(lista_cartas)
    imagens_cartas = [CARTAS_JOGADOR_GRANDES.get(nome) for nome in lista_cartas]
    total_largura = (quantidade - 1) * ESPACAMENTO_JOGADOR + LARGURA_CARTA_JOGADOR
    for i, imagem in enumerate(imagens_cartas):
        if imagem:
            rect = imagem.get_rect()
            rect.midbottom = (pos_base[0] - total_largura/2 + LARGURA_CARTA_JOGADOR/2 + i * ESPACAMENTO_JOGADOR, pos_base[1])
            TELA.blit(imagem, rect)

def desenhar_info_jogador(pos_texto, moedas, cor_texto=PRETO):
    texto_moedas = FONTE_GERAL.render(f"Moedas: {moedas}", True, cor_texto)
    rect_texto = texto_moedas.get_rect(center=pos_texto)
    TELA.blit(texto_moedas, rect_texto)

def desenhar_cartas_reveladas(lista_cartas):
    if not lista_cartas: return
    
    # NOVA ALTERAÇÃO 2: Posição inicial ajustada e título removido
    start_x = MARGEM
    pos_y = MARGEM * 3
    
    espacamento_reveladas = LARGURA_CARTA_REVELADA * 0.4 

    for i, nome_carta in enumerate(lista_cartas):
        imagem = CARTAS_REVELADAS_IMGS.get(nome_carta)
        if imagem:
            TELA.blit(imagem, (start_x + i * espacamento_reveladas, pos_y))

def desenhar_menu_de_acoes():
    fundo_transparente = pygame.Surface(TELA.get_size(), pygame.SRCALPHA); fundo_transparente.fill((0, 0, 0, 180)); TELA.blit(fundo_transparente, (0, 0))
    pygame.draw.rect(TELA, BRANCO, fundo_menu_rect); pygame.draw.rect(TELA, PRETO, fundo_menu_rect, 2)
    texto_titulo = FONTE_TITULO.render("Ações", True, PRETO); rect_titulo = texto_titulo.get_rect(center=(fundo_menu_rect.centerx, fundo_menu_rect.y + 40)); TELA.blit(texto_titulo, rect_titulo)
    for nome_acao, rect_acao in botoes_do_menu.items():
        pygame.draw.rect(TELA, CINZA, rect_acao); texto_acao = FONTE_GERAL.render(nome_acao, True, PRETO); rect_texto_acao = texto_acao.get_rect(center=rect_acao.center); TELA.blit(texto_acao, rect_texto_acao)


# --- FUNÇÃO PRINCIPAL DO MÓDULO ---
def rodar_tela_jogo(menu_visivel_atual):
    menu_acoes_visivel = menu_visivel_atual
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: return "sair", menu_acoes_visivel
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if menu_acoes_visivel:
                acao_escolhida = None
                for nome, rect in botoes_do_menu.items():
                    if rect.collidepoint(evento.pos): acao_escolhida = nome; break
                if acao_escolhida: estado_do_jogo["ultima_acao"] = f"Você usou: {acao_escolhida}"; menu_acoes_visivel = False
                elif not fundo_menu_rect.collidepoint(evento.pos): menu_acoes_visivel = False
            else:
                if botao_acao_rect.collidepoint(evento.pos): menu_acoes_visivel = True

    TELA.fill(BRANCO)
    TELA.blit(FONTE_GERAL.render(f"Rodada: {estado_do_jogo['rodada']}", True, PRETO), (MARGEM, MARGEM))
    
    MARGEM_MOEDAS_VERTICAL = 20 # Reduzido um pouco para melhor ajuste

    # --- Desenho dos Elementos com Posições Ajustadas ---
    
    # Jogador (Base)
    pos_base_jogador = (TELA_RECT.centerx, TELA_RECT.bottom)
    desenhar_cartas_jogador(pos_base_jogador, estado_do_jogo['jogador']['cartas'])
    desenhar_info_jogador((pos_base_jogador[0], pos_base_jogador[1] - ALTURA_CARTA_JOGADOR - MARGEM_MOEDAS_VERTICAL), estado_do_jogo['jogador']['moedas'])
    
    # Oponente Esquerda
    pos_base_esquerda = (TELA_RECT.left, TELA_RECT.centery)
    qtd_cartas_esq = estado_do_jogo['oponentes']['esquerda']['cartas']
    desenhar_cartas_oponente(pos_base_esquerda, qtd_cartas_esq, 90)
    # NOVA ALTERAÇÃO 2: Posição das moedas alinhada verticalmente com as cartas, mas posicionada abaixo
    if qtd_cartas_esq > 0:
        spread_vertical_esq = (qtd_cartas_esq - 1) * ESPACAMENTO_CARTAS + LARGURA_CARTA
        pos_y_moedas_esq = TELA_RECT.centery + spread_vertical_esq / 2 + MARGEM_MOEDAS_VERTICAL
        pos_x_moedas_esq = pos_base_esquerda[0] + ALTURA_CARTA / 2 
        desenhar_info_jogador((pos_x_moedas_esq, pos_y_moedas_esq), estado_do_jogo['oponentes']['esquerda']['moedas'])

    # Oponente Direita
    pos_base_direita = (TELA_RECT.right, TELA_RECT.centery)
    qtd_cartas_dir = estado_do_jogo['oponentes']['direita']['cartas']
    desenhar_cartas_oponente(pos_base_direita, qtd_cartas_dir, 270)
    # NOVA ALTERAÇÃO 2: Posição das moedas alinhada verticalmente com as cartas, mas posicionada abaixo
    if qtd_cartas_dir > 0:
        spread_vertical_dir = (qtd_cartas_dir - 1) * ESPACAMENTO_CARTAS + LARGURA_CARTA
        pos_y_moedas_dir = TELA_RECT.centery + spread_vertical_dir / 2 + MARGEM_MOEDAS_VERTICAL
        pos_x_moedas_dir = pos_base_direita[0] - ALTURA_CARTA / 2
        desenhar_info_jogador((pos_x_moedas_dir, pos_y_moedas_dir), estado_do_jogo['oponentes']['direita']['moedas'])
    
    # Oponente Topo
    pos_base_topo = (TELA_RECT.centerx, TELA_RECT.top)
    desenhar_cartas_oponente(pos_base_topo, estado_do_jogo['oponentes']['topo']['cartas'], 180)
    desenhar_info_jogador((pos_base_topo[0], pos_base_topo[1] + ALTURA_CARTA + MARGEM_MOEDAS_VERTICAL), estado_do_jogo['oponentes']['topo']['moedas'])
    
    # Cemitério (sem título)
    desenhar_cartas_reveladas(estado_do_jogo['cartas_reveladas'])
    
    # Caixa de informação (agora centralizada)
    pygame.draw.rect(TELA, (240, 240, 240), info_rect); pygame.draw.rect(TELA, PRETO, info_rect, 2)
    texto_acao = FONTE_ACAO.render(estado_do_jogo['ultima_acao'], True, PRETO)
    TELA.blit(texto_acao, texto_acao.get_rect(center=info_rect.center))

    # Botão de Ação e Menu
    pygame.draw.rect(TELA, CINZA, botao_acao_rect); texto_botao = FONTE_GERAL.render("Ação", True, PRETO); TELA.blit(texto_botao, texto_botao.get_rect(center=botao_acao_rect.center))
    if menu_acoes_visivel: desenhar_menu_de_acoes()
    
    return "tela_jogo", menu_acoes_visivel