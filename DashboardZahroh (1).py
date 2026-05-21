import pandas as pd
import streamlit as st
import os
import math
import io
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from streamlit_option_menu import option_menu

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Dashboard PKB SAMSAT",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CSS GLOBAL
# =====================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

    :root {
        --primary:        #4f46e5;
        --primary-dark:   #3730a3;
        --primary-light:  #818cf8;
        --secondary:      #0f172a;
        --success:        #10b981;
        --danger:         #ef4444;
        --background:     #f8fafc;
        --card-bg:        #ffffff;
        --text-main:      #1e293b;
        --text-muted:     #64748b;
        --border-color:   #e2e8f0;
        --sidebar-bg:     #0f172a;
        --shadow-subtle:  0 4px 6px -1px rgb(0 0 0 / 0.08), 0 2px 4px -2px rgb(0 0 0 / 0.06);
        --shadow-premium: 0 10px 15px -3px rgb(0 0 0 / 0.10), 0 4px 6px -4px rgb(0 0 0 / 0.08);
        --radius:         16px;
    }

    /* ── Base ── */
    .stApp {
        background: var(--background);
        font-family: 'Inter', sans-serif;
        color: var(--text-main) !important;
    }
    h1, h2, h3 { font-family: 'Outfit', sans-serif !important; font-weight: 700 !important; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        background-image: radial-gradient(circle at 0% 0%, rgba(79,70,229,.15) 0%, transparent 50%) !important;
        border-right: 1px solid rgba(255,255,255,.05);
    }
    [data-testid="stSidebar"] * { color: #f1f5f9 !important; }

    .sidebar-brand {
        font-family: 'Outfit', sans-serif;
        font-size: 1.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* ── Header card ── */
    .header-card {
        background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
        padding: 2.5rem;
        border-radius: var(--radius);
        margin-bottom: 2rem;
        box-shadow: var(--shadow-premium);
        position: relative;
        overflow: hidden;
    }
    .header-card::after {
        content: "";
        position: absolute; top: -50%; right: -10%;
        width: 300px; height: 300px;
        background: rgba(255,255,255,.05);
        border-radius: 50%; pointer-events: none;
    }
    .header-card h1 { color: white !important; font-size: 2.2rem !important; margin: 0 !important; }
    .header-card p  { color: rgba(241,245,249,.85) !important; font-size: 1rem; margin-top: .4rem !important; }

    /* ── KPI cards ── */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1.25rem; margin: 1.5rem 0;
    }
    .kpi-card {
        background: #ffffff;
        border-radius: var(--radius);
        padding: 1.5rem;
        box-shadow: var(--shadow-subtle);
        border: 1px solid var(--border-color);
        transition: transform .3s ease, box-shadow .3s ease;
    }
    .kpi-card:hover { transform: translateY(-6px); box-shadow: var(--shadow-premium); border-color: var(--primary-light); }
    .kpi-icon  { font-size: 1.75rem; margin-bottom: .75rem; }
    .kpi-label { font-size: .78rem; font-weight: 600; color: #475569; text-transform: uppercase; letter-spacing: .06em; margin-bottom: .35rem; }
    .kpi-value { font-family: 'Outfit', sans-serif; font-size: 1.75rem; font-weight: 700; color: #0f172a; line-height: 1.1; }
    .kpi-sub   { font-size: .75rem; color: #64748b; margin-top: .4rem; }

    /* ── Section headers ── */
    .section-header { margin: 2.5rem 0 1.25rem; padding-left: 1rem; border-left: 4px solid var(--primary); }
    .section-title  { font-family: 'Outfit', sans-serif; font-size: 1.5rem !important; font-weight: 700 !important; color: #0f172a !important; }
    .section-sub    { color: #64748b !important; font-size: .95rem; }

    /* ── Chart / Data cards ── */
    .card {
        background: #ffffff;
        border-radius: var(--radius);
        padding: 1.75rem;
        box-shadow: var(--shadow-subtle);
        border: 1px solid var(--border-color);
        margin-bottom: 1.25rem;
    }

    /* ── Fix: st.metric text selalu hitam ── */
    [data-testid="stMetricLabel"]  { color: #475569 !important; font-weight: 600 !important; }
    [data-testid="stMetricValue"]  { color: #0f172a !important; font-weight: 700 !important; }
    [data-testid="stMetricDelta"]  { color: #10b981 !important; }

    /* ── Buttons ── */
    .stButton > button {
        background: var(--primary) !important; color: white !important;
        border-radius: 10px !important; padding: .55rem 1.4rem !important;
        font-weight: 600 !important; border: none !important;
        transition: all .25s ease !important;
        box-shadow: 0 4px 6px -1px rgba(79,70,229,.25) !important;
    }
    .stButton > button:hover {
        background: var(--primary-dark) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 12px -2px rgba(79,70,229,.35) !important;
    }

    /* ── Tables ── */
    .stDataFrame { border: 1px solid var(--border-color) !important; border-radius: 12px !important; overflow: hidden !important; }

    /* ── Login card ── */
    .login-wrap {
        max-width: 420px; margin: 5vh auto 0;
        background: #ffffff; border-radius: 20px;
        padding: 2.5rem; box-shadow: 0 20px 40px rgba(0,0,0,.1);
        border: 1px solid var(--border-color);
        text-align: center;
    }
    .login-wrap h2 { color: #0f172a !important; font-size: 1.6rem !important; margin-bottom: .25rem !important; }
    .login-wrap p  { color: #64748b; font-size: .9rem; margin-bottom: 1.5rem; }

    /* ── Footer ── */
    .footer {
        margin-top: 4rem; padding: 3rem 2rem;
        background: #f1f5f9; text-align: center;
        border-radius: var(--radius) var(--radius) 0 0;
    }
    .footer-title { font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 700; color: #0f172a; }
    .footer-text  { color: #64748b; margin-top: .75rem; font-size: .875rem; }

    /* ── Upload area ── */
    [data-testid="stFileUploader"] {
        border: 2px dashed var(--primary-light) !important;
        border-radius: 12px !important; padding: 1rem !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 7px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>
""", unsafe_allow_html=True)


# =====================================================
# AUTENTIKASI
# =====================================================
CREDENTIALS = {"admin": "adminsamsat2026"}

def show_login():
    """Tampilkan halaman login fullscreen."""
    st.markdown("""
    <div style="text-align:center; padding-top: 3rem;">
        <div style="font-size:3.5rem;">🚗</div>
        <h1 style="font-family:'Outfit',sans-serif; color:#0f172a; font-size:2rem; margin:.5rem 0 .25rem;">
            SAMSAT Analytics
        </h1>
        <p style="color:#64748b; margin-bottom:2.5rem;">Sistem Dashboard PKB — Silakan login untuk melanjutkan</p>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_mid, col_r = st.columns([1, 1.2, 1])
    with col_mid:
        with st.form("login_form", clear_on_submit=False):
            st.markdown("#### 🔐 Login Akun")
            username = st.text_input("Username", placeholder="Masukkan username")
            password = st.text_input("Password", type="password", placeholder="Masukkan password")
            submitted = st.form_submit_button("Masuk →", use_container_width=True)

            if submitted:
                if username in CREDENTIALS and CREDENTIALS[username] == password:
                    st.session_state["logged_in"]  = True
                    st.session_state["username"]   = username
                    st.rerun()
                else:
                    st.error("❌ Username atau password salah. Silakan coba lagi.")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    show_login()
    st.stop()


# =====================================================
# LOAD DATA  (cache + support upload via session_state)
# =====================================================
@st.cache_data(show_spinner="Memuat data…")
def load_from_disk():
    """Baca semua CSV / Excel dari folder C:/laporan_pajak."""
    DATA_DIR = "C:/laporan_pajak"
    if not os.path.exists(DATA_DIR):
        return pd.DataFrame()

    all_files  = os.listdir(DATA_DIR)
    xlsx_files = [f for f in all_files if f.lower().endswith((".xlsx", ".xls"))]
    csv_files  = [f for f in all_files if f.lower().endswith(".csv")]

    dfs = []
    for f in xlsx_files:
        try:   dfs.append(pd.read_excel(os.path.join(DATA_DIR, f)))
        except Exception as e: st.warning(f"Gagal baca {f}: {e}")

    for f in csv_files:
        fp = os.path.join(DATA_DIR, f)
        try:   dfs.append(pd.read_csv(fp, encoding="utf-8",   sep=",", on_bad_lines="skip"))
        except Exception:
            try: dfs.append(pd.read_csv(fp, encoding="latin-1", sep=",", on_bad_lines="skip"))
            except Exception as e2: st.warning(f"Gagal baca {f}: {e2}")

    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


def process_df(raw) -> tuple:
    """Normalisasi kolom, tipe data, dan kolom tanggal.
    Menerima DataFrame tunggal. Selalu mengembalikan (DataFrame, str|None).
    """
    # ── guard: pastikan input valid ──────────────────────────────────────
    if raw is None:
        return pd.DataFrame(), None
    if not isinstance(raw, pd.DataFrame):
        try:
            raw = pd.DataFrame(raw)
        except Exception:
            return pd.DataFrame(), None
    if raw.empty:
        return raw.copy(), None

    df = raw.copy()

    # Normalisasi nama kolom
    df.columns = (df.columns.str.strip().str.upper()
                  .str.replace(" ", "_").str.replace(r"_+", "_", regex=True))

    # ── FIX 2a: buang kolom duplikat sebelum operasi apapun ──────────────
    df = df.loc[:, ~df.columns.duplicated()].reset_index(drop=True)

    if "JENIS_KB" in df.columns and "JENIS_KENDARAAN" not in df.columns:
        df["JENIS_KENDARAAN"] = df["JENIS_KB"]

    for col in ["TOTAL_POKOK_PKB", "TOTAL_POKOK_BBNKB", "TOTAL_DENDA_PKB", "TOTAL_DENDA_BBNKB"]:
        if col in df.columns:
            try:
                # Ambil kolom sebagai Series 1-d, antisipasi kolom duplikat sisa
                series = df[col]
                if isinstance(series, pd.DataFrame):
                    series = series.iloc[:, 0]
                df[col] = pd.to_numeric(series, errors="coerce").fillna(0)
            except Exception:
                df[col] = 0

    tgl_candidates = ["TGL_BAYAR", "TGL_DAFTAR", "TGL_PENETAPAN"]
    kolom_tgl = next((c for c in tgl_candidates if c in df.columns), None)
    if not kolom_tgl:
        kolom_tgl = next((c for c in df.columns if "TGL" in c or "TANGGAL" in c), None)

    if kolom_tgl:
        # ── FIX 2b: pastikan kolom tanggal adalah Series sebelum to_datetime
        tgl_series = df[kolom_tgl]
        if isinstance(tgl_series, pd.DataFrame):
            tgl_series = tgl_series.iloc[:, 0]
        df[kolom_tgl] = pd.to_datetime(tgl_series, dayfirst=True, errors="coerce")
        df = df.dropna(subset=[kolom_tgl]).reset_index(drop=True)
        df["TAHUN"]     = df[kolom_tgl].dt.year
        df["BULAN"]     = df[kolom_tgl].dt.month
        df["HARI"]      = df[kolom_tgl].dt.day
        nama_bulan = {1:"Januari",2:"Februari",3:"Maret",4:"April",5:"Mei",6:"Juni",
                      7:"Juli",8:"Agustus",9:"September",10:"Oktober",11:"November",12:"Desember"}
        df["BULAN_NAMA"] = df["BULAN"].map(nama_bulan)
        df["PERIODE"]    = df["BULAN_NAMA"] + " " + df["TAHUN"].astype(str)
        # Urutkan descending — data TERBARU di baris paling atas
        df = df.sort_values(kolom_tgl, ascending=False).reset_index(drop=True)

    return df, kolom_tgl


# Gabung data disk + upload — dengan validasi ketat
raw_disk = load_from_disk()

uploaded_dfs = st.session_state.get("uploaded_dfs", [])

# Filter hanya DataFrame yang valid & tidak kosong
valid_uploads = [
    d for d in uploaded_dfs
    if isinstance(d, pd.DataFrame) and not d.empty
]

if valid_uploads:
    parts = []
    if isinstance(raw_disk, pd.DataFrame) and not raw_disk.empty:
        parts.append(raw_disk)
    parts.extend(valid_uploads)
    try:
        # ── FIX 2c: reset_index setelah concat agar tidak ada index ganda ──
        raw_all = pd.concat(parts, ignore_index=True).reset_index(drop=True)
    except Exception as e:
        st.warning(f"⚠️ Gagal menggabungkan data upload: {e}")
        raw_all = raw_disk if isinstance(raw_disk, pd.DataFrame) else pd.DataFrame()
else:
    raw_all = raw_disk if isinstance(raw_disk, pd.DataFrame) else pd.DataFrame()

df, kolom_tanggal = process_df(raw_all)

if df.empty:
    st.warning("⚠️ Belum ada data. Silakan upload file Excel/CSV di menu **Data Master**.")


# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    # Brand
    st.markdown(f"""
    <div style="text-align:center; padding:1.25rem 0 1rem; border-bottom:1px solid rgba(255,255,255,.1);">
        <div style="font-size:2rem;">🚗</div>
        <div class="sidebar-brand">SAMSAT</div>
        <div style="color:rgba(255,255,255,.7); font-size:.8rem; margin-top:.25rem;">
            Dashboard Analisis PKB
        </div>
        <div style="margin-top:.5rem; font-size:.75rem; color:rgba(255,255,255,.5);">
            👤 {st.session_state.get('username','—')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

    # Navigasi — HANYA 4 menu
    menu = option_menu(
        menu_title=None,
        options=["Dashboard Utama", "Analisis Penerimaan", "Detail Transaksi", "Data Master"],
        icons=["house-fill", "bar-chart-fill", "search", "database-fill"],
        default_index=0,
        styles={
            "container":        {"padding": "0!important", "background-color": "transparent"},
            "icon":             {"color": "white", "font-size": "15px"},
            "nav-link": {
                "font-size": "13.5px", "text-align": "left",
                "margin": "3px 0", "padding": "11px 14px",
                "border-radius": "8px", "color": "white",
                "background-color": "rgba(255,255,255,.07)",
            },
            "nav-link-selected": {
                "background": "rgba(79,70,229,.55)",
                "color": "white", "font-weight": "600",
            },
        }
    )

    st.markdown("---")

    # Logout
    if st.button("🚪 Logout", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# ── df_f: tampilkan semua data tanpa filter ──────────
df_f       = df.copy() if not df.empty else pd.DataFrame()
start_date = df[kolom_tanggal].min().date() if (not df.empty and kolom_tanggal) else None
end_date   = df[kolom_tanggal].max().date() if (not df.empty and kolom_tanggal) else None


# ─── helper: plotly layout bersih ───────────────────
def clean_layout(fig, height=400):
    fig.update_layout(
        plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
        height=height, margin=dict(l=10, r=10, t=30, b=10),
        font=dict(family="Inter", color="#1e293b", size=12),
        legend=dict(font=dict(color="#1e293b")),
    )
    fig.update_xaxes(tickfont=dict(color="#475569"), title_font=dict(color="#475569"), gridcolor="#f1f5f9")
    fig.update_yaxes(tickfont=dict(color="#475569"), title_font=dict(color="#475569"), gridcolor="#f1f5f9")
    return fig

PALETTE_BAR  = ["#4f46e5","#6366f1","#818cf8","#a5b4fc","#c7d2fe"]
PALETTE_PIE  = ["#4f46e5","#7c3aed","#0ea5e9","#10b981","#f59e0b","#ef4444","#64748b","#0f172a"]

def fmt_rp(v):
    try:    return f"Rp {float(v):,.0f}"
    except: return v


# =====================================================
# HEADER
# =====================================================
period_txt = (f"{start_date} s/d {end_date}" if start_date and end_date else "Semua periode")
st.markdown(f"""
<div class="header-card">
    <h1>{menu}</h1>
    <p>Dashboard Pajak Kendaraan Bermotor (PKB) SAMSAT &nbsp;•&nbsp; Periode: {period_txt}</p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# ① DASHBOARD UTAMA
# =====================================================
if menu == "Dashboard Utama":
    if df_f.empty:
        st.info("Tidak ada data untuk periode yang dipilih.")
        st.stop()

    total_trx  = len(df_f)
    total_pkb  = df_f["TOTAL_POKOK_PKB"].sum()  if "TOTAL_POKOK_PKB"  in df_f.columns else 0
    total_bbnkb= df_f["TOTAL_POKOK_BBNKB"].sum() if "TOTAL_POKOK_BBNKB" in df_f.columns else 0
    avg_trx    = total_pkb / total_trx if total_trx else 0

    # KPI
    st.markdown("""<div class="section-header">
        <div class="section-title">📊 Ringkasan Kinerja</div>
        <div class="section-sub">Overview performa penerimaan PKB periode terpilih</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-icon">📋</div>
            <div class="kpi-label">Total Transaksi</div>
            <div class="kpi-value">{total_trx:,}</div>
            <div class="kpi-sub">Jumlah transaksi PKB</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Total Penerimaan PKB</div>
            <div class="kpi-value">Rp {total_pkb:,.0f}</div>
            <div class="kpi-sub">Akumulasi pokok PKB</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">🏷️</div>
            <div class="kpi-label">Total BBNKB</div>
            <div class="kpi-value">Rp {total_bbnkb:,.0f}</div>
            <div class="kpi-sub">Nilai Bea Balik Nama</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">📈</div>
            <div class="kpi-label">Rata-rata / Transaksi</div>
            <div class="kpi-value">Rp {avg_trx:,.0f}</div>
            <div class="kpi-sub">Nilai rata-rata per transaksi</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Grafik baris 1
    st.markdown("""<div class="section-header">
        <div class="section-title">📈 Visualisasi Tren</div>
        <div class="section-sub">Tren harian dan bulanan penerimaan PKB</div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📈 Penerimaan PKB Per Hari")
        if kolom_tanggal and "TOTAL_POKOK_PKB" in df_f.columns:
            daily = df_f.groupby(df_f[kolom_tanggal].dt.date)["TOTAL_POKOK_PKB"].sum().reset_index()
            daily.columns = ["Tanggal", "Total PKB"]
            fig = px.area(daily, x="Tanggal", y="Total PKB",
                          color_discrete_sequence=["#4f46e5"])
            fig.update_traces(line=dict(width=2.5), fillcolor="rgba(79,70,229,.15)",
                              hovertemplate="<b>%{x}</b><br>Total: Rp %{y:,.0f}<extra></extra>")
            st.plotly_chart(clean_layout(fig), use_container_width=True)
        else:
            st.info("Data tren harian tidak tersedia.")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📊 Penerimaan PKB Per Bulan")
        if "BULAN_NAMA" in df_f.columns and "TOTAL_POKOK_PKB" in df_f.columns:
            monthly = (df_f.groupby(["BULAN","BULAN_NAMA"])["TOTAL_POKOK_PKB"]
                       .sum().reset_index().sort_values("BULAN"))
            fig = px.bar(monthly, x="BULAN_NAMA", y="TOTAL_POKOK_PKB",
                         color_discrete_sequence=["#4f46e5"], text_auto=".2s")
            fig.update_traces(marker_line_width=0,
                              hovertemplate="<b>%{x}</b><br>Rp %{y:,.0f}<extra></extra>")
            st.plotly_chart(clean_layout(fig), use_container_width=True)
        else:
            st.info("Data tren bulanan tidak tersedia.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Grafik baris 2
    c3, c4 = st.columns([1.2, 1])

    with c3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🚗 Distribusi Jenis Kendaraan")
        if "JENIS_KENDARAAN" in df_f.columns:
            jc = df_f["JENIS_KENDARAAN"].value_counts().head(8)
            fig = px.pie(values=jc.values, names=jc.index,
                         color_discrete_sequence=PALETTE_PIE, hole=0.42)
            fig.update_traces(textposition="inside", textinfo="percent+label",
                              hovertemplate="<b>%{label}</b><br>%{value:,} kendaraan (%{percent})<extra></extra>")
            fig.update_layout(showlegend=False, height=380,
                              plot_bgcolor="#fff", paper_bgcolor="#fff",
                              margin=dict(l=10,r=10,t=20,b=10),
                              font=dict(family="Inter", color="#1e293b", size=12))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Data jenis kendaraan tidak tersedia.")
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🏆 Top 5 Kontribusi PKB")
        if "JENIS_KENDARAAN" in df_f.columns and "TOTAL_POKOK_PKB" in df_f.columns:
            top5 = df_f.groupby("JENIS_KENDARAAN")["TOTAL_POKOK_PKB"].sum().nlargest(5).reset_index()
            top5.columns = ["Jenis","PKB"]
            fig = px.bar(top5, x="PKB", y="Jenis", orientation="h",
                         color="PKB", color_continuous_scale=["#a5b4fc","#4f46e5"],
                         text_auto=".2s")
            fig.update_traces(hovertemplate="<b>%{y}</b><br>Rp %{x:,.0f}<extra></extra>",
                              marker_line_width=0)
            fig.update_layout(coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
            st.plotly_chart(clean_layout(fig, height=380), use_container_width=True)
        else:
            st.info("Data tidak tersedia.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Transaksi terbaru
    st.markdown("""<div class="section-header">
        <div class="section-title">📋 Transaksi Terbaru</div>
        <div class="section-sub">10 transaksi terakhir yang tercatat</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    prio = ([kolom_tanggal] if kolom_tanggal else []) + ["NOPOL","JENIS_KENDARAAN","TOTAL_POKOK_PKB","TOTAL_POKOK_BBNKB"]
    dcols = [c for c in prio if c in df_f.columns]
    recent = df_f.sort_values(kolom_tanggal, ascending=False).head(10) if kolom_tanggal in df_f.columns else df_f.head(10)
    disp = recent[dcols].copy()
    for col in ["TOTAL_POKOK_PKB","TOTAL_POKOK_BBNKB"]:
        if col in disp.columns: disp[col] = disp[col].apply(fmt_rp)
    if kolom_tanggal in disp.columns:
        disp[kolom_tanggal] = disp[kolom_tanggal].dt.strftime("%d-%m-%Y")
    st.dataframe(disp, use_container_width=True, height=380)
    st.markdown('</div>', unsafe_allow_html=True)


# =====================================================
# ② ANALISIS PENERIMAAN
# =====================================================
elif menu == "Analisis Penerimaan":
    if df_f.empty:
        st.info("Tidak ada data untuk periode yang dipilih.")
        st.stop()

    # Metric row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        if "TOTAL_POKOK_PKB" in df_f.columns and "BULAN_NAMA" in df_f.columns:
            avg_mo = df_f.groupby("BULAN_NAMA")["TOTAL_POKOK_PKB"].sum().mean()
            st.metric("Rata-rata Bulanan", f"Rp {avg_mo:,.0f}")
    with m2:
        if "TOTAL_POKOK_PKB" in df_f.columns and kolom_tanggal:
            max_d = df_f.groupby(kolom_tanggal)["TOTAL_POKOK_PKB"].sum().max()
            st.metric("Hari Tertinggi", f"Rp {max_d:,.0f}")
    with m3:
        if "TOTAL_POKOK_PKB" in df_f.columns and "JENIS_KENDARAAN" in df_f.columns:
            top_j = df_f.groupby("JENIS_KENDARAAN")["TOTAL_POKOK_PKB"].sum().idxmax()
            st.metric("Jenis Teratas", top_j[:18]+"…" if len(top_j)>18 else top_j)
    with m4:
        st.metric("Total PKB", f"Rp {df_f['TOTAL_POKOK_PKB'].sum():,.0f}" if "TOTAL_POKOK_PKB" in df_f.columns else "—")

    tab1, tab2, tab3 = st.tabs(["📈 Tren Waktu", "📊 Komparasi Jenis", "📉 Distribusi Nilai"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Tren Harian")
            if kolom_tanggal and "TOTAL_POKOK_PKB" in df_f.columns:
                daily = df_f.groupby(kolom_tanggal)["TOTAL_POKOK_PKB"].sum().reset_index()
                fig = px.line(daily, x=kolom_tanggal, y="TOTAL_POKOK_PKB",
                              color_discrete_sequence=["#4f46e5"], markers=True)
                fig.update_traces(line=dict(width=2.5), marker=dict(size=5),
                                  hovertemplate="<b>%{x|%d %b %Y}</b><br>Rp %{y:,.0f}<extra></extra>")
                st.plotly_chart(clean_layout(fig), use_container_width=True)
            else: st.info("Data tidak tersedia.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Tren Bulanan")
            if "BULAN_NAMA" in df_f.columns and "TOTAL_POKOK_PKB" in df_f.columns:
                monthly = (df_f.groupby(["BULAN","BULAN_NAMA"])["TOTAL_POKOK_PKB"]
                           .sum().reset_index().sort_values("BULAN"))
                fig = px.bar(monthly, x="BULAN_NAMA", y="TOTAL_POKOK_PKB",
                             color_discrete_sequence=["#4f46e5"], text_auto=".2s")
                fig.update_traces(marker_line_width=0)
                st.plotly_chart(clean_layout(fig), use_container_width=True)
            else: st.info("Data tidak tersedia.")
            st.markdown('</div>', unsafe_allow_html=True)

        # Perbandingan PKB vs BBNKB per bulan
        if all(c in df_f.columns for c in ["BULAN_NAMA","BULAN","TOTAL_POKOK_PKB","TOTAL_POKOK_BBNKB"]):
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### PKB vs BBNKB per Bulan")
            comp = (df_f.groupby(["BULAN","BULAN_NAMA"])[["TOTAL_POKOK_PKB","TOTAL_POKOK_BBNKB"]]
                    .sum().reset_index().sort_values("BULAN"))
            comp_melt = comp.melt(id_vars=["BULAN","BULAN_NAMA"],
                                  value_vars=["TOTAL_POKOK_PKB","TOTAL_POKOK_BBNKB"],
                                  var_name="Jenis", value_name="Nilai")
            comp_melt["Jenis"] = comp_melt["Jenis"].map({"TOTAL_POKOK_PKB":"PKB","TOTAL_POKOK_BBNKB":"BBNKB"})
            fig = px.bar(comp_melt, x="BULAN_NAMA", y="Nilai", color="Jenis", barmode="group",
                         color_discrete_map={"PKB":"#4f46e5","BBNKB":"#10b981"}, text_auto=".2s")
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(clean_layout(fig), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Top 10 Jenis Kendaraan (PKB)")
            if "JENIS_KENDARAAN" in df_f.columns and "TOTAL_POKOK_PKB" in df_f.columns:
                top10 = df_f.groupby("JENIS_KENDARAAN")["TOTAL_POKOK_PKB"].sum().nlargest(10).reset_index()
                fig = px.bar(top10, x="TOTAL_POKOK_PKB", y="JENIS_KENDARAAN", orientation="h",
                             color="TOTAL_POKOK_PKB",
                             color_continuous_scale=["#c7d2fe","#4f46e5"],
                             text_auto=".2s")
                fig.update_traces(marker_line_width=0)
                fig.update_layout(coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
                st.plotly_chart(clean_layout(fig, height=450), use_container_width=True)
            else: st.info("Data tidak tersedia.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Jumlah Transaksi per Jenis")
            if "JENIS_KENDARAAN" in df_f.columns:
                cnt = df_f["JENIS_KENDARAAN"].value_counts().head(8).reset_index()
                cnt.columns = ["Jenis","Jumlah"]
                fig = px.pie(cnt, values="Jumlah", names="Jenis",
                             color_discrete_sequence=PALETTE_PIE, hole=0.4)
                fig.update_traces(textinfo="percent+label", textposition="inside")
                fig.update_layout(showlegend=False, height=450,
                                  plot_bgcolor="#fff", paper_bgcolor="#fff",
                                  margin=dict(l=10,r=10,t=20,b=10),
                                  font=dict(family="Inter",color="#1e293b",size=12))
                st.plotly_chart(fig, use_container_width=True)
            else: st.info("Data tidak tersedia.")
            st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Distribusi Nilai PKB")
            if "TOTAL_POKOK_PKB" in df_f.columns:
                fig = px.histogram(df_f, x="TOTAL_POKOK_PKB", nbins=30,
                                   color_discrete_sequence=["#4f46e5"])
                fig.update_traces(marker_line_color="#ffffff", marker_line_width=.5)
                st.plotly_chart(clean_layout(fig), use_container_width=True)
            else: st.info("Data tidak tersedia.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Box Plot Nilai PKB per Jenis")
            if "JENIS_KENDARAAN" in df_f.columns and "TOTAL_POKOK_PKB" in df_f.columns:
                top5j = df_f["JENIS_KENDARAAN"].value_counts().head(5).index
                box_df = df_f[df_f["JENIS_KENDARAAN"].isin(top5j)]
                fig = px.box(box_df, x="JENIS_KENDARAAN", y="TOTAL_POKOK_PKB",
                             color="JENIS_KENDARAAN",
                             color_discrete_sequence=PALETTE_BAR)
                fig.update_layout(showlegend=False)
                st.plotly_chart(clean_layout(fig), use_container_width=True)
            else: st.info("Data tidak tersedia.")
            st.markdown('</div>', unsafe_allow_html=True)


# =====================================================
# ③ DETAIL TRANSAKSI
# =====================================================
elif menu == "Detail Transaksi":
    if df_f.empty:
        st.info("Tidak ada data untuk periode yang dipilih.")
        st.stop()

    # ── Inisialisasi default state untuk semua widget filter ─────────────
    _SORT_OPTIONS = ["Tanggal (Terbaru)", "Tanggal (Terlama)", "PKB (Tertinggi)", "PKB (Terendah)"]
    _RPP_OPTIONS  = [10, 25, 50, 100]

    for _k, _v in [("dt_search_q", ""), ("dt_sort_by", _SORT_OPTIONS[0]), ("dt_rpp", _RPP_OPTIONS[0])]:
        if _k not in st.session_state:
            st.session_state[_k] = _v

    # ── Callback: reset semua widget filter sekaligus ────────────────────
    def _reset_filter():
        st.session_state["dt_search_q"]  = ""
        st.session_state["dt_sort_by"]   = _SORT_OPTIONS[0]
        st.session_state["dt_rpp"]       = _RPP_OPTIONS[0]
        st.session_state["current_page"] = 1

    st.markdown('<div class="card">', unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns([3, 2, 1])
    with sc1:
        search_q = st.text_input("🔎 Cari transaksi…",
                                 placeholder="NOPOL, jenis kendaraan, kata kunci…",
                                 key="dt_search_q")
    with sc2:
        sort_by = st.selectbox("Urutkan", _SORT_OPTIONS, key="dt_sort_by")
    with sc3:
        rpp = st.selectbox("Baris/hal.", _RPP_OPTIONS, key="dt_rpp")
    st.markdown('</div>', unsafe_allow_html=True)

    df_disp = df_f.copy()
    if search_q:
        mask = df_disp.apply(lambda r: r.astype(str).str.contains(search_q, case=False, na=False).any(), axis=1)
        df_disp = df_disp[mask]

    sort_map = {
        "Tanggal (Terbaru)": (kolom_tanggal, False),
        "Tanggal (Terlama)": (kolom_tanggal, True),
        "PKB (Tertinggi)":   ("TOTAL_POKOK_PKB", False),
        "PKB (Terendah)":    ("TOTAL_POKOK_PKB", True),
    }
    scol, sasc = sort_map[sort_by]
    if scol and scol in df_disp.columns:
        df_disp = df_disp.sort_values(scol, ascending=sasc)

    total_rows  = len(df_disp)
    total_pages = max(1, math.ceil(total_rows / rpp))

    # ── Inisialisasi & clamp halaman di session_state ────────────────────
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = 1
    # Reset ke hal-1 kalau filter / pencarian berubah
    if st.session_state["current_page"] > total_pages:
        st.session_state["current_page"] = 1

    page_num = st.session_state["current_page"]

    # ── Callback tombol (aman, tidak menyentuh widget key) ───────────────
    def _go_prev():
        st.session_state["current_page"] = max(1, st.session_state["current_page"] - 1)

    def _go_next():
        st.session_state["current_page"] = min(total_pages, st.session_state["current_page"] + 1)

    s_idx = (page_num - 1) * rpp
    e_idx = min(page_num * rpp, total_rows)
    st.info(f"Menampilkan **{s_idx+1}–{e_idx}** dari **{total_rows:,}** transaksi &nbsp;|&nbsp; Halaman **{page_num}** / {total_pages}")

    prio = ([kolom_tanggal] if kolom_tanggal else []) + \
           ["NOPOL","JENIS_KENDARAAN","TOTAL_POKOK_PKB","TOTAL_POKOK_BBNKB","BULAN_NAMA"]
    dcols = [c for c in prio if c in df_disp.columns]
    page_df = df_disp.iloc[s_idx:e_idx][dcols].copy()

    for col in ["TOTAL_POKOK_PKB","TOTAL_POKOK_BBNKB"]:
        if col in page_df.columns: page_df[col] = page_df[col].apply(fmt_rp)
    if kolom_tanggal in page_df.columns:
        page_df[kolom_tanggal] = page_df[kolom_tanggal].dt.strftime("%d-%m-%Y")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(page_df, use_container_width=True, height=min(420, rpp*36+42))

    p1, p2, p3 = st.columns([2, 1, 2])
    with p1:
        st.button("⬅️ Sebelumnya",
                  on_click=_go_prev,
                  disabled=(page_num <= 1),
                  use_container_width=True)
    with p2:
        st.markdown(
            f"<div style='text-align:center;padding:.6rem 0;color:#475569;font-weight:600;'>"
            f"Hal {page_num}/{total_pages}</div>",
            unsafe_allow_html=True)
    with p3:
        st.button("Selanjutnya ➡️",
                  on_click=_go_next,
                  disabled=(page_num >= total_pages),
                  use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Export
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📥 Export Data")
    ex1, ex2, ex3 = st.columns(3)
    with ex1:
        st.download_button("📄 Download CSV",
            data=df_disp.to_csv(index=False).encode("utf-8"),
            file_name=f"pkb_{datetime.now():%Y%m%d_%H%M}.csv",
            mime="text/csv", use_container_width=True)
    with ex2:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            df_disp.to_excel(w, index=False, sheet_name="Data_PKB")
        st.download_button("📊 Download Excel",
            data=buf.getvalue(),
            file_name=f"pkb_{datetime.now():%Y%m%d_%H%M}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True)
    with ex3:
        st.button("🔄 Reset Filter", on_click=_reset_filter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =====================================================
# ④ DATA MASTER
# =====================================================
elif menu == "Data Master":

    # ── Upload file baru ──────────────────────────────
    st.markdown("""<div class="section-header">
        <div class="section-title">📤 Upload Data Baru</div>
        <div class="section-sub">Unggah file Excel (.xlsx) atau CSV — file akan disimpan permanen ke <code>C:/laporan_pajak</code></div>
    </div>""", unsafe_allow_html=True)

    DATA_DIR = "C:/laporan_pajak"

    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Pilih file Excel / CSV (bisa lebih dari satu)",
        type=["xlsx", "xls", "csv"],
        accept_multiple_files=True,
        help="File akan disimpan permanen ke C:/laporan_pajak dengan nama unik berbasis timestamp"
    )

    if uploaded_files:
        # ── Baca preview semua file yang dipilih ────────────────────────
        new_dfs = []
        for uf in uploaded_files:
            try:
                if uf.name.lower().endswith((".xlsx", ".xls")):
                    new_dfs.append((uf, pd.read_excel(uf)))
                else:
                    try:
                        new_dfs.append((uf, pd.read_csv(uf, encoding="utf-8",   sep=",", on_bad_lines="skip")))
                    except Exception:
                        new_dfs.append((uf, pd.read_csv(uf, encoding="latin-1", sep=",", on_bad_lines="skip")))
                st.success(f"✅ **{uf.name}** siap diunggah — {len(new_dfs[-1][1]):,} baris terdeteksi")
            except Exception as e:
                st.error(f"❌ Gagal membaca **{uf.name}**: {e}")

        if new_dfs:
            if st.button("➕ Tambahkan ke Dashboard", type="primary"):
                # ── Pastikan folder tujuan ada ───────────────────────────
                try:
                    os.makedirs(DATA_DIR, exist_ok=True)
                    dir_ok = True
                except Exception as dir_err:
                    st.error(f"❌ Tidak bisa membuat folder **{DATA_DIR}**: {dir_err}")
                    dir_ok = False

                saved_count  = 0
                fallback_dfs = []   # cadangan jika disk write gagal

                for idx, (uf, df_new) in enumerate(new_dfs):
                    # Nama file unik: upload_data_YYYYMMDD_HHMMSS_N.xlsx
                    ts    = datetime.now().strftime("%Y%m%d_%H%M%S")
                    fname = f"upload_data_{ts}_{idx + 1}.xlsx"
                    fpath = os.path.join(DATA_DIR, fname)

                    if dir_ok:
                        try:
                            df_new.to_excel(fpath, index=False, engine="openpyxl")
                            saved_count += 1
                            st.success(f"💾 Tersimpan permanen → `{fpath}`")
                        except Exception as write_err:
                            st.warning(
                                f"⚠️ **{uf.name}** gagal disimpan ke disk "
                                f"({write_err}) — dimuat ke memori sementara."
                            )
                            fallback_dfs.append(df_new)
                    else:
                        fallback_dfs.append(df_new)

                # Jika ada file yang gagal ke disk → simpan di session_state
                if fallback_dfs:
                    st.session_state["uploaded_dfs"] = fallback_dfs
                else:
                    # Semua sudah di disk — kosongkan session_state agar
                    # tidak ada duplikasi saat load_from_disk() dijalankan
                    st.session_state["uploaded_dfs"] = []

                if saved_count > 0:
                    st.info(
                        f"✅ **{saved_count} file** berhasil disimpan permanen ke "
                        f"`{DATA_DIR}`. Dashboard akan di-refresh dan memuat ulang data…"
                    )

                # Bersihkan cache agar load_from_disk() membaca file baru
                st.cache_data.clear()
                st.rerun()

    st.markdown("---")

    # ══════════════════════════════════════════════════
    # TOMBOL HAPUS DATA UPLOAD TERBARU
    # ══════════════════════════════════════════════════

    # Kumpulkan semua file upload_data_*.xlsx di folder, urutkan terbaru dulu
    def _cari_file_upload(folder: str) -> list[str]:
        """Kembalikan daftar path file upload_data_*.xlsx diurutkan terbaru dulu."""
        if not os.path.isdir(folder):
            return []
        hasil = []
        for f in os.listdir(folder):
            if f.startswith("upload_data_") and f.lower().endswith(".xlsx"):
                hasil.append(os.path.join(folder, f))
        # Urutkan berdasarkan waktu modifikasi, terbaru di depan
        hasil.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        return hasil

    file_upload_list = _cari_file_upload(DATA_DIR)

    if file_upload_list:
        # Tampilkan daftar file upload yang ada
        st.markdown(
            f"**📁 File upload tersimpan di `{DATA_DIR}`** "
            f"({len(file_upload_list)} file):"
        )
        for fp in file_upload_list:
            mtime = datetime.fromtimestamp(os.path.getmtime(fp)).strftime("%d-%m-%Y %H:%M:%S")
            st.caption(f"• `{os.path.basename(fp)}` — disimpan {mtime}")

        st.markdown("")  # spasi

        btn_col1, btn_col2 = st.columns([1, 2])
        with btn_col1:
            hapus_terbaru = st.button(
                "🗑️ Hapus Data Upload Terbaru",
                type="secondary",
                use_container_width=True,
                help="Menghapus SATU file upload terbaru (upload_data_*.xlsx) dari folder"
            )
        with btn_col2:
            hapus_semua = st.button(
                "🗑️🗑️ Hapus SEMUA Data Upload",
                type="secondary",
                use_container_width=True,
                help="Menghapus SEMUA file upload_data_*.xlsx dari folder sekaligus"
            )

        if hapus_terbaru:
            target = file_upload_list[0]   # file paling baru
            try:
                os.remove(target)
                st.session_state["uploaded_dfs"] = []
                st.cache_data.clear()
                st.success(
                    f"✅ **{os.path.basename(target)}** berhasil dihapus! "
                    f"Dashboard telah kembali ke data semula."
                )
                st.rerun()
            except Exception as err:
                st.error(f"❌ Gagal menghapus file: {err}")

        if hapus_semua:
            errors = []
            deleted = 0
            for fp in file_upload_list:
                try:
                    os.remove(fp)
                    deleted += 1
                except Exception as err:
                    errors.append(f"{os.path.basename(fp)}: {err}")
            st.session_state["uploaded_dfs"] = []
            st.cache_data.clear()
            if errors:
                st.warning(f"⚠️ {deleted} file dihapus, {len(errors)} gagal: {'; '.join(errors)}")
            else:
                st.success(
                    f"✅ Semua **{deleted} file upload** berhasil dihapus! "
                    f"Dashboard telah kembali ke data semula."
                )
            st.rerun()

    else:
        st.info("ℹ️ Tidak ada data hasil upload yang dapat dihapus.")

    # ── Status data fallback di session_state (jika disk write pernah gagal) ──
    if st.session_state.get("uploaded_dfs"):
        st.warning(
            f"⚠️ Ada **{sum(len(d) for d in st.session_state['uploaded_dfs']):,} baris** "
            f"data yang hanya tersimpan di memori sementara (disk write gagal)."
        )
        if st.button("🗑️ Hapus Data Sementara", type="secondary"):
            st.session_state["uploaded_dfs"] = []
            st.cache_data.clear()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Metadata ──────────────────────────────────────
    st.markdown("""<div class="section-header">
        <div class="section-title">📋 Metadata & Kualitas Data</div>
        <div class="section-sub">Informasi struktur dan kelengkapan data</div>
    </div>""", unsafe_allow_html=True)

    if df.empty:
        st.info("Belum ada data.")
    else:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Records",  f"{len(df):,}")
        m2.metric("Total Kolom",    len(df.columns))
        m3.metric("Kelengkapan",    f"{df.notna().mean().mean()*100:.1f}%")
        m4.metric("Duplikat",       f"{df.duplicated().sum():,}")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📊 Informasi Kolom")
        col_info = [{"Kolom": c, "Tipe": str(df[c].dtype),
                     "Non-Null": int(df[c].count()), "Unique": int(df[c].nunique()),
                     "Null": int(df[c].isnull().sum())} for c in df.columns]
        st.dataframe(pd.DataFrame(col_info), use_container_width=True, height=300)
        st.markdown('</div>', unsafe_allow_html=True)

        # Preview
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 👁️ Preview Data")
        ta, tb = st.tabs(["🔼 Data Awal (10 baris)", "🔽 Data Akhir (10 baris)"])
        with ta: st.dataframe(df.head(10), use_container_width=True, height=300)
        with tb: st.dataframe(df.tail(10), use_container_width=True, height=300)
        st.markdown('</div>', unsafe_allow_html=True)

        # Download seluruh data
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📥 Download Seluruh Data")
        dc1, dc2 = st.columns(2)
        with dc1:
            st.download_button("📄 Download CSV (semua)",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name=f"pkb_all_{datetime.now():%Y%m%d}.csv",
                mime="text/csv", use_container_width=True)
        with dc2:
            buf2 = io.BytesIO()
            with pd.ExcelWriter(buf2, engine="openpyxl") as w:
                df.to_excel(w, index=False, sheet_name="Data_PKB")
            st.download_button("📊 Download Excel (semua)",
                data=buf2.getvalue(),
                file_name=f"pkb_all_{datetime.now():%Y%m%d}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# =====================================================
# FOOTER
# =====================================================
total_rec = len(df_f) if not df_f.empty else 0
st.markdown(f"""
<div class="footer">
    <div class="footer-title">🚗 SAMSAT Analytics Platform</div>
    <div class="footer-text">
        © 2024 Sistem Informasi Analisis PKB SAMSAT &nbsp;|&nbsp;
        Dashboard Interaktif &nbsp;|&nbsp; Data diperbarui secara real-time<br>
        <small>Terakhir diperbarui: {datetime.now().strftime("%d %B %Y %H:%M")}
        &nbsp;•&nbsp; Menampilkan {total_rec:,} records</small>
    </div>
</div>
""", unsafe_allow_html=True)