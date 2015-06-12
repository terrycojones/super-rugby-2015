#!/usr/bin/env python3

import csv
import argparse
from collections import Counter
import matplotlib.pyplot as plt

from pylab import rcParams
rcParams['figure.figsize'] = 12, 8

GROUPS = {'AUS', 'NZ', 'RSA'}

assert 3 == len(GROUPS)

GROUP_COLOR = {
    'AUS': 'gold',
    'NZ': 'black',
    'RSA': 'green',
}

assert sorted(GROUPS) == sorted(GROUP_COLOR.keys())

MAX_GROUP_LEN = max(len(group) for group in GROUPS)

TEAMS = {
    'BLU': 'NZ',
    'BRU': 'AUS',
    'BUL': 'RSA',
    'CHF': 'NZ',
    'CHT': 'RSA',
    'CRU': 'NZ',
    'FOR': 'AUS',
    'HIG': 'NZ',
    'HUR': 'NZ',
    'LIO': 'RSA',
    'REB': 'AUS',
    'RED': 'AUS',
    'SHA': 'RSA',
    'STO': 'RSA',
    'WAR': 'AUS',
}

assert 15 == len(TEAMS)

# Check all groups have 5 teams.
for group in GROUPS:
    assert 5 == len([team for team in TEAMS.values()
                     if team == group])

# Check all teams are in a known group.
for team in TEAMS:
    assert TEAMS[team] in GROUPS


# The first round of results to show when plotting. It takes 5 rounds for
# the overall pattern to settle down.
FIRST_PLOT_ROUND = 5


class Team:
    def __init__(self, name):
        self.name = name
        self.outcomes = Counter()
        self.outcomesByGroup = {group: Counter() for group in GROUPS}

    def addResult(self, result):
        outcome, for_, against, opponent = result.pov(self.name)
        opponentGroup = TEAMS[opponent]
        self.outcomes[outcome] += 1
        self.outcomesByGroup[opponentGroup][outcome] += 1

    def __str__(self):
        return '%s: Played %d Wins %d Losses %d Draws %d' % (
            self.name, self.wins + self.losses + self.draws,
            self.wins, self.losses, self.draws)

    @property
    def group(self):
        return TEAMS[self.name]

    @property
    def won(self):
        return self.outcomes['won']

    @property
    def lost(self):
        return self.outcomes['lost']

    @property
    def drew(self):
        return self.outcomes['drew']

    @property
    def played(self):
        return self.won + self.lost + self.drew


class Group:
    def __init__(self, name):
        self.name = name
        self.playedInGroup = 0
        self.playedOutOfGroup = 0
        self.outcomesInGroup = Counter()
        self.outcomesOutOfGroup = {group: Counter()
                                   for group in GROUPS if group != name}

    def addOutOfGroupResult(self, result):
        self.playedOutOfGroup += 1
        outcome, for_, against, opponent = result.groupPov(self.name)
        self.outcomesOutOfGroup[opponent][outcome] += 1

    def addInGroupResult(self, result):
        self.playedInGroup += 2
        outcome, for_, against, opponent = result.groupPov(self.name)
        # The groups should match, else we've been called in error.
        assert self.name == opponent, '%s != %s' % (self.name, opponent)
        if outcome == 'drew':
            self.outcomesInGroup['drew'] += 2
        else:
            self.outcomesInGroup['won'] += 1
            self.outcomesInGroup['lost'] += 1

    def overallOutOfGroupOutcomes(self):
        """
        Return the overall out-of-group outcomes.
        """
        overall = Counter()
        for outcomes in self.outcomesOutOfGroup.values():
            overall += outcomes
        return overall

    def overallOutcomes(self):
        """
        Return the overall outcomes, of within- and without-group matches.
        """
        overall = Counter()
        for outcomes in self.outcomesOutOfGroup.values():
            overall += outcomes
        return overall + self.outcomesInGroup


