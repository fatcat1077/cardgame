from card_game import Card,Player
from expect_value_calculator import evaluate_players

player1_hand = [Card('Hearts', '2'), Card('Diamonds', '2')]  
player2_hand = [Card('Hearts', '3'), Card('Diamonds', '3')]  
player3_hand = [Card('Hearts', '4'), Card('Diamonds', '4')]  
player4_hand = [Card('Hearts', '5'), Card('Diamonds', '5')]  

player1 = Player(player_id=1, hand=player1_hand)
player2 = Player(player_id=2, hand=player2_hand)
player3 = Player(player_id=3, hand=player3_hand)
player4 = Player(player_id=4, hand=player4_hand)
players = [player1, player2, player3, player4]
result = evaluate_players(players)
print(result)