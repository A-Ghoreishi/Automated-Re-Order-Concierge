import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.google_sheets import read_inventory, update_inventory_row
from datetime import datetime
print("Reading inventory...")
rows = read_inventory()
for r in rows:
    print(r)

print("Updateing SKU123...")
update_inventory_row("SKU123",{"last_checked": datetime.now().strftime("%Y-%m-%d")})
