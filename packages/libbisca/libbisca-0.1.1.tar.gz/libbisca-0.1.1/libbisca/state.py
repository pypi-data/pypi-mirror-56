# -*- coding: utf-8 -*-

"""Bisca State

Implements the rules for Bisca.

This module exports the following classes:
    * State - bisca state implementing a specific variant TODO: document this better, subclass for variant
    * Player - enum representing all players: North, South
    * PlayerState - dataclass containing Player data (hand, pile, score) used in State

This module exports the following functions:
    * get_state - factory function, returns an initialized State (with default settings)
    * load_state - loads state from json
"""
# TODO: add typing only functions to this and card? or use .pyi?

from dataclasses import dataclass, field
from enum import Enum, auto
import json
import random
from typing import Dict, List, Tuple, Optional

# TODO: check issues with relative imports
from libbisca.card import Card, Cards, get_card, get_cards, get_deck


class Player(Enum):
    NORTH = auto()
    SOUTH = auto()

    def __repr__(self):
        return "North" if self == Player.NORTH else "South"

    @property
    def opponent(self) -> "Player":
        return Player.NORTH if self == Player.SOUTH else Player.SOUTH


PlayResult = Tuple[Player, int, Cards, Optional[Cards]]


@dataclass
class PlayerState:
    hand: Cards = field(default_factory=list)
    pile: List[Cards] = field(default_factory=list)  # TODO: is pile necessary?
    score: int = 0


def _get_players_states():
    return {p: PlayerState() for p in Player}


# TODO: more specific? table max 2 cards, pile list or 2cards -- use tuple?
@dataclass
class State:
    # standard rules - TODO: recheck rules

    hand_size: int
    turn: Player
    stock: Cards = field(default_factory=get_deck)
    trump: Card = None  # TODO: mypy error here, how to tell it to ignore it
    players: Dict[Player, PlayerState] = field(default_factory=_get_players_states)
    table: Cards = field(default_factory=list)

    # TODO: may be useful not to use field in any and just use a __init__ with super, etc. -- works better with load_state
    # TODO: need to do something to prevent __post_init__ from running if full state is loaded, for now, hack in load_state
    def __post_init__(self):
        self.trump: Card = self.stock[0]

        # deal cards to players
        for _ in range(self.hand_size):
            self._deal()

    @property
    def legal_moves(self) -> List[Card]:
        # this allows player to play any card in hand, subclass if that is not so
        return self.players[self.turn].hand

    def get_winner(self) -> Optional[Player]:
        if self.is_endgame():
            assert (
                self.players[Player.NORTH].score + self.players[Player.SOUTH].score
                == 120
            )

            if self.players[Player.NORTH].score > self.players[Player.SOUTH].score:
                return Player.NORTH
            elif self.players[Player.NORTH].score < self.players[Player.SOUTH].score:
                return Player.SOUTH
            else:
                return None  # Draw
        else:
            raise ValueError("game is not in endgame")  # TODO: better exception and msg

    def is_endgame(self) -> bool:
        return (
            len(self.stock)
            + len(self.players[Player.NORTH].hand)
            + len(self.players[Player.SOUTH].hand)
            == 0
        )

    def play(self, move: Card) -> Optional[PlayResult]:
        # return None or (winner, added_score, table [eldest, youngest], dealt_cards [winner, loser]) - TODO: all needed?

        # basic "take from hand and put in table"
        self.players[self.turn].hand.remove(move)
        self.table.append(move)

        if len(self.table) == 1:
            # eldest played
            self.turn = self.turn.opponent
            return None
        else:
            # youngest played
            winner = self._get_round_winner()

            added_score = sum(card.score for card in self.table)
            self.players[winner].score += added_score

            table = self.table
            self.players[winner].pile.append(table)
            self.table = []

            self.turn = winner
            dealt = self._deal() if self.stock else None

            return winner, added_score, table, dealt

    def do_random_move(self) -> Tuple[Card, Optional[PlayResult]]:
        # helpful for agents
        move = random.choice(self.legal_moves)
        return move, self.play(move)

    def do_random_rollout(self) -> None:
        while not self.is_endgame():
            self.do_random_move()
        # no need to return anything?

    def _deal(self) -> Cards:
        # return [new_winner_card, new_loser_card]
        dealt = []

        for player in (self.turn, self.turn.opponent):
            card = self.stock.pop()
            self.players[player].hand.append(card)
            dealt.append(card)

        return dealt

    # TODO: test this
    def _get_round_winner(self) -> Player:
        card1, card2 = self.table
        youngest = self.turn
        eldest = self.turn.opponent

        # follow is not mandatory, but if youngest plays a different suit than is not trump, eldest wins
        if card1.suit != card2.suit:
            if card2.suit == self.trump.suit:
                return youngest
            return eldest

        # default
        return eldest if card1 > card2 else youngest


def get_state(
    hand_size: int = 3, eldest: Player = Player.SOUTH, shuffle: bool = True
) -> State:
    # only testing for 3 for now

    if shuffle:
        return State(hand_size=hand_size, turn=eldest)
    else:
        return State(hand_size=hand_size, turn=eldest, stock=get_deck(shuffle=shuffle))


def load_state(fpath: str) -> State:
    # loads from json
    with open(fpath) as fp:
        return json.load(fp, object_hook=_decode_state)


# TODO: needs save_state


def _decode_state(dct) -> State:
    hand_size = dct["hand_size"]
    turn = Player.NORTH if dct["turn"] == "North" else Player.SOUTH

    stock = get_cards(dct["stock"])
    trump = get_card(dct["trump"])

    hands = dct["hands"]
    piles = dct["piles"]
    scores = dct["scores"]

    players = {}
    for player, hand, pile, score in zip(
        list(Player), hands, piles, scores
    ):  # TODO: check this PyCharm warning
        players[player] = PlayerState(
            get_cards(hand), [get_cards(s) for s in pile], score
        )

    table = get_cards(dct["table"])

    state = State(
        hand_size=hand_size, turn=turn
    )  # stock=stock, trump=trump, players=players, table=table)
    # TODO: hmm, need to handle full load better

    state.turn = turn
    state.stock = stock
    state.trump = trump
    state.players = players
    state.table = table

    return state
