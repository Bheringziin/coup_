import json

class DadosJogo:
    def __init__(self, caminho="estado_jogo.json"):
        self.caminho = caminho
        self.estado = self.carregar()

    def carregar(self):
        try:
            with open(self.caminho, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def salvar(self):
        with open(self.caminho, 'w', encoding='utf-8') as f:
            json.dump(self.estado, f, indent=4, ensure_ascii=False)

    def adicionar_log(self, mensagem):
        self.estado.setdefault("log", []).append(mensagem)
        self.salvar()

    def obter_jogador_atual(self):
        idx = self.estado["jogador_atual"]
        return self.estado["jogadores"][idx]
