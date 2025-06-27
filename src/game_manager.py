from action import *
from player import *

from typing import List, Optional, Dict
import json
from pathlib import Path
from Deck import Deck

class GameManager:
    def __init__(self, players: List[Player], state_file: str = "data/estado_jogo.json", load_existing: bool = False):
        self._players = players
        self._turn_index = 0
        self._history: List[str] = []
        self._deck = Deck()
        self._state_file = state_file

        if load_existing and Path(self._state_file).exists():
            self.load_state()
        else:
            for p in self._players:
                p.coins = 2
                drawn = self._deck.draw(2)
                for card in drawn:
                    p.add_character(card["character"])
            self.save_state()

    def play_turn(self) -> str:
        """Executa um turno completo com desafios e bloqueios"""
        player = self.current_player
        action = player.choose_action(self.get_available_actions(player), self._players)
        
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
        result = player.perform_action(action, target, self)
        self.next_turn()
        self.save_state()
        return result

    @property
    def current_player(self) -> Player:
        return self._players[self._turn_index]

    @property
    def players(self) -> List[Player]:
        return self._players

    @property
    def history(self) -> List[str]:
        return self._history

    def next_turn(self) -> None:
        """Avança para o próximo jogador vivo."""
        if not any(p.is_alive for p in self._players):
            return
        self._turn_index = (self._turn_index + 1) % len(self._players)
        while not self._players[self._turn_index].is_alive:
            self._turn_index = (self._turn_index + 1) % len(self._players)

    def get_available_actions(self, player: Player) -> List[Action]:
        actions = [
            IncomeAction(), ForeignAidAction(), TaxAction(),
            AssassinateAction(), StealAction(), ExchangeAction(), CoupAction()
        ]
        return [a for a in actions if player.coins >= a.cost]

    def add_to_history(self, message: str) -> None:
        self._history.append(message)
    
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
@@ -77,26 +126,54 @@ class GameManager:
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
            return random.choice(valid_targets)

    # ------------------------------------------------------------------
    # Persistência de dados
    def save_state(self) -> None:
        """Salva o estado atual do jogo em JSON."""
        data = {
            "turn_index": self._turn_index,
            "history": self._history,
            "players": [p.to_dict() for p in self._players],
            "deck_file": self._deck._json_file,
        }
        Path(self._state_file).parent.mkdir(parents=True, exist_ok=True)
        with open(self._state_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_state(self) -> None:
        """Carrega o estado do jogo se o arquivo existir."""
        if not Path(self._state_file).exists():
            return
        with open(self._state_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._turn_index = data.get("turn_index", 0)
        self._history = data.get("history", [])
        self._deck = Deck(data.get("deck_file", "deck_state.json"))
        self._players = [Player.from_dict(pdata) for pdata in data.get("players", [])]
