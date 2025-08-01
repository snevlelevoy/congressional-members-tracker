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

def parse_member_name(full_name):
    """Parse full name into first and last name"""
    # Names are typically in format "Last, First Middle" or "Last, First"
    if ',' in full_name:
        parts = full_name.split(',', 1)
        last_name = parts[0].strip()
        first_part = parts[1].strip()
        # Take only the first word as first name
        first_name = first_part.split()[0] if first_part else ""
    else:
        # Fallback if no comma
        parts = full_name.split()
        first_name = parts[0] if parts else ""
        last_name = parts[-1] if len(parts) > 1 else ""
    
    return first_name, last_name

def extract_member_data(member):
    """Extract only the requested fields from member data"""
    # Parse name
    full_name = member.get('name', '')
    first_name, last_name = parse_member_name(full_name)
    
    # Get current chamber (most recent term)
    chamber = ""
    if 'terms' in member and 'item' in member['terms']:
        terms = member['terms']['item']
        if terms:
            # Handle both single term (dict) and multiple terms (list)
            if isinstance(terms, list):
                # Get the most recent term (last in chronological list)
                recent_term = terms[-1]
            else:
                # Single term case
                recent_term = terms
            
            chamber_full = recent_term.get('chamber', '')
            # Simplify chamber name
            if 'House' in chamber_full:
                chamber = 'House'
            elif 'Senate' in chamber_full:
                chamber = 'Senate'
    
    # Handle district (Senators don't have districts)
    district = member.get('district')
    if district is None and chamber == 'Senate':
        district = 'At-Large'
    elif district is None:
        district = ''
    
    return {
        'first_name': first_name,
        'last_name': last_name,
        'state': member.get('state', ''),
        'district': str(district) if district else '',
        'party': member.get('partyName', ''),
        'chamber': chamber
    }

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
            
        # Extract only the requested fields from each member
        processed_members = []
        for member in members:
            processed_member = extract_member_data(member)
            processed_members.append(processed_member)
            
        all_members.extend(processed_members)
        print(f"Processed {len(processed_members)} members from offset {offset} (total: {len(all_members)})")
        
        # Rate limiting - be respectful to the API
        time.sleep(0.5)
    
    print(f"Total members processed: {len(all_members)}")
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
    
    # Define the specific fieldnames we want
    fieldnames = ['first_name', 'last_name', 'state', 'district', 'party', 'chamber']
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(members)
    
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
