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
        self.possible_hands = []  # 初始化為空列表
        self.initialize_possible_hands()

    def __repr__(self):
        return f"Player {self.player_id} with hand {self.hand}"

    def initialize_possible_hands(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = '23456789TJQKA'

        def get_other_suits(exclude_suits):
            return [suit for suit in suits if suit not in exclude_suits]

        hand_ranks = [card.rank for card in self.hand]
        hand_suits = [card.suit for card in self.hand]
        
        # 判斷是否是 AA 組合
        if hand_ranks[0] == 'A' and hand_ranks[1] == 'A':
            other_suits_A = get_other_suits(hand_suits)
            for suit_A in other_suits_A:
                for suits_combo in itertools.combinations(suits, 2):
                    self.possible_hands.append([Card(suit_A, 'A'), Card(suits_combo[0], 'J'), Card(suits_combo[1], 'J')])
                    self.possible_hands.append([Card(suit_A, 'A'), Card(suits_combo[0], 'Q'), Card(suits_combo[1], 'Q')])
                    self.possible_hands.append([Card(suit_A, 'A'), Card(suits_combo[0], 'K'), Card(suits_combo[1], 'K')])
        
        # 判斷是否是 AJ, AQ, AK 組合
        if set(hand_ranks) == {'A', 'J'} or set(hand_ranks) == {'A', 'Q'} or set(hand_ranks) == {'A', 'K'}:
            target_rank = [rank for rank in hand_ranks if rank != 'A'][0]
            other_suits_A = get_other_suits([card.suit for card in self.hand if card.rank == 'A'])
            other_suits_B = get_other_suits([card.suit for card in self.hand if card.rank == target_rank])
            for suit1 in itertools.combinations(other_suits_A, 2):
                for suit2 in other_suits_B:
                    self.possible_hands.append([Card(suit1[0], 'A'), Card(suit1[1], 'A'), Card(suit2, target_rank)])

        # 判斷是否是對子的組合
        if hand_ranks[0] == hand_ranks[1]:
            other_suits = get_other_suits(hand_suits)
            self.possible_hands.append([Card(other_suits[0], hand_ranks[0]), Card(other_suits[1], hand_ranks[0])])

        # 判斷是否是兩張不同數字的牌的組合
        if hand_ranks[0] != hand_ranks[1]:
            min_rank = min(hand_ranks, key=lambda x: ranks.index(x))
            max_rank = max(hand_ranks, key=lambda x: ranks.index(x))
            min_suits = get_other_suits([card.suit for card in self.hand if card.rank == min_rank])
            max_suits = get_other_suits([card.suit for card in self.hand if card.rank == max_rank])
            
            # 生成與較低rank同rank但不同花色的三張牌
            self.possible_hands.append([Card(suit, min_rank) for suit in min_suits[:3]])
            
            # 生成與較高rank同rank不同花色的三張牌
            self.possible_hands.append([Card(suit, max_rank) for suit in max_suits[:3]])

        # 判斷是否是兩張同樣花色的牌且數字相差小於等於4的組合
        if hand_suits[0] == hand_suits[1] and (abs(ranks.index(hand_ranks[0]) - ranks.index(hand_ranks[1])) <= 4 or set(hand_ranks) & {'A', '2', '3', '4', '5'}):
            min_rank = min(hand_ranks, key=lambda x: ranks.index(x))
            max_rank = max(hand_ranks, key=lambda x: ranks.index(x))
            min_index = ranks.index(min_rank)
            max_index = ranks.index(max_rank)

            def append_if_valid(indexes):
                if all(0 <= idx < len(ranks) for idx in indexes):
                    self.possible_hands.append([Card(hand_suits[0], ranks[idx]) for idx in indexes])

            if max_index - min_index == 4:
                append_if_valid([min_index+1, min_index+2, min_index+3])
            elif max_index - min_index == 3:
                append_if_valid([min_index-1, min_index+1, min_index+2])
                append_if_valid([min_index+1, min_index+2, min_index+4])
            elif max_index - min_index == 2:
                append_if_valid([min_index-2, min_index-1, min_index+1])
                append_if_valid([min_index-1, min_index+1, min_index+3])
                append_if_valid([min_index+1, min_index+3, min_index+4])
            elif max_index - min_index == 1:
                append_if_valid([min_index-3, min_index-2, min_index-1])
                append_if_valid([min_index-2, min_index-1, min_index+2])
                append_if_valid([min_index-1, min_index+2, min_index+3])
                append_if_valid([min_index+2, min_index+3, min_index+4])
            
            ##這一段用於特判A下順的情況
            if '5' in hand_ranks and 'A' in hand_ranks :
                self.possible_hands.append([ Card(hand_suits[0], '2'), Card(hand_suits[0], '3'), Card(hand_suits[0], '4')])
            if '5' in hand_ranks and '2' in hand_ranks :
                self.possible_hands.append([ Card(hand_suits[0], 'A'), Card(hand_suits[0], '3'), Card(hand_suits[0], '4')])
            if '5' in hand_ranks and '3' in hand_ranks :
                self.possible_hands.append([ Card(hand_suits[0], 'A'), Card(hand_suits[0], '2'), Card(hand_suits[0], '4')])
            if '5' in hand_ranks and '4' in hand_ranks :
                self.possible_hands.append([ Card(hand_suits[0], 'A'), Card(hand_suits[0], '2'), Card(hand_suits[0], '3')])
            if '4' in hand_ranks and 'A' in hand_ranks :
                self.possible_hands.append([ Card(hand_suits[0], '2'), Card(hand_suits[0], '3'), Card(hand_suits[0], '5')])
            if '4' in hand_ranks and '2' in hand_ranks :
                self.possible_hands.append([ Card(hand_suits[0], 'A'), Card(hand_suits[0], '3'), Card(hand_suits[0], '5')])
            if '4' in hand_ranks and '3' in hand_ranks :
                self.possible_hands.append([ Card(hand_suits[0], 'A'), Card(hand_suits[0], '2'), Card(hand_suits[0], '5')])
            if '3' in hand_ranks and 'A' in hand_ranks :
                self.possible_hands.append([ Card(hand_suits[0], '2'), Card(hand_suits[0], '4'), Card(hand_suits[0], '5')])
            if '3' in hand_ranks and '2' in hand_ranks :
                self.possible_hands.append([ Card(hand_suits[0], 'A'), Card(hand_suits[0], '4'), Card(hand_suits[0], '5')])
            if '2' in hand_ranks and 'A' in hand_ranks :
                self.possible_hands.append([ Card(hand_suits[0], '3'), Card(hand_suits[0], '4'), Card(hand_suits[0], '5')])
            
    #用於檢查有沒有在used_hand中
    def update_possible_hands(self, used_hand):
        self.possible_hands = [
            hand for hand in self.possible_hands
            if not any(card in used_hand for card in hand)
        ]        
            
            
            
            