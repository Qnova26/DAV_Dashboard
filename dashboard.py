import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

# ======================================================
# 1. KONFIGURASI HALAMAN
# ======================================================
st.set_page_config(
    page_title="Shopnesia Performance Report",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# 2. PALET WARNA MODERN (Indigo - Slate, minim tapi tegas)
# ======================================================
PRIMARY      = "#4F46E5"   # Indigo utama
PRIMARY_SOFT = "#818CF8"
ACCENT       = "#F97316"   # Oranye aksen (dipakai terbatas, untuk highlight)
ACCENT_SOFT  = "#FDBA74"
INK          = "#0F172A"   # Teks judul (slate-900)
SUBTEXT      = "#64748B"   # Teks sekunder (slate-500)
BG           = "#F5F6FA"   # Background halaman
CARD_BG      = "#FFFFFF"
BORDER       = "#E7E9F1"

CATEGORICAL_SEQUENCE = [PRIMARY, ACCENT, "#22C55E", "#EAB308", "#06B6D4", "#EC4899"]
GENDER_MAP = {"Male": PRIMARY, "Female": ACCENT}
YEAR_SEQUENCE = [PRIMARY, PRIMARY_SOFT, ACCENT_SOFT]

# Template Plotly global biar semua chart konsisten tanpa harus diulang tiap kali
pio.templates["shopnesia"] = pio.templates["plotly_white"]
pio.templates["shopnesia"].layout.update(
    font=dict(family="Inter, sans-serif", size=12, color=INK),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=30, r=20, t=10, b=30),
    colorway=CATEGORICAL_SEQUENCE,
    xaxis=dict(showgrid=False, linecolor=BORDER, tickfont=dict(size=11, color=SUBTEXT)),
    yaxis=dict(showgrid=True, gridcolor="#F1F2F7", linecolor=BORDER, tickfont=dict(size=11, color=SUBTEXT)),
    hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter, sans-serif"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11)),
)
pio.templates.default = "shopnesia"

# ======================================================
# 3. CSS GLOBAL
# ======================================================
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background-color: {BG};
    }}

    /* Hero header dengan gradient tipis */
    .hero {{
        background: linear-gradient(135deg, {PRIMARY} 0%, {PRIMARY_SOFT} 100%);
        border-radius: 18px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px rgba(79, 70, 229, 0.18);
    }}
    .hero-title {{
        color: #ffffff;
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.3px;
        margin: 0;
    }}
    .hero-sub {{
        color: rgba(255,255,255,0.85);
        font-size: 13.5px;
        margin-top: 4px;
        font-weight: 500;
    }}

    /* Section label di atas tiap grup chart */
    .section-label {{
        color: {SUBTEXT};
        font-size: 11.5px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 22px 0 10px 2px;
    }}

    /* Kartu untuk setiap chart */
    .chart-card {{
        background-color: {CARD_BG};
        padding: 20px 22px 8px 22px;
        border-radius: 16px;
        border: 1px solid {BORDER};
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
        margin-bottom: 18px;
        transition: box-shadow 0.2s ease;
    }}
    .chart-card:hover {{
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
    }}
    .chart-header {{
        color: {INK};
        font-weight: 700;
        font-size: 14.5px;
        margin-bottom: 2px;
    }}
    .chart-caption {{
        color: {SUBTEXT};
        font-weight: 400;
        font-size: 12px;
        margin-bottom: 12px;
    }}

    /* Metric cards */
    div[data-testid="stMetric"] {{
        background-color: {CARD_BG} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 14px !important;
        padding: 16px 20px !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
    }}
    div[data-testid="stMetricLabel"] > div {{
        color: {SUBTEXT} !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }}
    div[data-testid="stMetricValue"] > div {{
        color: {INK} !important;
        font-size: 23px !important;
        font-weight: 800 !important;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: #ffffff;
        border-right: 1px solid {BORDER};
    }}
    section[data-testid="stSidebar"] .stMarkdown h2, 
    section[data-testid="stSidebar"] .stMarkdown h3 {{
        color: {INK};
    }}

    /* Selectbox rounded */
    div[data-baseweb="select"] > div {{
        border-radius: 10px !important;
        border-color: {BORDER} !important;
    }}

    #MainMenu, footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# ======================================================
