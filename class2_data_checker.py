import argparse
import csv
import sys
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S"
)
# Create a module-level logger
logger = logging.getLogger(__name__)

def check_data(filename):
    """Read the CSV file and check for missing values."""
    with open(filename, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    header = rows[0]
    data = rows[1:]
    missing_rows = []

    for row_number, row in enumerate(data, start=2):
        if any(value == "" for value in row):
            missing_rows.append(row_number)

    return header, data, missing_rows

# Create an ArgumentParser
parser = argparse.ArgumentParser(
    description="Check the quality of a CSV file"
)

# Add a named argument (required)
parser.add_argument(
    "--input", "-i",
    required=True,
    help="CSV file to check"
)

# Add named arguments (optional)
parser.add_argument(
    "--output", "-o",
    default="data_quality.txt",
    help="Output report filename"
)

parser.add_argument(
    "--verbose", "-v", 
    action="store_true", 
    help="Show detailed DEBUG messages"
    # Note 1: verbose has its default value as False
    # Note 2: action="store_true" sets this to True.
)

# Parse the command-line arguments
args = parser.parse_args()
# e.g. args.input , args.output, args.verbose

if args.verbose:
    logger.setLevel(logging.DEBUG)

logger.debug(f"Arguments parsed: filename = {args.input}")

# Check if the file exists 
p = Path(args.input)
if not p.is_file():
    logger.error(f"File not found: '{args.input}'")
    sys.exit(1)

logger.info(f"File validated: '{args.input}'")

logger.debug(f"Loading data from: {args.input}")

# Check the data
#header, data, missing_rows = check_data(args.filename) # args.input
header, data, missing_rows = check_data(args.input)

logger.info(f"Loaded {len(data)} rows")

if len(data) == 0:
    logger.error("Input file contains no data; cannot continue")
    sys.exit(1)
    
for row_number in missing_rows:
    logger.warning(f"Row {row_number} has missing values")

# Save the report
with open(args.output, "w") as f:
    f.write(f"Number of rows: {len(data)}\n")
    f.write(f"Number of columns: {len(header)}\n")
    f.write(f"Number of rows with missing values: {len(missing_rows)}\n")
    
logger.info(f"Report saved to {args.output}")