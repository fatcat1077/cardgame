import random
import itertools
from card_game import Card, Player
from poker_methods import (
    create_deck,
    remove_player_hands_from_deck,
    check_player_with_community_cards,
    count_valid_hands
)
while True:
    count_times=0
    expect_times=0
    calling_times=0
    while count_times<376992:
        # 定義可能的花色和點數
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = '23456789TJQKA'

        # 創建一副完整的牌組
        full_deck = [Card(suit, rank) for suit in suits for rank in ranks]
        deck=full_deck
        # 打亂牌組
        random.shuffle(full_deck)

        # 分發給玩家手牌
        expect_times+=1
        players = []
        num_players = 4
        cards_per_player = 2

        for player_id in range(1, num_players + 1):
            hand = full_deck[:cards_per_player]
            full_deck = full_deck[cards_per_player:]
            players.append(Player(player_id=player_id, hand=hand))

        # 測試輸出玩家手牌
        #for player in players:
        #    print(f"Player {player.player_id}: {player.hand}")


        # 創建temp_deck，內容是所有的牌減掉現在玩家所有的手牌
        temp_deck = remove_player_hands_from_deck(deck, players)

        # 創建used_deck，內容是所有的牌減掉現在玩家所有的手牌
        used_deck = []
        for player in players:
            used_deck.extend(player.hand)

        #[expression for item in iterable if condition]增強式迴圈
        #更新以避免possible_hand出現過
        for player in players:
            player.update_possible_hands(used_deck)
        #print("--------------------------------------------------")
        #[print(len(player.possible_hands)) for player in players]
        #for possible in player1.possible_hands:
        #    print(possible)




        # 遍歷所有組合'
        for player1, player2 in itertools.combinations(players, 2):
            # 计算这两位玩家的count_valid_hands结果
            count_temp = count_valid_hands(player1, player2, temp_deck)
            # 判断count是否大于10
            #if count_temp>(200*0.12*0.45+200*2.5*0.06)*376992/1000000:
            if count_temp>(200*0.12*0.45)*376992/1000000:
                count_times+=count_temp
                calling_times+=1

        #假設獎池在100萬、每一手玩家加入的成本是0.12*0.45BB
    #寫入
    with open('output2.txt', 'a') as file:
        file.write(f'count_times: {count_times}, expect_times: {expect_times}, calling_times: {calling_times}\n')
    #print(count_times)
    #print(expect_times)
