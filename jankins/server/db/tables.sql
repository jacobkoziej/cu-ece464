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

CREATE TABLE IF NOT EXISTS job_state(
    value INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

DELETE FROM
    job_state;

INSERT INTO
    job_state(name)
VALUES
    ('CANCELED'),
    ('COMPLETE'),
    ('PENDING'),
    ('RUNNING'),
    ('TIMEOUT');

CREATE TABLE IF NOT EXISTS jobs(
    jid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    owner INTEGER NOT NULL,
    state INTEGER NOT NULL,
    exit_code INTEGER,
    artifact_path TEXT,
    FOREIGN KEY(owner) REFERENCES users(uid),
    FOREIGN KEY(state) REFERENCES job_state(value)
);