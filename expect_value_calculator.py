import itertools
from card_game import Card, Player
from poker_methods import (
    create_deck,
    remove_player_hands_from_deck,
    check_player_with_community_cards,
    count_valid_hands
)

def evaluate_players(players):
    # 創建一副完整的牌組
    deck = create_deck()

    # 創建temp_deck，內容是所有的牌減掉現在玩家所有的手牌
    temp_deck = remove_player_hands_from_deck(deck, players)

    # 創建used_deck，內容是所有的牌減掉現在玩家所有的手牌
    used_deck = []
    for player in players:
        used_deck.extend(player.hand)

    # 更新以避免possible_hand出現過
    for player in players:
        player.update_possible_hands(used_deck)

    # 初始化布林值字典
    player_results = {player.player_id: False for player in players}

    # 計算每個玩家的count_valid_hands結果
    threshold = (200 * 0.12 * 0.45) * 376992 / 1000000
    for player1, player2 in itertools.combinations(players, 2):
        count = count_valid_hands(player1, player2, temp_deck)
        if count > threshold:
            player_results[player1.player_id] = True
            player_results[player2.player_id] = True

    return player_results
'''
# 使用示例
player1_hand = [Card('Hearts', 'A'), Card('Diamonds', 'A')]  
player2_hand = [Card('Hearts', 'J'), Card('Diamonds', 'J')]  
player3_hand = [Card('Hearts', 'Q'), Card('Diamonds', 'Q')]  
player4_hand = [Card('Hearts', 'K'), Card('Diamonds', '7')]  

player1 = Player(player_id=1, hand=player1_hand)
player2 = Player(player_id=2, hand=player2_hand)
player3 = Player(player_id=3, hand=player3_hand)
player4 = Player(player_id=4, hand=player4_hand)

players = [player1, player2, player3, player4]

results = evaluate_players(players)
print(results)
'''