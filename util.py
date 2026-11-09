import streamlit as st
import requests
from bs4 import BeautifulSoup
from docx import Document
import re
import string
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import joblib


# ── Global CSS ────────────────────────────────────────────────────────────────
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: #0d0f14 !important;
    color: #e8eaf0 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stSidebar"] {
    background: #111318 !important;
    border-right: 1px solid #1e2232 !important;
}
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li { color: #b0b8cc !important; }
[data-testid="stSidebarNav"] a { border-radius: 8px !important; }
[data-testid="stHeader"] { background: transparent !important; }
section[data-testid="stMain"] { padding-top: 0.5rem !important; }

/* ── Buttons ── */
.stButton > button {
    background: #1a1d2a !important;
    color: #9aa3b8 !important;
    border: 1.5px solid #252838 !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 0.8px !important;
    padding: 0.55rem 1rem !important;
    transition: all 0.22s ease !important;
}
.stButton > button:hover {
    background: #5b7ef0 !important;
    color: #fff !important;
    border-color: #5b7ef0 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(91,126,240,0.38) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Inputs ── */
.stTextArea textarea, .stTextInput input {
    background: #111318 !important;
    color: #e8eaf0 !important;
    border: 1.5px solid #252838 !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #5b7ef0 !important;
    box-shadow: 0 0 0 3px rgba(91,126,240,0.15) !important;
}
.stTextArea label, .stTextInput label { display: none !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #111318 !important;
    border: 1.5px dashed #252838 !important;
    border-radius: 12px !important;
}

/* ── Misc ── */
#MainMenu, footer, [data-testid="stDecoration"] { visibility: hidden; }
hr { border-color: #1e2232 !important; margin: 1.5rem 0 !important; }
</style>
"""


def inject_global_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def set_background_color(hex_color=None):
    """Legacy shim — injects full global CSS."""
    inject_global_css()


# ── URL scraper ───────────────────────────────────────────────────────────────
def get_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        text = "\n".join([p.get_text() for p in soup.find_all('p')])
        return text
    except requests.exceptions.RequestException:
        return "Link tidak dapat diakses. Pastikan URL valid dan dapat dijangkau."
    except Exception:
        return "Akses ke URL ditolak atau terjadi kesalahan lainnya."


# ── File reader ───────────────────────────────────────────────────────────────
def read_uploaded_file(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    return "Format file tidak didukung."


# ── NLP pipeline ──────────────────────────────────────────────────────────────
stop_factory = StopWordRemoverFactory()
stopwords    = stop_factory.get_stop_words()
stem_factory = StemmerFactory()
stemmer      = stem_factory.create_stemmer()


def preprocess(text):
    text = str(text).lower()
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    text = re.sub(r'#\w+', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    tokens = [w for w in text.split() if w not in stopwords]
    return stemmer.stem(' '.join(tokens))


model = joblib.load('model.pkl')
tfidf = joblib.load('tfidf.pkl')
with open("labels.txt", "r") as f:
    class_names = [line.strip().split('=')[1].strip() for line in f]


def classify(text):
    clean = preprocess(text)
    weight = tfidf.transform([clean])
    return model.predict_proba(weight)


# ── Animated SVG ring helper ──────────────────────────────────────────────────
def _ring_svg(label, pct, color):
    R    = 52
    cx   = cy = 68
    sw   = 11
    circ = 2 * 3.14159265 * R
    dash = pct / 100 * circ
    return f"""
    <div style="display:flex;flex-direction:column;align-items:center;gap:8px;">
      <svg width="136" height="136" viewBox="0 0 136 136">
        <circle cx="{cx}" cy="{cy}" r="{R}"
          fill="none" stroke="#1e2232" stroke-width="{sw}"/>
        <circle cx="{cx}" cy="{cy}" r="{R}"
          fill="none" stroke="{color}" stroke-width="{sw}"
          stroke-linecap="round"
          stroke-dasharray="{dash:.3f} {circ:.3f}"
          transform="rotate(-90 {cx} {cy})"/>
        <text x="{cx}" y="{cy+7}" text-anchor="middle"
          font-size="19" font-weight="700" fill="{color}"
          font-family="Inter,sans-serif">{pct:.1f}%</text>
      </svg>
      <span style="font-size:12px;font-weight:700;letter-spacing:2px;
                   color:{color};text-transform:uppercase;">{label}</span>
    </div>"""


# ── Main result card ──────────────────────────────────────────────────────────
def _save_to_history(proba, snippet="—"):
    """Simpan hasil prediksi ke session history untuk halaman Statistik."""
    hoax_pct  = proba[0] * 100
    valid_pct = proba[1] * 100
    verdict   = "HOAKS" if hoax_pct >= valid_pct else "VALID"
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({
        "label":   verdict,
        "hoax":    proba[0],
        "valid":   proba[1],
        "snippet": snippet,
    })


def render_result_card(proba, labels=("HOAKS", "VALID"), colors=("#ef4444", "#22c55e"), snippet="—"):
    hoax_pct  = proba[0] * 100
    valid_pct = proba[1] * 100
    verdict   = "HOAKS" if hoax_pct >= valid_pct else "VALID"
    vc        = colors[0] if verdict == "HOAKS" else colors[1]
    icon      = "⚠️" if verdict == "HOAKS" else "✅"
    desc = (
        "Narasi ini terindikasi <b>mengandung informasi hoaks</b>. "
        "Periksa sumber berita terpercaya sebelum menyebarkan."
        if verdict == "HOAKS" else
        "Narasi ini terindikasi <b>valid dan dapat dipercaya</b>. "
        "Tetap bijak dalam menyebarkan informasi."
    )
    # Parse hex -> rgb for RGBA background
    hex_ = vc.lstrip('#')
    r_val, g_val, b_val = int(hex_[0:2], 16), int(hex_[2:4], 16), int(hex_[4:6], 16)

    _save_to_history(proba, snippet)

    rings = (
        _ring_svg(labels[0], hoax_pct,  colors[0]) +
        _ring_svg(labels[1], valid_pct, colors[1])
    )

    st.markdown(f"""
    <div style="margin-top:1.8rem;padding:2rem 2rem 1.6rem;border-radius:18px;
                background:linear-gradient(145deg,#111318 0%,#161922 100%);
                border:1px solid #1e2232;">

      <div style="display:flex;align-items:center;justify-content:center;gap:14px;
                  padding:1rem 1.8rem;border-radius:12px;margin-bottom:1.8rem;
                  background:rgba({r_val},{g_val},{b_val},0.10);
                  border:1.5px solid {vc};">
        <span style="font-size:30px;line-height:1;">{icon}</span>
        <div>
          <div style="font-size:10px;letter-spacing:2.5px;color:#6b7280;
                      font-weight:700;text-transform:uppercase;margin-bottom:3px;">Hasil Prediksi</div>
          <div style="font-size:28px;font-weight:800;color:{vc};letter-spacing:1px;">{verdict}</div>
        </div>
      </div>

      <div style="display:flex;justify-content:center;gap:48px;flex-wrap:wrap;margin-bottom:1.4rem;">
        {rings}
      </div>

      <p style="text-align:center;color:#6b7280;font-size:13px;line-height:1.75;
                max-width:480px;margin:0 auto;">{desc}</p>
    </div>
    """, unsafe_allow_html=True)


# ── Legacy circle_progress (kept for compatibility) ───────────────────────────
def circle_progress(label, percent, color):
    return f"""
    <div style="display:flex;flex-direction:column;align-items:center;margin:10px;">
      <div style="width:120px;height:120px;border-radius:50%;
                  border:10px solid {color};display:flex;align-items:center;
                  justify-content:center;font-size:20px;font-weight:bold;color:{color};">
        {percent:.2f}%
      </div>
      <div style="margin-top:10px;font-size:18px;color:{color};font-weight:bold;">{label}</div>
    </div>"""
