# part-3

An import thing for a boat rental service is knowing whether or not a
boat is "sea ready," or safe to rent. My addition to the original schema
is a `condition` table that keeps track of boat conditions following
inspections. To make this easier to work with, I've created a
`sea_ready` view which allows for employees to quickly check which boats
are safe to rent to clients by only reporting boats who's condition is
above a condition threshold. This can be further expanded with another
view table that reports the opposite, that being boats that need to be
serviced before they're rented again.
