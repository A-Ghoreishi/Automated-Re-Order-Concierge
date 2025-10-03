import os, json, gspread
from dotenv import load_dotenv

load_dotenv()
creds_path = os.getenv("GOOGLE_CREDENTIALS_JSON")
sheet_id = os.getenv("SHEET_ID")

if os.path.exists(creds_path):
    gc = gspread.service_account(filename=creds_path)
else:
    creds_dict = json.loads(creds_path)
    gc = gspread.service_account_from_dict(creds_dict)

worksheet = gc.open_by_key(sheet_id).sheet1


def read_inventory():
    return worksheet.get_all_records()


def update_inventory_row(sku, updates: dict):
    records = worksheet.get_all_records()
    for i, row in enumerate(records, start=2):
        if row["item_sku"] == sku:
            for key, value in updates.items():
                if key not in row:
                    raise KeyError(f"Column {key} not found in sheet")
                col_index = list(row.keys()).index(key) + 1
                worksheet.update_cell(i, col_index, value)
            return True
    return False
