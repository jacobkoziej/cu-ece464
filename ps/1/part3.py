# SPDX-License-Identifier: GPL-3.0-or-later
#
# part3.py -- part 3
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer

from part2 import Base


class Condition(Base):
    __tablename__ = "condition"

    bid = Column(Integer, primary_key=True)
    condition = Column(Integer, primary_key=True)
    inspection_time = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"Condition(bid={self.bid}, condition={self.condition}, inspection_time={self.inspection_time})"
