-- SPDX-License-Identifier: GPL-3.0-or-later
/*
 * tables.sql -- jankins server tables
 * Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>
 */
CREATE TABLE IF NOT EXISTS users(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    passwd TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS actions(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    command TEXT NOT NULL,
    active BOOL NOT NULL DEFAULT TRUE
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
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    ACTION INTEGER NOT NULL,
    owner INTEGER,
    state INTEGER NOT NULL,
    start_time INTEGER,
    end_time INTEGER,
    exit_code INTEGER,
    artifact_path TEXT,
    FOREIGN KEY(ACTION) REFERENCES actions(id),
    FOREIGN KEY(owner) REFERENCES users(id),
    FOREIGN KEY(state) REFERENCES job_state(value)
);