class Result:
    def __init__(self, round, team1, points1, team2, points2):
        self.round = int(round)
        assert team1 in TEAMS and team2 in TEAMS
        self.team1 = team1
        self.points1 = int(points1)
        self.team2 = team2
        self.points2 = int(points2)

    @property
    def group1(self):
        return TEAMS[self.team1]

    @property
    def group2(self):
        return TEAMS[self.team2]

    def pov(self, team):
        if team == self.team1:
            for_, against, opponent = self.points1, self.points2, self.team2
        elif team == self.team2:
            for_, against, opponent = self.points2, self.points1, self.team1
        else:
            raise Exception(
                'Irrelevant team %s passed to Result.pov for %s' %
                (team, self))

        result = ('won' if for_ > against else (
                  'lost' if for_ < against else 'drew'))

        return result, for_, against, opponent

    def groupPov(self, group):
        if group == TEAMS[self.team1]:
            for_, against, opponent = (self.points1, self.points2,
                                       TEAMS[self.team2])
        elif group == TEAMS[self.team2]:
            for_, against, opponent = (self.points2, self.points1,
                                       TEAMS[self.team1])
        else:
            raise Exception('Group %s was not involved in result %s' %
                            (group, self))

        result = ('won' if for_ > against else (
                  'lost' if for_ < against else 'drew'))

        return result, for_, against, opponent

    def withinGroup(self):
        return self.group1 == self.group2

    def __str__(self):
        return 'Round %d: %s (%s) %d vs %s (%s) %d' % (
            self.round,
            self.team1, TEAMS[self.team1], self.points1,
            self.team2, TEAMS[self.team2], self.points2)


