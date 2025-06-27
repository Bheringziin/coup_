# Arquivo: main.py (VERSÃO CORRIGIDA E MELHORADA)

import pygame
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.game_manager import GameManager
from src.player import HumanPlayer, AIPlayer

# Importa as funções de cada tela
from inicial import rodar_tela_inicial
from login import rodar_tela_login
from jogo import rodar_tela_jogo
# Importa o setup para inicializar o Pygame, que já acontece lá dentro
import setup

def main():
    """Função principal que gerencia o estado e o loop do jogo."""
    
    # Variáveis de estado que o main vai controlar
    estado_tela = "tela_inicial"
    
    # Variáveis específicas para a tela de jogo
    # Elas precisam "viver" aqui no main para não serem resetadas
    menu_acoes_visivel = False
    game_manager = None
    
    # Relógio para controlar o FPS
    relogio = pygame.time.Clock()

    # Loop principal do jogo
    rodando = True
    while rodando:
    
        # --- Máquina de Estados ---
        # Verifica qual tela deve estar ativa e chama a função correspondente
        
        if estado_tela == "tela_inicial":
            estado_tela = rodar_tela_inicial()
   
        elif estado_tela == "tela_login":
            estado_tela = rodar_tela_login()
            if estado_tela == "tela_jogo":
                from login import texto_usuario
                players = [
                    HumanPlayer(texto_usuario or "Jogador"),
                    AIPlayer("Bot 1"),
                    AIPlayer("Bot 2"),
                    AIPlayer("Bot 3"),
                ]
                game_manager = GameManager(players)

        elif estado_tela == "tela_jogo":
            estado_tela, menu_acoes_visivel = rodar_tela_jogo(game_manager, menu_acoes_visivel)

        elif estado_tela == "sair":
            rodando = False # Quebra o loop para sair do jogo
        
        # Atualiza a tela inteira com o que foi desenhado na função de tela ativa
        pygame.display.flip()
        
        # Garante que o jogo não passe de 60 frames por segundo
        relogio.tick(60)

    # Finaliza o Pygame e fecha o programa
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()