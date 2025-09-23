# util/query.py
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
import sqlite3
from typing import Dict, Iterable, Tuple, Any, List

# Marker format in your .sql file:
# -- QUERY: some_name
_MARKER = re.compile(r"^\s*--\s*QUERY\s*:\s*([A-Za-z0-9_\-\.]+)\s*$")

def parse_named_queries(sql_text: str) -> Dict[str, str]:
    """
    Split a .sql file into named blocks using lines like:
        -- QUERY: movies_avg_rating
        SELECT ...
        ;
    The block runs until the next marker or EOF.
    """
    lines = sql_text.splitlines()
    current: str | None = None
    blocks: Dict[str, List[str]] = {}

    for line in lines:
        m = _MARKER.match(line)
        if m:
            current = m.group(1)
            if current in blocks:
                raise ValueError(f"Duplicate QUERY name: {current}")
            blocks[current] = []
        else:
            if current is not None:
                blocks[current].append(line)

    named: Dict[str, str] = {}
    for name, chunk in blocks.items():
        sql = "\n".join(chunk).strip()
        # tolerate trailing semicolon
        if sql.endswith(";"):
            sql = sql[:-1].rstrip()
        named[name] = sql
    return named


@dataclass
class Query:
    con: sqlite3.Connection
    sql_query_file_path: Path
    sql_query_name: str
    description: str | None = None

    def _load_sql(self) -> str:
        text = Path(self.sql_query_file_path).read_text(encoding="utf-8")
        named = parse_named_queries(text)
        if self.sql_query_name not in named:
            available = ", ".join(sorted(named.keys())) or "(none)"
            raise KeyError(
                f"Query '{self.sql_query_name}' not found in {self.sql_query_file_path}. "
                f"Available: {available}"
            )
        return named[self.sql_query_name]

    def run(self) -> Tuple[Iterable[Tuple[Any, ...]], Iterable[str]]:
        sql = self._load_sql()
        cur = self.con.cursor()
        cur.execute(sql)  # static SQL (no params)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description] if cur.description else []
        return rows, cols

    def run_and_print(self, max_rows: int = 5) -> None:
        try:
            rows, cols = self.run()
        except sqlite3.Error as e:
            print(f"[SQL error] {e}")
            return

        if self.description:
            print(self.description)

        if not cols:
            print("(No result set)")
            return

        total = len(rows)
        print(f"Total rows: {total}")

        # compute column widths
        widths = [len(str(c)) for c in cols]
        for row in rows[:max_rows]:  # Only consider rows to be printed for width calculation
            for i, v in enumerate(row):
                s = "" if v is None else str(v)
                widths[i] = max(widths[i], len(s))

        # header
        header = " | ".join(str(c).ljust(w) for c, w in zip(cols, widths))
        sep = "-+-".join("-" * w for w in widths)
        print(header)
        print(sep)

        # rows
        to_print = rows[:max_rows]
        for r in to_print:
            line = " | ".join(
                ("" if v is None else str(v)).ljust(w) if isinstance(v, str)
                else ("" if v is None else str(v)).rjust(w)
                for v, w in zip(r, widths)
            )
            print(line)

        if total > max_rows:
            print(f"… ({max_rows} of {total} rows shown)")
        else:
            print(f"({total} rows)")
