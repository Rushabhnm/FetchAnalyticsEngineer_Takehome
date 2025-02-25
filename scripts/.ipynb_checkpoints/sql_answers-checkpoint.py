import pandas as pd
import sqlite3

conn = sqlite3.connect(':memory:') 

users = pd.read_csv("cleansed_file/users_cleansed_data.csv")
brands = pd.read_csv("cleansed_file/brands_cleansed_data.csv")
receipts = pd.read_csv("cleansed_file/cleansed_receipts.csv")
receipts_items = pd.read_csv("cleansed_file/cleansed_receipt_items.csv")

users.to_sql('users', conn, index=False, if_exists='replace')
brands.to_sql('brands', conn, index=False, if_exists='replace')
receipts.to_sql('receipts', conn, index=False, if_exists='replace')
receipts_items.to_sql('receipts_items', conn, index=False, if_exists='replace')


# Q1. When considering average spend from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?

q1_avgSpend = """with cte as(select 
                avg(case when rewardsReceiptStatus = 'FINISHED' or rewardsReceiptStatus = 'ACCEPTED' then totalSpent end) Accepted_avgTotalSpend,
                avg(case when rewardsReceiptStatus = 'REJECTED' then totalSpent end) Rejected_avgTotalSpend
                from receipts)
                select 
                case 
                    when Accepted_avgTotalSpend>Rejected_avgTotalSpend then 'Accepted' 
                    else 'Rejected'
                end  Q1_ans
                from cte;"""

q1_avgSpend_df = pd.read_sql(q1_avgSpend, conn)
print(q1_avgSpend_df)


# Q2. When considering total number of items purchased from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?

q2_sumCount = """with cte as(select 
                sum(case 
                        when rewardsReceiptStatus = 'FINISHED' or rewardsReceiptStatus = 'ACCEPTED'
                        then purchasedItemCount 
                    end) Accepted_sumTotalCount,
                sum(case 
                        when rewardsReceiptStatus = 'REJECTED' 
                        then purchasedItemCount 
                    end) Rejected_sumTotalCount
                from receipts)
                select 
                case 
                    when Accepted_sumTotalCount>Rejected_sumTotalCount 
                    then 'Accepted' 
                    else 'Rejected'
                end Q2_ans
                from cte;"""

q2_sumCount_df = pd.read_sql(q2_sumCount, conn)
print(q2_sumCount_df)


# Q3 What are the top 5 brands by receipts scanned for most recent month?

q3_mostspend = """ 
                 with cte as(select b.receiptID
                  from users a
                  join receipts b
                  on a.userID = b.userID
                  where strftime('%Y-%m', a.createdDate) = 
                  (SELECT strftime('%Y-%m', max(createdDate)) FROM users))
                
                 select brandCode, count(brandCode) total_count
                 from receipts_items 
                 where receiptID in (select receiptID from cte)
                 group by brandCode
                 order by total_count desc  
                """
  


# 
q3_mostspend_df = pd.read_sql(q3_mostspend, conn)

print(q3_mostspend_df.to_string(index=False))
# q3_mostspend_df.to_csv("Q3/q3_barcode2.csv",index=False)