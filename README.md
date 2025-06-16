Azure Billing Records Cost Optimization
This project provides a cost-optimized solution for managing large volumes of billing records in a serverless Azure architecture. It offloads cold data from Azure Cosmos DB to Azure Blob Storage without affecting API contracts or requiring downtime.

Problem Statement
Cosmos DB stores over 2 million billing records (~300KB each).
Records older than 3 months are rarely accessed.
High storage and RU costs in Cosmos DB.

Objectives
Reduce Azure Cosmos DB costs
Maintain API compatibility (no changes)
Ensure no data loss
Preserve low-latency access to old data (seconds)
Avoid service downtime
Keep solution simple and maintainable

Architecture Overview
Client/API Calls
     |
     v
Azure Functions (Read/Write APIs)
     |
     |---> Write -> Cosmos DB
     |
     |---> Read -> Cosmos DB
             |
             |--(if not found)--> Azure Blob (Cold Storage)

Scheduled Archival Function
     |
     v
Query Cosmos DB -> Move old data to Blob -> Delete from Cosmos DB

Implementation Overview
1. Blob Storage Setup
az storage account create --name mybillingstorage --resource-group myrg --location eastus --sku Standard_LRS
az storage container create --account-name mybillingstorage --name billing-archive --public-access off

2. Archival Function (Pseudocode)
Moves records older than 90 days to Blob and deletes from Cosmos DB.

3. Read Function
Attempts to read from Cosmos DB, falls back to Blob if not found.

4. Scheduler
Azure Timer Trigger (daily at midnight) runs the archival function.

Benefits
Major cost savings by offloading infrequently accessed data
Transparent to consumers (no API changes)
High availability and low-latency for all records
Fully serverless and scalable

Enhancements
Use Durable Functions for more robust archiving
Cache frequent cold reads using Azure CDN or Redis
Add data lifecycle policies and blob tiering (Cool → Archive)

Requirements
Azure Subscription
Azure CLI
Python 3.8+
Azure Functions Core Tools
