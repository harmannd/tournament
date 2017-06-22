-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE "player"
(
    id serial primary key,
    name text NOT NULL,
    wins int DEFAULT 0,
    matches int DEFAULT 0
);

CREATE TABLE "game"
(
    id serial primary key,
    player1 int references player(id),
    player2 int references player(id),
    winner int references player(id)
);
