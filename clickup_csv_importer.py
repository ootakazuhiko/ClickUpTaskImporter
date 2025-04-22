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
import os
from datetime import datetime
from dateutil import parser as date_parser

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# カスタム例外クラスの定義
class ClickUpImporterError(Exception):
    """ClickUp Importerの基本例外クラス"""
    pass

class APIError(ClickUpImporterError):
    """API接続に関するエラー"""
    pass

class AuthenticationError(APIError):
    """認証エラー"""
    pass

class ResourceNotFoundError(APIError):
    """リソースが見つからないエラー"""
    pass

class CSVError(ClickUpImporterError):
    """CSVファイルに関するエラー"""
    pass

class ConfigurationError(ClickUpImporterError):
    """設定に関するエラー"""
    pass

class ClickUpCSVImporter:
    """Class for importing tasks from CSV to ClickUp"""
    
    def __init__(self, api_token, list_id, dry_run=False, output_file=None):
        """Initialize with API token and list ID"""
        if not api_token:
            raise ConfigurationError("API token is required")
        if not list_id:
            raise ConfigurationError("List ID is required")
            
        self.api_token = api_token
        self.list_id = list_id
        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": api_token,
            "Content-Type": "application/json"
        }
        self.dry_run = dry_run
        self.output_file = output_file
        
        # Initialize results tracking
        self.results = {
            "success": [],
            "failure": []
        }
        
        # Verify API token and list ID if not in dry run mode
        if not dry_run:
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
            
            # Get list name for confirmation
            list_name = response.json().get('name', 'Unknown')
            logger.info(f"API token and list ID verified successfully. List name: {list_name}")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                msg = "Invalid API token. Please check your API token and try again."
                logger.error(msg)
                raise AuthenticationError(msg) from e
            elif e.response.status_code == 404:
                msg = f"List ID {self.list_id} not found. Please check your list ID and try again."
                logger.error(msg)
                raise ResourceNotFoundError(msg) from e
            else:
                msg = f"HTTP error occurred: {e}"
                logger.error(msg)
                raise APIError(msg) from e
        except requests.exceptions.RequestException as e:
            msg = f"Error connecting to ClickUp API: {e}"
            logger.error(msg)
            raise APIError(msg) from e
    
    def create_task(self, task_data):
        """Create a task in ClickUp"""
        # In dry run mode, just log and return a simulated success response
        if self.dry_run:
            logger.info(f"[DRY RUN] Would create task: {task_data['name']}")
            simulated_response = {
                "id": "dry-run-task-id",
                "name": task_data["name"],
                "url": "https://app.clickup.com/dry-run-url"
            }
            return simulated_response
            
        task_url = f"{self.base_url}/list/{self.list_id}/task"
        
        try:
            response = requests.post(task_url, headers=self.headers, json=task_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_msg = f"Failed to create task: {e.response.text}"
            logger.error(error_msg)
            return None
        except requests.exceptions.RequestException as e:
            error_msg = f"Error connecting to ClickUp API: {e}"
            logger.error(error_msg)
            return None
    
    def parse_date(self, date_str):
        """Parse date string to milliseconds timestamp for ClickUp API"""
        if not date_str:
            return None
        
        try:
            # Use dateutil parser which handles many date formats
            dt = date_parser.parse(date_str)
            # Convert to milliseconds timestamp
            return int(dt.timestamp() * 1000)
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
                    msg = "CSV must contain a 'name' column for task names"
                    logger.error(msg)
                    raise CSVError(msg)
                
                # Count rows in the file
                rows = list(reader)
                total_rows = len(rows)
                
                logger.info(f"Found {total_rows} tasks in CSV file")
                
                # Reset file pointer
                f.seek(0)
                reader = csv.DictReader(f)
                
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
                        task_id = response.get('id', 'unknown')
                        task_url = response.get('url', '')
                        success_msg = f"Successfully created task: {task_data['name']} with ID {task_id}"
                        logger.info(success_msg)
                        
                        # Add to results
                        self.results["success"].append({
                            "name": task_data['name'],
                            "id": task_id,
                            "url": task_url
                        })
                    else:
                        error_count += 1
                        error_msg = f"Failed to create task: {task_data['name']}"
                        logger.error(error_msg)
                        
                        # Add to results
                        self.results["failure"].append({
                            "name": task_data['name'],
                            "row": i,
                            "error": "API request failed"
                        })
        
        except FileNotFoundError:
            msg = f"CSV file not found: {csv_file}"
            logger.error(msg)
            raise CSVError(msg)
        except Exception as e:
            if isinstance(e, ClickUpImporterError):
                raise
            msg = f"Error processing CSV file: {e}"
            logger.error(msg)
            raise CSVError(msg) from e
        
        # Write results to output file if specified
        if self.output_file:
            self.write_results_to_csv()
            
        return success_count, error_count
    
    def write_results_to_csv(self):
        """Write import results to a CSV file"""
        if not self.output_file:
            return
            
        try:
            with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
                # Define fieldnames for the CSV
                fieldnames = ['task_name', 'status', 'task_id', 'task_url', 'error']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                # Write successful tasks
                for task in self.results["success"]:
                    writer.writerow({
                        'task_name': task['name'],
                        'status': 'SUCCESS',
                        'task_id': task['id'],
                        'task_url': task['url'],
                        'error': ''
                    })
                
                # Write failed tasks
                for task in self.results["failure"]:
                    writer.writerow({
                        'task_name': task['name'],
                        'status': 'FAILED',
                        'task_id': '',
                        'task_url': '',
                        'error': task.get('error', 'Unknown error')
                    })
                    
            logger.info(f"Results written to {self.output_file}")
        except Exception as e:
            msg = f"Failed to write results to CSV: {e}"
            logger.error(msg)
            # ここでは例外をスローせず、ログに記録するだけにする（結果の出力は重要だが、失敗しても処理を続行できる）

def get_api_token_from_env():
    """Get API token from environment variable"""
    return os.environ.get("CLICKUP_API_TOKEN")

def main():
    """Main function to run the script"""
    parser = argparse.ArgumentParser(description='Import tasks from CSV to ClickUp')
    parser.add_argument('--csv-file', required=True, help='Path to CSV file')
    parser.add_argument('--list-id', required=True, help='ClickUp list ID')
    parser.add_argument('--api-token', help='ClickUp API token (または環境変数 CLICKUP_API_TOKEN で指定)')
    parser.add_argument('--dry-run', action='store_true', help='Run in test mode without creating tasks')
    parser.add_argument('--output', help='Output file path for results CSV')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    try:
        args = parser.parse_args()
        
        # API token from command line or environment variable
        api_token = args.api_token or get_api_token_from_env()
        if not api_token:
            raise ConfigurationError("API token is required. Provide it via --api-token argument or CLICKUP_API_TOKEN environment variable.")
        
        # Set logging level based on verbose flag
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            
        # Initialize importer
        importer = ClickUpCSVImporter(
            api_token, 
            args.list_id, 
            dry_run=args.dry_run,
            output_file=args.output
        )
        
        # Log startup info
        if args.dry_run:
            logger.info(f"Starting DRY RUN import from {args.csv_file} to list {args.list_id}")
        else:
            logger.info(f"Starting import from {args.csv_file} to list {args.list_id}")
        
        # Process CSV
        success_count, error_count = importer.process_csv(args.csv_file)
        
        # Log completion info
        if args.dry_run:
            logger.info(f"DRY RUN completed. Would have created {success_count} tasks, {error_count} would have failed.")
        else:
            logger.info(f"Import completed. Successfully created {success_count} tasks, {error_count} failed.")
        
        # Output file info
        if args.output:
            logger.info(f"Results written to {args.output}")
            
        return 0  # 正常終了
            
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        return 1
    except AuthenticationError as e:
        logger.error(f"Authentication error: {e}")
        return 1
    except ResourceNotFoundError as e:
        logger.error(f"Resource not found: {e}")
        return 1
    except APIError as e:
        logger.error(f"API error: {e}")
        return 1
    except CSVError as e:
        logger.error(f"CSV error: {e}")
        return 1
    except ClickUpImporterError as e:
        logger.error(f"Error: {e}")
        return 1
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return 1

# コマンドライン実行のエントリーポイント
if __name__ == "__main__":
    sys.exit(main())
