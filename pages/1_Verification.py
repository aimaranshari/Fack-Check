import streamlit as st
<<<<<<< HEAD
from util import inject_global_css, get_text_from_url, read_uploaded_file, classify, render_result_card

st.set_page_config(
    page_title="Verifikasi — FactCheck",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:2.5rem 0 1.2rem;">
  <div style="font-size:10px;letter-spacing:3px;color:#5b7ef0;font-weight:700;
              text-transform:uppercase;margin-bottom:8px;">Alat Verifikasi</div>
  <h1 style="font-size:2.4rem;font-weight:800;color:#e8eaf0;
             letter-spacing:-1px;margin:0 0 8px;">Verifikasi Narasi</h1>
  <p style="color:#6b7280;font-size:14px;max-width:520px;line-height:1.7;margin:0;">
    Masukkan teks, URL artikel, atau unggah dokumen untuk dianalisis oleh model
    klasifikasi hoaks kami secara langsung.
  </p>
</div>
<hr style="border:1px solid #1e2232;margin-bottom:2rem;">
""", unsafe_allow_html=True)

# ── Mode selector ─────────────────────────────────────────────────────────────
MODES = {
    "✏️ Teks":     "TEXT",
    "🔗 URL":      "URL",
    "📄 Dokumen":  "DOC",
}
WIP_MODES = {
    "🎵 MP3":      "MP3",
    "🎬 MP4":      "MP4",
}

if "v_tab" not in st.session_state:
    st.session_state.v_tab = "TEXT"

left_col, right_col = st.columns([1, 3])

with left_col:
    st.markdown('<p style="font-size:11px;letter-spacing:2px;color:#6b7280;font-weight:700;text-transform:uppercase;margin-bottom:10px;">Pilih Mode</p>', unsafe_allow_html=True)
    for label, key in MODES.items():
        active_style = "background:#5b7ef0;color:#fff;border-color:#5b7ef0;" if st.session_state.v_tab == key else ""
        if st.button(label, key=f"vmode_{key}", use_container_width=True):
            st.session_state.v_tab = key

    st.markdown('<hr style="border-color:#1e2232;margin:12px 0;">', unsafe_allow_html=True)
    st.markdown('<p style="font-size:11px;letter-spacing:2px;color:#3d4252;font-weight:700;text-transform:uppercase;margin-bottom:10px;">Coming Soon</p>', unsafe_allow_html=True)
    for label, key in WIP_MODES.items():
        st.button(label, key=f"vmode_{key}_wip", use_container_width=True, disabled=True)

with right_col:
    mode = st.session_state.v_tab
    result_proba   = None
    result_snippet = "—"

    st.markdown(f"""
    <div style="background:#111318;border:1px solid #1e2232;border-radius:16px;padding:1.8rem 2rem 1.4rem;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:1.2rem;">
        <span style="font-size:18px;">{"✏️" if mode=="TEXT" else "🔗" if mode=="URL" else "📄"}</span>
        <div style="font-size:12px;font-weight:700;letter-spacing:2px;
                    color:#5b7ef0;text-transform:uppercase;">Mode: {mode}</div>
      </div>
    """, unsafe_allow_html=True)

    if mode == "TEXT":
        st.markdown('<p style="color:#9aa3b8;font-size:13px;margin-bottom:6px;">Teks / narasi yang ingin diverifikasi:</p>', unsafe_allow_html=True)
        user_text = st.text_area("", height=240,
                                 placeholder="Masukkan atau tempelkan teks berita, narasi, atau klaim di sini…",
                                 key="veri_text")
        char_count = len(user_text) if user_text else 0
        st.markdown(f'<p style="font-size:11px;color:#3d4252;text-align:right;margin-top:-8px;">{char_count} karakter</p>', unsafe_allow_html=True)

    elif mode == "URL":
        st.markdown('<p style="color:#9aa3b8;font-size:13px;margin-bottom:6px;">URL artikel berita:</p>', unsafe_allow_html=True)
        user_url = st.text_input("", placeholder="https://detik.com/berita/…", key="veri_url")
        if user_url:
            st.markdown(f'<p style="font-size:11px;color:#3d4252;margin-top:-8px;">🌐 {user_url[:60]}{"…" if len(user_url)>60 else ""}</p>', unsafe_allow_html=True)

    elif mode == "DOC":
        st.markdown('<p style="color:#9aa3b8;font-size:13px;margin-bottom:6px;">Unggah file dokumen:</p>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=["docx", "txt"], key="veri_doc")
        if uploaded_file:
            st.markdown(f'<p style="font-size:11px;color:#22c55e;margin-top:4px;">✅ {uploaded_file.name} diunggah</p>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([3, 2, 3])
    with btn_col:
        check = st.button("🔍  Analisis Sekarang", use_container_width=True, key="veri_check")

    if check:
        if mode == "TEXT":
            if user_text and user_text.strip():
                with st.spinner("Menganalisis teks…"):
                    result_proba   = classify(user_text)[0]
                    result_snippet = user_text
            else:
                st.warning("⚠️ Masukkan teks terlebih dahulu.")
        elif mode == "URL":
            if user_url and user_url.strip():
                with st.spinner("Mengambil konten URL…"):
                    article_text   = get_text_from_url(user_url)
                    result_proba   = classify(article_text)[0]
                    result_snippet = user_url
            else:
                st.warning("⚠️ Masukkan URL terlebih dahulu.")
        elif mode == "DOC":
            if uploaded_file:
                with st.spinner("Membaca dokumen…"):
                    doc_text       = read_uploaded_file(uploaded_file)
                    result_proba   = classify(doc_text)[0]
                    result_snippet = uploaded_file.name
            else:
                st.warning("⚠️ Unggah dokumen terlebih dahulu.")

    if result_proba is not None:
        render_result_card(result_proba, snippet=result_snippet)

# ── Tips section ──────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<hr style="border:1px solid #1e2232;margin-bottom:1.6rem;">
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-bottom:2.5rem;">

  <div style="background:#111318;border:1px solid #1e2232;border-radius:12px;padding:1.2rem;">
    <div style="font-size:20px;margin-bottom:8px;">💡</div>
    <div style="font-size:12px;font-weight:700;color:#e8eaf0;margin-bottom:5px;">Tips Teks</div>
    <div style="font-size:12px;color:#6b7280;line-height:1.6;">Gunakan teks minimal 50 kata agar model mendapat konteks yang cukup.</div>
  </div>

  <div style="background:#111318;border:1px solid #1e2232;border-radius:12px;padding:1.2rem;">
    <div style="font-size:20px;margin-bottom:8px;">🔗</div>
    <div style="font-size:13px;font-weight:700;color:#e8eaf0;margin-bottom:5px;">Tips URL</div>
    <div style="font-size:12px;color:#6b7280;line-height:1.6;">Pastikan URL dapat diakses publik dan merupakan artikel berbahasa Indonesia.</div>
  </div>

  <div style="background:#111318;border:1px solid #1e2232;border-radius:12px;padding:1.2rem;">
    <div style="font-size:20px;margin-bottom:8px;">📄</div>
    <div style="font-size:13px;font-weight:700;color:#e8eaf0;margin-bottom:5px;">Tips Dokumen</div>
    <div style="font-size:12px;color:#6b7280;line-height:1.6;">Format yang didukung: <code style="color:#5b7ef0;">.txt</code> dan <code style="color:#5b7ef0;">.docx</code>. Pastikan dokumen berisi teks yang terbaca.</div>
  </div>

  <div style="background:#111318;border:1px solid #1e2232;border-radius:12px;padding:1.2rem;">
    <div style="font-size:20px;margin-bottom:8px;">⚠️</div>
    <div style="font-size:13px;font-weight:700;color:#e8eaf0;margin-bottom:5px;">Disclaimer</div>
    <div style="font-size:12px;color:#6b7280;line-height:1.6;">Hasil prediksi bersifat indikatif. Selalu verifikasi dengan sumber berita terpercaya.</div>
  </div>

</div>
""", unsafe_allow_html=True)
=======
import pandas as pd
from util import set_background_color

set_background_color("#A9A9A9")

st.markdown(
    '<h1 style="color:black; font-size: 50px; text-align: center;">RIWAYAT VERIFIKASI</h1>',
    unsafe_allow_html=True
)

columns = ["Waktu", "Narasi Berita", "Prediksi", "Hasil Verifikasi", "Referensi", "Report"]

# Ambil dari session_state.history (yang diisi di page FACT CHECK)
history = st.session_state.get("history", [])

# Tombol reset/clear riwayat
c1, c2, c3 = st.columns([1,2,1])
with c2:
    if st.button("Hapus Semua Riwayat", use_container_width=True):
        st.session_state.history = []
        history = []

# Buat DataFrame dan tampilkan
df = pd.DataFrame(history, columns=columns)
st.dataframe(df, use_container_width=True)


>>>>>>> 6a806a3f6f44a54fe0d916b0419190b30b164279
