import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from class6_7_netflix_utils import (
    clean_text,
    drop_missing_rows,
    remove_duplicates,
    remove_iqr_outliers,
    show_overview,
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Explore Netflix titles"
    )
    parser.add_argument(
        "--input",
        default="data/messy_netflix_titles.csv",
        help="Path to the Netflix CSV file"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug messages"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )

    # TODO 4:
    # Create a Path object from args.input.
    # Inside a try block, load that path using pd.read_csv().
    # Catch FileNotFoundError, log an ERROR message,
    # and exit with sys.exit(1).
    # Log an INFO message.
    path = Path(args.input)
    try:
        df = pd.read_csv(path)
        df_original = df.copy()
    except FileNotFoundError:
        logger.error(f"Input file not found: {args.input}")
        sys.exit(1)
    logger.info(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns")

    # TODO 5:
    # Call show_overview().
    # Log an INFO message.
    show_overview(df)
    logger.info(f"Displayed dataframe overview")

    # TODO 6:
    # Call remove_duplicates().
    # Call drop_missing_rows().
    # Log an INFO message after each step that
    # includes the number of rows removed.
    rows_before = len(df)
    df = remove_duplicates(df)
    logger.info(f"Removed {rows_before - len(df)} duplicate row(s)")
    rows_before = len(df)
    df = drop_missing_rows(df)
    logger.info(f"Dropped {rows_before - len(df)} rows with missing values")

    # TODO 3:
    # Inside a try block, remove runtime_minutes outliers
    # using remove_iqr_outliers() with a threshold of 1.5.
    # Catch ValueError and exit with sys.exit(1).
    # Log an INFO message.
    rows_before_outliers = len(df)
    try:
        df = remove_iqr_outliers(df, "runtime_minutes", 1.5)
        logger.info(f"Removed {rows_before_outliers - len(df)} runtime minutes outlier(s)")
    except ValueError:
        logger.error(f"Column not found")
        sys.exit(1)
    
    # TODO 4:
    # Apply clean_text() to title, type, and country.
    # Log an INFO message.
    for col in ["title", "type", "country"]:
        df[col] = df[col].apply(clean_text)
        logger.info(f"Cleaned text column: {col}")

    # TODO 5:
    # Create a report (dictionary) containing rows_before, rows_after, rows_removed, and columns.
    # Log an INFO message reporting: rows_before, rows_after, rows_removed, and columns.    
    report = {
        "rows_before": len(df_original),
        "rows_after": len(df),
        "rows_removed": len(df_original) - len(df),
        "columns": df.shape[1]
    }
    logger.info(f"Cleaning complete: {report}")
    
if __name__ == "__main__":
    main()