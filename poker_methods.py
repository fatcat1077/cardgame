import itertools
from card_game import Card, Player

def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = '23456789TJQKA'
    deck = [Card(suit, rank) for suit in suits for rank in ranks]
    return deck

def remove_player_hands_from_deck(deck, players):
    temp_deck = deck[:]
    for player in players:
        for card in player.hand:
            temp_deck.remove(card)
    return temp_deck

#確認組合有效性
def check_player_with_community_cards(player, community_cards):
    best_hand = None
    best_hand_rank = (-1,)

    # 遍历所有7张牌中选择5张的组合
    for combo in itertools.combinations(community_cards + player.hand, 5):
        hand_rank = evaluate_hand(combo)
        if hand_rank > best_hand_rank:
            best_hand_rank = hand_rank
            best_hand = combo

    # 获取最佳手牌的牌型和比较值
    rank_type, *rank_values = best_hand_rank

    if rank_type in (7, 6):  # 铁支或葫芦
        # 比较玩家的两张手牌的rank是否都出现在best_hand中
        player_ranks = {card.rank for card in player.hand}
        best_hand_ranks = {card.rank for card in best_hand}
        if player_ranks <= best_hand_ranks:
            return True
        return False
    else:
        # 判断玩家的两张手牌是否都在最好的五张牌组合中
        player_hand_set = set(player.hand)
        best_hand_set = set(best_hand)
        if player_hand_set <= best_hand_set:
            return True
        return False


def evaluate_hand(hand):
    """
    评估给定的手牌，并返回一个表示手牌强度的元组。
    手牌强度以 (rank_type, rank_value) 的形式返回，其中：
    - rank_type：代表手牌类型的数字，越大越好（例如，同花顺为 8，铁支为 7，等等）。
    - rank_value：用于比较相同类型手牌的数值，具体含义因手牌类型而异。
    """
    rank_values = '23456789TJQKA'
    suits = [card.suit for card in hand]
    ranks = [card.rank for card in hand]
    rank_counts = {rank: ranks.count(rank) for rank in ranks}
    unique_ranks = sorted(set(ranks), key=lambda x: rank_values.index(x))
    
    # 判断同花
    is_flush = len(set(suits)) == 1
    # 判断顺子（特殊处理A,2,3,4,5顺子）
    is_straight = len(unique_ranks) == 5 and (
        rank_values.index(unique_ranks[-1]) - rank_values.index(unique_ranks[0]) == 4 or
        unique_ranks == ['2', '3', '4', '5', 'A']
    )
    # 判断同花顺
    if is_straight and is_flush:
        if unique_ranks == ['2', '3', '4', '5', 'A']:
            return (8, rank_values.index('5'))  # A2345顺子，同花顺元组返回(8, 5)
        else:
            return (8, rank_values.index(unique_ranks[-1]))  # 其他同花顺

    # 判断四条
    if 4 in rank_counts.values():
        rank_of_four = max(rank_counts, key=lambda rank: (rank_counts[rank], rank_values.index(rank)))
        # 找到剩下的一张牌
        kicker = max([rank_values.index(rank) for rank in ranks if rank != rank_of_four])
        return (7, rank_values.index(rank_of_four), kicker)
    
    # 判断葫芦
    if 3 in rank_counts.values() and 2 in rank_counts.values():
        rank_of_three = max([rank for rank, count in rank_counts.items() if count == 3], key=lambda rank: rank_values.index(rank))
        rank_of_two = max([rank for rank, count in rank_counts.items() if count == 2], key=lambda rank: rank_values.index(rank))
        # 如果有三张相同的牌，找到剩下的两张牌中的最大牌
        remaining_ranks = sorted([rank_values.index(rank) for rank in ranks if rank != rank_of_three], reverse=True)
        return (6, rank_values.index(rank_of_three), rank_values.index(rank_of_two), *remaining_ranks[:1])
    
    # 对于其他类型的手牌，返回 (1,)
    return (1,)

#刪除重複的項目
def remove_duplicates_from_nested_list(nested_list):
    """
    移除嵌套列表中重複的 Card 物件。

    :param nested_list: 一個包含許多列表的列表，這些內部列表中包含 Card 物件。
    :return: 處理完的列表，移除了重複的卡牌。
    """
    seen = set()
    result = []

    for inner_list in nested_list:
        unique_inner_list = []
        for card in inner_list:
            if (card.rank, card.suit) not in seen:
                seen.add((card.rank, card.suit))
                unique_inner_list.append(card)
        result.append(unique_inner_list)
    
    return result

def count_valid_hands(player1, player2, temp_deck):
    # 檢查兩個玩家的手牌是否有相同的 rank
    player1_ranks = {card.rank for card in player1.hand}
    player2_ranks = {card.rank for card in player2.hand}
    if player1.hand[0].rank == player2.hand[0].rank and player1.hand[1].rank == player2.hand[1].rank:
        print("chop")
        return 0
    if player1.hand[0].rank == player2.hand[1].rank and player1.hand[1].rank == player2.hand[0].rank:
        print("chop")
        return 0

    count = []

    # 取兩個玩家的possible_hands的內層list取聯集並形成新的possible_community_cards
    possible_community_cards = [
        hand1 + hand2 for hand1 in player1.possible_hands for hand2 in player2.possible_hands
    ]

    # 對每個子列表內部進行去重
    unique_possible_community_cards = []
    for community_hand in possible_community_cards:
        seen_cards = set()
        unique_hand = []
        for card in community_hand:
            card_key = (card.rank, card.suit)
            if card_key not in seen_cards:
                seen_cards.add(card_key)
                unique_hand.append(card)
        unique_possible_community_cards.append(unique_hand)

    # 遍歷unique_possible_community_cards
    for community_hand in unique_possible_community_cards:
        if len(community_hand) > 5:
            continue  # 長度大於5，跳過不需要做處理
        elif len(community_hand) == 5:
            if check_player_with_community_cards(player1, community_hand) and check_player_with_community_cards(player2, community_hand):
                count.append(community_hand)
        elif len(community_hand) == 4:
            # 長度等於4，從temp_deck中遍歷一張牌新增到possible_community_cards
            filtered_temp_deck = [card for card in temp_deck if (card.rank, card.suit) not in {(c.rank, c.suit) for c in community_hand}]
            for card in filtered_temp_deck:
                temp_community_hand = community_hand + [card]
                if check_player_with_community_cards(player1, temp_community_hand) and check_player_with_community_cards(player2, temp_community_hand):
                    count.append(temp_community_hand)
        elif len(community_hand) == 3:
            # 長度等於3，從temp_deck中遍歷兩張牌新增到possible_community_cards
            filtered_temp_deck = [card for card in temp_deck if (card.rank, card.suit) not in {(c.rank, c.suit) for c in community_hand}]
            for combo in itertools.combinations(filtered_temp_deck, 2):
                temp_community_hand = community_hand + list(combo)
                if check_player_with_community_cards(player1, temp_community_hand) and check_player_with_community_cards(player2, temp_community_hand):
                    count.append(temp_community_hand)

    # 去除count列表中的重複項
    unique_count = []
    seen = set()
    for hand in count:
        hand_key = tuple(sorted((card.rank, card.suit) for card in hand))
        if hand_key not in seen:
            seen.add(hand_key)
            unique_count.append(hand)
    #for unique in unique_count:
    #    print(unique)
    return len(unique_count)
