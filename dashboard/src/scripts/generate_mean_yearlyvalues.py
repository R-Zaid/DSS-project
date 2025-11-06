"""Generate mean_yearlyvalues.csv from mean_monthlyvalues.csv

This script reads `data/ProcessedData/mean_monthlyvalues.csv`, computes the
average of monthly values per year and province, and writes
`data/ProcessedData/mean_yearlyvalues.csv`.

Usage:
    python generate_mean_yearlyvalues.py [--input PATH] [--output PATH]

If run inside Docker where `./data` is mounted at `/data`, it will prefer
`/data/processedData/mean_monthlyvalues.csv`.
"""
from __future__ import annotations
import argparse
import os
import pandas as pd


def resolve_paths(input_path: str | None = None, output_path: str | None = None) -> tuple[str, str]:
    # prefer mounted /data when available (Docker)
    candidates = []
    if os.path.exists("/data"):
        # common names
        candidates.append(os.path.join("/data", "processedData", "mean_monthlyvalues.csv"))
        candidates.append(os.path.join("/data", "ProcessedData", "mean_monthlyvalues.csv"))
    # repo-relative
    candidates.append(os.path.join(os.getcwd(), "data", "ProcessedData", "mean_monthlyvalues.csv"))
    candidates.append(os.path.join(os.getcwd(), "data", "processedData", "mean_monthlyvalues.csv"))

    if input_path:
        src = input_path
    else:
        src = None
        for c in candidates:
            if os.path.exists(c):
                src = c
                break
        if src is None:
            raise FileNotFoundError(
                "mean_monthlyvalues.csv not found. Checked: " + ", ".join(candidates)
            )

    if output_path:
        dst = output_path
    else:
        # place output next to input in same folder
        src_dir = os.path.dirname(src)
        dst = os.path.join(src_dir, "mean_yearlyvalues.csv")

    return src, dst


def generate_yearly_mean(input_csv: str, output_csv: str) -> None:
    df = pd.read_csv(input_csv)

    if "Year_Month" not in df.columns:
        raise KeyError("Input CSV missing 'Year_Month' column")
    if "Province" not in df.columns:
        raise KeyError("Input CSV missing 'Province' column")

    # Extract year from Year_Month (e.g., '1990-01' -> 1990)
    df["Year"] = df["Year_Month"].astype(str).str.split("-", n=1).str[0].astype(int)

    # Numeric columns to average: any column that starts with 'Average'
    avg_cols = [c for c in df.columns if c.startswith("Average")]
    if not avg_cols:
        raise KeyError("No 'Average ...' columns found to aggregate")

    # Convert avg columns to numeric (coerce errors to NaN)
    for c in avg_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # Group by Year and Province and compute mean of avg_cols
    grouped = df.groupby(["Year", "Province"])[avg_cols].mean().reset_index()

    # Save to CSV
    grouped.to_csv(output_csv, index=False)
    print(f"Wrote yearly means to {output_csv}. Rows: {len(grouped)}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", help="Path to mean_monthlyvalues.csv")
    parser.add_argument("--output", "-o", help="Path to write mean_yearlyvalues.csv")
    args = parser.parse_args(argv)

    src, dst = resolve_paths(args.input, args.output)
    generate_yearly_mean(src, dst)


if __name__ == "__main__":
    main()
