from __future__ import annotations
from typing import List, Tuple
from collections import Counter
import random

from mcts_deck.draw import Draw

class Deck:
    """
    A class to hold any deck-like objected needed for the MCTS. Implements methods for drawing, copying itself, and returning averages
    """

    __slots__ = ('deck_elements', 'distribution')

    def __init__(self, elements=None, shuffle = True):
        if elements is None:
            elements = []
        self.deck_elements: List = elements
        if shuffle:
            self.shuffle() # shuffle on initialization
        self.distribution: Counter = Counter(self.deck_elements)

    def dupe_deck(self):
        return Deck(elements=self.deck_elements.copy())

    def shuffle(self):
        random.shuffle(self.deck_elements)


    def draw(self, n) -> Draw:
        """
        Draws n elements from a copy of the deck, and returns the draws in order as well as a reference to the new deck object
        """
        assert len(self.deck_elements) >= n, f'Tried to draw {n} elements from an {len(self.deck_elements)}-element deck'

        new_deck: Deck = self.dupe_deck()
        drawn_cards: List = sorted([new_deck.deck_elements.pop() for _ in range(n)], key=lambda card: card.value) # sorts the cards to make sure functionally equivalent draws are the same

        new_deck.update_distribution()

        return Draw(drawn_cards=drawn_cards, remaining_deck=new_deck)


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
        Removes one occurrence of a given element and returns it
        """
        self.deck_elements.remove(element)

    def update_distribution(self) -> None:
        """
        Updates self.distribution
        """

        self.distribution = Counter(self.deck_elements)


    def inverse_probability(self, draw: Tuple) -> float:
        """
        Returns the probability of a specific draw occurring from the deck.
        """
        draw_distribution: Counter = self.distribution.copy() # copy the distribution as we want to update counts
        draw_probability: float = 1.0
        for element in draw:
            element_count = draw_distribution[element]
            draw_probability *= element_count/draw_distribution.total()
            draw_distribution[element] -= min(1, element_count) # if there are 0, subtract none

        return draw_probability

    def update_draw(self, draw: List) -> None:
        """
        Used to update the deck after an irl draw
        """
        for element in draw:
            self.remove_element(element)

        self.update_distribution()