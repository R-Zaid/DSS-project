import argparse
import logging
from pathlib import Path
import re
import sys
import pandas as pd
from sqlalchemy import create_engine

#!/usr/bin/env python3
"""
load_the_db.py

Usage:
    python load_the_db.py --db sqlite:///my.db file1.csv file2.csv ...
    python load_the_db.py --db postgresql://user:pass@host/db --mode append data/*.csv

Requirements:
    pandas, sqlalchemy
"""



logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def sane_table_name(path: Path) -> str:
        name = path.stem
        # keep letters, numbers and underscores
        return re.sub(r'[^0-9a-zA-Z_]', '_', name)


def read_csv_auto(path: Path, **kwargs) -> pd.DataFrame:
        # try usual read_csv first, then try python engine with sep=None to sniff
        try:
                return pd.read_csv(path, **kwargs)
        except Exception:
                return pd.read_csv(path, sep=None, engine="python", **kwargs)


def load_csv_to_db(csv_path: Path, engine, table_name: str = None, if_exists: str = "replace", index: bool = False, chunksize: int = None):
        logging.info("Loading %s -> table=%s (if_exists=%s)", csv_path, table_name, if_exists)
        df = read_csv_auto(csv_path)
        if table_name is None:
                table_name = sane_table_name(csv_path)
        # to_sql uses SQLAlchemy engine
        df.to_sql(name=table_name, con=engine, if_exists=if_exists, index=index, chunksize=chunksize)
        logging.info("Loaded %d rows into %s", len(df), table_name)


def find_csvs(path: Path):
        if path.is_dir():
                return sorted([p for p in path.glob("*.csv") if p.is_file()])
        if path.is_file():
                return [path]
        return []


def main(argv=None):
        parser = argparse.ArgumentParser(description="Load CSV(s) into a database (SQLite, Postgres, etc.).")
        parser.add_argument("paths", nargs="+", help="CSV file(s) or directories containing CSVs")
        parser.add_argument("--db", 
                          default="postgresql://student:infomdss@db_dashboard:5432/dashboard",
                          help="SQLAlchemy DB URL (default: postgresql://student:infomdss@db_dashboard:5432/dashboard)")
        parser.add_argument("--mode", choices=("replace", "append", "fail"), default="replace", help="behavior if table exists")
        parser.add_argument("--no-index", dest="index", action="store_false", help="don't write DataFrame index as column")
        parser.add_argument("--chunksize", type=int, default=None, help="row chunk size for to_sql (useful for large files)")
        parser.add_argument("--name", help="override table name (for single CSV)")
        args = parser.parse_args(argv)

        try:
                engine = create_engine(args.db)
        except Exception as e:
                logging.error("Failed to create engine for %s: %s", args.db, e)
                sys.exit(2)

        all_paths = []
        for p in args.paths:
                ppath = Path(p)
                found = find_csvs(ppath)
                if not found:
                        logging.warning("No CSVs found at %s", p)
                all_paths.extend(found)

        if not all_paths:
                logging.error("No CSV files to load.")
                sys.exit(1)

        # If user passed a single CSV and provided --name, use it
        if args.name and len(all_paths) == 1:
                load_csv_to_db(all_paths[0], engine, table_name=args.name, if_exists=args.mode, index=args.index, chunksize=args.chunksize)
                return

        for csv in all_paths:
                tbl = sane_table_name(csv)
                load_csv_to_db(csv, engine, table_name=tbl, if_exists=args.mode, index=args.index, chunksize=args.chunksize)


if __name__ == "__main__":
        main()