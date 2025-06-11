import gspread
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
cred = Credentials.from_service_account_file("credentials.json", scopes=scopes)

client = gspread.authorize(cred)
sheet = client.open_by_key("1JtYtzxObTCawJejMX0yxtDjOGiAN3bk2hnv-OA9vDX8")
values_list = sheet.sheet1.row_values(1)
print(values_list)
