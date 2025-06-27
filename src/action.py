from abc import ABC, abstractmethod
from typing import Optional
from player import Player
from game_manager import *

class Action(ABC):
    def __init__(self, cost: int, requirement: str = None, blockable_by: List[str] = None):
        self._cost = cost
        self._requirement = requirement
        self._blockable_by = blockable_by or []  # Lista de personagens que podem bloquear
    
    @property
    def blockable_by(self) -> List[str]:
        return self._blockable_by
    
    @property
    def cost(self) -> int:
        return self._cost
    
    @property
    def requirement(self) -> str:
        return self._requirement
    
    @abstractmethod
    def execute(self, attacker, target, game_state) -> None:
        pass


class IncomeAction(Action):
    def __init__(self):
        super().__init__(cost=0)
    
    def execute(self, attacker, target, game_state) -> None:
        attacker.coins += 1


class ForeignAidAction(Action):
    def __init__(self):
        super().__init__(cost=0, blockable_by=["Duke"])
    
    def execute(self, attacker: 'Player', target: 'Player' = None) -> str:
        attacker.coins += 2
        return f"{attacker.name} recebeu 2 moedas de ajuda externa"



class CoupAction(Action):
    def __init__(self):
        """
        Inicializa a ação Coup (Golpe de Estado) com custo 7 moedas.
        O Coup não requer um personagem específico e não pode ser bloqueado.
        """
        super().__init__(cost=7)  # Coup custa 7 moedas
    
    def execute(self, attacker: 'Player', target: Optional['Player'], game_manager: 'GameManager') -> None:
        """
        Executa a ação Coup:
        1. Verifica se o atacante tem moedas suficientes (já verificado no perform_action)
        2. Verifica se o alvo é válido
        3. Força o alvo a perder uma influência (carta)
        
        Args:
            attacker: Jogador que está realizando a ação
            target: Jogador alvo do Coup (deve ser fornecido)
            game_manager: Gerenciador do jogo para atualizar estado
        """
        if target is None:
            raise ValueError("CoupAction requer um alvo específico")
        
        if not target.is_alive:
            raise ValueError("Não pode realizar Coup em jogador eliminado")
        
        # O atacante já pagou as 7 moedas (verificado no perform_action)
        # Força o alvo a perder uma influência
        target.lose_influence()
        
        # Registrar a ação no histórico do jogo
        if game_manager is not None:
            game_manager.add_to_history(f"{attacker.name} realizou Coup em {target.name}")

class AssassinateAction(Action):
    """Ação do Assassino - custa 3 moedas para eliminar uma influência"""
    def __init__(self):
        super().__init__(cost=3, requirement="Assassin", blockable_by=["Contessa"])
    
    def execute(self, attacker: 'Player', target: 'Player' = None) -> str:
        if not target:
            raise ValueError("Assassinar precisa de um alvo")
        
        if not target.is_alive:
            return f"{target.name} já está eliminado"
        
        target.lose_influence()
        return (f"{attacker.name} assassinou {target.name}!\n"
                f"(Pode ser bloqueado pela Condessa)")

class TaxAction(Action):
    """Ação do Duque - ganha 3 moedas"""
    def __init__(self):
        super().__init__(cost=0, requirement="Duke")
    
    def execute(self, attacker: 'Player', target: 'Player' = None) -> str:
        attacker.coins += 3
        return f"{attacker.name} coletou impostos como Duque (+3 moedas)"

class StealAction(Action):
    """Ação do Capitão - rouba 2 moedas de outro jogador"""
    def __init__(self):
        super().__init__(cost=0, requirement="Captain", blockable_by=["Captain", "Ambassador"])
    
    def execute(self, attacker: 'Player', target: 'Player' = None) -> str:
        if not target:
            raise ValueError("Roubo precisa de um alvo")
        
        stolen = min(2, target.coins)
        target.coins -= stolen
        attacker.coins += stolen
        
        return (f"{attacker.name} roubou {stolen} moedas de {target.name}!\n"
                f"(Pode ser bloqueado pelo Capitão ou Embaixador)")

class ExchangeAction(Action):
    """Ação do Embaixador - troca cartas com o baralho"""
    def __init__(self):
        super().__init__(cost=0, requirement="Ambassador")
    
    def execute(self, attacker: 'Player', target: 'Player' = None) -> str:
        # Em uma implementação completa, aqui seria a lógica de troca de cartas
        return f"{attacker.name} usou o Embaixador para trocar cartas"
    

class Challenge:
    """Representa um desafio a uma ação"""
    def __init__(self, challenger: 'Player', action: Action, target: 'Player' = None):
        self._challenger = challenger
        self._action = action
        self._target = target
    
    def resolve(self, game: 'GameManager') -> str:
        """Resolve o desafio verificando se o jogador tem o personagem requerido"""
        player_to_check = self._target if self._target else game.current_player
        
        # Verifica se o jogador tem o personagem necessário
        has_requirement = player_to_check.has_character(self._action.requirement)
        
        if has_requirement:
            # Desafio falhou - o jogador tinha o personagem
            self._challenger.lose_influence()
            return (f"{self._challenger.name} falhou no desafio e perdeu uma influência!\n"
                    f"{player_to_check.name} realmente tinha {self._action.requirement}.")
        else:
            # Desafio bem-sucedido - o jogador blefou
            player_to_check.lose_influence()
            return (f"{self._challenger.name} desafiou corretamente!\n"
                    f"{player_to_check.name} não tinha {self._action.requirement} e perdeu uma influência.")
        
class Block:
    """Representa um bloqueio a uma ação"""
    def __init__(self, blocker: 'Player', action: Action, blocking_character: str):
        self._blocker = blocker
        self._action = action
        self._blocking_character = blocking_character
    
    def resolve(self, game: 'GameManager') -> str:
        """Resolve o bloqueio"""
        # Verifica se o bloqueio é válido para esta ação
        if self._blocking_character not in self._action.blockable_by:
            return f"{self._blocking_character} não pode bloquear esta ação!"
        
        # A ação é bloqueada
        return (f"{self._blocker.name} bloqueou a ação com {self._blocking_character}!\n"
                f"A ação {self._action.__class__.__name__} foi cancelada.")
