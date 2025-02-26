-- SPDX-License-Identifier: GPL-3.0-or-later
/*
 * dataset.sql -- sailor boat reservation dataset
 * Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>
 */
CREATE TABLE sailors(
    sid int PRIMARY KEY,
    sname varchar(30),
    rating int,
    age int
);

CREATE TABLE reserves(
    sid int,
    bid int,
    DAY date,
    PRIMARY KEY (sid, bid, DAY)
);

CREATE TABLE boats(
    bid int PRIMARY KEY,
    bname char(20),
    color char(10),
    length int
);

CREATE TABLE condition(
    bid int,
    condition int,
    inspection_time int,
    PRIMARY KEY (bid, condition, inspection_time)
);

CREATE VIEW sea_ready AS
SELECT
    b.bid AS bid,
    b.bname AS name
FROM
    boats AS b,
    (
        SELECT
            bid,
            condition
        FROM
            condition
        GROUP BY
            bid
        ORDER BY
            max(inspection_time)
    ) AS c
WHERE
    b.bid == c.bid
    AND c.condition < 3;

INSERT INTO
    sailors
VALUES
    (22, 'dusting', 7, 45),
    (29, 'brutus', 1, 33),
    (31, 'lubber', 8, 55),
    (32, 'andy', 8, 25),
    (58, 'rusty', 10, 35),
    (64, 'horatio', 7, 16),
    (71, 'zorba', 10, 35),
    (74, 'horatio', 9, 25),
    (85, 'art', 3, 25),
    (95, 'bob', 3, 63),
    (23, 'emilio', 7, 45),
    (24, 'scruntus', 1, 33),
    (35, 'figaro', 8, 55),
    (59, 'stum', 8, 25),
    (60, 'jit', 10, 35),
    (61, 'ossola', 7, 16),
    (62, 'shaun', 10, 35),
    (88, 'dan', 9, 25),
    (89, 'dye', 3, 25),
    (90, 'vin', 3, 63);

INSERT INTO
    reserves
VALUES
    (23, 104, '1998/10/10'),
    (24, 104, '1998/10/10'),
    (35, 104, '1998/8/10'),
    (59, 105, '1998/7/10'),
    (23, 105, '1998/11/10'),
    (35, 105, '1998/11/6'),
    (59, 106, '1998/11/12'),
    (60, 106, '1998/9/5'),
    (60, 106, '1998/9/8'),
    (88, 107, '1998/9/8'),
    (89, 108, '1998/10/10'),
    (90, 109, '1998/10/10'),
    (89, 109, '1998/8/10'),
    (60, 109, '1998/7/10'),
    (59, 109, '1998/11/10'),
    (62, 110, '1998/11/6'),
    (88, 110, '1998/11/12'),
    (88, 110, '1998/9/5'),
    (88, 111, '1998/9/8'),
    (61, 112, '1998/9/8'),
    (22, 101, '1998/10/10'),
    (22, 102, '1998/10/10'),
    (22, 103, '1998/8/10'),
    (22, 104, '1998/7/10'),
    (31, 102, '1998/11/10'),
    (31, 103, '1998/11/6'),
    (31, 104, '1998/11/12'),
    (64, 101, '1998/9/5'),
    (64, 102, '1998/9/8'),
    (74, 103, '1998/9/8');

INSERT INTO
    boats
VALUES
    (101, 'Interlake', 'blue', 45),
    (102, 'Interlake', 'red', 45),
    (103, 'Clipper', 'green', 40),
    (104, 'Clipper', 'red', 40),
    (105, 'Marine', 'red', 35),
    (106, 'Marine', 'green', 35),
    (107, 'Marine', 'blue', 35),
    (108, 'Driftwood', 'red', 35),
    (109, 'Driftwood', 'blue', 35),
    (110, 'Klapser', 'red', 30),
    (111, 'Sooney', 'green', 28),
    (112, 'Sooney', 'red', 28);

INSERT INTO
    condition
VALUES
    (101, 1, unixepoch('1998-10-11')),
    (101, 2, unixepoch('1998-09-06')),
    (102, 1, unixepoch('1998-10-11')),
    (102, 2, unixepoch('1998-11-11')),
    (102, 3, unixepoch('1998-09-09')),
    (103, 1, unixepoch('1998-08-11')),
    (103, 2, unixepoch('1998-11-07')),
    (103, 3, unixepoch('1998-09-09')),
    (104, 1, unixepoch('1998-10-11')),
    (104, 2, unixepoch('1998-10-12')),
    (104, 3, unixepoch('1998-08-13')),
    (104, 4, unixepoch('1998-07-18')),
    (104, 5, unixepoch('1998-11-13')),
    (105, 3, unixepoch('1998-07-12')),
    (105, 3, unixepoch('1998-11-12')),
    (105, 4, unixepoch('1998-11-07')),
    (106, 2, unixepoch('1998-11-13')),
    (106, 3, unixepoch('1998-09-06')),
    (106, 4, unixepoch('1998-09-10')),
    (107, 2, unixepoch('1998-09-11')),
    (108, 2, unixepoch('1998-10-20')),
    (109, 2, unixepoch('1998-10-30')),
    (109, 3, unixepoch('1998-08-16')),
    (109, 4, unixepoch('1998-07-19')),
    (109, 5, unixepoch('1998-11-12')),
    (110, 2, unixepoch('1998-11-07')),
    (110, 3, unixepoch('1998-11-13')),
    (110, 4, unixepoch('1998-09-08')),
    (111, 2, unixepoch('1998-09-09')),
    (112, 2, unixepoch('1998-09-10'));