#!/bin/bash

set -e

# Config
IMAGE_NAME="concussion-agent"
ACR_NAME="agentformsacr"
TAG="latest"

echo "🔄 Building image..."
docker build -t $IMAGE_NAME .

echo "🔐 Logging in to Azure Container Registry..."
az acr login --name $ACR_NAME

echo "🚚 Tagging image..."
docker tag $IMAGE_NAME $ACR_NAME.azurecr.io/$IMAGE_NAME:$TAG

echo "📤 Pushing to ACR..."
docker push $ACR_NAME.azurecr.io/$IMAGE_NAME:$TAG

echo "✅ Done!"