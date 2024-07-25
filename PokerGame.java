import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

class Card {
    public static final String VALID_RANKS = "23456789TJQKA";
    private String suit;
    private String rank;

    public Card(String suit, String rank) {
        if (!VALID_RANKS.contains(rank)) {
            throw new IllegalArgumentException("Invalid rank: " + rank);
        }
        this.suit = suit;
        this.rank = rank;
    }

    public String getSuit() {
        return suit;
    }

    public String getRank() {
        return rank;
    }

    @Override
    public String toString() {
        return rank + " of " + suit;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        Card card = (Card) o;

        if (!suit.equals(card.suit)) return false;
        return rank.equals(card.rank);
    }

    @Override
    public int hashCode() {
        return suit.hashCode() * 31 + rank.hashCode();
    }
}

class Player {
    private int playerId;
    private List<Card> hand;

    public Player(int playerId, List<Card> hand) {
        this.playerId = playerId;
        this.hand = hand;
    }

    public int getPlayerId() {
        return playerId;
    }

    public List<Card> getHand() {
        return hand;
    }

    @Override
    public String toString() {
        return "Player " + playerId + " with hand " + hand;
    }
}

public class PokerGame {
    private static final String[] SUITS = {"Hearts", "Diamonds", "Clubs", "Spades"};
    private static final String RANKS = "23456789TJQKA";

    public static List<Card> createDeck() {
        List<Card> deck = new ArrayList<>();
        for (String suit : SUITS) {
            for (char rank : RANKS.toCharArray()) {
                deck.add(new Card(suit, String.valueOf(rank)));
            }
        }
        return deck;
    }

    public static List<Card> removePlayerHandsFromDeck(List<Card> deck, List<Player> players) {
        List<Card> tempDeck = new ArrayList<>(deck);
        for (Player player : players) {
            tempDeck.removeAll(player.getHand());
        }
        return tempDeck;
    }

    public static boolean isStraight(List<String> ranks) {
        List<Integer> indices = new ArrayList<>();
        for (String rank : ranks) {
            indices.add(RANKS.indexOf(rank));
        }
        Collections.sort(indices);
        for (int i = 0; i < indices.size() - 1; i++) {
            if (indices.get(i + 1) - indices.get(i) != 1) {
                return indices.equals(Arrays.asList(0, 1, 2, 3, 12)); // Special case for A, 2, 3, 4, 5
            }
        }
        return true;
    }

    public static boolean isStraightFlush(List<Card> cards) {
        Set<String> suits = new HashSet<>();
        List<String> ranks = new ArrayList<>();
        for (Card card : cards) {
            suits.add(card.getSuit());
            ranks.add(card.getRank());
        }
        return suits.size() == 1 && isStraight(ranks);
    }

    public static boolean isFourOfAKind(List<Card> cards) {
        List<String> ranks = new ArrayList<>();
        for (Card card : cards) {
            ranks.add(card.getRank());
        }
        for (String rank : ranks) {
            if (Collections.frequency(ranks, rank) == 4) {
                return true;
            }
        }
        return false;
    }

    public static boolean isFullHouse(List<Card> cards, String threeRank, String twoRank) {
        List<String> ranks = new ArrayList<>();
        for (Card card : cards) {
            ranks.add(card.getRank());
        }
        return Collections.frequency(ranks, threeRank) == 3 && Collections.frequency(ranks, twoRank) == 2;
    }

    public static boolean checkSpecialHand(List<Card> cards) {
        if (cards.size() != 5) {
            return false;
        }

        if (isStraightFlush(cards) || isFourOfAKind(cards)) {
            return true;
        }

        List<String> fullHouseRanks = Arrays.asList("A", "K", "Q", "J");
        for (String threeRank : fullHouseRanks) {
            for (String twoRank : fullHouseRanks) {
                if (!threeRank.equals(twoRank) && isFullHouse(cards, threeRank, twoRank)) {
                    return true;
                }
            }
        }

        return false;
    }

    public static boolean checkPlayerWithCommunityCards(Player player, List<Card> communityCards) {
        List<List<Card>> combos = combinations(communityCards, 3);
        for (List<Card> combo : combos) {
            List<Card> hand = new ArrayList<>(combo);
            hand.addAll(player.getHand());
            if (checkSpecialHand(hand)) {
                return true;
            }
        }
        return false;
    }

    public static <T> List<List<T>> combinations(List<T> list, int k) {
        List<List<T>> result = new ArrayList<>();
        combinationsHelper(list, k, 0, new ArrayList<>(), result);
        return result;
    }

    private static <T> void combinationsHelper(List<T> list, int k, int start, List<T> current, List<List<T>> result) {
        if (current.size() == k) {
            result.add(new ArrayList<>(current));
            return;
        }
        for (int i = start; i < list.size(); i++) {
            current.add(list.get(i));
            combinationsHelper(list, k, i + 1, current, result);
            current.remove(current.size() - 1);
        }
    }

    public static void main(String[] args) {
        List<Card> deck = createDeck();

        List<Card> player1Hand = Arrays.asList(new Card("Spades", "7"), new Card("Hearts", "A"));
        List<Card> player2Hand = Arrays.asList(new Card("Spades", "J"), new Card("Hearts", "2"));

        Player player1 = new Player(1, player1Hand);
        Player player2 = new Player(2, player2Hand);

        List<Player> players = Arrays.asList(player1, player2);
        List<Card> tempDeck = removePlayerHandsFromDeck(deck, players);

        List<List<Card>> tempCommunityCardsCombinations = combinations(tempDeck, 5);

        int count = 0;

        for (List<Card> tempCommunityCards : tempCommunityCardsCombinations) {
            if (checkPlayerWithCommunityCards(player1, tempCommunityCards) && checkPlayerWithCommunityCards(player2, tempCommunityCards)) {
                count++;
            }
        }

        System.out.println("Total count: " + count);
    }
}
