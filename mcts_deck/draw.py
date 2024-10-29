from __future__ import annotations
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from mcts_deck.deck import Deck

class Draw:

    __slots__ = ('drawn_cards', 'remaining_deck')

    def __init__(self, drawn_cards: List, remaining_deck: Deck):
        self.drawn_cards = drawn_cards
        self.remaining_deck = remaining_deck