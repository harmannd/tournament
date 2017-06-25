-- Table definitions for the tournament project.
DROP DATABASE tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE Players (
    id serial PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE Games (
    id serial PRIMARY KEY,
    winner int REFERENCES Players(id),
    loser int REFERENCES Players(id)
);

CREATE VIEW v_wins AS
    SELECT Players.id AS pl_id, count(Games.winner) AS wins
    FROM Players LEFT JOIN Games
    ON Players.id = Games.winner
    GROUP BY Players.id;

CREATE VIEW v_losses AS
    SELECT Players.id AS pl_id, count(Games.loser) AS losses
    FROM Players LEFT JOIN Games
    ON Players.id = Games.loser
    GROUP BY Players.id;

CREATE VIEW v_matches AS
    SELECT v_wins.pl_id AS pl_id, SUM(v_losses.losses + v_wins.wins) AS matches
    FROM v_wins JOIN v_losses
    ON v_wins.pl_id = v_losses.pl_id
    GROUP BY v_wins.pl_id;

CREATE VIEW v_standings AS
    SELECT Players.id, Players.name, v_wins.wins, v_matches.matches
    FROM Players
    LEFT JOIN v_wins ON Players.id = v_wins.pl_id
    LEFT JOIN v_matches ON Players.id = v_matches.pl_id
    GROUP BY Players.id, v_wins.wins, v_matches.matches
    ORDER BY wins DESC;
