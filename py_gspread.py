import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Path to your JSON key file
JSON_KEYFILE = r"D:\Study Material\pyprograms\path_to_your_service_account.json"

# Google Sheet URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1arvvl6svXbn170nPuwUrA-T5SOcm4NKESBm1VzIIvGc/edit?gid=0#gid=0"

def extract_google_sheet_data():
    # Authenticate using the service account credentials
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEYFILE, scopes=SCOPE)
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open_by_url(SHEET_URL).sheet1  # Access the first sheet

    # Fetch all data from the sheet
    data = sheet.get_all_records()  # Returns a list of dictionaries
    return data

if __name__ == "__main__":
    try:
        data = extract_google_sheet_data()
        print("Data extracted successfully:")
        for row in data:
            print(row)
    except Exception as e:
        print("An error occurred:", e)
