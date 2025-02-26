# SPDX-License-Identifier: GPL-3.0-or-later
#
# part3_test.py -- part 3 tests
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

import pytest

from os.path import dirname

from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import Session

from part2 import Boat
from part3 import Condition


@pytest.fixture
def session() -> Session:
    engine = create_engine(f"sqlite:///{dirname(__file__)}/dataset.sqlite")

    with Session(engine) as session:
        yield session


def test_sea_ready(session: Session) -> None:
    subquery = (
        session.query(Condition.bid, Condition.condition)
        .group_by(Condition.bid)
        .order_by(func.max(Condition.inspection_time))
        .subquery()
    )

    query = (
        session.query(
            Boat.bid,
            Boat.bname,
        )
        .join(subquery, Boat.bid == subquery.c.bid)
        .filter(subquery.c.condition < 3)
    )

    expected = [
        (111, "Sooney"),
        (112, "Sooney"),
        (107, "Marine"),
        (101, "Interlake"),
        (108, "Driftwood"),
        (103, "Clipper"),
        (102, "Interlake"),
        (106, "Marine"),
    ]

    result = query.all()

    assert expected == result
