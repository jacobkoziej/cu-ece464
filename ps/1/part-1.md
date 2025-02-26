# part-1

1. List, for every boat, the number of times it has been reserved,
   excluding those boats that have never been reserved (list the id and
   the name).

```sql
SELECT
    b.bid AS id,
    b.bname AS name,
    count(b.bid) AS "reservation count"
FROM
    boats AS b,
    reserves AS r
WHERE
    b.bid = r.bid
GROUP BY
    b.bid;
```

```
+-----+-----------+-------------------+
| id  |   name    | reservation count |
+-----+-----------+-------------------+
| 101 | Interlake | 2                 |
| 102 | Interlake | 3                 |
| 103 | Clipper   | 3                 |
| 104 | Clipper   | 5                 |
| 105 | Marine    | 3                 |
| 106 | Marine    | 3                 |
| 107 | Marine    | 1                 |
| 108 | Driftwood | 1                 |
| 109 | Driftwood | 4                 |
| 110 | Klapser   | 3                 |
| 111 | Sooney    | 1                 |
| 112 | Sooney    | 1                 |
+-----+-----------+-------------------+
```

2. List those sailors who have reserved every red boat (list the id and
   the name).

```sql
SELECT
    s.sid AS id,
    s.sname AS name
FROM
    sailors AS s
WHERE
    NOT EXISTS (
        SELECT
            b.bid
        FROM
            boats AS b
        WHERE
            NOT EXISTS (
                SELECT
                    r.bid
                FROM
                    reserves AS r
                WHERE
                    r.bid = b.bid
                    AND r.sid = s.sid
                    AND b.color = 'red'
            )
    );
```

```
NO MATCHES
```

3. List those sailors who have reserved only red boats.

```sql
SELECT
    s.sid AS id,
    s.sname AS name
FROM
    sailors AS s
WHERE
    s.sid NOT IN (
        SELECT
            r.sid
        FROM
            reserves AS r
        WHERE
            r.bid NOT IN (
                SELECT
                    b.bid
                FROM
                    boats AS b
                WHERE
                    b.color = 'red'
            )
    );
```

```
+----+----------+
| id |   name   |
+----+----------+
| 29 | brutus   |
| 32 | andy     |
| 58 | rusty    |
| 71 | zorba    |
| 85 | art      |
| 95 | bob      |
| 23 | emilio   |
| 24 | scruntus |
| 35 | figaro   |
| 61 | ossola   |
| 62 | shaun    |
+----+----------+
```

4. For which boat are there the most reservations?

```sql
SELECT
    b.bid AS id,
    b.bname AS name
FROM
    boats AS b,
    reserves AS r
WHERE
    b.bid = r.bid
GROUP BY
    b.bid
ORDER BY
    count(b.bid) DESC
LIMIT
    1;
```

```
+-----+---------+
| id  |  name   |
+-----+---------+
| 104 | Clipper |
+-----+---------+
```

5. Select all sailors who have never reserved a red boat.

```sql
SELECT
    s.sid AS id,
    s.sname AS name
FROM
    sailors AS s
WHERE
    s.sid NOT IN (
        SELECT
            r.sid
        FROM
            reserves AS r
        WHERE
            r.bid IN (
                SELECT
                    b.bid
                FROM
                    boats AS b
                WHERE
                    b.color = 'red'
            )
    );
```

```
+----+---------+
| id |  name   |
+----+---------+
| 29 | brutus  |
| 32 | andy    |
| 58 | rusty   |
| 71 | zorba   |
| 74 | horatio |
| 85 | art     |
| 95 | bob     |
| 60 | jit     |
| 90 | vin     |
+----+---------+
```

6. Find the average age of sailors with a rating of 10.

```sql
SELECT
    avg(s.age) AS "average age"
FROM
    sailors AS s
WHERE
    s.rating = 10;
```

```
+-------------+
| average age |
+-------------+
| 35.0        |
+-------------+
```

7. For each rating, find the name and id of the youngest sailor.

```sql
SELECT
    s.sid AS id,
    s.sname AS name,
    s.rating AS rating
FROM
    sailors AS s
GROUP BY
    s.rating
HAVING
    min(s.age);
```

```
+----+---------+--------+
| id |  name   | rating |
+----+---------+--------+
| 29 | brutus  | 1      |
| 85 | art     | 3      |
| 64 | horatio | 7      |
| 32 | andy    | 8      |
| 74 | horatio | 9      |
| 58 | rusty   | 10     |
+----+---------+--------+
```

8. Select, for each boat, the sailor who made the highest number of
   reservations for that boat.

```sql
WITH reserves_count(sid, bid, reserved_count) AS (
    SELECT
        bid,
        sid,
        count(sid)
    FROM
        reserves
    GROUP BY
        sid,
        bid
)
SELECT
    sid,
    bid,
    reserved_count AS reservations
FROM
    reserves_count
GROUP BY
    bid
HAVING
    max(reserved_count);
```

```
+-----+-----+--------------+
| bid | sid | reservations |
+-----+-----+--------------+
| 101 | 22  | 1            |
| 102 | 22  | 1            |
| 103 | 22  | 1            |
| 104 | 22  | 1            |
| 105 | 23  | 1            |
| 106 | 60  | 2            |
| 107 | 88  | 1            |
| 108 | 89  | 1            |
| 109 | 59  | 1            |
| 110 | 88  | 2            |
| 111 | 88  | 1            |
| 112 | 61  | 1            |
+-----+-----+--------------+
```
