import pygame
import os
import sys
from setup import *  # Importa tudo do setup
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.action import IncomeAction, ForeignAidAction, CoupAction
from src.player import HumanPlayer, AIPlayer
from src.game_manager import GameManager

def montar_estado(game_manager: GameManager) -> dict:
    players = game_manager.players
    descartadas = []
    if hasattr(game_manager, "_deck"):
        descartadas = [c.get("character") for c in game_manager._deck._discard_pile]

    def info_oponente(idx: int) -> dict:
        if idx < len(players):
            p = players[idx]
            return {"moedas": p.coins, "cartas": len(p.characters)}
        return {"moedas": 0, "cartas": 0}

    return {
        "rodada": len(game_manager.history) + 1,
        "ultima_acao": game_manager.history[-1] if game_manager.history else "Sua vez. Escolha uma ação.",
        "cartas_reveladas": descartadas,
        "jogador": {"moedas": players[0].coins, "cartas": players[0].characters},
        "oponentes": {
            "esquerda": info_oponente(1),
            "topo": info_oponente(2),
            "direita": info_oponente(3),
        },
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
@@ -74,91 +90,116 @@ def desenhar_info_jogador(pos_texto, moedas, cor_texto=PRETO):
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
def executar_acao(game_manager: GameManager, nome_acao: str) -> None:
    jogador = game_manager.current_player
    if nome_acao == "Renda":
        jogador.perform_action(IncomeAction(), None, game_manager)
    elif nome_acao == "Ajuda Externa":
        jogador.perform_action(ForeignAidAction(), None, game_manager)
    elif nome_acao == "Golpear":
        alvo = next((p for p in game_manager.players if p is not jogador and p.is_alive), None)
        if alvo:
            jogador.perform_action(CoupAction(), alvo, game_manager)
    game_manager.next_turn()
    while isinstance(game_manager.current_player, AIPlayer):
        game_manager.play_turn()

def rodar_tela_jogo(game_manager: GameManager, menu_visivel_atual: bool):
    menu_acoes_visivel = menu_visivel_atual
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: return "sair", menu_acoes_visivel
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if menu_acoes_visivel:
                acao_escolhida = None
                for nome, rect in botoes_do_menu.items():
                    if rect.collidepoint(evento.pos): acao_escolhida = nome; break
                if acao_escolhida:
                    executar_acao(game_manager, acao_escolhida)
                    menu_acoes_visivel = False
                elif not fundo_menu_rect.collidepoint(evento.pos): menu_acoes_visivel = False
            else:
                if botao_acao_rect.collidepoint(evento.pos): menu_acoes_visivel = True

    estado_do_jogo = montar_estado(game_manager)

    TELA.fill(BRANCO)
    TELA.blit(FONTE_GERAL.render(f"Rodada: {estado_do_jogo['rodada']}", True, PRETO), (MARGEM, MARGEM))
    
    MARGEM_MOEDAS_VERTICAL = 20 # Reduzido um pouco para melhor ajuste

    # --- Desenho dos Elementos com Posições Ajustadas ---
    
    # Jogador (Base)
    pos_base_jogador = (TELA_RECT.centerx, TELA_RECT.bottom)
    desenhar_cartas_jogador(pos_base_jogador, estado_do_jogo['jogador']['cartas'])
    desenhar_info_jogador(
        (pos_base_jogador[0], pos_base_jogador[1] - ALTURA_CARTA_JOGADOR - MARGEM_MOEDAS_VERTICAL),
        estado_do_jogo['jogador']['moedas']
    )
    
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
    desenhar_info_jogador(
        (pos_base_topo[0], pos_base_topo[1] + ALTURA_CARTA + MARGEM_MOEDAS_VERTICAL),
        estado_do_jogo['oponentes']['topo']['moedas']
    )
    
    # Cemitério (sem título)
    desenhar_cartas_reveladas(estado_do_jogo['cartas_reveladas'])
    
    # Caixa de informação (agora centralizada)
    pygame.draw.rect(TELA, (240, 240, 240), info_rect)
    pygame.draw.rect(TELA, PRETO, info_rect, 2)
    texto_acao = FONTE_ACAO.render(estado_do_jogo['ultima_acao'], True, PRETO)
    TELA.blit(texto_acao, texto_acao.get_rect(center=info_rect.center))

    # Botão de Ação e Menu
    pygame.draw.rect(TELA, CINZA, botao_acao_rect); texto_botao = FONTE_GERAL.render("Ação", True, PRETO); TELA.blit(texto_botao, texto_botao.get_rect(center=botao_acao_rect.center))
    if menu_acoes_visivel: desenhar_menu_de_acoes()
    
    return "tela_jogo", menu_acoes_visivel
