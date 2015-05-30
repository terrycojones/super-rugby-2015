## Some statistics on the 2015 Super Rugby thus far

If you take a look at
[the 2015 Super Rugby table](http://www.smh.com.au/rugby-union/super-rugby/ladder),
it's immediately clear that NZ teams are doing extremely well.  But the
overall competition table doesn't tell us how teams from one country are
doing against the teams from the other two countries.

I was interested to see what things looked like when we only consider
matches that are played between teams from different countries. Factoring
out how teams from within a country play each other might give us a clearer
picture of the relative strengths of the countries.

I wrote a program to examine this.

## Results

The results (see below) show that NZ group teams have won 41/70 (58.6%) of
their games overall. But if you look at their record just in out-of-group
games, the percentage goes up: they've won 25/38 (65.8%). In contrast,
Australian group teams have won 29/70 (41.4%) of their games overall, but
in out-of-group have won only 12/36 (33.3%).

I.e., the Australian record is worse than it appears if you just consider
their overall competition win/loss percentage.  Meanwhile, the NZ teams are
doing even better at beating everyone else than it might first appear from
their overall record. Meanwhile, the South African teams are doing about as
well beating teams from other countries others as they are overall.

This gives us some idea of the *overall strength of rugby* in the
countries: NZ well ahead of RSA, and RSA well ahead of AUS.

However, it doesn't give any indication about whether (e.g.) New Zealand is
likely to beat Australia in a test because the players in the Super Rugby
teams that are winning few games are much less likely to be picked for
their national sides.

The program's graphical and textual output (as of 2015-05-24, following
Round 16) are shown below.

The graph shows how the overall win fraction versus the out-of-group win
fraction has changed over time for each of the countries. Only rounds 5
onwards are shown as it took that long to have enough data for the general
pattern to stabilize.

<img src="graph.png"/>

### Details

Below is the detailed output of the program with results broken down by
group. Some notes:

* The team results table is not ordered by competition points, but by
number of wins.

* It's interesting to see that AUS teams are doing better against NZ teams
(7 wins out of 18) than they are against RSA teams (5 wins out of 18).

* RSA teams have won 13 out of 18 matches against AUS teams, but only 6
out of 20 against NZ teams.

```
Results through round 16

                  Overall    vs AUS     vs NZ      vs RSA
Team         P    W  L  D    W  L  D    W  L  D    W  L  D
 HUR (NZ) : 14   12  2  0    3  1  0    5  1  0    4  0  0
 HIG (NZ) : 14   10  4  0    3  1  0    4  2  0    3  1  0
 STO (RSA): 14   10  4  0    4  0  0    1  3  0    5  1  0
 CHF (NZ) : 14    9  5  0    2  1  0    4  3  0    3  1  0
 WAR (AUS): 14    9  5  0    5  2  0    3  1  0    1  2  0
 LIO (RSA): 15    9  6  0    3  1  0    2  2  0    4  3  0
 BRU (AUS): 14    8  6  0    4  3  0    1  2  0    3  1  0
 BUL (RSA): 14    7  7  0    2  1  0    1  3  0    4  3  0
 CRU (NZ) : 14    7  7  0    1  2  0    3  4  0    3  1  0
 REB (AUS): 14    6  8  0    3  4  0    3  1  0    0  3  0
 SHA (RSA): 15    6  9  0    3  1  0    1  3  0    2  5  0
 CHT (RSA): 14    4 10  0    1  2  0    1  3  0    2  5  0
 RED (AUS): 14    4 10  0    3  4  0    0  3  0    1  3  0
 BLU (NZ) : 14    3 11  0    2  2  0    0  6  0    1  3  0
 FOR (AUS): 14    2 12  0    2  4  0    0  4  0    0  4  0

AUS teams:
  70 games played (36 vs other groups, 34 within group)
  vs NZ   W  L  D
          7 11  0
  vs RSA  W  L  D
          5 13  0
  Wins overall: 29/70 (41.43%)
  Wins out-of-group: 12/36 (33.33%)

NZ  teams:
  70 games played (38 vs other groups, 32 within group)
  vs AUS  W  L  D
         11  7  0
  vs RSA  W  L  D
         14  6  0
  Wins overall: 41/70 (58.57%)
  Wins out-of-group: 25/38 (65.79%)

RSA teams:
  72 games played (38 vs other groups, 34 within group)
  vs AUS  W  L  D
         13  5  0
  vs NZ   W  L  D
          6 14  0
  Wins overall: 36/72 (50.00%)
  Wins out-of-group: 19/38 (50.00%)
```

## Technical stuff

This repo contains a results file (`results.txt`) and a Python program to
print stats and make a plot (`process.py`).

Neither the program nor its input have been fully checked for accuracy yet!
I'm fairly certain they're correct.

Usage is as follows:

```sh
$ ./process.py --help
usage: process.py [-h] [--rounds ROUNDS] [--printResults] [--plot]

Print statistics about the 2015 Super Rugby competition

optional arguments:
  -h, --help       show this help message and exit
  --rounds ROUNDS  Only consider games up to (and including) the given round.
  --printResults   If True, print individual match results.
  --plot           If True, plot round-by-round overall and out-of-group win
                   fractions
```

The `results.txt` file must have 5 fields per line: `round`, `team1`,
`points1`, `team2`, and `points2`. The round numbers *must* be
non-decreasing so that the end-of-round statistics gathering will work
correctly.
