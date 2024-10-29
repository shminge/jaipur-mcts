
from jaipur.state_handler import StateHandler
from jaipur.player import Player, HumanPlayer

from jaipur.cards import Cards



class JaipurGame:
    __slots__ = ('state_handler')

    def __init__(self):
        self.state_handler = StateHandler(human=HumanPlayer(), agent=Player(), deck=None, market=[self.card_input() for _ in range(3)], tokens=None)



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