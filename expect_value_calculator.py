import itertools
from card_game import Card, Player
from poker_methods import (
    create_deck,
    remove_player_hands_from_deck,
    check_player_with_community_cards,
    count_valid_hands
)

def evaluate_players(players):
    try:
        # 创建一副完整的牌组
        deck = create_deck()

        # 创建temp_deck，内容是所有的牌减掉现在玩家所有的手牌
        temp_deck = remove_player_hands_from_deck(deck, players)

        # 创建used_deck，内容是所有的牌减掉现在玩家所有的手牌
        used_deck = []
        for player in players:
            used_deck.extend(player.hand)

        # 更新以避免possible_hand出现过
        for player in players:
            player.update_possible_hands(used_deck)

        # 初始化布尔值字典
        player_results = {player.player_id: False for player in players}

        # 计算每个玩家的count_valid_hands结果
        threshold = (200 * 0.12 * 0.45) * 376992 / 1000000
        for player1, player2 in itertools.combinations(players, 2):
            count = count_valid_hands(player1, player2, temp_deck)
            if count > threshold:
                player_results[player1.player_id] = True
                player_results[player2.player_id] = True

    except Exception as e:
        print(f"Error detected: {e}")
        # 如果出现错误，返回所有玩家都fold的结果
        player_results = {player.player_id: False for player in players}

    return player_results
