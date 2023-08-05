# -*- coding: utf-8 -*-

import pytest

from libbisca.card import get_cards


@pytest.fixture
def deck():
    return get_cards(
        "AH 2H 3H 4H 5H 6H 7H QH JH KH AD 2D 3D 4D 5D 6D 7D QD JD KD "
        "AS 2S 3S 4S 5S 6S 7S QS JS KS AC 2C 3C 4C 5C 6C 7C QC JC KC"
    )