# 4. LOAD & CLEAN DATA
# ======================================================
@st.cache_data
def load_data():
    columns_fixed = [
        'order_id', 'order_date', 'customer_id', 'customer_gender', 'customer_age',
        'customer_city', 'customer_province', 'product_category', 'product_subcategory',
        'brand_tier', 'price', 'discount_percent', 'final_price', 'quantity',
        'payment_method', 'shipping_cost', 'delivery_days', 'is_returned', 'return_reason', 'rating'
    ]
    df = pd.read_csv('shopnesia_combined_2021_2023.csv', sep=';', skiprows=1, header=None, names=columns_fixed)

    df['rating'] = df['rating'].astype(str).str.split(',').str[0]
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df = df.dropna(subset=['order_id'])

    df['order_date'] = pd.to_datetime(df['order_date'], format='%d/%m/%Y', errors='coerce')
    df['year'] = df['order_date'].dt.year.astype(str)
    df['month_year'] = df['order_date'].dt.to_period('M').astype(str)

    def age_group(age):
        try:
            age_num = float(age)
            if age_num < 20: return 'Di bawah 20'
            elif 20 <= age_num <= 29: return '20-29'
            elif 30 <= age_num <= 39: return '30-39'
            elif 40 <= age_num <= 49: return '40-49'
            else: return '50+'
        except:
            return 'Tidak Diketahui'
    df['age_group'] = df['customer_age'].apply(age_group)

    df['final_price'] = pd.to_numeric(df['final_price'], errors='coerce').fillna(0)
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
    df['discount_percent'] = pd.to_numeric(df['discount_percent'], errors='coerce').fillna(0)
    df['total_sales'] = df['final_price'] * df['quantity']
    return df

try:
    df_raw = load_data()
except Exception as e:
    st.error(f"Gagal memuat berkas dataset. Pastikan file 'shopnesia_combined_2021_2023.csv' berada di direktori yang sama. Error: {e}")
    st.stop()

# ======================================================
# 5. SIDEBAR — FILTER GLOBAL
# ======================================================
with st.sidebar:
    st.markdown("### 🛍️ Shopnesia")
    st.caption("Executive Performance Dashboard")
    st.markdown("---")
    st.markdown("**Filter Data**")

    year_options = ["Semua Tahun"] + sorted(df_raw['year'].dropna().unique().tolist())
    selected_year = st.selectbox("Tahun", year_options)

    cat_options = ["Semua Kategori"] + sorted(df_raw['product_category'].dropna().unique().tolist())
    selected_category_filter = st.selectbox("Kategori Produk", cat_options)

    st.markdown("---")
    st.caption("Dashboard ini menampilkan performa penjualan Shopnesia periode 2021–2023.")

df = df_raw.copy()
if selected_year != "Semua Tahun":
    df = df[df['year'] == selected_year]
if selected_category_filter != "Semua Kategori":
    df = df[df['product_category'] == selected_category_filter]

# ======================================================
# 6. HERO HEADER
# ======================================================
st.markdown(f"""
    <div class="hero">
        <p class="hero-title">Shopnesia Business Performance Report</p>
        <p class="hero-sub">Periode Analisis 2021–2023 · Global Core Executive Dashboard</p>
    </div>
""", unsafe_allow_html=True)

# ======================================================
# 7. SUMMARY METRICS
# ======================================================
m1, m2, m3, m4 = st.columns(4)
with m1:
    total_revenue = df['total_sales'].sum()
    st.metric(label="💰 Total Penjualan", value=f"IDR {total_revenue:,.0f}")
with m2:
    total_orders = df['order_id'].nunique()
    st.metric(label="🧾 Total Transaksi", value=f"{total_orders:,}")
with m3:
    total_qty = df['quantity'].sum()
    st.metric(label="📦 Volume Terjual", value=f"{int(total_qty):,}")
with m4:
    avg_rating = df['rating'].mean()
    st.metric(label="⭐ Kepuasan Pelanggan", value=f"{avg_rating:.2f} / 5.0")

# ======================================================
# 8. HELPER: CHART CARD WRAPPER
# ======================================================
def chart_card_open(title, caption=""):
    caption_html = f"<div class='chart-caption'>{caption}</div>" if caption else ""
    st.markdown(f"<div class='chart-card'><div class='chart-header'>{title}</div>{caption_html}", unsafe_allow_html=True)

def chart_card_close():
    st.markdown("</div>", unsafe_allow_html=True)

def style_bar(fig, width=0.5):
    fig.update_traces(marker_line_width=0, width=width)
    return fig

