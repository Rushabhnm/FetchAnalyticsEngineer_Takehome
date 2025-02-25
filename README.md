# Fetch Take Home Test - Analytics Engineer

## Overview

This repository contains my completed assessment for the Fetch Rewards Data Engineering exercise. The goal was to review unstructured JSON data, create a structured relational data model, write SQL queries to answer business questions, evaluate data quality issues, and communicate findings effectively to stakeholders.

## Data Modeling

I have normalized the three unstructured JSON files (Receipts, Users, and Brands) and cleansed the data. The rewardsReceiptItemList column in the Receipts dataset contained a list of dictionaries describing purchased items, which I further normalized into a separate table. As a result, I have structured the data using a Snowflake Schema, ensuring efficiency and ease of querying.

The relational diagram depicting the structured data model has been included in this repository.

![Fetch Relational Diagram](RelationalDiagram.png)


## Project Structure
The repository is organized as follows:
- Relational Diagram: A diagram showcasing the structured relational model is included.
- scripts Folder:
  - FlatteningRawFile.ipynb: Contains Python code used for normalizing and structuring the raw JSON data.
  - StakeholderAnswers.ipynb: SQL queries that answer the stakeholder’s business questions.
  - DataQualityIssue.ipynb: Queries and analysis identifying data quality issues.
- StakeholderEmail.pdf: Contains message for a business leader, showcasing my data communication skills.
