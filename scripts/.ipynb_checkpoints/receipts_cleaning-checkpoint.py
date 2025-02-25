import pandas as pd
import json

# Load JSON file
receipts_file_path = "/Users/rushabhnm/Fetch_TakeHome/raw_files/receipts.json"

with open(receipts_file_path, "r") as file:
    receipts_data = [json.loads(row) for row in file]

# Extract and flatten the Receipt Table
receipts_cleansed_data = []
items_cleansed_data = []

# Step 1: Find all unique keys in rewardsReceiptItemList
all_item_keys = set()

for entry in receipts_data:
    if "rewardsReceiptItemList" in entry:
        for item in entry["rewardsReceiptItemList"]:
            all_item_keys.update(item.keys())  # Collect all unique keys

# Step 2: Extract data while ensuring all keys are present
for entry in receipts_data:
    receipt_id = entry["_id"]["$oid"]

    # Flattening receipt-level data
    receipt_cleaned_entry = {
        "receiptID": receipt_id,
        "bonusPointsEarned": entry.get("bonusPointsEarned", None),
        "bonusPointsEarnedReason": entry.get("bonusPointsEarnedReason", None),
        "createDate": pd.to_datetime(entry["createDate"]["$date"], unit='ms') if "createDate" in entry else None,
        "dateScanned": pd.to_datetime(entry["dateScanned"]["$date"], unit='ms') if "dateScanned" in entry else None,
        "finishedDate": pd.to_datetime(entry["finishedDate"]["$date"], unit='ms') if "finishedDate" in entry else None,
        "modifyDate": pd.to_datetime(entry["modifyDate"]["$date"], unit='ms') if "modifyDate" in entry else None,
        "pointsAwardedDate": pd.to_datetime(entry["pointsAwardedDate"]["$date"], unit='ms') if "pointsAwardedDate" in entry else None,
        "pointsEarned": entry.get("pointsEarned", None),
        "purchaseDate": pd.to_datetime(entry["purchaseDate"]["$date"], unit='ms') if "purchaseDate" in entry else None,
        "purchasedItemCount": entry.get("purchasedItemCount", None),
        "rewardsReceiptStatus": entry.get("rewardsReceiptStatus", None),
        "totalSpent": entry.get("totalSpent", None),
        "userID": entry.get("userId", None),
    }
    receipts_cleansed_data.append(receipt_cleaned_entry)

    # Flattening item-level data
    if "rewardsReceiptItemList" in entry:
        for item in entry["rewardsReceiptItemList"]:
            item_cleaned_entry = {"receiptID": receipt_id}  # Link item to receipt
            for key in all_item_keys:
                item_cleaned_entry[key] = item.get(key, None)  # Fill missing keys with None
            items_cleansed_data.append(item_cleaned_entry)

# Convert to DataFrames
receipts_df = pd.DataFrame(receipts_cleansed_data)
items_df = pd.DataFrame(items_cleansed_data)
# items_df.drop(columns=)

# Optional: Export to CSV for further analysis
receipts_df.to_csv("/Users/rushabhnm/Fetch_TakeHome/cleansed_file/cleansed_receipts.csv", index=False)
items_df.to_csv("/Users/rushabhnm/Fetch_TakeHome/cleansed_file/cleansed_receipt_items.csv", index=False)
