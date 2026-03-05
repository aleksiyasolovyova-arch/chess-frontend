import base64
import time
from pathlib import Path

import streamlit as st
import requests
from PIL import Image

API_URL = "http://localhost:8000"
MAX_SIZE = 10 * 1024 * 1024  # 10 MB
ACCEPTED_TYPES = ["image/jpeg", "image/png", "image/webp", "application/pdf"]

ASSETS = Path(__file__).parent / "assets"

FONT_PATH = ASSETS / "fonts" / "conthrax" / "Conthrax-SemiBold.otf"
_font_b64 = base64.b64encode(FONT_PATH.read_bytes()).decode()

LOGO_PATH = ASSETS / "images" / "logo.png"
_logo_b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode()

LOGO_LETTERS_PATH = ASSETS / "images" / "logo_letters.png"
_logo_letters_b64 = base64.b64encode(LOGO_LETTERS_PATH.read_bytes()).decode()

LOGO_PIC_PATH = ASSETS / "images" / "logo_pic.png"
_logo_pic_b64 = base64.b64encode(LOGO_PIC_PATH.read_bytes()).decode()

LOGO_ROOK_PATH = ASSETS / "images" / "logo_rook.png"
_logo_rook_b64 = base64.b64encode(LOGO_ROOK_PATH.read_bytes()).decode()



_rook_icon = Image.open(LOGO_ROOK_PATH)
st.set_page_config(page_title="Chess Scoresheet", page_icon=_rook_icon, layout="wide")

