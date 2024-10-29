from __future__ import annotations
from typing import List


class Player:
    """
    A Generic class to hold hand and score information.
    """
    __slots__ = ('hand', 'points', 'herd')

    def __init__(self):
        self.hand: List = []
        self.points: int = 0
        self.herd: int = 0








class HumanPlayer(Player):
    """
    A subclass to handle all the unknowns involved with the opponent
    """

    __slots__ = ('unknown_hand', 'unknown_tokens')

    def __init__(self):
        super().__init__()
        self.unknown_hand: int = 0
        self.unknown_tokens: List[int] = [0, 0, 0]
