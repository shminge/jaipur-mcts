from __future__ import annotations
from typing import List, Tuple
from collections import Counter
import random

class Deck:
    """
    A class to hold any deck-like objected needed for the MCTS. Implements methods for drawing, copying itself, and returning averages
    """

    def __init__(self, elements=None):
        if elements is None:
            elements = []
        self.deck_elements: List = elements

    def dupe_deck(self):
        return Deck(elements=self.deck_elements.copy())

    def shuffle(self):
        random.shuffle(self.deck_elements)


    def draw(self, n) -> Tuple[List, Deck]:
        """
        Draws n elements from a copy of the deck, and returns the draws in order as well as a reference to the new deck object
        """
        assert len(self.deck_elements) >= n, 'Tried to draw {n} elements from an {len(self.deck_elements)}-element deck'

        new_deck: Deck = self.dupe_deck()
        new_deck.shuffle()
        drawn_cards: List = [new_deck.deck_elements.pop() for _ in range(n)]

        return drawn_cards, new_deck


    def average_element(self) -> float:
        """
        Used for numbered decks only. Returns the average
        """
        return sum(self.deck_elements) / len(self.deck_elements)

    def add_element(self, element) -> None:
        """
        Takes a value to add to the deck
        """
        self.deck_elements.append(element)

    def remove_element(self, element) -> None:
        """
        Removes one occurrence of a given element
        """
        self.deck_elements.remove(element)

    def probability_distribution(self) -> dict:
        """
        Returns the probabilities of any specific element being drawn
        """

        distribution = Counter(self.deck_elements)

        return distribution