# ======================================================
# ROW 1 — TREN WAKTU
# ======================================================
st.markdown("<div class='section-label'>Tren Penjualan</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    chart_card_open("Tren Penjualan Tahunan")
    yearly_sales = df.groupby('year')['total_sales'].sum().reset_index()
    fig1 = px.bar(yearly_sales, x='year', y='total_sales', color_discrete_sequence=[PRIMARY])
    st.plotly_chart(style_bar(fig1, 0.4), use_container_width=True)
    chart_card_close()

with col2:
    chart_card_open("Tren Penjualan Bulanan")
    monthly_sales = df.groupby('month_year')['total_sales'].sum().reset_index().sort_values('month_year')
    fig2 = px.area(monthly_sales, x='month_year', y='total_sales', color_discrete_sequence=[ACCENT])
    fig2.update_traces(line=dict(width=2.5), fillcolor="rgba(249, 115, 22, 0.12)")
    st.plotly_chart(fig2, use_container_width=True)
    chart_card_close()

# ======================================================
# ROW 2 — DEMOGRAFI & KATEGORI
# ======================================================
st.markdown("<div class='section-label'>Demografi & Kategori Produk</div>", unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    chart_card_open("Segmentasi Berdasarkan Profil Usia")
    age_profile = df['age_group'].value_counts().reset_index()
    age_profile.columns = ['Profil Usia', 'Jumlah']
    fig3 = px.pie(age_profile, names='Profil Usia', values='Jumlah', hole=0.65,
                  color_discrete_sequence=CATEGORICAL_SEQUENCE)
    fig3.update_traces(textfont_size=11, marker=dict(line=dict(color='#ffffff', width=2)))
    st.plotly_chart(fig3, use_container_width=True)
    chart_card_close()

with col4:
    chart_card_open("Distribusi Volume Pembelian per Kategori")
    category_sales = df['product_category'].value_counts().reset_index()
    category_sales.columns = ['Kategori', 'Jumlah']
    fig4 = px.bar(category_sales, x='Kategori', y='Jumlah', color_discrete_sequence=[PRIMARY_SOFT])
    st.plotly_chart(style_bar(fig4, 0.5), use_container_width=True)
    chart_card_close()

# ======================================================
# ROW 3 — GENDER
# ======================================================
col5, col6 = st.columns(2)

with col5:
    chart_card_open("Distribusi Produk Berdasarkan Gender")
    gender_category = df.groupby(['product_category', 'customer_gender']).size().reset_index(name='Jumlah')
    fig5 = px.bar(gender_category, x='product_category', y='Jumlah', color='customer_gender',
                  barmode='group', color_discrete_map=GENDER_MAP)
    st.plotly_chart(style_bar(fig5, 0.3), use_container_width=True)
    chart_card_close()

with col6:
    chart_card_open("Proporsi Gender per Kategori", "Gunakan dropdown untuk memilih kategori")
    selected_cat = st.selectbox("Filter Kategori:", df['product_category'].unique(), key="donut_cat", label_visibility="collapsed")
    gender_prop = df[df['product_category'] == selected_cat]['customer_gender'].value_counts().reset_index()
    gender_prop.columns = ['Gender', 'Jumlah']
    fig6 = px.pie(gender_prop, names='Gender', values='Jumlah', hole=0.65, color_discrete_map=GENDER_MAP)
    fig6.update_traces(marker=dict(line=dict(color='#ffffff', width=2)))
    st.plotly_chart(fig6, use_container_width=True)
    chart_card_close()

# ======================================================
# ROW 4 — STRATEGI HARGA
# ======================================================
st.markdown("<div class='section-label'>Strategi Diskon & Harga</div>", unsafe_allow_html=True)
col7, col8 = st.columns(2)

with col7:
    chart_card_open("Dampak Diskon terhadap Kuantitas Pembelian")
    def discount_bin(pct):
        if pct == 0: return 'Tanpa Diskon'
        elif pct <= 10: return 'Diskon 1-10%'
        elif pct <= 20: return 'Diskon 11-20%'
        else: return 'Diskon >20%'
    df['discount_group'] = df['discount_percent'].apply(discount_bin)
    discount_qty = df.groupby(['discount_group', 'year'])['quantity'].mean().reset_index()
    fig7 = px.bar(discount_qty, x='discount_group', y='quantity', color='year',
                  barmode='group', color_discrete_sequence=YEAR_SEQUENCE)
    st.plotly_chart(style_bar(fig7, 0.6), use_container_width=True)
    chart_card_close()

with col8:
    chart_card_open("Korelasi Nilai Diskon terhadap Rating")
    discount_rating = df.groupby('discount_percent')['rating'].mean().reset_index().sort_values('discount_percent')
    fig8 = px.line(discount_rating, x='rating', y='discount_percent', color_discrete_sequence=[PRIMARY])
    fig8.update_traces(line=dict(width=2.5))
    st.plotly_chart(fig8, use_container_width=True)
    chart_card_close()

# ======================================================
# ROW 5 — GEOGRAFIS
# ======================================================
st.markdown("<div class='section-label'>Sebaran Geografis</div>", unsafe_allow_html=True)
col9, col10 = st.columns(2)

with col9:
    chart_card_open("Top 10 Provinsi Kontributor Penjualan")
    province_sales = df.groupby('customer_province')['total_sales'].sum().reset_index()
    province_sales = province_sales.sort_values(by='total_sales', ascending=True).tail(10)
    fig9 = px.bar(province_sales, x='total_sales', y='customer_province', orientation='h',
                  color_discrete_sequence=[PRIMARY])
    st.plotly_chart(style_bar(fig9, 0.6), use_container_width=True)
    chart_card_close()

with col10:
    chart_card_open("Top 10 Kota Kontributor Penjualan")
    city_sales = df.groupby('customer_city')['total_sales'].sum().reset_index()
    city_sales = city_sales.sort_values(by='total_sales', ascending=True).tail(10)
    fig10 = px.bar(city_sales, x='total_sales', y='customer_city', orientation='h',
                   color_discrete_sequence=[ACCENT])
    st.plotly_chart(style_bar(fig10, 0.6), use_container_width=True)
    chart_card_close()