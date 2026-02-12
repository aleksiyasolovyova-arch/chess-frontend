# Chess Scoresheet Frontend

Streamlit web app for uploading and managing chess scoresheets. Part of the Chesslooks Lier project.

## Overview

Users upload a photo or scan of a handwritten chess scoresheet. The app sends it to a FastAPI backend for OCR, then presents the extracted data in an editable dialog where moves can be reviewed, corrected, and validated for legality before saving.

## Features

- **Scoresheet upload** — Drag-and-drop or browse for images (JPG, PNG, WebP) and PDFs up to 10 MB
- **Move editing** — Extracted moves are shown in editable text inputs; switch between edit mode and a read-only table view
- **Move validation** — Submitting calls the backend validation endpoint; illegal moves are flagged with status and reason in the results table
- **Multi-language UI** — All interface text is available in English, Nederlands, and Fran&ccedil;ais via a language picker; validation reasons from the backend also respect the selected language
- **Custom theme** — Chess-themed design with Conthrax font, chessboard-pattern background, and branded navbar

## Prerequisites

- Python 3.10+
- The FastAPI backend running on `http://localhost:8000` (provides `/api/scoresheets`, `/api/validate`, and `/api/scoresheets/{filename}` endpoints)

## Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` by default.

## Project Structure

```
chess-frontend/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── config.toml                 # Streamlit theme configuration
└── assets/
    ├── fonts/
    │   └── conthrax/               # Custom font files
    └── images/
        ├── logo.png                # Full logo
        ├── logo_letters.png        # Text-only logo
        ├── logo_pic.png            # Logo mark
        ├── logo_rook.png           # Rook icon (favicon)
        └── background.jpg          # Background image
```

## API Endpoints Used

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/scoresheets` | Upload a scoresheet image for OCR processing |
| POST | `/api/validate` | Validate a list of moves for legality (accepts `moves` and `lang`) |
| PUT | `/api/scoresheets/{filename}` | Save corrected scoresheet data |

## Configuration

- **Backend URL** — Set `API_URL` in `app.py` (defaults to `http://localhost:8000`)
- **Max upload size** — Set `MAX_SIZE` in `app.py` (defaults to 10 MB)
- **Theme** — Edit `.streamlit/config.toml` to change the Streamlit color theme

## Adding a Language

1. Add the language to `LANG_OPTIONS` in `app.py` (display name to ISO code mapping)
2. Add a new entry in the `T` dictionary with all required translation keys
3. Ensure the backend `/api/validate` endpoint supports the new language code for localized reason strings
