import os
import json
import gspread
from google.oauth2.service_account import Credentials

# Set the required scope for Google Sheets
scopes = ["https://www.googleapis.com/auth/spreadsheets"]

# Check if environment variable is available (Render, etc.)
if "GOOGLE_CREDS" in os.environ:
    service_account_info = json.loads(os.environ["GOOGLE_CREDS"])
    cred = Credentials.from_service_account_info(service_account_info, scopes=scopes)
else:
    # Local development fallback
    cred = Credentials.from_service_account_file("credentials.json", scopes=scopes)

# Authorize and access the spreadsheet
client = gspread.authorize(cred)
sheet = client.open_by_key("1JtYtzxObTCawJejMX0yxtDjOGiAN3bk2hnv-OA9vDX8").sheet1
values_list = sheet.row_values(1)

print(values_list)
