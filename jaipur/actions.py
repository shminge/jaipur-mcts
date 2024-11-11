
from typing import TYPE_CHECKING, List

from jaipur.cards import Cards
from jaipur.player import Player

class Action:
    """
    A generic class to handle all the actions. Made to be subclassed
    """
    __slots__ = ()

    def perform(self, player: Player, verbose = True):
        """
        Take the given action for the given player
        """
        raise NotImplementedError


class TakeAction(Action):
    """
    Take a single card
    """

    __slots__ = 'card'

    def __init__(self, card: Cards):
        self.card: Cards = card

    def perform(self, player: Player, verbose = True):

        assert player.game.market.distribution[self.card] > 0, 'Tried to take a non-existent card from the market'
        assert self.card is not Cards.CAMEL, 'Do not use Take for Camels'

        player.game.market.remove_element(self.card)

        player.hand.append(self.card)

        player.game.market.distribution.subtract({self.card: 1})


class CamelAction(Action):
    """
    Take the camels in the marketplace
    """
    def perform(self, player: Player, verbose = True):

        camel_count = player.game.market.distribution[Cards.CAMEL]

        assert camel_count > 0, 'Tried to take 0 camels'

        if verbose:
            print(f'Taking {camel_count} camels')

        for i in range(camel_count):
            player.game.market.remove_element(Cards.CAMEL)
            player.herd += 1

        player.game.market.distribution.subtract({Cards.CAMEL: camel_count})



class SwapAction(Action):
    """
    Switch Cards
    """
    __slots__ = ('num_camels', 'hand_swap', 'market_swap')

    def __init__(self, num_camels: int, hand_cards: List, market_cards: List):
        self.num_camels = num_camels
        self.hand_swap = hand_cards
        self.market_swap = market_cards

    def perform(self, player: Player, verbose = True):
        assert self.num_camels <= player.herd, 'Tried to use more camels than available'

        [player.game.market.add_element(Cards.CAMEL) for _ in range(self.num_camels)]
        player.herd -= self.num_camels

        [(player.game.market.add_element(card), player.hand.remove(card)) for card in self.hand_swap]

        [(player.game.market.remove_element(card), player.hand.append(card)) for card in self.market_swap]

        player.game.market.update_distribution()


class SellAction(Action):
    """
    Sell cards
    """
    __slots__ = 'cards'

    def __init__(self, cards: List):
        self.cards: List = cards

    def perform(self, player: Player, verbose = True):
        card_type = self.cards[0]
        assert all(card is card_type for card in self.cards), 'Tried to sell a mix'

        sale_count = len(self.cards)

        for card in self.cards:
            player.hand.remove(card)
            if len(player.game.goods_tokens[card]) > 0:
                player.points += player.game.goods_tokens[card].pop()

        if sale_count >= 2:
            player.take_bonus(min(5, sale_count))
