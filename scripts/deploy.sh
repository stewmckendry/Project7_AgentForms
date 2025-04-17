#!/bin/bash

set -e

RESOURCE_GROUP="baseball-tutor-rg"  # Reused from last project
PLAN_NAME="aiapps-plan"
APP_NAME="concussion-agent-app"  # New app name for Concussion Assistant
ACR_NAME="agentformsacr"  # Optional: new ACR name
IMAGE_NAME="concussion-agent"  # Updated image name

echo "🔄 Updating container image for Azure App Service..."
az webapp config container set --name $APP_NAME   --resource-group $RESOURCE_GROUP   --docker-custom-image-name $ACR_NAME.azurecr.io/$IMAGE_NAME:latest   --docker-registry-server-url https://$ACR_NAME.azurecr.io

echo "🚀 Restarting app..."
az webapp restart --name $APP_NAME --resource-group $RESOURCE_GROUP

echo "🩺 Checking app status..."
az webapp show --name $APP_NAME --resource-group $RESOURCE_GROUP   --query "state" --output tsv

echo "🧪 Open Azure debug console if needed:"
echo "🔗 https://portal.azure.com/#resource/subscriptions/<subscription-id>/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Web/sites/$APP_NAME/advancedTools"