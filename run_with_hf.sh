#!/bin/bash
# Helper script to run commands with HuggingFace environment variables using uv
# Usage: ./run_with_hf.sh test-supervisor
# Or: ./run_with_hf.sh python -m trialagent.scripts.test_supervisor

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cat > .env << EOF
HF_HUB_ETAG_TIMEOUT=86400
HF_HUB_DOWNLOAD_TIMEOUT=86400
HF_ENDPOINT=https://jfrog.apps.ocpdmzp.wclalit.org.il/artifactory/api/huggingfaceml/huggingface
HF_TOKEN=cmVmdGtu0jAx0jE3OTgwMTIxNDY6Q11zTXp4RHAYRXI2b3Z6bn1WMWRBSUthSnNp
EOF
    echo ".env file created. You can edit it if needed."
fi

# Run the command with uv using the .env file
uv run --env-file .env "$@"
