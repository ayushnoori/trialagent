# Setup script for Hugging Face Hub with JFrog Artifactory (PowerShell)
# Run this script: . .\setup_hf.ps1 (note the dot-space before the path)

# Set Hugging Face Hub timeout configurations
$env:HF_HUB_ETAG_TIMEOUT = "86400"
$env:HF_HUB_DOWNLOAD_TIMEOUT = "86400"

# Set Hugging Face endpoint to JFrog Artifactory
$env:HF_ENDPOINT = "https://jfrog.apps.ocpdmzp.wclalit.org.il/artifactory/api/huggingfaceml/huggingface"

# Set Hugging Face token for authentication
$env:HF_TOKEN = "cmVmdGtu0jAx0jE3OTgwMTIxNDY6Q11zTXp4RHAYRXI2b3Z6bn1WMWRBSUthSnNp"

Write-Host "Hugging Face Hub configured for JFrog Artifactory"
Write-Host "HF_ENDPOINT: $env:HF_ENDPOINT"
Write-Host "HF_TOKEN: $($env:HF_TOKEN.Substring(0, 20))..."
Write-Host ""
Write-Host "NOTE: These variables are set for this PowerShell session only."
Write-Host "To verify, run: echo `$env:HF_ENDPOINT"
