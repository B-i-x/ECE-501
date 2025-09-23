"""
Load MovieLens (ml-latest-small) CSVs into a SQLite database using Python's built-in sqlite3.

Usage (from the directory containing this script):
    python question1.py
"""

import csv
import sqlite3
from pathlib import Path

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))
from query import Query 

def create_tables(con: sqlite3.Connection):
    cur = con.cursor()
    # Drop existing tables for a clean re-load
    cur.executescript(
        """
        DROP TABLE IF EXISTS movies;
        DROP TABLE IF EXISTS ratings;
        DROP TABLE IF EXISTS links;
        DROP TABLE IF EXISTS tags;

        CREATE TABLE movies (
            movieId INTEGER PRIMARY KEY,
            title   TEXT NOT NULL,
            genres  TEXT NOT NULL
        );

        CREATE TABLE ratings (
            userId    INTEGER NOT NULL,
            movieId   INTEGER NOT NULL,
            rating    REAL    NOT NULL,
            timestamp INTEGER NOT NULL
        );

        CREATE TABLE links (
            movieId INTEGER PRIMARY KEY,
            imdbId  TEXT,
            tmdbId  TEXT
        );

        CREATE TABLE tags (
            userId    INTEGER NOT NULL,
            movieId   INTEGER NOT NULL,
            tag       TEXT,
            timestamp INTEGER NOT NULL
        );
        """
    )
    con.commit()


def load_csv(con: sqlite3.Connection, path: Path, table: str, columns: list[str]):
    """
    Generic CSV loader that inserts rows into the specified table.
    - `columns` must match the CSV header order (and table schema order).
    """
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    placeholders = ",".join(["?"] * len(columns))
    collist = ",".join(columns)

    to_insert = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vals = [row.get(c) for c in columns]

            # Light type normalization to match schema
            if table == "movies":
                # movieId int
                vals[0] = int(vals[0]) if vals[0] is not None else None
                # title (TEXT), genres (TEXT) left as-is
            elif table == "ratings":
                # userId, movieId int; rating float; timestamp int
                vals[0] = int(vals[0]) if vals[0] is not None else None
                vals[1] = int(vals[1]) if vals[1] is not None else None
                vals[2] = float(vals[2]) if vals[2] is not None else None
                vals[3] = int(vals[3]) if vals[3] is not None else None
            elif table == "links":
                # movieId int; keep imdbId/tmdbId as TEXT to preserve leading zeros
                vals[0] = int(vals[0]) if vals[0] is not None else None
            elif table == "tags":
                # userId, movieId int; tag TEXT; timestamp int
                vals[0] = int(vals[0]) if vals[0] is not None else None
                vals[1] = int(vals[1]) if vals[1] is not None else None
                vals[3] = int(vals[3]) if vals[3] is not None else None

            to_insert.append(tuple(vals))

    with con:
        con.executemany(
            f"INSERT INTO {table} ({collist}) VALUES ({placeholders})",
            to_insert
        )


def main():
    sql_query_file_path_hw2 = Path("Homework/2/question1/question1.sql")
    
    data_dir = r"data/ml-latest-small"
    db_path = Path("Homework/2/question1/movielens_small.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)


    con = sqlite3.connect(db_path)
    try:
        create_tables(con)

        # Load files
        data_root = Path(data_dir)
        load_csv(con, data_root / "movies.csv",  "movies",  ["movieId", "title", "genres"])
        load_csv(con, data_root / "ratings.csv", "ratings", ["userId", "movieId", "rating", "timestamp"])
        load_csv(con, data_root / "links.csv",   "links",   ["movieId", "imdbId", "tmdbId"])
        load_csv(con, data_root / "tags.csv",    "tags",    ["userId", "movieId", "tag", "timestamp"])

        print(f"Loaded all data into SQLite: {db_path.resolve()}")
    finally:
        con.close()

    # Example usage of the provided Query helper (adjust path to your SQL file)
    Query(
        con=sqlite3.connect(db_path),
        sql_query_file_path=sql_query_file_path_hw2,
        sql_query_name="movies_avg_rating",
        description="Movie with average rating of at least 4.0:"
    ).run_and_print()
    # print("Query1 Results:")
    # for row in Query1_results:
    #     print(row)

if __name__ == "__main__":
    main()
