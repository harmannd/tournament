#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format("tournament"))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print "Unable to connect to database"
        sys.exit(1)


def executeQuery(query, action):
    db, c = connect()
    c.execute(query)
    if action == "select_count":
        return c.fetchone()[0]
    elif action == "select":
        return c.fetchall()
    db.commit()
    db.close()


def deleteMatches():
    """Remove all the match records from the database."""
    executeQuery("DELETE FROM Games", "delete")


def deletePlayers():
    """Remove all the player records from the database."""
    executeQuery("DELETE FROM Players", "delete")


def countPlayers():
    """Returns the number of players currently registered."""
    return executeQuery("SELECT count(*) FROM Players", "select_count")


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, c = connect()
    c.execute("INSERT INTO Players VALUES (DEFAULT, %s)", (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    return executeQuery("SELECT * FROM v_standings", "select")


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, c = connect()
    # c.execute("UPDATE Players SET wins = wins + 1, matches = matches + 1 WHERE id = {}".format(winner))
    # c.execute("UPDATE Players SET matches = matches + 1 WHERE id = {}".format(loser))
    c.execute("INSERT INTO Games VALUES (DEFAULT, %s, %s)", (winner, loser))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    rows = executeQuery("SELECT * FROM v_wins ORDER BY wins DESC", "select")
    x = 0
    pairings = []
    while x < len(rows) - 1:
        pairings.append([rows[x][0], rows[x][1], rows[x+1][0], rows[x+1][1]])
        x += 2
    return pairings


