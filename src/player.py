from action import Action, CoupAction

import random

class Player:
    def __init__(self, name: str):
        self._name = name
        self._coins = 0
        self._characters = []
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
    
    def lose_influence(self) -> None:
        if self.characters:
            self._characters.pop()
            if not self.characters:
                self._alive = False
    
    def perform_action(self, action: Action, target=None) -> None:
        if self.coins >= action.cost:
            self.coins -= action.cost
            action.execute(self, target, None)# Classes Player, HumanPlayer e AIPlayer

    def has_character(self, character_name: str) -> bool:
        """Verifica se o jogador tem um determinado personagem"""
        # Em uma implementação real, isso verificaria as cartas do jogador
        # Aqui vamos simular que tem 50% de chance para testes
        import random
        return random.choice([True, False])
    
    def can_block(self, action: Action) -> bool:
        """Verifica se o jogador pode bloquear uma ação"""
        # Verifica se tem algum personagem que pode bloquear esta ação
        for character in action.blockable_by:
            if self.has_character(character):
                return True
        return False

class HumanPlayer(Player):
    def choose_action(self, available_actions: list) -> Action:
        # Implementação será feita com a interface gráfica
        pass

class AIPlayer(Player):
    def choose_action(self, available_actions: list, players: list) -> Action:
        from random import choice
        
        # Se tiver 7 ou mais moedas, 80% de chance de escolher Coup
        if self.coins >= 7 and random.random() < 0.8:
            # Escolhe um alvo aleatório que não está eliminado
            valid_targets = [p for p in players if p.is_alive and p != self]
            if valid_targets:
                target = choice(valid_targets)
                return CoupAction()
        
        # Caso contrário, escolhe uma ação aleatória
        return choice(available_actions)# Classes Player, HumanPlayer e AIPlayer
