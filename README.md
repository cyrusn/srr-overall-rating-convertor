# Student Report Rating (SRR) Converter

This project calculates student ratings and percentiles based on report data. It has been upgraded to integrate directly with Google Sheets for easier data management.

## Project Structure

- `v1/`: Legacy version using local JSON files (Backup).
- `v2/`: Current version with **Google Sheets Integration**.
- `run_v2.sh`: macOS/Linux shortcut script.
- `run_v2.bat`: Windows shortcut script.

## Getting Started (v2)

### 1. Prerequisites
- **Python 3.8+**
- **Google Cloud Service Account Key**: A JSON file with access to the Google Sheets API.
- **Spreadsheet Access**: Share your Google Sheet with the `client_email` found in your JSON key.

### 2. Setup
First, set up your Python environment in the `v2` folder:

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

### 3. Configuration
Open `v2/config.py` and update the following:
- `SPREADSHEET_ID`: The ID of your Google Spreadsheet.
- `GOOGLE_KEY_FILE`: The filename of your JSON key (e.g., `.env.key.json`).

### 4. Running
You can run the program directly from this root directory:

**macOS / Linux:**
```bash
./run_v2.sh
```

**Windows:**
Double-click `run_v2.bat` or run from Command Prompt/PowerShell:
```powershell
.\run_v2.bat
```

### 5. Advanced Usage (Arguments)
You can override the configuration using command-line flags.

**macOS / Linux:**
```bash
./run_v2.sh --ssid "YOUR_SPREADSHEET_ID" --key-file "path/to/key.json"
```

**Windows:**
```powershell
.\run_v2.bat --ssid "YOUR_SPREADSHEET_ID" --key-file "path/to/key.json"
```

For detailed technical details, see the [v2 README](./v2/README.md).
