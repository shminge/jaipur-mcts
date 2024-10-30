from __future__ import annotations

from jaipur.jaipur import JaipurGame
from jaipur.actions import CamelAction, SellAction
from jaipur.cards import Cards

game: JaipurGame = JaipurGame()

print(game)
print(game.agent)
a = SellAction(cards=[Cards.RED, Cards.RED])

a.perform(game.agent)

print(game)
print(game.agent)