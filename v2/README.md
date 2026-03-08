# SRR Converter v2 (Google Sheets Integration)

This program processes student report data, calculates ratings and percentiles, and syncs data with Google Sheets.

## Prerequisites

- **Python 3.8+** installed on your system.
- **Google Cloud Service Account Key** (JSON file) for authentication.
- **Spreadsheet ID** of the Google Sheet you want to use.

## Setup Instructions

### 1. Prepare Environment

Navigate to the `v2` directory in your terminal (macOS/Linux) or Command Prompt/PowerShell (Windows).

**macOS / Linux:**
```bash
cd v2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```powershell
cd v2
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configuration

1.  **Create `.env` file:**
    - Copy `.env.example` to a new file named `.env`.
    - Open `.env` and set your `SPREADSHEET_ID` and the path to your service account key file.
    
    Example `.env` content:
    ```ini
    SPREADSHEET_ID=your_spreadsheet_id_here
    GOOGLE_APPLICATION_CREDENTIALS=.env.key.json
    ```

2.  **Add Credentials:**
    - Place your Google Cloud service account JSON key file in the `v2` directory.
    - Rename it to `.env.key.json` (or match the name in your `.env` file).

3.  **Share Spreadsheet:**
    - Open your Google Sheet in the browser.
    - Click "Share" and add the **client email** found in your `.env.key.json` file as an **Editor**.

## Running the Program

### Step 1: Upload Data (Optional / First Time)
If you need to populate the spreadsheet with data from local JSON files (e.g., from `v1/data`), run the upload tool.

**macOS / Linux:**
```bash
# Must run from v2 directory
PYTHONPATH=. python tools/upload_data.py
```

**Windows:**
```powershell
# Must run from v2 directory
$env:PYTHONPATH="."
python tools/upload_data.py
```

### Step 2: Generate Reports
This is the main command. It reads data from the Google Sheet, calculates scores/percentiles, and writes the results back to the output sheets.

**macOS / Linux:**
```bash
python main.py
```

**Windows:**
```powershell
python main.py
```

### Command Line Arguments
You can override the configuration in `config.py` using command-line arguments.

**Show Help:**
```bash
python main.py --help
```

**Override Spreadsheet ID and Key File:**
```bash
python main.py --ssid "YOUR_SPREADSHEET_ID" --key-file "path/to/key.json"
```

**Using Helper Scripts:**
Arguments are passed through to the python script:
```bash
./run_v2.sh --ssid "123456789abc"
```

## Output

The program will:
1.  Read student data and scores from the configured Google Sheet.
2.  Generate local report files in `v2/report_output/`:
    - `students.json`
    - `overallRating.csv`
    - `percentile.csv`
    - `statistic.csv`
3.  Upload these results to the corresponding tabs in your Google Spreadsheet.

## Troubleshooting

- **ModuleNotFoundError: No module named 'google_sheets'**:
  - Ensure you are running the command from the `v2` directory.
  - On Windows, make sure to set `$env:PYTHONPATH="."` before running `upload_data.py`.

- **Permission Denied (403)**:
  - Verify that you have shared the Google Sheet with the service account email address.

- **Empty/Zero Percentiles**:
  - Ensure the spreadsheet data is correct. Empty cells in report sheets mean "subject not taken". A score of `0` means the subject was taken but scored 0.
