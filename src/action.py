from abc import ABC, abstractmethod
from typing import Optional, List, TYPE_CHECKING
from player import Player

if TYPE_CHECKING:
    from game_manager import GameManager

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
    def execute(self, attacker: 'Player', target: Optional['Player'] = None, game_manager: Optional['GameManager'] = None) -> Optional[str]:
        """Executa a ação."""
        pass


@@ -131,25 +133,61 @@ class ExchangeAction(Action):
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
            game.add_to_history(
                f"{self._challenger.name} desafiou {player_to_check.name} corretamente"
            )
            return (
                f"{self._challenger.name} desafiou corretamente! {player_to_check.name} "
                f"não tinha {self._action.requirement} e perdeu uma influência."
            )


class Block:
    """Representa um bloqueio de ação."""

    def __init__(self, blocker: Player, action: Action, character: str):
        self._blocker = blocker
        self._action = action
        self._character = character

    def resolve(self, game: 'GameManager') -> str:
        """Resolve o bloqueio verificando se o personagem é válido."""
        if self._character not in self._action.blockable_by:
            return f"{self._character} não pode bloquear esta ação."

        if self._blocker.has_character(self._character):
            game.add_to_history(
                f"{self._blocker.name} bloqueou a ação com {self._character}"
            )
            return f"{self._blocker.name} bloqueou a ação com {self._character}"
        else:
            self._blocker.lose_influence()
            game.add_to_history(
                f"{self._blocker.name} tentou bloquear blefando e perdeu uma influência"
            )
            return (
                f"{self._blocker.name} blefou ao tentar bloquear e perdeu uma influência!"
            )
