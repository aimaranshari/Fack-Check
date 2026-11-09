import streamlit as st
from util import inject_global_css, get_text_from_url, read_uploaded_file, classify, render_result_card

st.set_page_config(
    page_title="FactCheck — Verifikasi Narasi",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

# ── Hero section ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:3.5rem 1rem 1rem;">
  <div style="display:inline-block;background:rgba(91,126,240,0.12);
              border:1px solid rgba(91,126,240,0.3);border-radius:99px;
              padding:5px 16px;margin-bottom:18px;">
    <span style="font-size:12px;font-weight:600;letter-spacing:2px;
                 color:#5b7ef0;text-transform:uppercase;">AI-Powered Fact Check</span>
  </div>
  <h1 style="font-size:clamp(2.4rem,6vw,4.2rem);font-weight:800;
             color:#e8eaf0;letter-spacing:-1.5px;line-height:1.1;margin:0 0 14px;">
    Fact<span style="color:#5b7ef0;">Check</span>
  </h1>
  <p style="color:#6b7280;font-size:15px;max-width:500px;
            margin:0 auto 2.5rem;line-height:1.7;">
    Tidak yakin dengan suatu berita? Tempelkan teks, URL, atau dokumen —
    model <em>machine learning</em> kami akan menganalisis dalam hitungan detik.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Input tab state ───────────────────────────────────────────────────────────
TABS = ["TEXT", "URL", "DOC", "MP3", "MP4"]
ICONS = ["✏️", "🔗", "📄", "🎵", "🎬"]
WIP   = {"MP3", "MP4"}

if "tab" not in st.session_state:
    st.session_state.tab = "TEXT"

# Tab selector — centered pill buttons
cols = st.columns([2] + [1] * len(TABS) + [2])
for i, (tab, icon) in enumerate(zip(TABS, ICONS)):
    with cols[i + 1]:
        label = f"{icon} {tab}"
        if st.button(label, key=f"tab_{tab}", use_container_width=True):
            st.session_state.tab = tab

st.markdown("<br>", unsafe_allow_html=True)

# ── Main card ─────────────────────────────────────────────────────────────────
_, card_col, _ = st.columns([1, 6, 1])

with card_col:
    st.markdown(f"""
    <div style="background:#111318;border:1px solid #1e2232;border-radius:18px;
                padding:2rem 2.2rem 1.6rem;">
      <div style="font-size:12px;letter-spacing:2px;color:#5b7ef0;
                  font-weight:700;text-transform:uppercase;margin-bottom:1rem;">
        MODE : {st.session_state.tab}
      </div>
    """, unsafe_allow_html=True)

    active = st.session_state.tab
    result_proba   = None
    result_snippet = "—"

    if active == "TEXT":
        st.markdown('<p style="color:#9aa3b8;font-size:13px;margin-bottom:6px;">Masukkan teks atau narasi yang ingin diverifikasi:</p>', unsafe_allow_html=True)
        user_text = st.text_area("", height=220, placeholder="Tempelkan teks berita / narasi di sini…", key="txt_input")
        st.markdown("<br>", unsafe_allow_html=True)
        _, btn_col, _ = st.columns([3, 2, 3])
        with btn_col:
            check = st.button("🔍  Verifikasi", use_container_width=True, key="check_txt")
        if check and user_text.strip():
            with st.spinner("Menganalisis…"):
                result_proba   = classify(user_text)[0]
                result_snippet = user_text

    elif active == "URL":
        st.markdown('<p style="color:#9aa3b8;font-size:13px;margin-bottom:6px;">Masukkan URL artikel berita:</p>', unsafe_allow_html=True)
        user_url = st.text_input("", placeholder="https://example.com/berita/…", key="url_input")
        st.markdown("<br>", unsafe_allow_html=True)
        _, btn_col, _ = st.columns([3, 2, 3])
        with btn_col:
            check = st.button("🔍  Verifikasi", use_container_width=True, key="check_url")
        if check and user_url.strip():
            with st.spinner("Mengambil konten URL…"):
                article_text   = get_text_from_url(user_url)
                result_proba   = classify(article_text)[0]
                result_snippet = user_url

    elif active == "DOC":
        st.markdown('<p style="color:#9aa3b8;font-size:13px;margin-bottom:6px;">Unggah dokumen (.txt atau .docx):</p>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=["docx", "txt"], key="doc_input")
        st.markdown("<br>", unsafe_allow_html=True)
        _, btn_col, _ = st.columns([3, 2, 3])
        with btn_col:
            check = st.button("🔍  Verifikasi", use_container_width=True, key="check_doc")
        if check and uploaded_file:
            with st.spinner("Membaca dokumen…"):
                doc_text       = read_uploaded_file(uploaded_file)
                result_proba   = classify(doc_text)[0]
                result_snippet = uploaded_file.name

    elif active in WIP:
        st.markdown(f"""
        <div style="text-align:center;padding:3rem 1rem;">
          <div style="font-size:48px;margin-bottom:12px;">
            {"🎵" if active == "MP3" else "🎬"}
          </div>
          <p style="color:#6b7280;font-size:14px;">
            Fitur <b style="color:#5b7ef0;">{active}</b> sedang dalam tahap pengembangan.<br>
            Pantau terus pembaruan kami!
          </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Prediction result ─────────────────────────────────────────────────────
    if result_proba is not None:
        render_result_card(result_proba, snippet=result_snippet)

# ── Feature highlights ────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
_, feat_col, _ = st.columns([1, 6, 1])
with feat_col:
    st.markdown("""
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;
                margin-bottom:3rem;">

      <div style="background:#111318;border:1px solid #1e2232;border-radius:14px;padding:1.4rem;">
        <div style="font-size:26px;margin-bottom:10px;">🧠</div>
        <div style="font-size:13px;font-weight:700;color:#e8eaf0;margin-bottom:6px;">Machine Learning</div>
        <div style="font-size:12px;color:#6b7280;line-height:1.6;">
          Menggunakan model klasifikasi terlatih dengan data berita Indonesia nyata.
        </div>
      </div>

      <div style="background:#111318;border:1px solid #1e2232;border-radius:14px;padding:1.4rem;">
        <div style="font-size:26px;margin-bottom:10px;">⚡</div>
        <div style="font-size:13px;font-weight:700;color:#e8eaf0;margin-bottom:6px;">Analisis Cepat</div>
        <div style="font-size:12px;color:#6b7280;line-height:1.6;">
          Prediksi dalam hitungan detik — teks, URL, maupun dokumen.
        </div>
      </div>

      <div style="background:#111318;border:1px solid #1e2232;border-radius:14px;padding:1.4rem;">
        <div style="font-size:26px;margin-bottom:10px;">📊</div>
        <div style="font-size:13px;font-weight:700;color:#e8eaf0;margin-bottom:6px;">Skor Probabilitas</div>
        <div style="font-size:12px;color:#6b7280;line-height:1.6;">
          Hasil ditampilkan sebagai skor keyakinan, bukan sekadar label biner.
        </div>
      </div>

    </div>
    """, unsafe_allow_html=True)
