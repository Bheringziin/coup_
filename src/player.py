from action import Action, CoupAction
from typing import List, Dict, Type

import random

class Player:
    def __init__(self, name: str):
        self._name = name
        self._coins = 0
        self._characters: List[str] = []
        self._alive = True
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def coins(self) -> int:
        return self._coins
    
    @coins.setter
    def coins(self, value: int) -> None:
        self._coins = max(0, value)
    
    @property
    def characters(self) -> list:
        return self._characters
    
    @property
    def is_alive(self) -> bool:
        return self._alive

    def add_character(self, character: str) -> None:
        """Adiciona uma nova carta de personagem ao jogador"""
        self._characters.append(character)
    
    def lose_influence(self) -> None:
        if self.characters:
            self._characters.pop()
            if not self.characters:
                self._alive = False
    
    def perform_action(self, action: Action, target=None, game_manager=None) -> None:
        """Executa uma ação descontando o custo."""
        if self.coins >= action.cost:
            self.coins -= action.cost
            return action.execute(self, target, game_manager)

    def has_character(self, character_name: str) -> bool:
        """Verifica se o jogador tem um determinado personagem"""
        # Em uma implementação real, isso verificaria as cartas do jogador
        # Aqui vamos simular que tem 50% de chance para testes
        import random
        return random.choice([True, False])

    def choose_blocking_character(self, action: Action) -> str:
        """Escolhe um personagem para bloquear uma ação, se possível"""
        for character in self._characters:
            if character in action.blockable_by:
                return character
        return action.blockable_by[0] if action.blockable_by else ""

    def wants_to_challenge(self) -> bool:
        return False

    def wants_to_block(self) -> bool:
        return False
    
    def can_block(self, action: Action) -> bool:
        """Verifica se o jogador pode bloquear uma ação"""
        # Verifica se tem algum personagem que pode bloquear esta ação
        for character in action.blockable_by:
            if self.has_character(character):
                return True
        return False

    # --- Persistência -----------------------------------------------------
    def to_dict(self) -> Dict:
        """Retorna uma representação serializável do jogador."""
        return {
            "name": self._name,
            "coins": self._coins,
            "characters": self._characters,
            "alive": self._alive,
            "type": self.__class__.__name__,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'Player':
        """Cria um jogador a partir de um dicionário salvo."""
        player_class: Type[Player] = HumanPlayer if data.get("type") == "HumanPlayer" else AIPlayer
        player = player_class(data.get("name", "Jogador"))
        player._coins = data.get("coins", 0)
        player._characters = data.get("characters", [])
        player._alive = data.get("alive", True)
        return player

class HumanPlayer(Player):
    def choose_action(self, available_actions: list, players: list) -> Action:
        """Solicita ao usuário qual ação deseja executar."""
        print("\nEscolha uma ação:")
        for i, action in enumerate(available_actions, 1):
            print(f"{i}. {action.__class__.__name__}")
        choice = int(input("Sua escolha: ")) - 1
        return available_actions[choice]

    def wants_to_challenge(self) -> bool:
        answer = input("Deseja desafiar? (s/n): ").lower()
        return answer == 's'

    def wants_to_block(self) -> bool:
        answer = input("Deseja bloquear? (s/n): ").lower()
        return answer == 's'

class AIPlayer(Player):
    def choose_action(self, available_actions: list, players: list) -> Action:
        """Escolhe uma ação de maneira simples."""
        from random import choice

        if self.coins >= 7 and random.random() < 0.8:
            return CoupAction()

        return choice(available_actions)

    def wants_to_challenge(self) -> bool:
        return random.random() < 0.1

    def wants_to_block(self) -> bool:
        return random.random() < 0.2

    def choose_blocking_character(self, action: Action) -> str:
        options = [c for c in self._characters if c in action.blockable_by]
        return random.choice(options) if options else ""

