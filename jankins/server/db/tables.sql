-- SPDX-License-Identifier: GPL-3.0-or-later
/*
 * tables.sql -- jankins server tables
 * Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>
 */
CREATE TABLE IF NOT EXISTS users(
    uid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    passwd TEXT NOT NULL
);