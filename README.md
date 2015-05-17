## Some statistics on the 2015 Super Rugby thus far

If you take a look at
[the 2015 Super Rugby table](http://www.smh.com.au/rugby-union/super-rugby/ladder),
it's immediately clear that NZ teams are doing extremely well.

I was interested to see how teams in each of the three groups are doing
against teams from other groups. For example, the Australian teams are
doing OK, but might it be that they are mainly good at beating each other
or are they winning well across the board?

Two interesting things come from the results (below):

1. Although all groups have played roughly the same number of matches (AUS
   61, NZ 61, RSA 62), the number played against teams from other groups is
   not as evenly balanced (AUS 29, NZ 35, RSA 32).

1. NZ teams have won 36/61 (59%) of their games overall. But if you look at
   their record in out-of-group games, the percentage goes up: they've won
   29/35 (65.7%). In contrast, Australian teams have won 26/61 (42.6%) of
   their games overall, but out-of-group have won just 10/29 (34.5%).

The conclusion of all this?

Relative to other countries, the Australian teams are doing worse than it
might first appear (i.e., they're doing a good job of beating each other)
and the NZ teams are doing even better at beating everyone else than it
might first appear.

## Results

This repo contains a results file and a Python program to print some
stats.  *Note: Neither has been fully checked for accuracy yet!*

The output (as of 2015-05-17, following Round 14) is shown below:

```
TEAMS
                  Overall    vs AUS     vs NZ      vs RSA
Team         P    W  L  D    W  L  D    W  L  D    W  L  D
 HUR (NZ) : 12   11  1  0    3  1  0    4  0  0    4  0  0
 CHF (NZ) : 12    8  4  0    2  1  0    4  2  0    2  1  0
 HIG (NZ) : 12    8  4  0    2  1  0    3  2  0    3  1  0
 STO (RSA): 12    8  4  0    3  0  0    1  3  0    4  1  0
 WAR (AUS): 12    8  4  0    5  2  0    2  1  0    1  1  0
 BUL (RSA): 12    7  5  0    2  0  0    1  2  0    4  3  0
 BRU (AUS): 13    7  6  0    4  3  0    1  2  0    2  1  0
 LIO (RSA): 13    7  6  0    2  1  0    2  2  0    3  3  0
 CRU (NZ) : 12    6  6  0    1  1  0    2  4  0    3  1  0
 REB (AUS): 12    6  6  0    3  4  0    3  1  0    0  1  0
 CHT (RSA): 12    4  8  0    1  2  0    1  3  0    2  3  0
 SHA (RSA): 13    4  9  0    1  1  0    1  3  0    2  5  0
 RED (AUS): 12    3  9  0    2  4  0    0  3  0    1  2  0
 BLU (NZ) : 13    3 10  0    2  2  0    0  5  0    1  3  0
 FOR (AUS): 12    2 10  0    2  3  0    0  3  0    0  4  0

GROUPS
AUS teams:
  45 games played (29 vs other groups, 16 within group)
  vs NZ   W  L  D
          6 10  0
  vs RSA  W  L  D
          4  9  0
  Wins overall: 26/61 (42.62%)
  Wins out-of-group: 10/29 (34.48%)

NZ  teams:
  48 games played (35 vs other groups, 13 within group)
  vs AUS  W  L  D
         10  6  0
  vs RSA  W  L  D
         13  6  0
  Wins overall: 36/61 (59.02%)
  Wins out-of-group: 23/35 (65.71%)

RSA teams:
  47 games played (32 vs other groups, 15 within group)
  vs AUS  W  L  D
          9  4  0
  vs NZ   W  L  D
          6 13  0
  Wins overall: 30/62 (48.39%)
  Wins out-of-group: 15/32 (46.88%)
```
