# -*- coding: utf-8 -*-

# TODO: improve docstrings
"""Card

Implements Bisca card related classes.

This module exports the following classes:
    * Rank - enum representing all ranks supported by Bisca cards: 23456QJK7A
    * Suit - enum representing all suits: Hearts, Diamonds, Spades, Clubs
    * Card - Bisca Card

This module exports the following functions:
    * get_card -- TODO
    * get_cards -- TODO
    * get_deck -- returns a shuffled bisca deck
"""
# TODO: improve doctring
# TODO: convert Card to Enum?

from dataclasses import dataclass
from enum import Enum
from random import SystemRandom
from typing import List


class Rank(Enum):
    # order, repr, score
    TWO = 0, "2", 0
    THREE = 1, "3", 0
    FOUR = 2, "4", 0
    FIVE = 3, "5", 0
    SIX = 4, "6", 0
    QUEEN = 5, "Q", 2
    JACK = 6, "J", 3
    KING = 7, "K", 4
    SEVEN = 8, "7", 10
    ACE = 9, "A", 11

    def __init__(self, order, repr_, score):
        self.order = order
        self.repr = repr_
        self.score = score

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.order > other.order
        return NotImplemented

    def __repr__(self):
        return f"{self.repr}"


_STR_TO_RANK = {rank.repr: rank for rank in Rank}


class Suit(Enum):

    HEARTS = "H"
    DIAMONDS = "D"
    SPADES = "S"
    CLUBS = "C"

    def __repr__(self):
        return f"{self.value}"  # TODO: add "pprint" (unicode card suits?)


_STR_TO_SUIT = {suit.value: suit for suit in Suit}


# TODO: optimization to access "singleton" cards in DECK or... turn this into Enum
@dataclass(frozen=True)  # TODO: performance hit, check in profiling
class Card:
    rank: Rank
    suit: Suit

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.rank > other.rank
        return NotImplemented

    def __repr__(self):
        # "Although practicality beats purity." -- The Zen of Python
        return f"{self.rank!r}{self.suit!r}"

    @property
    def score(self) -> int:
        return self.rank.score


Cards = List[Card]


def get_deck(shuffle: bool = True) -> Cards:
    # TODO: needs to be like this for the mock.patch to work in tests - think about it later (it's slower)
    deck = [Card(_STR_TO_RANK[r], s) for s in Suit for r in "A234567QJK"]

    if shuffle:
        # SystemRandom is necessary to generate all of the 40! possibilities
        # TODO: possible alternative with less issues, need to research deck = random.sample(deck, len(deck))
        SystemRandom().shuffle(deck)

    return deck


def get_card(card: str) -> Card:
    # helper function, useful for testing
    rank, suit = card
    return Card(_STR_TO_RANK[rank], _STR_TO_SUIT[suit])


def get_cards(cards: str) -> Cards:
    # helper function, useful for testing
    return [get_card(c) for c in cards.split(" ") if c != ""]
