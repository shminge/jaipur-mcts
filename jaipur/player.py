from __future__ import annotations
from typing import List
import jaipur.jaipur as jaipur
from jaipur.cards import Cards


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