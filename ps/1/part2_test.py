# SPDX-License-Identifier: GPL-3.0-or-later
#
# part2_test.py -- part 2 tests
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

import pytest

from os.path import dirname

from sqlalchemy import create_engine
from sqlalchemy.sql.expression import (
    exists,
    func,
    not_,
    select,
)
from sqlalchemy.orm import Session

from part2 import (
    Boat,
    Reservation,
    Sailor,
)


@pytest.fixture
def session() -> Session:
    engine = create_engine(f"sqlite:///{dirname(__file__)}/dataset.sqlite")

    with Session(engine) as session:
        yield session


def test_1(session: Session) -> None:
    query = (
        session.query(
            Boat.bid,
            Boat.bname,
            func.count(Reservation.bid),
        )
        .join(Reservation, Boat.bid == Reservation.bid)
        .group_by(Boat.bid)
    )

    expected = [
        (101, "Interlake", 2),
        (102, "Interlake", 3),
        (103, "Clipper", 3),
        (104, "Clipper", 5),
        (105, "Marine", 3),
        (106, "Marine", 3),
        (107, "Marine", 1),
        (108, "Driftwood", 1),
        (109, "Driftwood", 4),
        (110, "Klapser", 3),
        (111, "Sooney", 1),
        (112, "Sooney", 1),
    ]

    result = query.all()

    assert expected == result


def test_2(session: Session) -> None:
    subquery_reserves = (
        session.query(Reservation.bid)
        .filter(
            Reservation.bid == Boat.bid,
            Reservation.sid == Sailor.sid,
            Boat.color == "red",
        )
        .subquery()
    )

    subquery_boats = (
        session.query(Boat.bid)
        .filter(not_(exists(subquery_reserves)))
        .subquery()
    )

    query = session.query(Sailor.sid).filter(exists(subquery_boats))

    expected = []

    result = query.all()

    assert expected == result


def test_3(session: Session) -> None:
    subquery_boats = session.query(Boat.bid).filter(Boat.color == "red")

    subquery_reserves = session.query(Reservation.sid).filter(
        Reservation.bid.notin_(subquery_boats)
    )

    query = session.query(Sailor.sid, Sailor.sname).filter(
        Sailor.sid.notin_(subquery_reserves)
    )

    expected = [
        (29, "brutus"),
        (32, "andy"),
        (58, "rusty"),
        (71, "zorba"),
        (85, "art"),
        (95, "bob"),
        (23, "emilio"),
        (24, "scruntus"),
        (35, "figaro"),
        (61, "ossola"),
        (62, "shaun"),
    ]

    result = query.all()

    assert expected == result


def test_4(session: Session) -> None:
    query = (
        session.query(Boat.bid, Boat.bname)
        .join(Reservation, Boat.bid == Reservation.bid)
        .group_by(Boat.bid)
        .order_by(func.count(Boat.bid).desc())
        .limit(1)
    )

    expected = [(104, "Clipper")]

    result = query.all()

    assert expected == result


def test_5(session: Session) -> None:
    subquery_boats = session.query(Boat.bid).filter(Boat.color == "red")

    subquery_reserves = session.query(Reservation.sid).filter(
        Reservation.bid.in_(subquery_boats)
    )

    query = session.query(Sailor.sid, Sailor.sname).filter(
        Sailor.sid.notin_(subquery_reserves)
    )

    expected = [
        (29, "brutus"),
        (32, "andy"),
        (58, "rusty"),
        (71, "zorba"),
        (74, "horatio"),
        (85, "art"),
        (95, "bob"),
        (60, "jit"),
        (90, "vin"),
    ]

    result = query.all()

    assert expected == result


def test_6(session: Session) -> None:
    query = session.query(func.avg(Sailor.age)).filter(Sailor.rating == 10)

    expected = [(35.0,)]

    result = query.all()

    assert expected == result


def test_7(session: Session) -> None:
    query = (
        session.query(Sailor.sid, Sailor.sname, Sailor.rating)
        .group_by(Sailor.rating)
        .having(func.min(Sailor.age))
    )

    expected = [
        (29, "brutus", 1),
        (85, "art", 3),
        (64, "horatio", 7),
        (32, "andy", 8),
        (74, "horatio", 9),
        (58, "rusty", 10),
    ]

    result = query.all()

    assert expected == result


def test_8(session: Session) -> None:
    reserves_count = (
        select(
            Reservation.bid,
            Reservation.sid,
            func.count(Reservation.sid).label("reserved_count"),
        )
        .group_by(Reservation.sid, Reservation.bid)
        .cte("reserves_count")
    )

    query = (
        session.query(
            reserves_count.c.bid,
            reserves_count.c.sid,
            reserves_count.c.reserved_count,
        )
        .group_by(reserves_count.c.bid)
        .having(func.max(reserves_count.c.reserved_count))
    )

    expected = [
        (101, 22, 1),
        (102, 22, 1),
        (103, 22, 1),
        (104, 22, 1),
        (105, 23, 1),
        (106, 60, 2),
        (107, 88, 1),
        (108, 89, 1),
        (109, 59, 1),
        (110, 88, 2),
        (111, 88, 1),
        (112, 61, 1),
    ]

    result = query.all()

    assert expected == result
