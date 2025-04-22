#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for ClickUp CSV Importer
"""

import unittest
import os
import sys
import tempfile
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path to import module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clickup_csv_importer import ClickUpCSVImporter

class TestClickUpCSVImporter(unittest.TestCase):
    """Test cases for ClickUpCSVImporter"""
    
    def setUp(self):
        """Set up test environment"""
        self.api_token = "test_token"
        self.list_id = "test_list_id"
        self.test_csv_content = """name,description,due_date,priority,status,tags,assignees,subtasks
Test Task 1,Description 1,2025-05-01,high,to do,tag1,12345,Sub1;Sub2
Test Task 2,Description 2,2025-05-15,normal,in progress,tag2;tag3,67890,
"""
    
    @patch('clickup_csv_importer.requests.get')
    def test_verify_access(self, mock_get):
        """Test API token and list ID verification"""
        # Mock successful responses
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"name": "Test List"}
        mock_get.return_value = mock_response
        
        # Create importer with patched requests
        with patch('sys.exit') as mock_exit:  # Patch sys.exit to prevent test from exiting
            importer = ClickUpCSVImporter(self.api_token, self.list_id, dry_run=False)
        
        # Verify that requests.get was called twice (once for user, once for list)
        self.assertEqual(mock_get.call_count, 2)
        # Verify sys.exit was not called
        mock_exit.assert_not_called()
    
    @patch('clickup_csv_importer.requests.post')
    def test_create_task(self, mock_post):
        """Test task creation"""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "id": "test_task_id",
            "name": "Test Task",
            "url": "https://app.clickup.com/test_url"
        }
        mock_post.return_value = mock_response
        
        # Create importer with patched verify_access
        with patch.object(ClickUpCSVImporter, 'verify_access'):
            importer = ClickUpCSVImporter(self.api_token, self.list_id, dry_run=False)
            
            # Test create_task
            task_data = {"name": "Test Task", "description": "Test Description"}
            result = importer.create_task(task_data)
            
            # Verify that requests.post was called with expected arguments
            mock_post.assert_called_once()
            self.assertEqual(result["id"], "test_task_id")
    
    def test_parse_date(self):
        """Test date parsing"""
        # Use dry_run=True to avoid API calls
        importer = ClickUpCSVImporter(self.api_token, self.list_id, dry_run=True)
        
        # Test various date formats
        date_tests = [
            ("2025-05-01", True),  # YYYY-MM-DD
            ("05/01/2025", True),  # MM/DD/YYYY
            ("01/05/2025", True),  # DD/MM/YYYY (ambiguous but should work)
            ("2025/05/01", True),  # YYYY/MM/DD
            ("invalid date", False),  # Invalid date
            ("", False),  # Empty string
            (None, False)  # None
        ]
        
        for date_str, should_parse in date_tests:
            result = importer.parse_date(date_str)
            if should_parse:
                self.assertIsNotNone(result, f"Date '{date_str}' should be parsed")
                self.assertIsInstance(result, int, f"Parsed date should be an integer timestamp")
            else:
                self.assertIsNone(result, f"Date '{date_str}' should not be parsed")
    
    def test_process_csv_dry_run(self):
        """Test CSV processing in dry run mode"""
        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(self.test_csv_content)
            temp_file_path = temp_file.name
        
        try:
            # Create importer in dry run mode
            importer = ClickUpCSVImporter(self.api_token, self.list_id, dry_run=True)
            
            # Process the CSV
            success_count, error_count = importer.process_csv(temp_file_path)
            
            # Verify results
            self.assertEqual(success_count, 2)
            self.assertEqual(error_count, 0)
            self.assertEqual(len(importer.results["success"]), 2)
            self.assertEqual(len(importer.results["failure"]), 0)
        finally:
            # Clean up
            os.unlink(temp_file_path)

if __name__ == '__main__':
    unittest.main()