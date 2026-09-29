import logging

logger = logging.getLogger(__name__)


def show_overview(df):
    """Display basic information about a DataFrame."""
    # TODO 1:
    # Log a DEBUG message containing the shape.
    # Print the shape, first five rows, column names, and data types.
    logger.debug(f"Shape: {df.shape}")
    print(df.shape)
    print(df.head())
    print(list(df.columns))
    df.info


def remove_duplicates(df):
    """Remove exact duplicate rows."""
    # TODO 2:
    # Remove exact duplicate rows.
    # Log a DEBUG message containing the before and after row counts.
    # Return the resulting DataFrame.
    before = len(df)
    df = df.drop_duplicates()
    logger.debug(f"{before} rows before removal and {len(df)} rows after removal")
    return df


def drop_missing_rows(df):
    """Remove rows containing missing values."""
    # TODO 3:
    # Drop rows containing one or more missing values.
    # Log a DEBUG message containing the before and after row counts.
    # Return the resulting DataFrame.
    rows_before = df.shape[0]
    df = df.dropna()
    logger.debug(f"{rows_before} rows before removal and {df.shape[0]} rows after removal")
    return df