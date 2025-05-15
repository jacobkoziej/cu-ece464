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

## Running the Server

You can start the server by running `jankins-server`.

On startup, the server takes care of creating a database with empty
tables if they do not exist. By default this is under
`~/.local/share/jankins/database.sqlite`, however this can be changed by
specifying a configuration file withe the `--config` file.

The following configuration options are application defaults:

```yaml
---

user_data_path: null # defaults to ~/.local/share/jankins on UNIX
port: 4640
recieve_bufsize: 1024
```

> [!TIP] You can populate the server's database with synthetic data by
> feeding in a SQL script available in the repository:
>
> ```
> $ sqlite3 path/to/database.sqlite < jankins/server/db/synthetic.sql
> ```

## Running the Client

The client behaves much like `git` where you must specify a sub-command
to perform a useful application.

Adding a new action:

```
$ jankins-client action --name hello_world --command 'echo hello world'
```

Queuing up an action:

```
$ jankins-client queue --action-id ACTION_ID
```

Running a job:

```
$ jankins-client work
```

Running a job with a specific ID:

```
$ jankins-client work --job-id JOB_ID
```

Get pending jobs:

```
$ jankins-client stat
```

Get completed jobs:

```
$ jankins-client stat --state COMPLETE
```

There are more options so feel free to explore these using the `--help`
flag for each command/sub-command.

## Copyright & Licensing

Copyright (C) 2025 Jacob Koziej [`<jacobkoziej@gmail.com>`]

Distributed under the [GPLv3] or later.

[course page]: https://github.com/eugsokolov/ece464-databases
[david katz]: https://github.com/katzdave
[gplv3]: LICENSE.md
[`<jacobkoziej@gmail.com>`]: mailto:jacobkoziej@gmail.com
