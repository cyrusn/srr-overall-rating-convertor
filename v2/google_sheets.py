from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import SPREADSHEET_ID, GOOGLE_KEY_FILE

class GoogleSheet:
    def __init__(self, spreadsheet_id=None, key_file=None):
        self.spreadsheet_id = spreadsheet_id or SPREADSHEET_ID
        self.key_file = key_file or GOOGLE_KEY_FILE
        
        if not self.spreadsheet_id:
            raise ValueError("Error: SPREADSHEET_ID is missing. Please set it in v2/config.py.")
            
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        try:
            self.creds = service_account.Credentials.from_service_account_file(
                self.key_file, scopes=self.scopes
            )
            self.service = build('sheets', 'v4', credentials=self.creds)
        except Exception as e:
            print(f"Error initializing Google Sheets service: {e}")
            self.service = None

    def create_sheet_if_missing(self, sheet_title):
        """Creates a new sheet (tab) if it doesn't exist."""
        if not self.service or not self.spreadsheet_id:
            return

        try:
            spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
            sheets = spreadsheet.get('sheets', [])
            existing_titles = [s['properties']['title'] for s in sheets]
            
            if sheet_title not in existing_titles:
                print(f"Creating sheet '{sheet_title}'...")
                body = {
                    'requests': [{
                        'addSheet': {
                            'properties': {
                                'title': sheet_title
                            }
                        }
                    }]
                }
                self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body=body
                ).execute()
        except Exception as e:
            print(f"Error creating sheet '{sheet_title}': {e}")

    def get_sheet_data(self, sheet_range):
        """Retrieves data from a specific range and converts it to a list of dicts."""
        if not self.service or not self.spreadsheet_id:
            return []
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=sheet_range,
                valueRenderOption='UNFORMATTED_VALUE'
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return []
                
            headers = values[0]
            rows = values[1:]
            
            data = []
            for row in rows:
                # Pad row with None if it's shorter than headers
                padded_row = row + [None] * (len(headers) - len(row))
                data.append(dict(zip(headers, padded_row)))
                
            return data
        except Exception as e:
            print(f"Error fetching data from range {sheet_range}: {e}")
            return []

    def clear_data(self, sheet_range):
        """Clears a specific range."""
        if not self.service or not self.spreadsheet_id:
            return
        self.service.spreadsheets().values().clear(
            spreadsheetId=self.spreadsheet_id,
            range=sheet_range
        ).execute()

    def update_data(self, sheet_range, values, input_option='USER_ENTERED'):
        """Updates a specific range with new values."""
        if not self.service or not self.spreadsheet_id:
            return
        body = {
            'values': values
        }
        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=sheet_range,
            valueInputOption=input_option,
            body=body
        ).execute()

    def append_data(self, sheet_range, values, input_option='USER_ENTERED'):
        """Appends values to a specific range."""
        if not self.service or not self.spreadsheet_id:
            return
        body = {
            'values': values
        }
        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=sheet_range,
            valueInputOption=input_option,
            body=body
        ).execute()
