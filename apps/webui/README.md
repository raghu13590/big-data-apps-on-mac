
# Docker UI Manager (Python/Streamlit)

This web app provides a UI to manage Docker containers for services in the `apps/` folder using Makefile targets. Now uses Streamlit for the frontend.

## Features
- Lists all service folders with Makefiles
- Parses Makefile targets (e.g., up, down, build)
- Allows running targets from the UI
- Shows output/status in dialogs
- Manage Docker containers (start/stop/restart)

## Usage

### Build Docker Image
```
make build
```

### Run Web UI Container
```
make run
```

The app will be available at http://localhost:8501

## Requirements
- Docker
- Python 3.11 (for local dev)

## Development
Install dependencies:
```
pip install -r requirements.txt
```
Run locally:
```
streamlit run main.py
```
