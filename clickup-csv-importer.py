#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ClickUp CSV Task Importer

This script reads task data from a CSV file and creates tasks in ClickUp via the API.
You need to provide your ClickUp API token and list ID to use this script.

Usage:
    python clickup_csv_importer.py --csv-file tasks.csv --list-id YOUR_LIST_ID --api-token YOUR_API_TOKEN
"""

import argparse
import csv
import json
import requests
import sys
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ClickUpCSVImporter:
    """Class for importing tasks from CSV to ClickUp"""
    
    def __init__(self, api_token, list_id):
        """Initialize with API token and list ID"""
        self.api_token = api_token
        self.list_id = list_id
        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": api_token,
            "Content-Type": "application/json"
        }
        
        # Verify API token and list ID
        self.verify_access()
    
    def verify_access(self):
        """Verify API token and list ID are valid"""
        try:
            # Test API token by getting user info
            user_url = f"{self.base_url}/user"
            response = requests.get(user_url, headers=self.headers)
            response.raise_for_status()
            
            # Test list ID
            list_url = f"{self.base_url}/list/{self.list_id}"
            response = requests.get(list_url, headers=self.headers)
            response.raise_for_status()
            
            logger.info("API token and list ID verified successfully.")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logger.error("Invalid API token. Please check your API token and try again.")
                sys.exit(1)
            elif e.response.status_code == 404:
                logger.error(f"List ID {self.list_id} not found. Please check your list ID and try again.")
                sys.exit(1)
            else:
                logger.error(f"HTTP error occurred: {e}")
                sys.exit(1)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error connecting to ClickUp API: {e}")
            sys.exit(1)
    
    def create_task(self, task_data):
        """Create a task in ClickUp"""
        task_url = f"{self.base_url}/list/{self.list_id}/task"
        
        try:
            response = requests.post(task_url, headers=self.headers, json=task_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to create task: {e.response.text}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error connecting to ClickUp API: {e}")
            return None
    
    def parse_date(self, date_str):
        """Parse date string to milliseconds timestamp for ClickUp API"""
        if not date_str:
            return None
        
        try:
            # Try different date formats
            for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d'):
                try:
                    dt = datetime.strptime(date_str, fmt)
                    # Convert to milliseconds timestamp
                    return int(dt.timestamp() * 1000)
                except ValueError:
                    continue
            
            # If none of the formats match
            logger.warning(f"Could not parse date: {date_str}. Using None instead.")
            return None
        except Exception as e:
            logger.warning(f"Error parsing date {date_str}: {e}")
            return None
    
    def process_csv(self, csv_file):
        """Process CSV file and create tasks in ClickUp"""
        success_count = 0
        error_count = 0
        
        try:
            with open(csv_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Check if required field 'name' is in the CSV
                if 'name' not in reader.fieldnames:
                    logger.error("CSV must contain a 'name' column for task names")
                    sys.exit(1)
                
                total_rows = sum(1 for _ in reader)
                f.seek(0)  # Reset file pointer
                next(reader)  # Skip header row
                
                logger.info(f"Found {total_rows} tasks in CSV file")
                
                for i, row in enumerate(reader, 1):
                    # Skip empty rows
                    if not row or not row.get('name'):
                        logger.warning(f"Skipping row {i} - no task name provided")
                        continue
                    
                    # Prepare task data
                    task_data = {
                        "name": row.get('name', ''),
                        "description": row.get('description', ''),
                    }
                    
                    # Add due date if available
                    if 'due_date' in row and row['due_date']:
                        due_date = self.parse_date(row['due_date'])
                        if due_date:
                            task_data['due_date'] = due_date
                    
                    # Add priority if available
                    if 'priority' in row and row['priority']:
                        # Map priority text to ClickUp priority values (1=Urgent, 2=High, 3=Normal, 4=Low)
                        priority_map = {
                            'urgent': 1,
                            'high': 2,
                            'normal': 3,
                            'low': 4
                        }
                        priority_text = row['priority'].lower()
                        if priority_text in priority_map:
                            task_data['priority'] = priority_map[priority_text]
                    
                    # Add status if available
                    if 'status' in row and row['status']:
                        task_data['status'] = row['status']
                    
                    # Add tags if available
                    if 'tags' in row and row['tags']:
                        tags = [tag.strip() for tag in row['tags'].split(',')]
                        task_data['tags'] = tags
                    
                    # Add assignees if available (comma-separated user IDs)
                    if 'assignees' in row and row['assignees']:
                        assignees = [assignee.strip() for assignee in row['assignees'].split(',')]
                        task_data['assignees'] = assignees
                        
                    # Process subtasks if available
                    if 'subtasks' in row and row['subtasks']:
                        subtasks = [{'name': subtask.strip()} for subtask in row['subtasks'].split(';')]
                        if subtasks:
                            task_data['subtasks'] = subtasks
                    
                    # Add any custom fields if available
                    for key, value in row.items():
                        if key.startswith('custom_') and value:
                            custom_field_id = key.replace('custom_', '')
                            if 'custom_fields' not in task_data:
                                task_data['custom_fields'] = []
                            task_data['custom_fields'].append({
                                'id': custom_field_id,
                                'value': value
                            })
                    
                    # Create task in ClickUp
                    logger.info(f"Creating task {i}/{total_rows}: {task_data['name']}")
                    response = self.create_task(task_data)
                    
                    if response:
                        success_count += 1
                        logger.info(f"Successfully created task: {task_data['name']} with ID {response.get('id')}")
                    else:
                        error_count += 1
                        logger.error(f"Failed to create task: {task_data['name']}")
        
        except FileNotFoundError:
            logger.error(f"CSV file not found: {csv_file}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error processing CSV file: {e}")
            sys.exit(1)
        
        return success_count, error_count

def main():
    """Main function to run the script"""
    parser = argparse.ArgumentParser(description='Import tasks from CSV to ClickUp')
    parser.add_argument('--csv-file', required=True, help='Path to CSV file')
    parser.add_argument('--list-id', required=True, help='ClickUp list ID')
    parser.add_argument('--api-token', required=True, help='ClickUp API token')
    
    args = parser.parse_args()
    
    importer = ClickUpCSVImporter(args.api_token, args.list_id)
    
    logger.info(f"Starting import from {args.csv_file} to list {args.list_id}")
    success_count, error_count = importer.process_csv(args.csv_file)
    
    logger.info(f"Import completed. Successfully created {success_count} tasks, {error_count} failed.")

if __name__ == "__main__":
    main()