# Load custom font and background image
st.markdown(
    f"""
    <style>
    @font-face {{
        font-family: 'Conthrax';
        src: url(data:font/otf;base64,{_font_b64}) format('opentype');
        font-weight: normal;
        font-style: normal;
    }}
    .stApp {{
        background:
          conic-gradient(from 90deg,
            #e8e4df 0 25%,
            #ddd9d3 0 50%,
            #e8e4df 0 75%,
            #ddd9d3 0
          ) 0 0 / 200px 200px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Custom CSS for chess theme
st.markdown(
    f"""
    <style>
    .stApp {{
        min-height: 100vh;
    }}
    /* Navbar */
    .navbar {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        display: flex;
        align-items: center;
        padding: 12px 24px;
        background: rgba(255, 255, 255, 0.65);
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }}
    .navbar-logo {{
        margin-left: 16px;
    }}
    /* Language picker - positioned in navbar */
    .st-key-lang_picker {{
        position: fixed !important;
        top: 75px;
        right: 150px;
        z-index: 1001;
        width: fit-content !important;
        pointer-events: none;
        background: none !important;
        border: none !important;
        padding: 0 !important;
    }}
    .st-key-lang_picker * {{
        pointer-events: auto;
    }}
    .st-key-lang_picker [data-testid="stVerticalBlockBorderWrapper"],
    .st-key-lang_picker [data-testid="stVerticalBlock"] {{
        width: fit-content !important;
    }}
    .st-key-lang_picker [data-testid="stSelectbox"] {{
        min-width: 130px;
    }}
    .st-key-lang_picker [data-testid="stWidgetLabel"] {{
        display: none !important;
    }}
    .navbar-center {{
        display: flex;
        align-items: center;
        gap: 12px;
        flex: 1;
    }}
    .navbar-text {{
        display: flex;
        flex-direction: column;
    }}
    .hero-subtitle {{
        font-family: 'Conthrax', 'Georgia', serif;
        font-size: 20px;
        font-weight: 700;
        color: #1a1a1a;
        letter-spacing: 1px;
        line-height: 1.2;
    }}
    .hero-sub {{
        color: #1a1a1a;
        font-size: 13px;
        letter-spacing: 0.5px;
        margin-top: 2px;
    }}
    /* Vertically center content below navbar */
    .block-container {{
        max-width: 100% !important;
        padding: 0 !important;
        padding-top: 40vh !important;
    }}

    /* Upload area wrapper */
    .upload-wrapper {{
        max-width: 480px;
        margin: 0 auto;
        text-align: center;
    }}
    .upload-hint {{
        color: #1a1a1a;
        font-size: 12px;
        letter-spacing: 0.5px;
        text-align: center;
        margin-top: 10px;
    }}

    /* Style the file uploader container */
    [data-testid="stFileUploader"] {{
        border: 2px dashed rgba(60, 60, 60, 0.35);
        border-radius: 16px;
        padding: 32px 24px;
        background: rgba(255, 255, 255, 0.65);
        transition: all 0.3s ease;
    }}
    [data-testid="stFileUploader"]:hover {{
        border-color: rgba(60, 60, 60, 0.6);
        background: rgba(255, 255, 255, 0.8);
    }}
    [data-testid="stFileUploaderDropzone"] {{
        background: transparent !important;
        text-align: center !important;
    }}
    [data-testid="stFileUploaderDropzone"] > div {{
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 12px;
    }}
    /* Hide default upload icon */
    [data-testid="stFileUploaderDropzone"] svg {{
        display: none !important;
    }}
    /* Style the browse button */
    [data-testid="stFileUploaderDropzone"] button {{
        background: #1a1a1a !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 28px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        cursor: pointer !important;
        transition: background 0.2s ease !important;
        order: 2 !important;
    }}
    [data-testid="stFileUploaderDropzone"] button:hover {{
        background: #333 !important;
    }}
    /* Hide all default text in dropzone, keep only button */
    [data-testid="stFileUploaderDropzone"] > div > * {{
        display: none !important;
    }}
    [data-testid="stFileUploaderDropzone"] > div > button {{
        display: inline-flex !important;
    }}
    /* Custom upload text above button */
    [data-testid="stFileUploaderDropzone"] > div::before {{
        content: 'Upload scoresheet image here';
        color: #1a1a1a;
        font-family: 'Conthrax', 'Georgia', serif;
        font-size: 14px;
        text-align: center;
        order: 1 !important;
    }}

    /* Results area */
    .results {{
        max-width: 600px;
        margin: 20px auto;
        padding: 20px;
        background: rgba(224, 122, 47, 0.06);
        border: 1px solid rgba(224, 122, 47, 0.2);
        border-radius: 12px;
    }}

    /* Footer */
    .custom-footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        text-align: center;
        padding: 10px;
        font-family: 'Conthrax', 'Georgia', serif;
        font-size: 11px;
        color: #1a1a1a;
        letter-spacing: 0.5px;
    }}

    /* Loading overlay */
    .loading-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.7);
        z-index: 2000;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 20px;
    }}
    .loading-text {{
        font-family: 'Conthrax', 'Georgia', serif;
        font-size: 16px;
        color: #1a1a1a;
        letter-spacing: 1px;
    }}
    .chess-loader {{
        display: flex;
        gap: 8px;
    }}
    .chess-loader span {{
        width: 16px;
        height: 16px;
        background: #1a1a1a;
        animation: bounce 1.4s ease-in-out infinite;
    }}
    .chess-loader span:nth-child(1) {{ animation-delay: 0s; }}
    .chess-loader span:nth-child(2) {{ animation-delay: 0.2s; }}
    .chess-loader span:nth-child(3) {{ animation-delay: 0.4s; }}
    .chess-loader span:nth-child(4) {{ animation-delay: 0.6s; }}
    @keyframes bounce {{
        0%, 80%, 100% {{ transform: scaleY(0.4); opacity: 0.3; }}
        40% {{ transform: scaleY(1); opacity: 1; }}
    }}

    /* Hide default Streamlit header/footer */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
    """,
    unsafe_allow_html=True,
)

LANG_OPTIONS = {"English": "en", "Nederlands": "nl", "Fran\u00e7ais": "fr"}

T = {
    "en": {
        "scoresheet_upload": "Scoresheet Upload",
        "upload_hint": "Upload scoresheet image here",
        "white": "White",
        "black": "Black",
        "elo": "Elo",
        "date": "Date",
        "tournament": "Tournament",
        "moves": "Moves",
        "moves_editing": "Moves *(editing)*",
        "done": "Done",
        "submit": "Submit",
        "close": "Close",
        "result_title": "Scoresheet Result",
        "status": "Status",
        "all_legal": "All moves are legal!",
        "some_illegal": "Some moves are illegal.",
        "saved": "Saved!",
        "save_failed": "Save failed",
        "validation_failed": "Validation failed",
        "file_too_large": "File too large. Maximum size is 10 MB.",
        "processing": "Processing scoresheet...",
        "upload_failed": "Upload failed",
        "no_backend": "Cannot connect to backend. Is FastAPI running on localhost:8000?",
    },
    "nl": {
        "scoresheet_upload": "Scoreblad Uploaden",
        "upload_hint": "Upload hier een scoreblad",
        "white": "Wit",
        "black": "Zwart",
        "elo": "Elo",
        "date": "Datum",
        "tournament": "Toernooi",
        "moves": "Zetten",
        "moves_editing": "Zetten *(bewerken)*",
        "done": "Klaar",
        "submit": "Verzenden",
        "close": "Sluiten",
        "result_title": "Scoreblad Resultaat",
        "status": "Status",
        "all_legal": "Alle zetten zijn geldig!",
        "some_illegal": "Sommige zetten zijn ongeldig.",
        "saved": "Opgeslagen!",
        "save_failed": "Opslaan mislukt",
        "validation_failed": "Validatie mislukt",
        "file_too_large": "Bestand te groot. Maximale grootte is 10 MB.",
        "processing": "Scoreblad verwerken...",
        "upload_failed": "Uploaden mislukt",
        "no_backend": "Kan geen verbinding maken met de backend. Draait FastAPI op localhost:8000?",
    },
    "fr": {
        "scoresheet_upload": "T\u00e9l\u00e9charger la feuille",
        "upload_hint": "T\u00e9l\u00e9chargez une feuille de match ici",
        "white": "Blancs",
        "black": "Noirs",
        "elo": "Elo",
        "date": "Date",
        "tournament": "Tournoi",
        "moves": "Coups",
        "moves_editing": "Coups *(\u00e9dition)*",
        "done": "Termin\u00e9",
        "submit": "Soumettre",
        "close": "Fermer",
        "result_title": "R\u00e9sultat de la feuille",
        "status": "Statut",
        "all_legal": "Tous les coups sont l\u00e9gaux !",
        "some_illegal": "Certains coups sont ill\u00e9gaux.",
        "saved": "Enregistr\u00e9 !",
        "save_failed": "\u00c9chec de l'enregistrement",
        "validation_failed": "\u00c9chec de la validation",
        "file_too_large": "Fichier trop volumineux. La taille maximale est de 10 Mo.",
        "processing": "Traitement de la feuille de match...",
        "upload_failed": "\u00c9chec du t\u00e9l\u00e9chargement",
        "no_backend": "Impossible de se connecter au backend. FastAPI tourne-t-il sur localhost:8000 ?",
    },
}

with st.container(key="lang_picker"):
    lang_label = st.selectbox("Language", options=list(LANG_OPTIONS.keys()), label_visibility="collapsed")
lang_code = LANG_OPTIONS[lang_label]
t = T[lang_code]

# Hero section (rendered after language is known for translated subtitle)
st.markdown(
    f"""
    <div class="navbar">
        <div class="navbar-center">
            <img src="data:image/png;base64,{_logo_rook_b64}" alt="Chesslooks Lier Rook" style="width:120px;height:auto;">
            <div class="navbar-text">
                <img src="data:image/png;base64,{_logo_letters_b64}" alt="Chesslooks Lier" style="width:200px;height:auto;margin-left:-10px;">
                <div class="hero-subtitle">{t["scoresheet_upload"]}</div>
            </div>
        </div>
        <div class="navbar-logo">
            <img src="data:image/png;base64,{_logo_pic_b64}" alt="Chesslooks Lier" style="width:100px;height:auto;">
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Override dropzone text with translated string
st.markdown(
    f"""<style>
    [data-testid="stFileUploaderDropzone"] > div::before {{
        content: '{t["upload_hint"]}' !important;
    }}
    </style>""",
    unsafe_allow_html=True,
)

