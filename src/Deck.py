import json
import random
from typing import List, Dict, Optional
from pathlib import Path

class Deck:
    """Classe que gerencia o baralho do jogo Coup com persistência em JSON"""
    
    def __init__(self, json_file: str = "deck_state.json"):
        """
        Inicializa o baralho carregando do JSON ou criando novo
        
        Args:
            json_file: Caminho para o arquivo de estado do deck
        """
        self._json_file = json_file
        self._cards = []
        self._discard_pile = []
        
        if Path(json_file).exists():
            self._load_from_json()  # Método a ser implementado
        else:
            self._initialize_new_deck()  # Método a ser implementado
    
    def _initialize_new_deck(self) -> None:
        """Inicializa um novo baralho (implementação parcial)"""
        # TODO: Implementar a criação inicial das cartas
        # Exemplo básico (substituir pela lógica real):
        self._cards = [
            {"id": 1, "character": "Duke", "in_game": False},
            {"id": 2, "character": "Assassin", "in_game": False},
            # ... outras cartas
        ]
        self.shuffle()
        self._save_to_json()  # Método a ser implementado
    
    def _load_from_json(self) -> None:
        """Carrega o estado do baralho do JSON (esqueleto)"""
        # TODO: Implementar carregamento do JSON
        try:
            with open(self._json_file, 'r') as f:
                data = json.load(f)
                self._cards = data.get('cards', [])
                self._discard_pile = data.get('discard_pile', [])
        except Exception as e:
            print(f"Erro ao carregar deck: {e}")
            self._initialize_new_deck()
    
    def _save_to_json(self) -> None:
        """Salva o estado atual do baralho em JSON (esqueleto)"""
        # TODO: Implementar salvamento completo
        data = {
            "cards": self._cards,
            "discard_pile": self._discard_pile
        }
        try:
            with open(self._json_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar deck: {e}")
    
    def shuffle(self) -> None:
        """Embaralha as cartas do baralho principal"""
        random.shuffle(self._cards)
        # TODO: Adicionar registro de shuffle no JSON
    
    def draw(self, count: int = 1) -> List[Dict]:
        """Compra cartas do topo do baralho (parcial)"""
        # TODO: Implementar lógica completa com JSON
        drawn = self._cards[:count]
        self._cards = self._cards[count:]
        
        # Atualizar estado no JSON
        for card in drawn:
            card["in_game"] = True
        self._save_to_json()
        
        return drawn
    
    def discard(self, card: Dict) -> None:
        """Descarta uma carta para a pilha de descarte (parcial)"""
        # TODO: Implementar lógica completa
        self._discard_pile.append(card)
        self._save_to_json()
    
    def return_cards(self, cards: List[Dict]) -> None:
        """Devolve cartas para o baralho (parcial)"""
        # TODO: Implementar lógica de retorno com JSON
        for card in cards:
            card["in_game"] = False
        self._cards.extend(cards)
        self._save_to_json()
    
    def get_deck_state(self) -> Dict:
        """Retorna o estado atual do baralho para debug"""
        return {
            "remaining_cards": len(self._cards),
            "discarded_cards": len(self._discard_pile),
            "total_cards": len(self._cards) + len(self._discard_pile)
        }
    
    def __str__(self) -> str:
        return f"Deck: {len(self._cards)} cartas | Descarte: {len(self._discard_pile)}"
