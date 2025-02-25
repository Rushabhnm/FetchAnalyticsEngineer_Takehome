import pandas as pd
import json

# Read JSON file (assuming it's line-delimited JSON)
users_file_path = "/Users/rushabhnm/Fetch_TakeHome/raw_files/users.json"

# Load the JSON data
with open(users_file_path, "r") as file:
    users_data = [json.loads(row) for row in file]

# Extract and flatten the JSON data while handling missing keys
users_cleansed_data = []
for entry in users_data:
    users_cleaned_entry = {
        "userID": entry["_id"]["$oid"], 
        "signUpSource": entry.get("signUpSource", None),
        "state": entry.get("state", None),
        "active": entry.get("active", None),
        "role": entry.get("role", None),
        "createdDate": pd.to_datetime(entry["createdDate"]["$date"], unit='ms').date() if "createdDate" in entry else None,
        "lastLogin": pd.to_datetime(entry["lastLogin"]["$date"], unit='ms').date() if "lastLogin" in entry else None
    }
    users_cleansed_data.append(users_cleaned_entry)

# Convert to DataFrame
users_df = pd.DataFrame(users_cleansed_data)

# converting into proper format
# users_df["createdDate"] = users_df["createdDate"].dt.strftime("%Y-%m-%d %H:%M:%S")
# users_df["lastLogin"] = users_df["lastLogin"].dt.strftime("%Y-%m-%d %H:%M:%S")

# dropping the duplicate values
users_df = users_df.drop_duplicates()

#reordering the columns
users_df = users_df.reindex(columns=["userID", "signUpSource", "state", "active", "role", "createdDate", "lastLogin"])

# Save the file as csv
users_df.to_csv("/Users/rushabhnm/Fetch_TakeHome/cleansed_file/users_cleansed_data.csv", index=False)