# Clear cached validation results when language changes so reasons update
if lang_code != st.session_state.get("_last_val_lang"):
    st.session_state.validation_results = None
    st.session_state._last_val_lang = lang_code

# Upload area — centered using columns
_, col_center, _ = st.columns([1, 2, 1])
with col_center:
    uploaded_file = st.file_uploader(
        "Upload scoresheet",
        type=["jpg", "jpeg", "png", "webp", "pdf"],
        label_visibility="collapsed",
    )

@st.dialog(t["result_title"], width="large")
def show_result(data):
    if "validation_results" not in st.session_state:
        st.session_state.validation_results = None
    if "editing_moves" not in st.session_state:
        st.session_state.editing_moves = True

    col_w, col_we, col_b, col_be = st.columns([3, 1, 3, 1])
    with col_w:
        white = st.text_input(t["white"], value=data.get("white", ""))
    with col_we:
        white_elo = st.number_input(t["elo"], value=data.get("white_elo", 0), min_value=0, step=1, key="white_elo")
    with col_b:
        black = st.text_input(t["black"], value=data.get("black", ""))
    with col_be:
        black_elo = st.number_input(t["elo"], value=data.get("black_elo", 0), min_value=0, step=1, key="black_elo")

    col_d, col_t = st.columns(2)
    with col_d:
        date = st.text_input(t["date"], value=data.get("date", ""))
    with col_t:
        tournament = st.text_input(t["tournament"], value=data.get("tournament", ""))

    moves = data.get("moves", [])
    val_results = st.session_state.validation_results

    if st.session_state.editing_moves:
        # ── Edit mode: text inputs for each move ──
        hdr_left, hdr_right = st.columns([5, 1])
        with hdr_left:
            st.markdown(f'**{t["moves_editing"]}**')
        with hdr_right:
            if st.button(t["done"], key="done_editing", use_container_width=True):
                committed = []
                for i in range(0, len(moves), 2):
                    move_num = i // 2 + 1
                    committed.append(st.session_state.get(f"w_{move_num}", ""))
                    committed.append(st.session_state.get(f"b_{move_num}", ""))
                st.session_state.committed_moves = committed
                st.session_state.editing_moves = False
                st.rerun()

        edited_moves = []
        for i in range(0, len(moves), 2):
            move_num = i // 2 + 1
            c1, c2, c3 = st.columns([0.5, 2, 2])
            with c1:
                st.markdown(f"**{move_num}.**")
            with c2:
                # Extract san_intent from MoveDTO dict
                w_move_dict = moves[i] if i < len(moves) else {}
                w_move_str = w_move_dict.get("san_intent", "") if isinstance(w_move_dict, dict) else str(w_move_dict)
                w_move = st.text_input(
                    f"W{move_num}", value=w_move_str,
                    label_visibility="collapsed", key=f"w_{move_num}",
                )
                edited_moves.append(w_move)
            with c3:
                b_move_dict = moves[i + 1] if i + 1 < len(moves) else {}
                b_move_str = b_move_dict.get("san_intent", "") if isinstance(b_move_dict, dict) else str(b_move_dict)
                b_move = st.text_input(
                    f"B{move_num}", value=b_move_str,
                    label_visibility="collapsed", key=f"b_{move_num}",
                )
                edited_moves.append(b_move)

    else:
        # ── Table mode: read-only moves with validation status ──
        hdr_left, hdr_right = st.columns([5, 1])
        with hdr_left:
            st.markdown(f'**{t["moves"]}**')
        with hdr_right:
            if st.button(":material/edit:", key="edit_moves", use_container_width=True):
                st.session_state.editing_moves = True
                st.rerun()

        # Build the table
        header = f'| # | {t["white"]} | {t["black"]} |'
        separator = "|---|-------|-------|"
        if val_results:
            header = f'| # | {t["white"]} | {t["status"]} | {t["black"]} | {t["status"]} |'
            separator = "|---|-------|--------|-------|--------|"

        rows = ""
        for i in range(0, len(moves), 2):
            move_num = i // 2 + 1
            w = moves[i].get("san_intent", "") if i < len(moves) and isinstance(moves[i], dict) else ""
            b = moves[i + 1].get("san_intent", "") if i + 1 < len(moves) and isinstance(moves[i + 1], dict) else ""
            if val_results:
                w_res = val_results[i] if i < len(val_results) else None
                b_res = val_results[i + 1] if i + 1 < len(val_results) else None
                w_status = ""
                b_status = ""
                if w_res:
                    if w_res["legal"]:
                        w_status = "OK"
                    else:
                        w_status = f'ILLEGAL – {w_res.get("reason", "")}'
                        if w_res.get("suggestion"):
                            w_status += f' (suggestion: {w_res["suggestion"]})'
                if b_res:
                    if b_res["legal"]:
                        b_status = "OK"
                    else:
                        b_status = f'ILLEGAL – {b_res.get("reason", "")}'
                        if b_res.get("suggestion"):
                            b_status += f' (suggestion: {b_res["suggestion"]})'
                rows += f"| {move_num} | {w} | {w_status} | {b} | {b_status} |\n"
            else:
                rows += f"| {move_num} | {w} | {b} |\n"

        st.markdown(f"{header}\n{separator}\n{rows}")

        if val_results and any(not r["legal"] for r in val_results):
            st.error(t["some_illegal"])

    # ── Action buttons ──
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t["submit"], use_container_width=True):
            if st.session_state.editing_moves:
                source_moves = edited_moves
            else:
                source_moves = st.session_state.get("committed_moves", [
                    m.get("san_intent", "") if isinstance(m, dict) else str(m)
                    for m in moves
                ])
            clean_moves = [m for m in source_moves if m.strip()]
            # Switch to table view to show results
            st.session_state.editing_moves = False

            try:
                val_resp = requests.post(
                    f"{API_URL}/api/validate",
                    json={"moves": clean_moves, "lang": lang_code},
                    timeout=30,
                )
            except requests.RequestException as e:
                st.error(f'{t["validation_failed"]}: {e}')
                val_resp = None

            if val_resp is not None:
                if not val_resp.ok:
                    st.error(f'{t["validation_failed"]} ({val_resp.status_code})')
                else:
                    val_data = val_resp.json()
                    if val_data["legal"]:
                        st.session_state.validation_results = None
                        st.success(t["all_legal"])
                        try:
                            resp = requests.put(
                                f"{API_URL}/api/scoresheets/{data['filename']}",
                                json={
                                    "white": white,
                                    "white_elo": white_elo,
                                    "black": black,
                                    "black_elo": black_elo,
                                    "date": date,
                                    "tournament": tournament,
                                    "moves": clean_moves,
                                },
                                timeout=30,
                            )
                            if resp.ok:
                                st.success(t["saved"])
                            else:
                                st.error(f'{t["save_failed"]} ({resp.status_code})')
                        except requests.RequestException as e:
                            st.error(f'{t["save_failed"]}: {e}')
                    else:
                        st.session_state.validation_results = val_data["moves"]
                        st.rerun()
    with col2:
        if st.button(t["close"], use_container_width=True):
            st.session_state.validation_results = None
            st.session_state.editing_moves = False
            st.rerun()


