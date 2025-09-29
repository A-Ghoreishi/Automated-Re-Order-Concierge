import os
import json
import gspread
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(".env")

# Loading credentials
creds_path = os.getenv("GOOGLE_CREDENTIALS_JSON")
sheet_id = os.getenv("SHEET_ID")

if not creds_path or not sheet_id:
    raise ValueError("Missing GOOGLE_CREDENTIALS_JSON or SHEET_ID in .env")

# Handle if Google_Credentials_JSON is a path is a path vs inline JSON string

if os.path.exists(creds_path):
    gc = gspread.service_account(filename=creds_path)

else:
    creds_dict = json.loads(creds_path)
    gc = gspread.service_account_from_dict(creds_dict)

# Open the sheets
sheet = gc.open_by_key(sheet_id)
worksheet = sheet.sheet1

def read_inventory():
    """Return all rows from Google Sheets as list of dicts."""
    records = worksheet.get_all_records()
    return records

def update_inventory_row(sku,updates):
    """
    Update a row by SKU.
    Example: update_inventory_row("SKU123", {"last_checked": "2025-09-29", "comments": "Approved"})
    """

    records = worksheet.get_all_records()
    for i, row in enumerate(records, start=2):
        if row["item_sku"] == sku:
            for key, value in updates.items():
                col_index = list(row.keys()).index(key) + 1
                worksheet.update_cell(i,col_index,value)
            return True
    return False