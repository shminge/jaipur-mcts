from mcts_deck.deck import Deck

d = Deck(elements=[1,2,3,4,5,5,3,2,5,7,1,3,5,76,4,2])


d.add_element(6)
d.remove_element(4)
print(d.probability_distribution())
drawn, deck = d.draw(3)
print(drawn, deck.deck_elements)
print(deck.probability_distribution())