# Handle upload
if uploaded_file is not None:
    if uploaded_file.size > MAX_SIZE:
        st.error(t["file_too_large"])
    else:
        loading = st.empty()
        loading.markdown(
            f"""<div class="loading-overlay">
                <div class="chess-loader">
                    <span></span><span></span><span></span><span></span>
                </div>
                <div class="loading-text">{t["processing"]}</div>
            </div>""",
            unsafe_allow_html=True,
        )
        time.sleep(2)
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            response = requests.post(f"{API_URL}/api/scoresheets", files=files, timeout=30)
            loading.empty()
            if response.ok:
                data = response.json()
                # Reset state only for a genuinely new upload
                if st.session_state.get("_last_upload_id") != uploaded_file.file_id:
                    st.session_state._last_upload_id = uploaded_file.file_id
                    st.session_state.editing_moves = True
                    st.session_state.validation_results = None
                show_result(data)
            else:
                st.error(f'{t["upload_failed"]} ({response.status_code})')
        except requests.ConnectionError:
            loading.empty()
            st.error(t["no_backend"])
        except requests.RequestException as e:
            loading.empty()
            st.error(f'{t["upload_failed"]}: {e}')

# Footer
st.markdown('<div class="custom-footer">&copy; FAE 2026</div>', unsafe_allow_html=True)
