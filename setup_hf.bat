@echo off
REM Setup script for Hugging Face Hub with JFrog Artifactory (Windows Batch)
REM IMPORTANT: Run this script using: call setup_hf.bat
REM Or run the commands directly in your current shell before running Python scripts

REM Set Hugging Face Hub timeout configurations
set HF_HUB_ETAG_TIMEOUT=86400
set HF_HUB_DOWNLOAD_TIMEOUT=86400

REM Set Hugging Face endpoint to JFrog Artifactory
set HF_ENDPOINT=https://jfrog.apps.ocpdmzp.wclalit.org.il/artifactory/api/huggingfaceml/huggingface

REM Set Hugging Face token for authentication
set HF_TOKEN=cmVmdGtu0jAx0jE3OTgwMTIxNDY6Q11zTXp4RHAYRXI2b3Z6bn1WMWRBSUthSnNp

echo Hugging Face Hub configured for JFrog Artifactory
echo HF_ENDPOINT: %HF_ENDPOINT%
echo HF_TOKEN: %HF_TOKEN:~0,20%...
echo.
echo NOTE: These variables are set for this shell session only.
echo To verify, run: echo %HF_ENDPOINT%
