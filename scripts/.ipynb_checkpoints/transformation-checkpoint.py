import pandas as pd
import duckdb

users = pd.read_csv("cleansed_file/users_cleansed_data.csv")
brands = pd.read_csv("cleansed_file/brands_cleansed_data.csv")
receipts = pd.read_csv("cleansed_file/cleansed_receipts.csv")
receipts_items = pd.read_csv("cleansed_file/cleansed_receipt_items.csv")



distinct_brands = """ 
    select brand_id, barcode, brandCode from brands where brandcode in(
    select  brandcode from brands
    group by brandcode
    having count(brandcode)>1)
    order by brandcode;
"""



# distinct_brands_df = duckdb.query(distinct_brands).to_df()
# print(distinct_brands_df)


# distinct_brandcode_df = duckdb.query(distinct_brandcode).to_df()
# print(distinct_brandcode_df)

#Q1

# topbrands_scanned = """
#     WITH recent_month AS (
#     SELECT strftime('%Y-%m', MAX(CAST(dateScanned AS DATE))) AS most_recent_month
#     FROM receipts
#     )
#     SELECT a.brandcode, COUNT(DISTINCT a.receipt_id)
#     FROM receipts_items a
#     JOIN receipts b 
#     ON a.receipt_id = b.receipt_id
#     JOIN recent_month rm ON strftime('%Y-%m', CAST(a.dateScanned AS DATE)) = rm.most_recent_month
#     GROUP BY a.brandcode
#     ORDER BY COUNT(DISTINCT a.receipt_id) DESC;

# """


# topbrands_scanned_df = duckdb.query(topbrands_scanned).to_df()
# print(topbrands_scanned_df)

barcode = """
    SELECT a.receipt_id, a.brandcode ,a.barcode, b.barcode
    FROM receipts_items a
    JOIN brands b ON a.barcode = b.barcode
    WHERE a.barcode ~ '^\d+$'
    order by receipt_id
"""
brandcode = """
    SELECT a.receipt_id, a.brandcode ,a.barcode, b.barcode
    FROM receipts_items a
    JOIN brands b ON a.brandcode = b.brandcode
    order by receipt_id
"""

barcode_df = duckdb.query(barcode).to_df()
brandcode_df = duckdb.query(brandcode).to_df()                  # gives more records

#####################################################################################################################################################################


##### BRANDS TRANSFORMATION #####

brands_unique_brandcode = """select distinct brandCode Brands_UbrandCode from brands"""
brands_unique_brandcode_df = duckdb.query(brands_unique_brandcode).to_df()

count_brands_brandcode = """select count(brandCode) Brands_CbrandCode from brands"""
count_brands_brandcode_df = duckdb.query(count_brands_brandcode).to_df()

repeating_brandcode = """select brandCode, count(brandCode) from brands group by brandCode having  count(brandCode)>1 """
count_brands_repeating_brandcode_df = duckdb.query(repeating_brandcode).to_df()


distinct_cpgID= """select cpgID, count(cpgID) from brands group by cpgID having  count(cpgID)>1 """
distinct_cpgID_df = duckdb.query(distinct_cpgID).to_df()



# print(brands_unique_brandcode_df)
brands_unique_brandcode_df["Brands_UbrandCode"] = brands_unique_brandcode_df["Brands_UbrandCode"].astype(str)
brands_unique_brandcode_df.to_csv("brands_unique_brandcode_df.csv",index=False)
print(count_brands_brandcode_df)
print(count_brands_repeating_brandcode_df)

print(distinct_cpgID_df)

#####################################################################################################################################################################

#### RECEIPTS TABLE #####

# r_receipt_count = """ select count(receipt_id) total_receipt_count from receipts;"""
# r_receipt_count_df = duckdb.query(r_receipt_count).to_df()
# print(r_receipt_count_df)

# #### RECEIPTS ITEMS TABLE #####
# ri_receipt_count = """ select count(receipt_id) total_receipt_count from receipts_items;"""
# ri_receipt_count_df = duckdb.query(ri_receipt_count).to_df()
# print(ri_receipt_count_df)

# ri_unique_brandcode = """select distinct brandCode RI_UbrandCode from receipts_items"""
# ri_unique_brandcode_df = duckdb.query(ri_unique_brandcode).to_df()

# ri_count_brandcode = """select count(brandCode) RI_CbrandCode from receipts_items"""
# ri_count_brandcode_df = duckdb.query(ri_count_brandcode).to_df()

# ri_unique_brandcode_df.to_csv("ri_unique_brandcode.csv",index=False)

# print(ri_unique_brandcode_df)
# print(ri_count_brandcode_df)