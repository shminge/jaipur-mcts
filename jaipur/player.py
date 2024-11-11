from __future__ import annotations
from typing import List, TYPE_CHECKING
import jaipur.jaipur as jaipur
from jaipur.cards import Cards

if TYPE_CHECKING:
    from mcts_deck.deck import Deck

class Player:
    """
    A Generic class to hold hand and score information.
    """
    __slots__ = ('hand', 'points', 'herd', 'game')

    def __init__(self, game: jaipur.JaipurGame):
        self.hand: List = []
        self.points: int = 0
        self.herd: int = 0
        self.game: jaipur.JaipurGame = game

    def setup(self) -> None:
        print("What is the agent's initial hand?")
        initial_hand = [jaipur.JaipurGame.card_input() for _ in range(5)]
        for card in initial_hand:
            if card is Cards.CAMEL:
                self.herd += 1
            else:
                self.hand.append(card)
            self.game.deck.remove_element(card)


    def __str__(self):
        return f'This player has a hand of {self.hand}, {self.herd} camels and {self.points} points'

    def take_bonus(self, value: int) -> None:
        bonus_stack: Deck = self.game.bonus_tokens[value-3]
        draw = bonus_stack.draw(1)
        self.game.bonus_tokens[value-3] = draw.remaining_deck
        self.points += draw.drawn_cards[0]

    def score(self):
        return self.points








class HumanPlayer(Player):
    """
    A subclass to handle all the unknowns involved with the opponent
    """

    __slots__ = ('unknown_hand', 'unknown_tokens')

    def __init__(self, game: jaipur.JaipurGame):
        super().__init__(game)
        self.unknown_hand: int = 0
        self.unknown_tokens: List[int] = [0, 0, 0]

    def setup(self) -> None:
        self.herd = int(input('How many camels did your opponent draw? '))
        for i in range(self.herd):
            self.game.deck.remove_element(Cards.CAMEL)
        self.unknown_hand = 5 - self.herd

    def take_bonus(self, value: int) -> None:
        self.unknown_tokens[value - 3] += 1

    def score(self):
        sample_score = self.points
        for i, token_stack in enumerate(self.game.bonus_tokens):
            token_stack: Deck
            if self.unknown_tokens[i] > 0:
                draw = token_stack.draw(self.unknown_tokens[i])
                sample_score += sum(draw.drawn_cards)

    def __str__(self):
        return f'This player has a hand of {self.hand}, {self.unknown_hand} unknown cards, {self.herd} camels and {self.points} points'