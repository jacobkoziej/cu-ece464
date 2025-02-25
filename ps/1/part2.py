# SPDX-License-Identifier: GPL-3.0-or-later
#
# part2.py -- part 2
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

from sqlalchemy.orm import (
    DeclarativeBase,
    backref,
    relationship,
)
from sqlalchemy.schema import (
    Column,
    ForeignKey,
    PrimaryKeyConstraint,
)
from sqlalchemy.types import (
    DateTime,
    Integer,
    String,
)


class Base(DeclarativeBase):
    pass


class Sailor(Base):
    __tablename__ = "sailors"

    sid = Column(Integer, primary_key=True)
    sname = Column(String(30))
    rating = Column(Integer)
    age = Column(Integer)

    def __repr__(self):
        return f"Sailor(id={self.sid}, name='{self.sname}', age={self.age})"


class Boat(Base):
    __tablename__ = "boats"

    bid = Column(Integer, primary_key=True)
    bname = Column(String(20))
    color = Column(String(10))
    length = Column(Integer)

    reservations = relationship(
        "Reservation",
        backref=backref("boat", cascade="delete"),
    )

    def __repr__(self):
        return f"Boat(id={self.bid}, name='{self.bname}', color='{self.color}', length={self.length})"


class Reservation(Base):
    __tablename__ = "reserves"
    __table_args__ = (PrimaryKeyConstraint("sid", "bid", "day"),)

    sid = Column(Integer, ForeignKey("sailors.sid"))
    bid = Column(Integer, ForeignKey("boats.bid"))
    day = Column(DateTime)

    sailor = relationship("Sailor")

    def __repr__(self):
        return f"Reservation(sid={self.sid}, bid={self.bid}, day={self.day})"
