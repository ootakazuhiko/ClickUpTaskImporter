# ClickUp CSV Task Importer - Usage Guide

This program is a tool for creating tasks in ClickUp from CSV files using the API.

## Preparation

### 1. Requirements

- Python 3.6 or later
- Required Python packages (requests, python-dateutil)
- ClickUp API token
- ClickUp list ID for the import destination

### 2. Getting an API Token

1. Log in to ClickUp
2. Click on your profile avatar in the bottom left
3. Select "Settings"
4. Click on "Apps" in the left sidebar
5. Click "Generate" to create an API token
6. Copy the created token

### 3. Getting a List ID

1. Open the list in ClickUp web interface where you want to import tasks
2. Find the "list/XXXXXXXXX" part in the URL (XXXXXXXXX is the list ID)

Example: For `https://app.clickup.com/123456/v/li/789012345`, the list ID is `789012345`

## Environment Setup

```bash
# Clone the repository
git clone https://github.com/ootakazuhiko/ClickUpTaskImporter.git
cd ClickUpTaskImporter

# Create a virtual environment
python -m venv venv

# Activate the virtual environment (Windows/Git Bash)
source venv/Scripts/activate

# Install required packages
pip install -r requirements.txt
```

## Preparing CSV Files

Create a CSV file in the following format:

- The first row should be a header row containing the following fields (at minimum, `name` is required)
- Available fields:
  - `name`: Task name (required)
  - `description`: Task description
  - `due_date`: Due date (supports YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, YYYY/MM/DD formats)
  - `priority`: Priority (urgent, high, normal, low)
  - `status`: Status (to do, in progress, complete, etc.)
  - `tags`: Tags (comma-separated)
  - `assignees`: User IDs of assignees (comma-separated)
  - `subtasks`: Subtask names (semicolon-separated)
  - `custom_[ID]`: Custom field (ID is the ClickUp custom field ID)

A template CSV file is available at `template/tasks_template.csv` for reference.

## Usage

### Basic Usage

```bash
# Activate the virtual environment (if not already activated)
source venv/Scripts/activate

# Import tasks
python clickup_csv_importer.py --csv-file tasks.csv --list-id YOUR_LIST_ID --api-token YOUR_API_TOKEN
```

### Additional Options

```bash
# Dry run (test run without actually creating tasks)
python clickup_csv_importer.py --csv-file tasks.csv --list-id YOUR_LIST_ID --api-token YOUR_API_TOKEN --dry-run

# Output results to a CSV file
python clickup_csv_importer.py --csv-file tasks.csv --list-id YOUR_LIST_ID --api-token YOUR_API_TOKEN --output results.csv

# Enable detailed logging
python clickup_csv_importer.py --csv-file tasks.csv --list-id YOUR_LIST_ID --api-token YOUR_API_TOKEN --verbose
```

## Other Features

- If task creation fails, an error message will be displayed, but processing will continue
- Multiple date formats are supported (YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, YYYY/MM/DD)
- Priority is automatically converted from text (urgent, high, normal, low) to ClickUp's numeric format
- Dry run mode (`--dry-run`) allows simulation of task creation
- Results output (`--output`) saves import results to a CSV file

## Troubleshooting

- API authentication error: Verify that your API token is correct
- List ID error: Check that your list ID is correct and that you have access to that list
- CSV format error: Ensure that your CSV file is in the correct format and is UTF-8 encoded
- Date conversion error: Verify that dates are entered in the correct format
- Network error: Check your internet connection and the status of the ClickUp API

## Running Tests

To run tests, use the following command:

```bash
# Activate the virtual environment (if not already activated)
source venv/Scripts/activate

# Run tests
python -m unittest discover -s tests
```