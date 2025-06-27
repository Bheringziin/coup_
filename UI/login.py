import pygame
from setup import TELA, BRANCO, PRETO, CINZA, AZUL_ATIVO, FONTE_TITULO, FONTE_GERAL

# Elementos da UI e estado da Tela de Login
input_usuario_rect = pygame.Rect(250, 250, 300, 50)
botao_confirmar_rect = pygame.Rect(300, 350, 200, 60)
texto_usuario = ""
input_ativo = False

def rodar_tela_login():
    """
    Função para rodar a lógica e o desenho da tela de login.
    Retorna o próximo estado do jogo.
    """
    global texto_usuario, input_ativo # Usamos 'global' para modificar as variáveis do módulo

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return "sair"
            
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if input_usuario_rect.collidepoint(evento.pos):
                input_ativo = True
            elif botao_confirmar_rect.collidepoint(evento.pos):
                print(f"Nome de Usuário: {texto_usuario}")
                # Quando a lógica do jogo estiver pronta, você retornará "tela_jogo"
                return "tela_jogo"
                
            else:
                input_ativo = False
        
        if evento.type == pygame.KEYDOWN and input_ativo:
            if evento.key == pygame.K_BACKSPACE:
                texto_usuario = texto_usuario[:-1]
            else:
                texto_usuario += evento.unicode

    # Desenho
    TELA.fill(BRANCO)
    
    texto_titulo = FONTE_TITULO.render("Login", True, PRETO)
    TELA.blit(texto_titulo, (TELA.get_width()/2 - texto_titulo.get_width()/2, 100))
    
    label_usuario = FONTE_GERAL.render("Nome de Usuário:", True, PRETO)
    TELA.blit(label_usuario, (input_usuario_rect.x, input_usuario_rect.y - 40))
    
    cor_borda = AZUL_ATIVO if input_ativo else PRETO
    pygame.draw.rect(TELA, cor_borda, input_usuario_rect, 2)
    
    texto_surf = FONTE_GERAL.render(texto_usuario, True, PRETO)
    TELA.blit(texto_surf, (input_usuario_rect.x + 10, input_usuario_rect.y + 10))

    pygame.draw.rect(TELA, CINZA, botao_confirmar_rect)
    texto_confirmar = FONTE_GERAL.render("Confirmar", True, PRETO)
    TELA.blit(texto_confirmar, (botao_confirmar_rect.centerx - texto_confirmar.get_width()/2, botao_confirmar_rect.centery - texto_confirmar.get_height()/2))

    return "tela_login" # Continua nesta tela