import json
import random

# Função para adicionar um novo jogador ao jogo
def adicionar_jogador(jogo_info, nome_jogador):
    novo_jogador = {
        "nome": nome_jogador,
        "moedas": 2,  # Todo jogador começa com 2 moedas
        "cartas_ativas": [],
        "cartas_reveladas": []
    }
    jogo_info["jogadores"].append(novo_jogador)
    print(f"'{nome_jogador}' entrou no jogo!")

# Função para dar as cartas iniciais aos jogadores
def distribuir_cartas_iniciais(jogo_info):
    random.shuffle(jogo_info["baralho"]) # Embaralha o baralho
    for jogador in jogo_info["jogadores"]:
        # Cada jogador compra 2 cartas
        jogador["cartas_ativas"].append(jogo_info["baralho"].pop())
        jogador["cartas_ativas"].append(jogo_info["baralho"].pop())

# Função para um jogador perder uma carta (revelar)
def revelar_carta(jogo_info, nome_jogador, carta_a_revelar):
    # Encontra o jogador na lista
    for jogador in jogo_info["jogadores"]:
        if jogador["nome"] == nome_jogador:
            # Move a carta de 'ativas' para 'reveladas'
            if carta_a_revelar in jogador["cartas_ativas"]:
                jogador["cartas_ativas"].remove(carta_a_revelar)
                jogador["cartas_reveladas"].append(carta_a_revelar)
                print(f"'{nome_jogador}' revelou a carta '{carta_a_revelar}'.")
                return
    print(f"Atenção: '{nome_jogador}' não possui a carta '{carta_a_revelar}' na mão.")

# Função para salvar o estado atual em um arquivo .json
def salvar_jogo(jogo_info, nome_arquivo="estado_jogo.json"):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(jogo_info, f, indent=4, ensure_ascii=False)
    print(f"\nJogo salvo em '{nome_arquivo}'!")