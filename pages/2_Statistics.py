"""
Halaman Statistik — melacak riwayat prediksi dalam session saat ini
dan menampilkan ringkasan distribusi hasil.
"""
import streamlit as st
from util import inject_global_css

st.set_page_config(
    page_title="Statistik — FactCheck",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:2.5rem 0 1.2rem;">
  <div style="font-size:10px;letter-spacing:3px;color:#5b7ef0;font-weight:700;
              text-transform:uppercase;margin-bottom:8px;">Riwayat Sesi</div>
  <h1 style="font-size:2.4rem;font-weight:800;color:#e8eaf0;
             letter-spacing:-1px;margin:0 0 8px;">Statistik Prediksi</h1>
  <p style="color:#6b7280;font-size:14px;max-width:520px;line-height:1.7;margin:0;">
    Ringkasan semua verifikasi yang telah kamu lakukan selama sesi ini.
    Data akan direset saat halaman di-refresh.
  </p>
</div>
<hr style="border:1px solid #1e2232;margin-bottom:2rem;">
""", unsafe_allow_html=True)

# ── Session history init ──────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []   # list of {"label": str, "hoax": float, "valid": float, "snippet": str}

history = st.session_state.history

# ── Summary cards ─────────────────────────────────────────────────────────────
total  = len(history)
n_hoax = sum(1 for h in history if h["label"] == "HOAKS")
n_valid = total - n_hoax
pct_hoax  = (n_hoax  / total * 100) if total else 0
pct_valid = (n_valid / total * 100) if total else 0

col_a, col_b, col_c, col_d = st.columns(4)

def stat_card(col, emoji, title, value, color):
    with col:
        st.markdown(f"""
        <div style="background:#111318;border:1px solid #1e2232;border-radius:14px;
                    padding:1.4rem;text-align:center;">
          <div style="font-size:28px;margin-bottom:6px;">{emoji}</div>
          <div style="font-size:26px;font-weight:800;color:{color};">{value}</div>
          <div style="font-size:12px;color:#6b7280;margin-top:4px;">{title}</div>
        </div>
        """, unsafe_allow_html=True)

stat_card(col_a, "🔍", "Total Verifikasi", total,    "#e8eaf0")
stat_card(col_b, "⚠️", "Terdeteksi Hoaks",  n_hoax,  "#ef4444")
stat_card(col_c, "✅", "Terdeteksi Valid",  n_valid,  "#22c55e")
stat_card(col_d, "📈", "Akurasi Rata-Rata", f"{pct_valid:.0f}%" if total else "—", "#5b7ef0")

st.markdown("<br>", unsafe_allow_html=True)

# ── Distribution bar ──────────────────────────────────────────────────────────
if total > 0:
    st.markdown(f"""
    <div style="background:#111318;border:1px solid #1e2232;border-radius:14px;padding:1.6rem 2rem;margin-bottom:1.6rem;">
      <div style="font-size:11px;letter-spacing:2px;color:#6b7280;font-weight:700;
                  text-transform:uppercase;margin-bottom:14px;">Distribusi Hasil</div>
      <div style="display:flex;gap:0;border-radius:8px;overflow:hidden;height:28px;margin-bottom:10px;">
        <div style="width:{pct_hoax:.1f}%;background:#ef4444;
                    display:flex;align-items:center;justify-content:center;">
          {"" if pct_hoax < 8 else f'<span style="font-size:11px;font-weight:700;color:#fff;">{pct_hoax:.0f}%</span>'}
        </div>
        <div style="width:{pct_valid:.1f}%;background:#22c55e;
                    display:flex;align-items:center;justify-content:center;">
          {"" if pct_valid < 8 else f'<span style="font-size:11px;font-weight:700;color:#fff;">{pct_valid:.0f}%</span>'}
        </div>
      </div>
      <div style="display:flex;gap:20px;">
        <div style="display:flex;align-items:center;gap:6px;">
          <div style="width:10px;height:10px;border-radius:50%;background:#ef4444;"></div>
          <span style="font-size:12px;color:#6b7280;">Hoaks ({n_hoax})</span>
        </div>
        <div style="display:flex;align-items:center;gap:6px;">
          <div style="width:10px;height:10px;border-radius:50%;background:#22c55e;"></div>
          <span style="font-size:12px;color:#6b7280;">Valid ({n_valid})</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── History table ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="font-size:11px;letter-spacing:2px;color:#6b7280;font-weight:700;
            text-transform:uppercase;margin-bottom:12px;">Riwayat Detail</div>
""", unsafe_allow_html=True)

if total == 0:
    st.markdown("""
    <div style="background:#111318;border:1px dashed #1e2232;border-radius:14px;
                padding:3rem;text-align:center;color:#3d4252;">
      <div style="font-size:36px;margin-bottom:10px;">📭</div>
      <p style="font-size:14px;margin:0;">Belum ada verifikasi dalam sesi ini.<br>
      Mulai dari halaman <b>Verifikasi</b> atau <b>Home</b>.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Header row
    h_cols = st.columns([1, 5, 3, 2, 2])
    h_cols[0].markdown('<p style="font-size:11px;color:#3d4252;font-weight:700;letter-spacing:1px;margin:0;">#</p>', unsafe_allow_html=True)
    h_cols[1].markdown('<p style="font-size:11px;color:#3d4252;font-weight:700;letter-spacing:1px;margin:0;">TEKS</p>', unsafe_allow_html=True)
    h_cols[2].markdown('<p style="font-size:11px;color:#3d4252;font-weight:700;letter-spacing:1px;text-align:center;margin:0;">HASIL</p>', unsafe_allow_html=True)
    h_cols[3].markdown('<p style="font-size:11px;color:#ef4444;font-weight:700;letter-spacing:1px;text-align:right;margin:0;">HOAKS %</p>', unsafe_allow_html=True)
    h_cols[4].markdown('<p style="font-size:11px;color:#22c55e;font-weight:700;letter-spacing:1px;text-align:right;margin:0;">VALID %</p>', unsafe_allow_html=True)

    st.markdown('<hr style="border-color:#1e2232;margin:6px 0 2px;">', unsafe_allow_html=True)

    for i, h in enumerate(reversed(history), 1):
        vc   = "#ef4444" if h["label"] == "HOAKS" else "#22c55e"
        icon = "⚠️" if h["label"] == "HOAKS" else "✅"
        snip = h["snippet"][:80] + "…" if len(h["snippet"]) > 80 else h["snippet"]
        hex_ = vc.lstrip("#")
        r_val, g_val, b_val = int(hex_[0:2], 16), int(hex_[2:4], 16), int(hex_[4:6], 16)

        r_cols = st.columns([1, 5, 3, 2, 2])
        r_cols[0].markdown(f'<p style="font-size:12px;color:#6b7280;margin:0;padding:6px 0;">{i}</p>', unsafe_allow_html=True)
        r_cols[1].markdown(f'<p style="font-size:12px;color:#9aa3b8;margin:0;padding:6px 0;">{snip}</p>', unsafe_allow_html=True)
        r_cols[2].markdown(
            f'<div style="text-align:center;padding:4px 0;">'
            f'<span style="background:rgba({r_val},{g_val},{b_val},0.15);color:{vc};'
            f'font-size:11px;font-weight:700;border-radius:6px;padding:3px 10px;letter-spacing:1px;">'
            f'{icon} {h["label"]}</span></div>',
            unsafe_allow_html=True
        )
        r_cols[3].markdown(f'<p style="font-size:12px;color:#ef4444;text-align:right;margin:0;padding:6px 0;">{h["hoax"]*100:.1f}%</p>', unsafe_allow_html=True)
        r_cols[4].markdown(f'<p style="font-size:12px;color:#22c55e;text-align:right;margin:0;padding:6px 0;">{h["valid"]*100:.1f}%</p>', unsafe_allow_html=True)
        st.markdown('<hr style="border-color:#1e2232;margin:2px 0;">', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, _, btn_col = st.columns([3, 3, 1])
    with btn_col:
        if st.button("🗑️ Reset Riwayat", use_container_width=True):
            st.session_state.history = []
            st.rerun()
