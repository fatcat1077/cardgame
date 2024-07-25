import itertools
from card_game import Card, Player
from poker_methods import (
    create_deck,
    remove_player_hands_from_deck,
    check_player_with_community_cards,
    count_valid_hands
)

# 主程式在這裡開始
deck = create_deck()

# 宣告玩家一與玩家二的手牌
player1_hand = [Card('Spades', 'A'), Card('Clubs', 'A')]  
player2_hand = [Card('Diamonds', 'J'), Card('Clubs', 'J')]  
player3_hand = [Card('Clubs', '6'), Card('Diamonds', '6')]  
player4_hand = [Card('Hearts', '6'), Card('Spades', '6')]  
player5_hand = [Card('Clubs', '3'), Card('Diamonds', '3')]  
player6_hand = [Card('Hearts', '3'), Card('Spades', '3')]  
player7_hand = [Card('Clubs', '4'), Card('Diamonds', '4')]  
player8_hand = [Card('Hearts', 'A'), Card('Spades', '4')]  


# 創建九個玩家
player1 = Player(player_id=1, hand=player1_hand)
player2 = Player(player_id=2, hand=player2_hand)
player3 = Player(player_id=3, hand=player3_hand)
player4 = Player(player_id=4, hand=player4_hand)
player5 = Player(player_id=5, hand=player5_hand)
player6 = Player(player_id=6, hand=player6_hand)
player7 = Player(player_id=7, hand=player7_hand)
player8 = Player(player_id=8, hand=player8_hand)


# 創建temp_deck，內容是所有的牌減掉現在玩家所有的手牌
players = [player1, player2, player3, player4, player5, player6, player7, player8]
temp_deck = remove_player_hands_from_deck(deck, players)

# 創建used_deck，內容是所有的牌減掉現在玩家所有的手牌
used_deck = []
for player in players:
    used_deck.extend(player.hand)

#[expression for item in iterable if condition]增強式迴圈
#更新以避免possible_hand出現過
for player in players:
    player.update_possible_hands(used_deck)
print("--------------------------------------------------")
#[print(len(player.possible_hands)) for player in players]
#for possible in player1.possible_hands:
#    print(possible)




# 遍歷所有組合
count = count_valid_hands(player1,player2,temp_deck)

print(f"Total count: {count}")
