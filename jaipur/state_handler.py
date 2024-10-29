from __future__ import annotations
from typing import List, Tuple, Optional, TYPE_CHECKING

from mcts_deck.deck import Deck
from jaipur.cards import Cards

if TYPE_CHECKING:
    from mcts_deck.draw import Draw
    from jaipur.player import Player, HumanPlayer

class StateHandler:

    __slots__ = ('deck', 'market', 'tokens', 'human_player', 'agent')

    def __init__(self, human: HumanPlayer, agent: Player, deck: Optional[Deck], market: List, tokens: Optional[Tuple[Deck,Deck,Deck]]):

        self.human_player = human
        self.agent = agent

        if any(param is None for param in [deck, market, tokens]):
            # we must perform initial setup
            self.setup(market)
        else:
            self.deck: Deck = deck
            self.market: List = market
            self.tokens: Tuple[Deck, Deck, Deck] = tokens # 3s, 4s, 5s


    def setup(self, market_draw: List) -> None:
        """
        Perform the initial setup for a game of Jaipur.
        """
        main_deck_cards = ([Cards.RED] * 6 +
                           [Cards.YELLOW] * 6 +
                           [Cards.SILVER] * 6 +
                           [Cards.PURPLE] * 8 +
                           [Cards.GREEN] * 8 +
                           [Cards.BROWN] * 10 +
                           [Cards.CAMEL] * 8)
        # These values are sourced from https://boardgamegeek.com/filepage/86610/jaipur-parts-list-v10
        # Camels begin with 3 less due to their introduction to the market

        self.deck = Deck(elements=main_deck_cards)

        self.market = [Cards.CAMEL] * 3 + market_draw

        for element in market_draw:
            self.deck.remove_element(element)

        self.deck.update_distribution()

        three_tokens = Deck(elements=[1, 1, 2, 2, 2, 3, 3])
        four_tokens = Deck(elements=[4, 4, 5, 5, 6, 6])
        five_tokens = Deck(elements=[8, 8, 9, 10, 10])

        self.tokens = (three_tokens, four_tokens, five_tokens)


    def __str__(self):
        return f'The market currently contains: {self.market}. \nThe deck has distribution {self.deck.distribution}'