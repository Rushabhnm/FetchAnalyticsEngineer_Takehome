import pandas as pd
import json

# Read JSON file (assuming it's line-delimited JSON)
brands_file_path = "/Users/rushabhnm/Fetch_TakeHome/raw_files/brands.json"

# Load the JSON data
with open(brands_file_path, "r") as file:
    brands_data = [json.loads(row) for row in file]


brands_cleansed_data = []

for entry in brands_data:
    brands_cleaned_entry = {
        "brandID": entry.get("_id", {}).get("$oid", None),  
        "brandName": entry.get("name", None),   
        "barcode": str(entry.get("barcode", None)),  
        "brandCode": str(entry.get("brandCode",None)),  
        "category": entry.get("category", None),  
        "categoryCode": entry.get("categoryCode", None),  
        "cpgID": entry.get("cpg", {}).get("$id", {}).get("$oid", None),  
        "cpgRef": entry.get("cpg", {}).get("$ref", None),  
        "topBrand": entry.get("topBrand", None)
        }

    brands_cleansed_data.append(brands_cleaned_entry)

brands_df = pd.DataFrame(brands_cleansed_data)

#reordering the columns
brands_df = brands_df.reindex(columns=["brandID","barcode", "brandName", "brandCode", "category", "categoryCode", "cpgID", "cpgRef","topBrand"])

brands_df.drop_duplicates()

brands_df.to_csv("/Users/rushabhnm/Fetch_TakeHome/cleansed_file/brands_cleansed_data.csv", index=False)
