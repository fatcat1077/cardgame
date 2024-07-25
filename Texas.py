import itertools

class Card:
    VALID_RANKS = '23456789TJQKA'

    def __init__(self, suit, rank):
        if rank not in Card.VALID_RANKS:
            raise ValueError(f"Invalid rank: {rank}")
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank

    def __hash__(self):
        return hash((self.suit, self.rank))

class Player:
    def __init__(self, player_id, hand):
        self.player_id = player_id
        self.hand = hand

    def __repr__(self):
        return f"Player {self.player_id} with hand {self.hand}"

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

def is_straight(ranks):
    sorted_ranks = sorted(ranks, key=lambda x: '23456789TJQKA'.index(x))
    if all('23456789TJQKA'.index(sorted_ranks[i+1]) - '23456789TJQKA'.index(sorted_ranks[i]) == 1 for i in range(len(sorted_ranks) - 1)):
        return True
    # 特別處理 A, 2, 3, 4, 5 的情況
    if sorted_ranks == ['2', '3', '4', '5', 'A']:
        return True
    return False

def is_straight_flush(cards):
    suits = [card.suit for card in cards]
    ranks = [card.rank for card in cards]
    if len(set(suits)) == 1 and is_straight(ranks):
        return True
    return False

def is_four_of_a_kind(cards):
    ranks = [card.rank for card in cards]
    for rank in ranks:
        if ranks.count(rank) == 4:
            return True
    return False

def is_full_house(cards, three_rank, two_rank):
    ranks = [card.rank for card in cards]
    if ranks.count(three_rank) == 3 and ranks.count(two_rank) == 2:
        return True
    return False

def check_special_hand(cards):
    if len(cards) != 5:
        return False

    if is_straight_flush(cards):
        return True

    if is_four_of_a_kind(cards):
        return True

    if is_full_house(cards, 'A', 'K'):
        return True

    if is_full_house(cards, 'A', 'Q'):
        return True

    if is_full_house(cards, 'A', 'J'):
        return True

    return False
#用來遍歷五張牌中三張加玩家的兩張
def check_player_with_community_cards(player, community_cards):
    for combo in itertools.combinations(community_cards, 3):
        hand = list(combo) + player.hand
        if check_special_hand(hand):
            return True
    return False

#主程式在這裡開始
deck = create_deck()

# 宣告玩家一與玩家二的手牌
player1_hand = [Card('Spades', 'A'), Card('Spades', '5')]
player2_hand = [Card('Diamonds', '2'), Card('Hearts', '2')]
player3_hand = [Card('Clubs', '6'), Card('Diamonds', '6')]
player4_hand = [Card('Hearts', '7'), Card('Spades', '7')]
player5_hand = [Card('Clubs', '8'), Card('Diamonds', '8')]
player6_hand = [Card('Hearts', '9'), Card('Spades', '9')]
player7_hand = [Card('Clubs', 'T'), Card('Diamonds', 'T')]
player8_hand = [Card('Hearts', 'J'), Card('Spades', 'J')]
player9_hand = [Card('Clubs', 'Q'), Card('Diamonds', 'Q')]

# 創建九個玩家
player1 = Player(player_id=1, hand=player1_hand)
player2 = Player(player_id=2, hand=player2_hand)
player3 = Player(player_id=3, hand=player3_hand)
player4 = Player(player_id=4, hand=player4_hand)
player5 = Player(player_id=5, hand=player5_hand)
player6 = Player(player_id=6, hand=player6_hand)
player7 = Player(player_id=7, hand=player7_hand)
player8 = Player(player_id=8, hand=player8_hand)
player9 = Player(player_id=9, hand=player9_hand)

# 創建temp_deck，內容是所有的牌減掉現在玩家所有的手牌
players = [player1, player2, player3, player4, player5, player6, player7, player8, player9]
temp_deck = remove_player_hands_from_deck(deck, players)

# 生成所有可能的五張牌組合
temp_community_cards_combinations = list(itertools.combinations(temp_deck, 5))

# 遍歷所有組合
count = 0

for temp_community_cards in temp_community_cards_combinations:
    if check_player_with_community_cards(player1, temp_community_cards) and check_player_with_community_cards(player2, temp_community_cards):
        count += 1
        #print(f"Community cards: {temp_community_cards}")

print(f"Total count: {count}")

'''
# 測試
cards1 = [Card('Spades', 'A'), Card('Spades', 'K'), Card('Spades', 'Q'), Card('Spades', 'J'), Card('Spades', 'T')]
cards2 = [Card('Hearts', '6'), Card('Hearts', '6'), Card('Hearts', '6'), Card('Hearts', '6'), Card('Spades', '6')]
cards3 = [Card('Spades', 'A'), Card('Hearts', 'A'), Card('Diamonds', 'A'), Card('Clubs', 'K'), Card('Spades', 'K')]
cards4 = [Card('Spades', 'A'), Card('Hearts', 'A'), Card('Diamonds', 'A'), Card('Clubs', 'Q'), Card('Spades', 'Q')]
cards5 = [Card('Spades', 'A'), Card('Hearts', 'A'), Card('Diamonds', 'A'), Card('Clubs', 'J'), Card('Spades', 'J')]
cards6 = [Card('Spades', '2'), Card('Hearts', '3'), Card('Diamonds', '4'), Card('Clubs', '5'), Card('Spades', 'A')]

print(check_special_hand(cards1))  # True (同花順)
print(check_special_hand(cards2))  # True (鐵支)
print(check_special_hand(cards3))  # True (AAAKK)
print(check_special_hand(cards4))  # True (AAAQQ)
print(check_special_hand(cards5))  # True (AAAJJ)
print(check_special_hand(cards6))  # True (A, 2, 3, 4, 5的順子)
'''
