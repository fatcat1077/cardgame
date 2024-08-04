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
player1_hand = [Card('Hearts', 'A'), Card('Diamonds', 'A')]  
player2_hand = [Card('Hearts', 'J'), Card('Diamonds', 'J')]  
player3_hand = [Card('Hearts', 'Q'), Card('Diamonds', 'Q')]  
player4_hand = [Card('Hearts', 'K'), Card('Diamonds', '7')]  



# 創建九個玩家
player1 = Player(player_id=1, hand=player1_hand)
player2 = Player(player_id=2, hand=player2_hand)
player3 = Player(player_id=3, hand=player3_hand)
player4 = Player(player_id=4, hand=player4_hand)



# 創建temp_deck，內容是所有的牌減掉現在玩家所有的手牌
players = [player1, player2, player3, player4]
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





    
count = count_valid_hands(player1,player2,temp_deck)
print("player1 and player2",f"Total count: {count}")
count = count_valid_hands(player1,player3,temp_deck)
print("player1 and player3",f"Total count: {count}")
count = count_valid_hands(player1,player4,temp_deck)
print("player1 and player4",f"Total count: {count}")
count = count_valid_hands(player2,player3,temp_deck)
print("player2 and player3",f"Total count: {count}")
count = count_valid_hands(player2,player4,temp_deck)
print("player2 and player4",f"Total count: {count}")
count = count_valid_hands(player3,player4,temp_deck)
print("player3 and player4",f"Total count: {count}")
#假設獎池在100萬、每一手玩家加入的成本是0.12*0.45BB

#print(f"Total count: {count}")
