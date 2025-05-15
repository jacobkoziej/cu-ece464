# cu-ece464

> The Cooper Union - ECE 464: Databases

The following was completed under the supervision of Professor
[David Katz] for the Spring of 2025. All distributed course material can
be found on the [course page].

## Getting Started

Optionally create a virtual environment:

```
$ python3 -m venv .venv
$ source .venv/bin/activate
```

Install dependencies:

```
$ pip install .
```

Create a client configuration under `~/.config/jankins/config.yaml`:

```yaml
---

username: USERNAME
passwd: PASSWORD

# the following are defaults and can be overwritten:
hostname: localhost
port: 4640
```

Or optionally pass a configuration file to the client using the
`--config` flag.

## Copyright & Licensing

Copyright (C) 2025 Jacob Koziej [`<jacobkoziej@gmail.com>`]

Distributed under the [GPLv3] or later.

[course page]: https://github.com/eugsokolov/ece464-databases
[david katz]: https://github.com/katzdave
[gplv3]: LICENSE.md
[`<jacobkoziej@gmail.com>`]: mailto:jacobkoziej@gmail.com
