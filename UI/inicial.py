import pygame
from setup import TELA, BRANCO, CINZA, PRETO, FONTE_TITULO, FONTE_GERAL

botao_iniciar_rect = pygame.Rect(300, 400, 200, 70)

def rodar_tela_inicial():
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return "sair"  
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if botao_iniciar_rect.collidepoint(evento.pos):
                return "tela_login" 
            
    TELA.fill(BRANCO)
    texto_titulo = FONTE_TITULO.render("Coup", True, PRETO)
    TELA.blit(texto_titulo, (TELA.get_width()/2 - texto_titulo.get_width()/2, 150))
    

    pygame.draw.rect(TELA, CINZA, botao_iniciar_rect)
    texto_botao = FONTE_GERAL.render("Iniciar", True, PRETO)
    TELA.blit(texto_botao, (botao_iniciar_rect.centerx - texto_botao.get_width()/2, botao_iniciar_rect.centery - texto_botao.get_height()/2))

    return "tela_inicial" 