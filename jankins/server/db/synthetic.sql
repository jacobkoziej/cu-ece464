-- SPDX-License-Identifier: GPL-3.0-or-later
/*
 * synthetic.sql -- jankins server synthetic data
 * Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>
 */
INSERT INTO
    users(username, passwd)
VALUES
    ('alek.turkmen', 'founder'),
    ('david.katz', 'prof'),
    ('evan.rosenfeld', 'present'),
    ('grace.ee', 'infinite'),
    ('isaiah.rivera', '$10'),
    ('jacob.koziej', 'cooked'),
    ('joya.debi', 'goya'),
    ('nicholas.storniolo', 'carvel'),
    ('surinderpal.singh', 'hm'),
    ('vaibhav.hariani', 'f1');

INSERT INTO
    actions(name, command, active)
VALUES
    (
        'boulder',
        'dd if=/dev/random of=boulder bs=1M count=1',
        TRUE
    ),
    ('client date', 'date', TRUE),
    ('fetch os-release', 'cp /etc/os-release .', TRUE),
    ('long-runner', 'sleep 3600', TRUE),
    ('malicious', 'cp /etc/passwd', FALSE);

INSERT INTO
    jobs(
        id,
        ACTION,
        owner,
        state,
        start_time,
        end_time,
        heartbeat_time,
        exit_code
    )
VALUES
    (
        1,
        3,
        6,
        1,
        1746513810905108065,
        513810956117748,
        513810905108242,
        0
    ),
    (
        2,
        2,
        6,
        1,
        1746514361984532115,
        514362010593597,
        514361984532407,
        0
    ),
    (
        3,
        1,
        6,
        1,
        1746514364139261644,
        514364196324812,
        514364139261802,
        0
    ),
    (
        4,
        4,
        6,
        4,
        1746514366701302307,
        NULL,
        514369778649124,
        NULL
    );