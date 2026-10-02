import logging
import re
import pandas as pd

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
    df.info()


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

def clean_text(value):
    """Normalize one text value."""
    # TODO 1:
    # Strip surrounding whitespace.
    # Convert text to lowercase.
    # Collapse repeated whitespace.
    value = value.strip()
    value = value.lower()
    value = re.sub(r"\s+", " ", value)
    return value


def remove_iqr_outliers(df, column, threshold):
    """Remove IQR outliers from one column."""
    # TODO 2:
    # If column does not exist:
    # Log an ERROR message and raise ValueError.
    # Calculate Q1, Q3, and IQR.
    # Use threshold to calculate lower and upper bounds.
    # Keep rows inside the bounds.
    # Log a DEBUG message containing the bounds and the number of rows removed.
    # Return the resulting DataFrame.
    if not column in df.columns:
        logger.error(f"Column not found: {column}")
        raise ValueError(f"Column not found: {column}")
    
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    
    lower = q1 - threshold * iqr
    upper = q3 + threshold * iqr
    
    df_filtered = df[(df[column] >= lower) & (df[column] <= upper)]
    
    rows_before = len(df)
    rows_after = len(df_filtered)
    logger.debug(f"Bounds: [{lower}, {upper}], removed {rows_before - rows_after} rows")
    
    return df_filtered