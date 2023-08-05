# -*- coding: utf-8 -*-

import pytest

from libbisca.state import *


class TestGetState:
    def test__default__returns_correctly(self):
        # act
        state = get_state()

        # assert
        assert isinstance(state, State)
        assert state.hand_size == 3
        assert state.turn == Player.SOUTH


class TestState:
    def test__eq__two_equal_states__returns_correctly(self, mocker):
        # arrange
        mocker.patch("random.SystemRandom.shuffle")

        state1 = get_state()
        state2 = get_state()

        # act & assert
        assert state1 == state2

    def test__eq__two_diff_states__returns_correctly(self, mocker):
        # arrange
        mocker.patch("random.SystemRandom.shuffle")

        state1 = get_state()
        state2 = get_state()
        state2.players[Player.NORTH].hand.pop()
        state2.players[Player.NORTH].score = 120

        # act & assert
        assert state1 != state2

    @pytest.mark.parametrize("eldest", list(Player))  # TODO: check PyCharm warning
    def test__init__3cards_and_eldest_player_is_given__initializes_correctly(
        self, mocker, deck, eldest
    ):
        # arrange
        mock = mocker.patch("random.SystemRandom.shuffle")

        opponent = eldest.opponent

        # act
        state = get_state(eldest=eldest)

        # assert
        assert state.hand_size == 3
        assert state.turn == eldest
        assert state.stock == deck[:34]  # AH to 4C
        assert state.trump == get_card("AH")

        assert state.players[eldest].hand == get_cards("KC QC 6C")
        assert state.players[eldest].pile == []
        assert state.players[eldest].score == 0

        assert state.players[opponent].hand == get_cards("JC 7C 5C")
        assert state.players[opponent].pile == []
        assert state.players[opponent].score == 0

        assert state.table == []

    def test__is_endgame__init_state__returns_correctly(self):
        # arrange
        state = get_state()

        # act & assert
        assert state.is_endgame() is False

    def test__is_endgame__terminal_state__returns_correctly(self):
        # arrange
        state = get_state()
        state.stock = []
        state.players[Player.NORTH].hand = []
        state.players[Player.SOUTH].hand = []

        # act & assert
        assert state.is_endgame() is True

    def test__get_winner__init_state__raises_error(self):
        # arrange
        state = get_state()

        # act & assert
        with pytest.raises(ValueError):
            state.get_winner()

    @pytest.mark.parametrize(
        "north, south, expected",
        [
            (0, 120, Player.SOUTH),
            (30, 90, Player.SOUTH),
            (60, 60, None),
            (90, 30, Player.NORTH),
            (120, 0, Player.NORTH),
        ],
    )
    def test__get_winner__endgame_state_with_given_scores__returns_correctly(
        self, north, south, expected
    ):
        # arrange
        state = get_state()
        state.stock = []
        state.players[Player.NORTH].hand = []
        state.players[Player.SOUTH].hand = []

        state.players[Player.NORTH].score = north
        state.players[Player.SOUTH].score = south

        # act & assert
        assert state.get_winner() == expected

    # TODO: should this be in integration?
    # TODO: really need to this better -- this is an incorrect usage of parametrize
    @pytest.mark.parametrize(
        "moves, expected_results, expected_end_state_fpaths",
        [
            (
                get_cards("6C 7C JC QC"),
                [
                    None,
                    (Player.NORTH, 10, get_cards("6C 7C"), get_cards("4C 3C")),
                    None,
                    (Player.NORTH, 5, get_cards("JC QC"), get_cards("2C AC")),
                ],
                # TODO: really need directory path fixture
                [
                    "tests/unit/fixtures/default_state/1_move.json",
                    "tests/unit/fixtures/default_state/2_move.json",
                    "tests/unit/fixtures/default_state/3_move.json",
                    "tests/unit/fixtures/default_state/4_move.json",
                ],
            )
        ],
    )
    def test__play__after_given_moves__state_is_as_expected(
        self, mocker, moves, expected_results, expected_end_state_fpaths
    ):
        # arrange
        mocker.patch("random.SystemRandom.shuffle")

        # arrange, act & assert
        state = get_state()
        for move, expected_result, expected_end_state_fpath in zip(
            moves, expected_results, expected_end_state_fpaths
        ):
            expected_end_state = load_state(expected_end_state_fpath)
            assert state.play(move) == expected_result
            assert state == expected_end_state

    def test__do_random_move__init_state__works_correctly(self, mocker):
        # arrange
        mocker.patch("random.SystemRandom.shuffle")
        state1 = get_state()
        state2 = get_state()

        card = get_card("KC")
        state2.play(card)
        mock = mocker.patch("random.choice")
        mock.return_value = card

        # act
        results = state1.do_random_move()  # should play KC

        # assert
        assert state1 == state2
        assert results == (card, None)

    # TODO: should this one be in integration?
    def test__do_random_rollout__init_state__works_correctly(self):
        # arrange
        state = get_state()

        # act
        state.do_random_rollout()

        # assert
        assert state.is_endgame()
        assert (
            state.players[Player.NORTH].score + state.players[Player.SOUTH].score == 120
        )

    def test__do_random_rollout_with_controlled_random__init_state__works_correctly(
        self, mocker
    ):
        # arrange
        mocker.patch("random.SystemRandom.shuffle")
        mock = mocker.patch("random.choice")
        mock.side_effect = lambda hand: hand[-1]

        expected_state = load_state("tests/unit/fixtures/default_state/end.json")
        state = get_state()

        # act
        state.do_random_rollout()

        # assert
        assert state == expected_state


class TestLoadState:
    def test__empty_json__raises_error(self, tmp_path):
        # arrange
        fpath = tmp_path / "empty.json"
        fpath.write_text("")

        # act & assert -- TODO: need to do this better
        with pytest.raises(Exception):  # JSONDecodeError):
            load_state(fpath)

    def test__equivalent_to_default_state__returns_correctly(self, mocker):
        # arrange
        mocker.patch("random.SystemRandom.shuffle")

        expected_state = get_state()
        # TODO: need "fixture directory" stuff
        fpath = "tests/unit/fixtures/default_state/0_init.json"

        # act
        state = load_state(fpath)

        # assert
        assert expected_state == state
