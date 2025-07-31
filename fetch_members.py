#!/usr/bin/env python3
"""
Congressional Members Tracker
Fetches member data from api.congress.gov and saves as JSON and CSV
"""

import requests
import json
import csv
import os
from datetime import datetime
import time
import sys

# Configuration
API_KEY = os.getenv('CONGRESS_API_KEY', 'gUq4UMKwmLo76ysUJ8Jn00aCUDgXmZU1CFNFW5xr')
BASE_URL = 'https://api.congress.gov/v3/member'
LIMIT = 250
OUTPUT_DIR = 'data'

def ensure_output_directory():
    """Create output directory if it doesn't exist"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def fetch_members_page(offset=0):
    """Fetch a single page of members data"""
    params = {
        'format': 'json',
        'offset': offset,
        'limit': LIMIT,
        'api_key': API_KEY
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data at offset {offset}: {e}")
        return None

def fetch_all_members():
    """Fetch all members using three specific requests"""
    all_members = []
    offsets = [0, 250, 500]  # Three specific requests to ensure we get all members
    
    print("Starting to fetch congressional members data...")
    
    for offset in offsets:
        print(f"Fetching page at offset {offset}...")
        data = fetch_members_page(offset)
        
        if not data or 'members' not in data:
            print(f"No data found at offset {offset}")
            continue
            
        members = data['members']
        if not members:
            print(f"No members found at offset {offset}")
            continue
            
        all_members.extend(members)
        print(f"Fetched {len(members)} members from offset {offset} (total: {len(all_members)})")
        
        # Rate limiting - be respectful to the API
        time.sleep(0.5)
    
    print(f"Total members fetched: {len(all_members)}")
    return all_members

def save_as_json(members, filename):
    """Save members data as JSON"""
    data = {
        'last_updated': datetime.now().isoformat(),
        'total_members': len(members),
        'members': members
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved JSON data to {filename}")

def save_as_csv(members, filename):
    """Save members data as CSV"""
    if not members:
        print("No members data to save as CSV")
        return
    
    # Get all unique field names from all members
    fieldnames = set()
    for member in members:
        fieldnames.update(member.keys())
    
    fieldnames = sorted(list(fieldnames))
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for member in members:
            # Handle nested objects by converting to string
            row = {}
            for field in fieldnames:
                value = member.get(field, '')
                if isinstance(value, (dict, list)):
                    value = json.dumps(value)
                row[field] = value
            writer.writerow(row)
    
    print(f"Saved CSV data to {filename}")

def main():
    """Main function"""
    ensure_output_directory()
    
    # Fetch all members
    members = fetch_all_members()
    
    if not members:
        print("No members data fetched. Exiting.")
        sys.exit(1)
    
    # Generate filenames with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_filename = os.path.join(OUTPUT_DIR, f'congressional_members_{timestamp}.json')
    csv_filename = os.path.join(OUTPUT_DIR, f'congressional_members_{timestamp}.csv')
    
    # Also save as latest files (without timestamp)
    latest_json = os.path.join(OUTPUT_DIR, 'congressional_members_latest.json')
    latest_csv = os.path.join(OUTPUT_DIR, 'congressional_members_latest.csv')
    
    # Save data
    save_as_json(members, json_filename)
    save_as_csv(members, csv_filename)
    
    # Save latest versions
    save_as_json(members, latest_json)
    save_as_csv(members, latest_csv)
    
    print(f"\nData fetch completed successfully!")
    print(f"Files saved:")
    print(f"  - {json_filename}")
    print(f"  - {csv_filename}")
    print(f"  - {latest_json}")
    print(f"  - {latest_csv}")

if __name__ == '__main__':
    main()
