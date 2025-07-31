# Congressional Members Tracker

This repository automatically tracks and updates data for all members of the U.S. Congress using the official Congress.gov API. The data is refreshed daily and made available in both JSON and CSV formats.

## Features

- **Daily Updates**: Automated data fetching via GitHub Actions
- **Complete Coverage**: Fetches all congressional members using pagination
- **Multiple Formats**: Outputs data in both JSON and CSV formats
- **Timestamped Archives**: Keeps historical snapshots with timestamps
- **Latest Files**: Always-current `latest` files for easy access

## Data Files

The repository contains the following data files in the `data/` directory:

- `congressional_members_latest.json` - Most recent data in JSON format
- `congressional_members_latest.csv` - Most recent data in CSV format
- `congressional_members_YYYYMMDD_HHMMSS.json` - Timestamped JSON archives
- `congressional_members_YYYYMMDD_HHMMSS.csv` - Timestamped CSV archives

## Data Source

Data is fetched from the official [Congress.gov API](https://api.congress.gov/), specifically the `/v3/member` endpoint. The API provides comprehensive information about current and former members of Congress.

## Setup

### Prerequisites

- Python 3.9+
- Congress.gov API key (free from [api.congress.gov](https://api.congress.gov/sign-up/))

### Local Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/congressional-members-tracker.git
   cd congressional-members-tracker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your API key as an environment variable:
   ```bash
   export CONGRESS_API_KEY=your_api_key_here
   ```

4. Run the script:
   ```bash
   python fetch_members.py
   ```

### GitHub Repository Setup

1. Fork or create this repository on GitHub
2. Add your Congress.gov API key as a repository secret:
   - Go to Settings → Secrets and variables → Actions
   - Add a new secret named `CONGRESS_API_KEY`
   - Set the value to your API key

The GitHub Action will automatically run daily at 6:00 AM UTC and update the data files.

## Manual Updates

You can manually trigger an update by:

1. **GitHub UI**: Go to Actions → Update Congressional Members Data → Run workflow
2. **Local execution**: Run `python fetch_members.py` in your local environment

## Data Structure

The JSON files contain:
- `last_updated`: ISO timestamp of when the data was fetched
- `total_members`: Total number of members in the dataset
- `members`: Array of member objects with detailed information

The CSV files flatten the member data for easy analysis in spreadsheet applications.

## Rate Limiting

The script includes respectful rate limiting (0.5 second delays between requests) to avoid overwhelming the Congress.gov API servers.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is in the public domain. The data comes from official U.S. government sources and is not subject to copyright.

## Disclaimer

This is an unofficial tool. For the most up-to-date and authoritative information, please refer directly to [Congress.gov](https://www.congress.gov/).
