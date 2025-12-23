@echo off
REM Helper script to run commands with HuggingFace environment variables using uv
REM Usage: run_with_hf.bat test-supervisor
REM Or: run_with_hf.bat python -m trialagent.scripts.test_supervisor

REM Check if .env file exists
if not exist .env (
    echo Creating .env file from template...
    (
        echo HF_HUB_ETAG_TIMEOUT=86400
        echo HF_HUB_DOWNLOAD_TIMEOUT=86400
        echo HF_ENDPOINT=https://jfrog.apps.ocpdmzp.wclalit.org.il/artifactory/api/huggingfaceml/huggingface
        echo HF_TOKEN=cmVmdGtu0jAx0jE3OTgwMTIxNDY6Q11zTXp4RHAYRXI2b3Z6bn1WMWRBSUthSnNp
    ) > .env
    echo .env file created. You can edit it if needed.
)

REM Run the command with uv using the .env file
uv run --env-file .env %*
