## Some statistics on the 2015 Super Rugby thus far

If you take a look at
[the 2015 Super Rugby table](http://www.smh.com.au/rugby-union/super-rugby/ladder),
it's immediately clear that NZ teams are doing extremely well.  But the
overall competition table doesn't show us how teams from one country are
doing against the teams from the other two countries.

I was interested to see what things looked like when we only consider
matches that are played between teams from different countries. Factoring
out how teams from within a country play each other might give us a clearer
picture of the relative strengths of the countries.

I wrote a program to examine this.

## Results

The results (see the Details section below) show that NZ group teams
won 47/80 (58.75%) of their games overall. But if you look at their record
just in out-of-group games, the percentage goes up: they've won 27/40
(67.5%). In contrast, Australian group teams won 34/80 (42.5%) of
their games overall, but in out-of-group have won only 14/40 (35%).

I.e., the Australian record is worse than it appears if you just consider
their overall competition win/loss percentage.  Meanwhile, the NZ teams are
doing even better at beating everyone else than it might first appear from
their overall record. Meanwhile, the South African teams are doing about as
well beating teams from other countries others as they are overall.

This gives us some idea of the *overall strength* of rugby in the
countries: NZ well ahead of RSA, and RSA well ahead of AUS.

However, it doesn't give any indication about whether, for example, New
Zealand is likely to beat Australia in a test. That's because the players
in the Super Rugby teams that are winning very few games are much less
likely to be picked for their national sides.

The program's graphical and textual output (as of June 13 2015, following
Round 18) are shown below.

The graph shows how the overall win fraction versus the out-of-group win
fraction has changed over time for each of the countries. Only rounds 5
onwards are shown as it took that long to have enough data for the general
pattern to stabilize.

<img src="graph.png"/>

### Details

Below is the detailed output of the program with results broken down by
group.

```
Results through round 18

                  Overall    vs AUS     vs NZ      vs RSA
Team         P    W  L  D    W  L  D    W  L  D    W  L  D
 HUR (NZ) : 16   14  2  0    3  1  0    7  1  0    4  0  0
 HIG (NZ) : 16   11  5  0    3  1  0    5  3  0    3  1  0
 WAR (AUS): 16   11  5  0    6  2  0    3  1  0    2  2  0
 STO (RSA): 16   10  5  1    4  0  0    1  3  0    5  2  1
 CHF (NZ) : 16   10  6  0    3  1  0    4  4  0    3  1  0
 LIO (RSA): 16    9  6  1    3  1  0    2  2  0    4  3  1
 BRU (AUS): 16    9  7  0    5  3  0    1  3  0    3  1  0
 CRU (NZ) : 16    9  7  0    2  2  0    4  4  0    3  1  0
 BUL (RSA): 16    7  9  0    2  2  0    1  3  0    4  4  0
 REB (AUS): 16    7  9  0    3  5  0    3  1  0    1  3  0
 SHA (RSA): 16    7  9  0    3  1  0    1  3  0    3  5  0
 CHT (RSA): 16    5 11  0    1  3  0    1  3  0    3  5  0
 RED (AUS): 16    4 12  0    3  5  0    0  4  0    1  3  0
 BLU (NZ) : 16    3 13  0    2  2  0    0  8  0    1  3  0
 FOR (AUS): 16    3 13  0    3  5  0    0  4  0    0  4  0

AUS teams:
  80 games played (40 vs other groups, 40 within group)
  vs NZ   W  L  D
          7 13  0
  vs RSA  W  L  D
          7 13  0
  Wins overall: 34/80 (42.50%)
  Wins out-of-group: 14/40 (35.00%)

NZ  teams:
  80 games played (40 vs other groups, 40 within group)
  vs AUS  W  L  D
         13  7  0
  vs RSA  W  L  D
         14  6  0
  Wins overall: 47/80 (58.75%)
  Wins out-of-group: 27/40 (67.50%)

RSA teams:
  80 games played (40 vs other groups, 40 within group)
  vs AUS  W  L  D
         13  7  0
  vs NZ   W  L  D
          6 14  0
  Wins overall: 38/80 (47.50%)
  Wins out-of-group: 19/40 (47.50%)
```

Some notes:

* The team results table is not ordered by competition points, but by
number of wins.

* RSA teams have won 13 out of 20 matches against AUS teams, but only 6
out of 20 against NZ teams.

* AUS has an equal record against NZ and RSA, 7 games won out of 20 in both
cases.

## Technical stuff

This repo contains a results file (`results.txt`) and a Python program to
print stats and make a plot (`process.py`).

Neither the program nor its input have been fully checked for accuracy yet!
I'm fairly certain they're correct.

Usage is as follows:

```sh
$ ./process.py --help
usage: process.py [-h] [--rounds ROUND] [--printResults] [--plot]
                  [--firstPlotRound ROUND]

Print statistics about the 2015 Super Rugby competition.

optional arguments:
  -h, --help            show this help message and exit
  --rounds ROUND        Only consider games up to (and including) the given
                        round. Default is to use data from all rounds.
  --printResults        Print individual match results (default: False).
  --plot                Plot a graph showing round-by-round overall and out-
                        of-group win fractions (default: False).
  --firstPlotRound ROUND
                        The first round of results to show when --plot is used
                        (default: 5).
```

The `results.txt` file must have 5 fields per line: `round`, `team1`,
`points1`, `team2`, and `points2`. The `round` numbers *must* be
non-decreasing so that the end-of-round statistics gathering will work
correctly.
