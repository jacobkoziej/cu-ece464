# write-up

For my final project I've decided to implement a jank version of
Jenkins, hence jankins. That said, jankins implements the bare minimum
of what I consider acceptable for such software: basic authentication,
action definitions, job history, artifact storage, support for queuing
and executing jobs, and basic functionality to query the job history.

## Changes from the Original Plan

The major change from my initial proposal has been a shift from having a
distinction between clients and workers. The initial plan intended to
have a pool of workers connected to the main server at all times
awaiting a job with clients which connect ever so often to queue up new
jobs. In the final implementation, clients and workers share most of the
same code and do not stay connected to the server longer than necessary
to avoid keeping open sockets. Instead of the server delegating which
worker gets which job, the server instead hands out jobs on a first come
basis, meaning that workers request jobs only when they wish to work on
a new job.

Another change involves dropping CPU time (since this varies between
different hosts) and swapping out using squashfs for artifacts to zip
files. The server's database schema was also adjusted slightly to remove
redundancy by combining the queue history, job queue, worker, and job
tables into one unified jobs table. This was done to allow rows to be
updated instead of necessitating moving them between tables throughout
the lifetime of a job.

## Database and Data Description

Data storage is split into three parts: a configuration file, SQLite
database, and on-disk storage of artifacts associated with jobs.

The configuration file is read to determine which port to bind the
server to, a path for user data storage, and a default buffer size for
received data. All values have defaults, but can optionally be
overwritten on server startup.

The database itself has four primary tables: users, actions, job states,
and jobs. The users table stores usernames and passwords along with a
unique user id. The actions table keeps track of commands that can be
executed for jobs. Each action has a name, a unique id, and a field
indicating that the action is active or disabled. The job states table
acts as an enumeration of different job states to avoid having to store
tons of strings in the job table. Finally, the jobs table has a unique
entry for each job keeping track of the user that worked on the job, the
action associated to the job, state, when the job was started and ended,
the exit code of the completed process on the client, as well as a
hidden column used to keep track of worker heartbeats to allow for jobs
to be timed-out.

That leaves us with stored artifacts. Since each job has a unique id,
all completed jobs have their artifacts written on disk as a zip file
where the name corresponds to the job id. We can then store these
relative to the user data path allowing us to implicitly find all
artifact paths.

## Functionality Description

A server starts and creates a database if it doesn't exist. Once
created, it will start a TCP server which awaits connections from
registered clients. When a client creates a connection, the server
spawns a thread for the connection and authenticates the client. If
authentication is successful, the server attempts to execute the action
requested by the client and returns the appropriate response.

On the client side, an new action can be added to the server, actions
can be added to the queue, jobs can be executed, and basic queries made
about jobs in different states (COMPLETE, PENDING, TIMEOUT, RUNNING).
Most of these sub-commands are one-shot and result in the process
exiting the moment a response is received. However, when the client
decides to work, a job may take a non-zero amount of time, so additional
"heartbeat" messages are sent to the server every 500ms to "prove" that
the job is still being executed. If the server or client fails to
send/acknowledge the heartbeat, the job client ceases execution of the
job and the server will perform house keeping and change the state of
the job from RUNNING to TIMEOUT.

## Known Bugs or Missing Features

- Unsafe authentication due to no encryption or hashing of passwords.
- No way for clients to query available actions.
- No way for a client to change job to active/inactive.
- No way for a client to register with the server.
- No way for a client to fetch job artifacts.
- A few unhandled exceptions which can unexpectedly cause TCP connection
  threads to crash.

## Technical Highlight

The most challenging part of this project was dealing with concurrency
and inter-process communication (IPC).

Since the server and client are different processes and potentially on
different machines, the most sensible means of communication was over a
socket. This proved particularly difficult as I had to write my own IPC
protocol from scratch to make sure both processes could be in agreement.
To get around this I decided to utilize [MessagePack], a more efficient
binary version of JSON. I found this beneficial to creating something
like a REST API as it required far less overhead to implement, and with
a recursive decoder and encoder, made the socket communication seem
transparent as Python objects would be rebuilt on the server and client.

Once I had a protocol settled on, I also had to figure out how to best
debug logic errors between my server and client. I ended up finding that
writing skeleton scripts to get the server and client to a known state
vastly sped up the process. I found this to let me avoid the time
investment of writing unit tests since it allowed me to quickly pivot to
different designs of components as things ended up behaving in ways
which I didn't expect as this was my first time doing more involved
socket programming.

## Scaling Discussion

In its current form, my project would not scale well to millions of jobs
since I do not chunk my responses to clients when they create queries.
The correct way to implement this would be to send up to a certain
amount of rows per connection to decrease the memory footprint on the
server and client side.

That said, I do believe my database schema itself would scale well to
millions of users, actions, and jobs since I made an effort to ensure
minimal use of foreign keys and no cascades. This was possible because I
have incrementing ids and do not allow deletion of rows, ensuring that
any references between tables stay valid. I also minimize what is
returned from queries to avoid additional strain on the database.

## Conclusion

When I set out to complete this project, I intended to do as much as
possible with as few external libraries as possible to maximize treating
this project as a learning experience. However, I do now regret not
using so many external libraries as it drastically increased the amount
of boilerplate code causing a fair bit of irritation throughout the
process of writing this project. I'm sure if I had more time I could
have made my own decorators to allow me to decrease boilerplate, but I'm
sure if I used more external libraries I could have substantially
decreased this pain point.

That said, I am overall happy with the outcome of this project as I've
become far more comfortable with SQL, database design, and now have an
idea of how to program with sockets to allow for easy IPC.

[messagepack]: https://msgpack.org/index.html
