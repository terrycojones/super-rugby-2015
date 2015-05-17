#!/usr/bin/env python3

import csv
from collections import Counter

GROUPS = {'AUS', 'NZ', 'RSA'}

assert 3 == len(GROUPS)

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
        self.played = 0
        self.playedWithin = 0
        self.outcomes = {group: Counter()
                         for group in GROUPS if group != name}

    def addResult(self, result):
        self.played += 1
        outcome, for_, against, opponent = result.groupPov(self.name)
        self.outcomes[opponent][outcome] += 1

    def addWithin(self):
        self.playedWithin += 1


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
        return 'Round %d: %s %d %s %d' % (
            self.round,
            self.team1, self.points1,
            self.team2, self.points2)


class Results:
    def __init__(self):
        self.teams = {name: Team(name) for name in TEAMS}
        self.groups = {name: Group(name) for name in GROUPS}

    def add(self, result):
        self.teams[result.team1].addResult(result)
        self.teams[result.team2].addResult(result)
        if result.withinGroup():
            self.groups[result.group1].addWithin()
        else:
            self.groups[result.group1].addResult(result)
            self.groups[result.group2].addResult(result)

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
                  'group)' % (group.played + group.playedWithin,
                              group.played, group.playedWithin))

            # Win/lose/draw record outside group.
            outOfGroupWins = 0
            for otherGroupName in sorted(GROUPS):
                if groupName != otherGroupName:
                    print('  vs %-3s  W  L  D' % otherGroupName)
                    outcomes = group.outcomes[otherGroupName]
                    outOfGroupWins += outcomes['won']
                    print('         %2d %2d %2d' % (
                        outcomes['won'],
                        outcomes['lost'],
                        outcomes['drew']))

            # Overall wins/losses/draws for teams in this group.
            outcomes = Counter()
            for team in self.teams.values():
                if team.group == groupName:
                    outcomes += team.outcomes
            played = sum(outcomes.values())
            print('  Wins overall: %d/%d (%.2f%%)' % (
                outcomes['won'], played,
                100.0 * float(outcomes['won']) / played))

            print('  Wins out-of-group: %d/%d (%.2f%%)' % (
                outOfGroupWins, group.played,
                100.0 * float(outOfGroupWins) / group.played))


def readResults():
    with open('results.txt', newline='') as csvfile:
        first = True
        for row in csv.reader(csvfile, delimiter=' '):
            assert 5 == len(row)
            if first:
                # Make sure we have a header, and skip it.
                assert 'Round' == row[0]
                first = False
            else:
                yield Result(*row)


if __name__ == '__main__':
    results = Results()
    for result in readResults():
        results.add(result)
    results.printTable()
    results.printGroups()
