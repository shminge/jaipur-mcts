
from __future__ import annotations
from typing import List, Tuple, Optional, TYPE_CHECKING

from mcts_deck.deck import Deck
from jaipur.cards import Cards
import jaipur.player as players

if TYPE_CHECKING:
    from mcts_deck.draw import Draw




class JaipurGame:
    """
    Should handle the entire game at one state
    """

    __slots__ = ('deck', 'market', 'goods_tokens', 'bonus_tokens', 'human_player', 'agent')

    def __init__(self,
                 human: players.HumanPlayer = None,
                 agent: players.Player = None,
                 deck: Optional[Deck] = None,
                 market: Deck = None,
                 bonus_tokens: Optional[List[Deck, Deck, Deck]] = None,
                 goods_tokens: dict[Cards] = None
                 ):

        self.human_player: players.HumanPlayer = human
        self.agent: players.Player = agent

        if any(param is None for param in [deck, market, bonus_tokens]):
            # we must perform initial setup
            self.setup()
        else:
            self.deck: Deck = deck
            self.market: Deck = market
            self.bonus_tokens: List[Deck, Deck, Deck] = bonus_tokens  # 3s, 4s, 5s
            self.goods_tokens: dict[Cards] = goods_tokens

    def setup(self) -> None:
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

        #ask which cards have been placed in the market
        print(f'Apart from the 3 Camels, what cards are in the market?')
        market_draw = [self.card_input() for _ in range(2)]


        self.market = Deck(elements=[Cards.CAMEL] * 3 + market_draw, shuffle=False)
        self.market.update_distribution()

        for element in market_draw:
            self.deck.remove_element(element)

        self.deck.update_distribution()

        three_tokens = Deck(elements=[1, 1, 2, 2, 2, 3, 3])
        four_tokens = Deck(elements=[4, 4, 5, 5, 6, 6])
        five_tokens = Deck(elements=[8, 8, 9, 10, 10])

        self.bonus_tokens = [three_tokens, four_tokens, five_tokens]

        self.human_player: players.HumanPlayer = players.HumanPlayer(game=self)
        self.human_player.setup()

        self.agent: players.Player = players.Player(game=self)
        self.agent.setup()

        self.deck.update_distribution()

        self.goods_tokens = {
            Cards.RED: [5, 5, 5, 7, 7],
            Cards.GOLD: [5, 5, 5, 6, 6],
            Cards.SILVER: [5, 5, 5, 5, 5],
            Cards.PURPLE: [1, 1, 2, 2, 3, 3, 5],
            Cards.GREEN: [1, 1, 2, 2, 3, 3, 5],
            Cards.BROWN: [1, 1, 1, 1, 1, 1, 2, 3, 4]



        }

    def __str__(self):
        return f'The market currently contains: {self.market.deck_elements}. \nThe deck has distribution {self.deck.distribution}'

    @staticmethod
    def card_input() -> Cards:
        """
        Handles getting user input about cards
        """
        input_card = input(':-: ').upper()
        while input_card not in Cards.__members__:
            print('invalid')
            input_card = input(':-: ').upper()
        return Cards[input_card]