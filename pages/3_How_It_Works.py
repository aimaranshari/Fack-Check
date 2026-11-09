"""
Halaman How It Works — penjelasan pipeline NLP dan cara kerja model.
"""
import streamlit as st
from util import inject_global_css

st.set_page_config(
    page_title="How It Works — FactCheck",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:2.5rem 0 1.2rem;">
  <div style="font-size:10px;letter-spacing:3px;color:#5b7ef0;font-weight:700;
              text-transform:uppercase;margin-bottom:8px;">Dokumentasi</div>
  <h1 style="font-size:2.4rem;font-weight:800;color:#e8eaf0;
             letter-spacing:-1px;margin:0 0 8px;">Cara Kerja Model</h1>
  <p style="color:#6b7280;font-size:14px;max-width:560px;line-height:1.7;margin:0;">
    Pelajari bagaimana FactCheck mengolah teks, mengekstrak fitur,
    dan menghasilkan prediksi hoaks vs. valid.
  </p>
</div>
<hr style="border:1px solid #1e2232;margin-bottom:2.5rem;">
""", unsafe_allow_html=True)

_, main_col, _ = st.columns([0.5, 5, 0.5])

with main_col:

    # ── Pipeline steps ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-size:11px;letter-spacing:2px;color:#6b7280;font-weight:700;
                text-transform:uppercase;margin-bottom:16px;">Pipeline Lengkap</div>

    <div style="display:flex;flex-direction:column;gap:0;position:relative;">

      <!-- Step connector line -->
      <div style="position:absolute;left:27px;top:54px;bottom:54px;
                  width:2px;background:#1e2232;z-index:0;"></div>

      <!-- Step 1 -->
      <div style="display:flex;gap:16px;align-items:flex-start;margin-bottom:16px;position:relative;z-index:1;">
        <div style="width:54px;height:54px;border-radius:50%;background:#1a1d2a;border:2px solid #5b7ef0;
                    display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:20px;">📥</div>
        <div style="background:#111318;border:1px solid #1e2232;border-radius:14px;padding:1.2rem 1.4rem;flex:1;">
          <div style="font-size:11px;color:#5b7ef0;font-weight:700;letter-spacing:1.5px;
                      text-transform:uppercase;margin-bottom:4px;">Step 1</div>
          <div style="font-size:15px;font-weight:700;color:#e8eaf0;margin-bottom:6px;">Input Teks</div>
          <p style="font-size:13px;color:#6b7280;margin:0;line-height:1.7;">
            Pengguna memasukkan narasi dalam bentuk <b style="color:#9aa3b8;">teks bebas</b>,
            <b style="color:#9aa3b8;">URL artikel</b>, atau <b style="color:#9aa3b8;">dokumen</b>.
            Untuk URL, konten halaman web di-scrape otomatis menggunakan <code style="color:#5b7ef0;">BeautifulSoup</code>.
          </p>
        </div>
      </div>

      <!-- Step 2 -->
      <div style="display:flex;gap:16px;align-items:flex-start;margin-bottom:16px;position:relative;z-index:1;">
        <div style="width:54px;height:54px;border-radius:50%;background:#1a1d2a;border:2px solid #f59e0b;
                    display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:20px;">🧹</div>
        <div style="background:#111318;border:1px solid #1e2232;border-radius:14px;padding:1.2rem 1.4rem;flex:1;">
          <div style="font-size:11px;color:#f59e0b;font-weight:700;letter-spacing:1.5px;
                      text-transform:uppercase;margin-bottom:4px;">Step 2</div>
          <div style="font-size:15px;font-weight:700;color:#e8eaf0;margin-bottom:6px;">Pre-processing Teks</div>
          <p style="font-size:13px;color:#6b7280;margin:0 0 10px;line-height:1.7;">
            Teks dibersihkan melalui serangkaian langkah:
          </p>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
            <div style="background:#0d0f14;border-radius:8px;padding:8px 12px;font-size:12px;color:#9aa3b8;">
              ✂️ Lowercase & hapus HTML tag
            </div>
            <div style="background:#0d0f14;border-radius:8px;padding:8px 12px;font-size:12px;color:#9aa3b8;">
              🔗 Hapus URL & hashtag
            </div>
            <div style="background:#0d0f14;border-radius:8px;padding:8px 12px;font-size:12px;color:#9aa3b8;">
              🔢 Hapus angka & tanda baca
            </div>
            <div style="background:#0d0f14;border-radius:8px;padding:8px 12px;font-size:12px;color:#9aa3b8;">
              🛑 Stopword Removal (Sastrawi)
            </div>
            <div style="background:#0d0f14;border-radius:8px;padding:8px 12px;font-size:12px;color:#9aa3b8;">
              🌿 Stemming (Sastrawi)
            </div>
            <div style="background:#0d0f14;border-radius:8px;padding:8px 12px;font-size:12px;color:#9aa3b8;">
              😀 Hapus emoji & karakter non-ASCII
            </div>
          </div>
        </div>
      </div>

      <!-- Step 3 -->
      <div style="display:flex;gap:16px;align-items:flex-start;margin-bottom:16px;position:relative;z-index:1;">
        <div style="width:54px;height:54px;border-radius:50%;background:#1a1d2a;border:2px solid #7c5cd8;
                    display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:20px;">⚖️</div>
        <div style="background:#111318;border:1px solid #1e2232;border-radius:14px;padding:1.2rem 1.4rem;flex:1;">
          <div style="font-size:11px;color:#7c5cd8;font-weight:700;letter-spacing:1.5px;
                      text-transform:uppercase;margin-bottom:4px;">Step 3</div>
          <div style="font-size:15px;font-weight:700;color:#e8eaf0;margin-bottom:6px;">Pembobotan TF-IDF</div>
          <p style="font-size:13px;color:#6b7280;margin:0;line-height:1.7;">
            Teks bersih diubah menjadi vektor numerik menggunakan
            <b style="color:#7c5cd8;">TF-IDF</b> (Term Frequency–Inverse Document Frequency).
            Setiap kata mendapatkan bobot berdasarkan seberapa sering muncul di dokumen
            dibanding seluruh korpus. Vectorizer dimuat dari <code style="color:#7c5cd8;">tfidf.pkl</code>.
          </p>
        </div>
      </div>

      <!-- Step 4 -->
      <div style="display:flex;gap:16px;align-items:flex-start;margin-bottom:16px;position:relative;z-index:1;">
        <div style="width:54px;height:54px;border-radius:50%;background:#1a1d2a;border:2px solid #22c55e;
                    display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:20px;">🤖</div>
        <div style="background:#111318;border:1px solid #1e2232;border-radius:14px;padding:1.2rem 1.4rem;flex:1;">
          <div style="font-size:11px;color:#22c55e;font-weight:700;letter-spacing:1.5px;
                      text-transform:uppercase;margin-bottom:4px;">Step 4</div>
          <div style="font-size:15px;font-weight:700;color:#e8eaf0;margin-bottom:6px;">Klasifikasi Model ML</div>
          <p style="font-size:13px;color:#6b7280;margin:0;line-height:1.7;">
            Vektor TF-IDF dikirimkan ke model terlatih (<code style="color:#22c55e;">model.pkl</code>).
            Model mengembalikan <b style="color:#22c55e;">probabilitas</b> untuk setiap kelas:
            <b style="color:#ef4444;">HOAKS</b> dan <b style="color:#22c55e;">VALID</b>.
            Kelas dengan probabilitas tertinggi menjadi prediksi akhir.
          </p>
        </div>
      </div>

      <!-- Step 5 -->
      <div style="display:flex;gap:16px;align-items:flex-start;position:relative;z-index:1;">
        <div style="width:54px;height:54px;border-radius:50%;background:#1a1d2a;border:2px solid #ef4444;
                    display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:20px;">📊</div>
        <div style="background:#111318;border:1px solid #1e2232;border-radius:14px;padding:1.2rem 1.4rem;flex:1;">
          <div style="font-size:11px;color:#ef4444;font-weight:700;letter-spacing:1.5px;
                      text-transform:uppercase;margin-bottom:4px;">Step 5</div>
          <div style="font-size:15px;font-weight:700;color:#e8eaf0;margin-bottom:6px;">Visualisasi Hasil</div>
          <p style="font-size:13px;color:#6b7280;margin:0;line-height:1.7;">
            Prediksi ditampilkan sebagai <b style="color:#e8eaf0;">verdict card</b> dengan
            skor probabilitas berupa <b style="color:#e8eaf0;">SVG ring chart</b> untuk
            setiap kelas. Disertai penjelasan deskriptif berdasarkan hasil prediksi.
          </p>
        </div>
      </div>

    </div>
    """, unsafe_allow_html=True)

    # ── Tech stack ────────────────────────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:11px;letter-spacing:2px;color:#6b7280;font-weight:700;
                text-transform:uppercase;margin-bottom:16px;">Tech Stack</div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-bottom:2.5rem;">

      <div style="background:#111318;border:1px solid #1e2232;border-radius:12px;padding:1.2rem;text-align:center;">
        <div style="font-size:24px;margin-bottom:8px;">🐍</div>
        <div style="font-size:13px;font-weight:700;color:#e8eaf0;">Python 3</div>
        <div style="font-size:11px;color:#6b7280;margin-top:3px;">Core Language</div>
      </div>

      <div style="background:#111318;border:1px solid #1e2232;border-radius:12px;padding:1.2rem;text-align:center;">
        <div style="font-size:24px;margin-bottom:8px;">🔴</div>
        <div style="font-size:13px;font-weight:700;color:#e8eaf0;">Streamlit</div>
        <div style="font-size:11px;color:#6b7280;margin-top:3px;">Web Framework</div>
      </div>

      <div style="background:#111318;border:1px solid #1e2232;border-radius:12px;padding:1.2rem;text-align:center;">
        <div style="font-size:24px;margin-bottom:8px;">📐</div>
        <div style="font-size:13px;font-weight:700;color:#e8eaf0;">scikit-learn</div>
        <div style="font-size:11px;color:#6b7280;margin-top:3px;">ML Library</div>
      </div>

      <div style="background:#111318;border:1px solid #1e2232;border-radius:12px;padding:1.2rem;text-align:center;">
        <div style="font-size:24px;margin-bottom:8px;">🌿</div>
        <div style="font-size:13px;font-weight:700;color:#e8eaf0;">Sastrawi</div>
        <div style="font-size:11px;color:#6b7280;margin-top:3px;">Indonesian NLP</div>
      </div>

      <div style="background:#111318;border:1px solid #1e2232;border-radius:12px;padding:1.2rem;text-align:center;">
        <div style="font-size:24px;margin-bottom:8px;">🍜</div>
        <div style="font-size:13px;font-weight:700;color:#e8eaf0;">BeautifulSoup</div>
        <div style="font-size:11px;color:#6b7280;margin-top:3px;">Web Scraping</div>
      </div>

    </div>
    """, unsafe_allow_html=True)
