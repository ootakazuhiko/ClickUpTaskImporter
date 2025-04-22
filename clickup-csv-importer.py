#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
[DEPRECATED] ClickUp CSV Task Importer

このスクリプトは非推奨です。代わりに clickup_csv_importer.py を使用してください。
This script is deprecated. Please use clickup_csv_importer.py instead.

This script reads task data from a CSV file and creates tasks in ClickUp via the API.
You need to provide your ClickUp API token and list ID to use this script.

Usage:
    python clickup_csv_importer.py --csv-file tasks.csv --list-id YOUR_LIST_ID --api-token YOUR_API_TOKEN
"""

import sys
import logging

# Set up logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main function to warn about deprecation"""
    logger.warning("This script (clickup-csv-importer.py) is deprecated. Please use clickup_csv_importer.py instead.")
    logger.warning("Run: python clickup_csv_importer.py --help for usage information.")
    sys.exit(1)

if __name__ == "__main__":
    main()
