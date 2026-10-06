import logging

logger = logging.getLogger(__name__)

def require_columns(df, required_columns):
    """Check that all required columns exist."""
    # TODO 2:
    # Check if any of the configured columns (list) are missing from df.
    # If any are missing, log an ERROR and raise ValueError.
    # Log an INFO.
    # Return the DataFrame.
    missing_col = [col for col in required_columns if col not in df.columns]
    if missing_col:
        logger.error(f"Missing columns: {','.join(missing_col)}")
        raise ValueError(f"One or more required columns are missing")
    
    logger.info(f"Columns validated")
    return df