class Results:

    def __init__(self, filename, maxRounds=None):
        self._filename = filename
        self._maxRounds = maxRounds
        self.rounds = 0
        self.teams = {name: Team(name) for name in TEAMS}
        self.groups = {name: Group(name) for name in GROUPS}
        self.roundStats = {}
        for name in GROUPS:
            self.roundStats[name + '-overall-win-fraction'] = []
            self.roundStats[name + '-out-of-group-win-fraction'] = []

    def add(self, result):
        self.teams[result.team1].addResult(result)
        self.teams[result.team2].addResult(result)
        if result.withinGroup():
            self.groups[result.group1].addInGroupResult(result)
        else:
            self.groups[result.group1].addOutOfGroupResult(result)
            self.groups[result.group2].addOutOfGroupResult(result)

    def sortTeams(self):
        return sorted(
            sorted(
                sorted(
                    sorted(
                        sorted(TEAMS),
                        key=lambda t: self.teams[t].played
                    ),
                    key=lambda t: self.teams[t].drew
                ),
                key=lambda t: self.teams[t].lost,
            ),
            key=lambda t: self.teams[t].won, reverse=True)

    def printTable(self):
        print('Results through round %d' % self.rounds, end='\n\n')
        print('                  Overall', end=' ')
        for group in sorted(GROUPS):
            print('   %-7s' % ('vs ' + group), end=' ')
        print()
        print('Team         P    W  L  D', end=' ')
        for group in sorted(GROUPS):
            print('   W  L  D', end=' ')
        print()
        for teamName in self.sortTeams():
            team = self.teams[teamName]
            print('%4s %-*s: %2d   %2d %2d %2d' % (
                teamName,
                MAX_GROUP_LEN + 2, '(' + team.group + ')',
                team.played,
                team.won, team.lost, team.drew), end=' ')
            for group in sorted(GROUPS):
                outcomes = team.outcomesByGroup[group]
                print('  %2d %2d %2d' % (
                    outcomes['won'],
                    outcomes['lost'],
                    outcomes['drew']), end=' ')
            print()

    def printGroups(self):
        for groupName in sorted(GROUPS):
            group = self.groups[groupName]
            print('\n%-*s teams:' % (MAX_GROUP_LEN, groupName))
            print('  %2d games played (%2d vs other groups, %2d within '
                  'group)' % (group.playedOutOfGroup + group.playedInGroup,
                              group.playedOutOfGroup, group.playedInGroup))

            # Win/lose/draw record outside group.
            for otherGroupName in sorted(GROUPS):
                if groupName != otherGroupName:
                    print('  vs %-3s  W  L  D' % otherGroupName)
                    outcomes = group.outcomesOutOfGroup[otherGroupName]
                    print('         %2d %2d %2d' % (
                        outcomes['won'],
                        outcomes['lost'],
                        outcomes['drew']))

            # Overall wins/losses/draws for teams in this group.
            outcomes = group.overallOutcomes()
            played = sum(outcomes.values())
            print('  Wins overall: %d/%d (%.2f%%)' % (
                outcomes['won'], played,
                100.0 * float(outcomes['won']) / played))

            # Out of group wins/losses/draws for teams in this group.
            outcomes = group.overallOutOfGroupOutcomes()
            played = sum(outcomes.values())
            print('  Wins out-of-group: %d/%d (%.2f%%)' % (
                outcomes['won'], played,
                100.0 * float(outcomes['won']) / played))

    def read(self, printResults):
        maxRounds = self._maxRounds
        first = True
        currentRound = 1
        with open(self._filename, newline='') as csvfile:
            for row in csv.reader(csvfile, delimiter=' '):
                assert 5 == len(row)
                if first:
                    # Make sure we have a header, and skip it.
                    assert 'Round' == row[0]
                    first = False
                else:
                    result = Result(*row)
                    if maxRounds is not None and result.round > maxRounds:
                        break
                    else:
                        if printResults:
                            print(result)
                        self.add(result)
                        if result.round != currentRound:
                            self.endRound()
                            currentRound = result.round
        self.endRound()

    def endRound(self):
        self.rounds += 1
        for groupName in sorted(GROUPS):
            group = self.groups[groupName]

            # Overall wins/losses/draws for teams in this group.
            outcomes = group.overallOutcomes()
            played = sum(outcomes.values())
            self.roundStats[groupName + '-overall-win-fraction'].append(
                float(outcomes['won']) / played)

            # Out of group wins/losses/draws for teams in this group.
            outcomes = group.overallOutOfGroupOutcomes()
            played = sum(outcomes.values())
            self.roundStats[groupName + '-out-of-group-win-fraction'].append(
                float(outcomes['won']) / played)

    def plot(self, firstPlotRound=FIRST_PLOT_ROUND):
        if firstPlotRound > self.rounds:
            print('Cannot plot %d rounds, we only have %d rounds of data.' %
                  (firstPlotRound, self.rounds))
            return

        x = list(range(firstPlotRound, self.rounds + 1))
        handles = []
        for groupName in sorted(GROUPS):
            stats = self.roundStats[groupName + '-overall-win-fraction']
            handles.append(
                plt.plot(x, stats[firstPlotRound - 1:],
                         label='%s overall' % groupName, linewidth=2,
                         color=GROUP_COLOR[groupName])[0])
            stats = self.roundStats[groupName + '-out-of-group-win-fraction']
            handles.append(
                plt.plot(x, stats[firstPlotRound - 1:],
                         label='%s out-of-group' % groupName, linewidth=2,
                         color=GROUP_COLOR[groupName], linestyle='dashed')[0])
        plt.title('Overall vs out-of-group win fraction', fontsize=20)
        plt.legend(handles=handles)
        plt.ylim(0.0, 1.0)
        plt.xlim(firstPlotRound, self.rounds)
        plt.xticks(x)
        plt.yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        plt.xlabel('Round', fontsize=16)
        plt.ylabel('Win fraction', fontsize=16)
        plt.grid()
        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Print statistics about the 2015 Super Rugby competition.')

    parser.add_argument(
        '--rounds', type=int, metavar='ROUND',
        help='Only consider games up to (and including) the given round. '
        'Default is to use data from all rounds.')

    parser.add_argument(
        '--printResults', action='store_true', default=False,
        help='Print individual match results (default: %(default)s).')

    parser.add_argument(
        '--plot', action='store_true', default=False,
        help=('Plot a graph showing round-by-round overall and '
              'out-of-group win fractions (default: %(default)s).'))

    parser.add_argument(
        '--firstPlotRound', type=int, default=FIRST_PLOT_ROUND,
        metavar='ROUND',
        help=('The first round of results to show when --plot is used '
              '(default: %(default)s).'))

    args = parser.parse_args()
    results = Results('results.txt', args.rounds)
    results.read(args.printResults)
    results.printTable()
    results.printGroups()
    if args.plot:
        results.plot(args.firstPlotRound)
