# Arquivo: main.py (VERSÃO CORRIGIDA E MELHORADA)

import pygame
import sys

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

        elif estado_tela == "tela_jogo":
            # AQUI ESTÁ A CORREÇÃO:
            # Passamos o estado do menu para a função...
            # ...e recebemos de volta o novo estado da tela e o novo estado do menu.
            estado_tela, menu_acoes_visivel = rodar_tela_jogo(menu_acoes_visivel)

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