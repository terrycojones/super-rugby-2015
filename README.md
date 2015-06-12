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

The results (see the Details section below) show that NZ group teams have
won 44/75 (58.7%) of their games overall. But if you look at their record
just in out-of-group games, the percentage goes up: they've won 26/39
(66.6%). In contrast, Australian group teams have won 32/75 (42.7%) of
their games overall, but in out-of-group have won only 14/39 (35.9%).

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

The program's graphical and textual output (as of June 7 2015, following
Round 17) are shown below.

The graph shows how the overall win fraction versus the out-of-group win
fraction has changed over time for each of the countries. Only rounds 5
onwards are shown as it took that long to have enough data for the general
pattern to stabilize.

<img src="graph.png"/>

### Details

Below is the detailed output of the program with results broken down by
group.

```
Results through round 17

                  Overall    vs AUS     vs NZ      vs RSA
Team         P    W  L  D    W  L  D    W  L  D    W  L  D
 HUR (NZ) : 15   13  2  0    3  1  0    6  1  0    4  0  0
 STO (RSA): 15   10  4  1    4  0  0    1  3  0    5  1  1
 CHF (NZ) : 15   10  5  0    3  1  0    4  3  0    3  1  0
 HIG (NZ) : 15   10  5  0    3  1  0    4  3  0    3  1  0
 WAR (AUS): 15   10  5  0    5  2  0    3  1  0    2  2  0
 BRU (AUS): 15    9  6  0    5  3  0    1  2  0    3  1  0
 LIO (RSA): 16    9  6  1    3  1  0    2  2  0    4  3  1
 CRU (NZ) : 15    8  7  0    1  2  0    4  4  0    3  1  0
 BUL (RSA): 15    7  8  0    2  2  0    1  3  0    4  3  0
 REB (AUS): 15    7  8  0    3  4  0    3  1  0    1  3  0
 SHA (RSA): 15    6  9  0    3  1  0    1  3  0    2  5  0
 CHT (RSA): 15    4 11  0    1  3  0    1  3  0    2  5  0
 RED (AUS): 15    4 11  0    3  4  0    0  4  0    1  3  0
 BLU (NZ) : 15    3 12  0    2  2  0    0  7  0    1  3  0
 FOR (AUS): 15    2 13  0    2  5  0    0  4  0    0  4  0

AUS teams:
  75 games played (39 vs other groups, 36 within group)
  vs NZ   W  L  D
          7 12  0
  vs RSA  W  L  D
          7 13  0
  Wins overall: 32/75 (42.67%)
  Wins out-of-group: 14/39 (35.90%)

NZ  teams:
  75 games played (39 vs other groups, 36 within group)
  vs AUS  W  L  D
         12  7  0
  vs RSA  W  L  D
         14  6  0
  Wins overall: 44/75 (58.67%)
  Wins out-of-group: 26/39 (66.67%)

RSA teams:
  76 games played (40 vs other groups, 36 within group)
  vs AUS  W  L  D
         13  7  0
  vs NZ   W  L  D
          6 14  0
  Wins overall: 36/76 (47.37%)
  Wins out-of-group: 19/40 (47.50%)
```

Some notes:

* The team results table is not ordered by competition points, but by
number of wins.

* RSA teams have won 13 out of 18 matches against AUS teams, but only 6
out of 20 against NZ teams.

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
