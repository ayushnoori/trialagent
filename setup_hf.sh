#!/bin/bash
# Setup script for Hugging Face Hub with JFrog Artifactory (Unix/Linux/macOS)
# Run this script: source setup_hf.sh

# Set Hugging Face Hub timeout configurations
export HF_HUB_ETAG_TIMEOUT=86400
export HF_HUB_DOWNLOAD_TIMEOUT=86400

# Set Hugging Face endpoint to JFrog Artifactory
export HF_ENDPOINT=https://jfrog.apps.ocpdmzp.wclalit.org.il/artifactory/api/huggingfaceml/huggingface

# Set Hugging Face token for authentication
export HF_TOKEN=cmVmdGtu0jAx0jE3OTgwMTIxNDY6Q11zTXp4RHAYRXI2b3Z6bn1WMWRBSUthSnNp

echo "Hugging Face Hub configured for JFrog Artifactory"
echo "HF_ENDPOINT: $HF_ENDPOINT"
echo "HF_TOKEN: ${HF_TOKEN:0:20}..."
