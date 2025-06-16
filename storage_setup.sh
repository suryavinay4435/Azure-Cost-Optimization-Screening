#!/bin/bash

# Variables
RESOURCE_GROUP="myrg"
STORAGE_ACCOUNT="mybillingstorage"
CONTAINER_NAME="billing-archive"
LOCATION="eastus"

# Create resource group (if not exists)
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create storage account
az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Standard_LRS

# Get storage account key
STORAGE_KEY=$(az storage account keys list --account-name $STORAGE_ACCOUNT --resource-group $RESOURCE_GROUP --query [0].value -o tsv)

# Create container
az storage container create \
  --name $CONTAINER_NAME \
  --account-name $STORAGE_ACCOUNT \
  --account-key $STORAGE_KEY \
  --public-access off

echo "Blob storage setup complete: $STORAGE_ACCOUNT / $CONTAINER_NAME"
