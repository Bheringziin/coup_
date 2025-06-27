from action import *
from player import *

from typing import Optional

class GameManager:
    # ... (outros métodos permanecem)
    
    def play_turn(self) -> str:
        """Executa um turno completo com desafios e bloqueios"""
        player = self.current_player
        action = player.choose_action(self.get_available_actions(player))
        
        # Lógica de alvo
        target = None
        if isinstance(action, (AssassinateAction, StealAction, CoupAction)):
            target = self._choose_target(player)
            if not target:
                return "Nenhum alvo válido encontrado"
        
        # Fase de desafio
        if action.requirement:  # Ações que requerem personagem podem ser desafiadas
            challenge_result = self._handle_challenge(player, action, target)
            if "desafiou corretamente" in challenge_result:
                # Ação foi desafiada com sucesso, turno acaba
                self.next_turn()
                return challenge_result
        
        # Fase de bloqueio
        if action.blockable_by:
            block_result = self._handle_block(player, action, target)
            if "bloqueou a ação" in block_result:
                # Ação foi bloqueada, turno acaba
                self.next_turn()
                return block_result
        
        # Executa a ação se passou por desafios e bloqueios
        result = player.perform_action(action, target)
        self.next_turn()
        return result
    
    def _handle_challenge(self, player: Player, action: Action, target: Player = None) -> str:
        """Gerencia a fase de desafio"""
        challenger = self._get_challenger(player)
        if challenger:
            challenge = Challenge(challenger, action, target)
            return challenge.resolve(self)
        return "Nenhum desafio foi feito"
    
    def _handle_block(self, player: Player, action: Action, target: Player = None) -> str:
        """Gerencia a fase de bloqueio"""
        blocker = self._get_blocker(player, action, target)
        if blocker:
            blocking_character = blocker.choose_blocking_character(action)
            block = Block(blocker, action, blocking_character)
            return block.resolve(self)
        return "Nenhum bloqueio foi feito"
    
    def _get_challenger(self, current_player: Player) -> Optional[Player]:
        """Encontra um jogador que queira desafiar"""
        for player in self._players:
            if player != current_player and player.is_alive:
                if isinstance(player, HumanPlayer):
                    answer = input(f"{player.name}, deseja desafiar? (s/n): ").lower()
                    if answer == 's':
                        return player
                elif isinstance(player, AIPlayer) and player.wants_to_challenge():
                    return player
        return None
    
    def _get_blocker(self, current_player: Player, action: Action, target: Player = None) -> Optional[Player]:
        """Encontra um jogador que queira bloquear"""
        # Bloqueio pode vir do alvo ou de outros jogadores, dependendo da ação
        possible_blockers = [target] if target else self._players
        possible_blockers = [p for p in possible_blockers if p and p != current_player and p.is_alive]
        
        for player in possible_blockers:
            if player.can_block(action):
                if isinstance(player, HumanPlayer):
                    answer = input(f"{player.name}, deseja bloquear? (s/n): ").lower()
                    if answer == 's':
                        return player
                elif isinstance(player, AIPlayer) and player.wants_to_block():
                    return player
        return None
    
    def _choose_target(self, current_player: Player) -> Optional[Player]:
        """Seleciona um alvo para ações que requerem"""
        valid_targets = [p for p in self._players if p != current_player and p.is_alive]
        
        if not valid_targets:
            return None
        
        if isinstance(current_player, HumanPlayer):
            print("\nEscolha um alvo:")
            for i, target in enumerate(valid_targets, 1):
                print(f"{i}. {target.name}")
            choice = int(input("Sua escolha: ")) - 1
            return valid_targets[choice]
        else:
            import random
            return random.choice(valid_targets)# Classe que controla o fluxo do jogo
