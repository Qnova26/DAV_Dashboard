import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
# 2. PALET WARNA MODERN (Premium Dark Theme)
# ======================================================
PRIMARY      = "#48CAE4"   # Light Blue
PRIMARY_SOFT = "#90E0EF"   
ACCENT       = "#FF6B35"   # Bright Orange
ACCENT_SOFT  = "#FF9770"
INK          = "#F8FAFC"   # White
SUBTEXT      = "#94A3B8"   # Slate 400
BG           = "#0B1121"   # Deep Dark Blue
CARD_BG      = "#151F32"   # Lighter Dark Blue for cards
BORDER       = "#2A3B5C"   # Subtle border
HERO_GRAD    = "linear-gradient(135deg, #121E31 0%, #0B1121 100%)"

CATEGORICAL_SEQUENCE = [PRIMARY, ACCENT, PRIMARY_SOFT, "#FBBF24", "#34D399", "#F472B6"]
GENDER_MAP = {"Male": PRIMARY, "Female": ACCENT}
YEAR_SEQUENCE = [PRIMARY, PRIMARY_SOFT, ACCENT_SOFT]

# Template Plotly global
pio.templates["shopnesia"] = pio.templates["plotly_dark"]
pio.templates["shopnesia"].layout.update(
    font=dict(family="Inter, sans-serif", size=12, color=INK),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=30, r=20, t=10, b=30),
    colorway=CATEGORICAL_SEQUENCE,
    xaxis=dict(showgrid=False, linecolor=BORDER, tickfont=dict(size=11, color=SUBTEXT)),
    yaxis=dict(showgrid=True, gridcolor=BORDER, linecolor=BORDER, tickfont=dict(size=11, color=SUBTEXT)),
    hoverlabel=dict(bgcolor=CARD_BG, font_size=12, font_family="Inter, sans-serif", font_color=INK),
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
    
    [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}

    /* Hero header */
    .hero {{
        background: {HERO_GRAD};
        border-radius: 20px;
        padding: 32px 36px;
        margin-bottom: 28px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        border: 1px solid #2A3B5C;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        overflow: hidden;
    }}
    /* Glowing effect behind */
    .hero::before {{
        content: '';
        position: absolute;
        top: -50px;
        right: -50px;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(72,202,228,0.15) 0%, rgba(0,0,0,0) 70%);
        border-radius: 50%;
    }}
    .hero-content {{
        position: relative;
        z-index: 1;
    }}
    .hero-title {{
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0 0 8px 0;
        /* Apple-style gradient text */
        background: linear-gradient(90deg, #FFFFFF 0%, {PRIMARY_SOFT} 50%, {PRIMARY} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .hero-sub {{
        color: #94A3B8;
        font-size: 14px;
        margin-top: 0;
        margin-bottom: 18px;
        font-weight: 500;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }}
    .hero-badges {{
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
    }}
    .badge {{
        background: rgba(42, 59, 92, 0.4);
        border: 1px solid rgba(72, 202, 228, 0.2);
        padding: 6px 14px;
        border-radius: 6px;
        font-size: 12px;
        color: #E2E8F0;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    .badge-green {{
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34D399;
    }}
    .hero-icon {{
        font-size: 80px;
        opacity: 0.9;
        filter: drop-shadow(0 0 20px rgba(72,202,228,0.25));
        z-index: 1;
    }}

    /* Section label */
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
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
        margin-bottom: 18px;
        transition: box-shadow 0.2s ease;
    }}
    .chart-card:hover {{
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
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
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important;
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
    
    /* Style untuk Tabs */
    button[data-baseweb="tab"] {{
        font-size: 14px;
        font-weight: 600;
        color: {SUBTEXT};
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {PRIMARY};
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
    df = pd.read_csv('shopnesia_total.csv', sep=';', skiprows=1, header=None, names=columns_fixed)

    df['rating'] = df['rating'].astype(str).str.split(',').str[0]
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df = df.dropna(subset=['order_id'])

    for col in ['product_category', 'product_subcategory', 'customer_gender',
                'customer_province', 'customer_city', 'brand_tier', 'payment_method']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    parsed_dates = pd.to_datetime(df['order_date'], format='%d/%m/%Y', errors='coerce')
    still_missing = parsed_dates.isna()
    if still_missing.any():
        parsed_dates.loc[still_missing] = pd.to_datetime(
            df.loc[still_missing, 'order_date'], errors='coerce', dayfirst=True
        )
    df['order_date'] = parsed_dates
    df['year'] = df['order_date'].dt.year.astype('Int64').astype(str)
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
    st.error(f"Gagal memuat berkas dataset. Pastikan file 'shopnesia_total.csv' berada di direktori yang sama. Error: {e}")
    st.stop()

# ======================================================
# 5. SIDEBAR — FILTER GLOBAL
# ======================================================
with st.sidebar:
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 40px; margin-bottom: -10px;">🛍️</div>
            <h2 style="color: {PRIMARY}; margin-bottom: 0px; font-weight: 800; font-size: 24px; letter-spacing: -0.5px;">Shopnesia</h2>
            <p style="color: {SUBTEXT}; font-size: 12px; margin-top: 2px; font-weight: 500; text-transform: uppercase;">Executive Dashboard</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<div style='margin: 15px 0; border-bottom: 1px solid {BORDER};'></div>", unsafe_allow_html=True)
    
    st.markdown(f"<div style='color: {INK}; font-size: 13px; font-weight: 700; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px;'>🎛️ Filter Analisis</div>", unsafe_allow_html=True)

    valid_years = sorted([y for y in df_raw['year'].dropna().unique().tolist() if y not in ('nan', '<NA>', 'NaT')])
    year_options = ["Total"] + valid_years
    selected_year = st.selectbox("Tahun Transaksi", year_options)

    valid_categories = sorted([c for c in df_raw['product_category'].dropna().unique().tolist() if c not in ('nan', 'Nan')])
    cat_options = ["Semua Kategori"] + valid_categories
    selected_category_filter = st.selectbox("Kategori Produk", cat_options)

    st.markdown(f"<div style='margin: 20px 0; border-bottom: 1px solid {BORDER};'></div>", unsafe_allow_html=True)
    
    # IDENTITAS KELOMPOK
    st.markdown(f"""
        <div style="background-color: {CARD_BG}; padding: 18px 16px; border-radius: 12px; border: 1px solid {BORDER}; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 16px;">
                <span style="background-color: {PRIMARY}; color: #0B1121; padding: 4px 12px; border-radius: 20px; font-size: 10.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px;">🏆 Kelompok 10</span>
            </div>
            <div style="margin-bottom: 12px; border-bottom: 1px dashed rgba(255,255,255,0.1); padding-bottom: 10px;">
                <div style="color: {INK}; font-size: 13px; font-weight: 600; margin-bottom: 2px; line-height: 1.4;">Carlos Qnova Bha'a Gani</div>
                <div style="color: {PRIMARY_SOFT}; font-size: 11px; font-family: monospace;">NIM: 2305551100</div>
            </div>
            <div style="margin-bottom: 12px; border-bottom: 1px dashed rgba(255,255,255,0.1); padding-bottom: 10px;">
                <div style="color: {INK}; font-size: 13px; font-weight: 600; margin-bottom: 2px; line-height: 1.4;">Made Pradnyan Pranata</div>
                <div style="color: {PRIMARY_SOFT}; font-size: 11px; font-family: monospace;">NIM: 2305551107</div>
            </div>
            <div style="margin-bottom: 12px; border-bottom: 1px dashed rgba(255,255,255,0.1); padding-bottom: 10px;">
                <div style="color: {INK}; font-size: 13px; font-weight: 600; margin-bottom: 2px; line-height: 1.4;">I Made Rangga Harikesa Subhiksa</div>
                <div style="color: {PRIMARY_SOFT}; font-size: 11px; font-family: monospace;">NIM: 2305551150</div>
            </div>
            <div style="margin-bottom: 4px;">
                <div style="color: {INK}; font-size: 13px; font-weight: 600; margin-bottom: 2px; line-height: 1.4;">Ni Putu Putri Ayu Antari </div>
                <div style="color: {PRIMARY_SOFT}; font-size: 11px; font-family: monospace;">NIM: 2305551163</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Data Analytics and Visualization Project © 2026")

df = df_raw.copy()
if selected_year != "Total":
    df = df[df['year'] == selected_year]
if selected_category_filter != "Semua Kategori":
    df = df[df['product_category'] == selected_category_filter]

# ======================================================
# 6. HERO HEADER
# ======================================================
total_records = len(df)
badge_year = selected_year if selected_year != "Total" else "Semua Tahun (2021-2023)"
badge_cat = selected_category_filter

st.markdown(f"""
    <div class="hero">
        <div class="hero-content">
            <h1 class="hero-title">Shopnesia Business Performance Report</h1>
            <p class="hero-sub">Global Core Executive Dashboard</p>
            <div class="hero-badges">
                <div class="badge badge-green">
                    <span style="font-size: 8px;">🟢</span> Sistem Online
                </div>
                <div class="badge">
                    📊 Total Data: {total_records:,} Baris
                </div>
                <div class="badge">
                    🔍 Filter: {badge_year} | {badge_cat}
                </div>
            </div>
        </div>
        <div class="hero-icon">
            🛍️
        </div>
    </div>
""", unsafe_allow_html=True)

# ======================================================
# 7. HELPER: CHART CARD WRAPPER
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
# 8. TABS
# ======================================================
tab1, tab2, tab3 = st.tabs([
    "📈 Tab 1: Ringkasan Bisnis & Geografi", 
    "👥 Tab 2: Demografi & Kategori Produk", 
    "🔥 Tab 3: Promosi & Loyalitas"
])

# ================= TAB 1 =================
with tab1:
    # 1. SUMMARY METRICS WITH DELTA YoY
    if selected_year != "Total":
        prev_year = str(int(selected_year) - 1)
        df_prev = df_raw[df_raw['year'] == prev_year]
        if selected_category_filter != "Semua Kategori":
            df_prev = df_prev[df_prev['product_category'] == selected_category_filter]
    else:
        df_curr = df_raw[df_raw['year'] == '2023']
        df_prev = df_raw[df_raw['year'] == '2022']
        if selected_category_filter != "Semua Kategori":
            df_curr = df_curr[df_curr['product_category'] == selected_category_filter]
            df_prev = df_prev[df_prev['product_category'] == selected_category_filter]
            
    def get_delta(curr_val, prev_val):
        if prev_val == 0 or pd.isna(prev_val): return None
        pct = ((curr_val - prev_val) / prev_val) * 100
        return f"{pct:+.1f}% YoY"

    curr_rev = df['total_sales'].sum() if selected_year != "Total" else df_curr['total_sales'].sum()
    prev_rev = df_prev['total_sales'].sum()
    rev_delta = get_delta(curr_rev, prev_rev)

    curr_orders = df['order_id'].nunique() if selected_year != "Total" else df_curr['order_id'].nunique()
    prev_orders = df_prev['order_id'].nunique()
    orders_delta = get_delta(curr_orders, prev_orders)

    curr_qty = df['quantity'].sum() if selected_year != "Total" else df_curr['quantity'].sum()
    prev_qty = df_prev['quantity'].sum()
    qty_delta = get_delta(curr_qty, prev_qty)

    curr_rating = df['rating'].mean() if selected_year != "Total" else df_curr['rating'].mean()
    prev_rating = df_prev['rating'].mean()
    rating_delta = f"{curr_rating - prev_rating:+.2f} YoY" if not pd.isna(prev_rating) else None

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="💰 Total Penjualan", value=f"IDR {df['total_sales'].sum():,.0f}", delta=rev_delta)
    with m2:
        st.metric(label="🧾 Total Transaksi", value=f"{df['order_id'].nunique():,}", delta=orders_delta)
    with m3:
        st.metric(label="📦 Volume Terjual", value=f"{int(df['quantity'].sum()):,}", delta=qty_delta)
    with m4:
        st.metric(label="⭐ Kepuasan Pelanggan", value=f"{df['rating'].mean():.2f} / 5.0", delta=rating_delta)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. INSIGHT PANEL
    st.markdown(f"""
        <div style="background-color: {CARD_BG}; border-left: 4px solid {ACCENT}; padding: 16px 20px; border-radius: 8px; margin-bottom: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
            <h4 style="color: {INK}; margin-top: 0; margin-bottom: 8px; font-size: 15px; font-weight: 700;">💡 Executive Insights</h4>
            <p style="color: {SUBTEXT}; margin: 0; font-size: 13px; line-height: 1.6;">
                <b>Dominasi Geografis:</b> Pulau Jawa terus menunjukkan hegemoni pasar dengan kontribusi terbesar dari DKI Jakarta, Jawa Tengah, dan Jawa Timur.<br>
                <b>Pergerakan Musiman:</b> Terlihat tren lonjakan pada akhir tahun (Q4), menandakan promosi musiman bekerja dengan baik. Pastikan inventaris cukup mengantisipasi *spike* ini.
            </p>
        </div>
        <div style="background-color: #1A2740; padding: 8px 14px; border-radius: 6px; display: inline-block; font-size: 11.5px; color: {PRIMARY_SOFT}; border: 1px solid {BORDER}; margin-bottom: 24px;">
            <b>ℹ️ Panduan Singkatan:</b> &nbsp; <b>k</b> = Ribu &nbsp;|&nbsp; <b>M</b> = Juta &nbsp;|&nbsp; <b>G</b> = Miliar &nbsp;|&nbsp; <b>YoY</b> = <i>Year-over-Year</i> (Dibandingkan Tahun Sebelumnya)
        </div>
    """, unsafe_allow_html=True)
    
    # 3. TREN PENJUALAN
    col1, col2 = st.columns(2)
    with col1:
        chart_card_open("Tren Penjualan Tahunan")
        yearly_sales = df.groupby('year')['total_sales'].sum().reset_index()
        fig1 = px.bar(yearly_sales, x='year', y='total_sales', text_auto='.2s')
        fig1.update_traces(marker=dict(color=yearly_sales['total_sales'], colorscale=["#1E40AF", PRIMARY]),
                           textfont_size=12, textposition="outside", cliponaxis=False)
        st.plotly_chart(style_bar(fig1, 0.4), use_container_width=True, theme=None)
        chart_card_close()

    with col2:
        chart_card_open("Tren Penjualan Bulanan & Moving Average")
        monthly_sales = df.groupby('month_year')['total_sales'].sum().reset_index().sort_values('month_year')
        monthly_sales['Moving Average (3M)'] = monthly_sales['total_sales'].rolling(window=3, min_periods=1).mean()
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=monthly_sales['month_year'], y=monthly_sales['total_sales'],
            fill='tozeroy', mode='lines+markers', name='Penjualan Aktual',
            line=dict(color=PRIMARY_SOFT, width=2), fillcolor="rgba(72, 202, 228, 0.15)",
            marker=dict(size=6, color=PRIMARY)
        ))
        fig2.add_trace(go.Scatter(
            x=monthly_sales['month_year'], y=monthly_sales['Moving Average (3M)'],
            mode='lines', name='Tren (3M MA)',
            line=dict(color=ACCENT, width=2.5, dash='dot')
        ))
        fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0), 
                           legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=INK, size=11)))
        st.plotly_chart(fig2, use_container_width=True, theme=None)
        chart_card_close()

# 4. GEOGRAFI
    st.markdown("<div class='section-label'>Sebaran Geografis (Gradient Profiling)</div>", unsafe_allow_html=True)
    
    # Hitung total untuk persentase hover
    total_sales_all = df['total_sales'].sum()
    
    col9, col10 = st.columns(2)
    with col9:
        chart_card_open("Top 10 Provinsi Kontributor Penjualan")   
        province_sales = df.groupby('customer_province')['total_sales'].sum().reset_index()
        province_sales = province_sales.sort_values(by='total_sales', ascending=True).tail(10)
        province_sales['pct'] = (province_sales['total_sales'] / total_sales_all * 100).round(1)
        
        fig9 = px.bar(province_sales, x='total_sales', y='customer_province', orientation='h', text_auto='.2s', 
                      color='total_sales', color_continuous_scale=["#1E40AF", PRIMARY])
    
        fig9.update_traces(
            textfont_size=11, textposition="outside", cliponaxis=False,
            hovertemplate="<b>DATA PROVINSI: %{y}</b><br>" +
                          "Total Penjualan: %{x:,.0f}<br>" +
                          "Kontribusi: %{customdata}% dari Total Nasional<br>" +
                          "<extra></extra>",
            customdata=province_sales['pct']
        )
        fig9.update_coloraxes(showscale=False)
        st.plotly_chart(style_bar(fig9, 0.7), use_container_width=True, theme=None)
        chart_card_close()

    with col10:
        chart_card_open("Top 10 Kota Kontributor Penjualan")
        city_sales = df.groupby('customer_city')['total_sales'].sum().reset_index()
        city_sales = city_sales.sort_values(by='total_sales', ascending=True).tail(10)
        
        # Kolom persen untuk dipakai di hover
        city_sales['pct'] = (city_sales['total_sales'] / total_sales_all * 100).round(1)
        
        fig10 = px.bar(city_sales, x='total_sales', y='customer_city', orientation='h', text_auto='.2s', 
                       color='total_sales', color_continuous_scale=["#9A3412", ACCENT])
        
        # Kustomisasi Hover
        fig10.update_traces(
            textfont_size=11, textposition="outside", cliponaxis=False,
            hovertemplate="<b>DATA KOTA: %{y}</b><br>" +
                          "Total Penjualan: %{x:,.0f}<br>" +
                          "Kontribusi: %{customdata}% dari Total Nasional<br>" +
                          "<extra></extra>",
            customdata=city_sales['pct']
        )
        fig10.update_coloraxes(showscale=False)
        st.plotly_chart(style_bar(fig10, 0.7), use_container_width=True, theme=None)
        chart_card_close()

# ================= TAB 2 =================
with tab2:
    # INSIGHT PANEL TAB 2
    st.markdown(f"""
        <div style="background-color: {CARD_BG}; border-left: 4px solid {PRIMARY_SOFT}; padding: 16px 20px; border-radius: 8px; margin-bottom: 24px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
            <h4 style="color: {INK}; margin-top: 0; margin-bottom: 8px; font-size: 15px; font-weight: 700;">💡 Executive Insights (Demografi & Kategori)</h4>
            <p style="color: {SUBTEXT}; margin: 0; font-size: 13px; line-height: 1.6;">
                <b>Dominasi Demografi Gen Z & Millenials:</b> Kelompok usia 20-39 tahun mendominasi lebih dari 85% total basis pengguna. Penyesuaian gaya kampanye (*youth-centric*) sangat direkomendasikan.<br>
                <b>Behavioral Symmetry (Simetri Perilaku):</b> Meskipun volume total transaksi pria dan wanita berbeda, proporsi isi keranjang mereka (*basket composition*) nyaris identik (cth: Kategori Atasan stabil di ~30%). <br>
                <b>Rekomendasi Aksi:</b> Lakukan standarisasi rasio inventaris (30% Atasan, 25% Bawahan, dst) untuk kedua gender. Ini akan meminimalisir risiko penumpukan stok (*dead stock*).
            </p>
        </div>
    """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        chart_card_open("Segmentasi Konsumen Berdasarkan Usia")
        age_profile = df.groupby('age_group').size().reset_index(name='Jumlah')
        age_profile.rename(columns={'age_group': 'Profil Usia'}, inplace=True)
        # Urutkan berdasarkan kelompok usia secara logis
        age_profile = age_profile.sort_values('Profil Usia') 
        
        fig3 = px.pie(age_profile, names='Profil Usia', values='Jumlah', hole=0.65,
                      color_discrete_sequence=CATEGORICAL_SEQUENCE)
        fig3.update_traces(textfont_size=11, marker=dict(line=dict(color=BG, width=2)))
        st.plotly_chart(fig3, use_container_width=True, theme=None)
        chart_card_close()

    with col4:
        chart_card_open("Distribusi Volume Pembelian Kategori Produk")
        category_sales = df['product_category'].value_counts().reset_index()
        category_sales.columns = ['Kategori', 'Jumlah']
        category_sales = category_sales.sort_values('Jumlah', ascending=True)
        
        fig4 = px.bar(category_sales, x='Jumlah', y='Kategori', orientation='h', text_auto='.2s',
                      color='Jumlah', color_continuous_scale=["#1E40AF", PRIMARY_SOFT])
        fig4.update_coloraxes(showscale=False)
        fig4.update_traces(textfont_size=11, textposition="outside", cliponaxis=False)
        st.plotly_chart(style_bar(fig4, 0.7), use_container_width=True, theme=None)
        chart_card_close()

    col5, col6 = st.columns(2)
    with col5:
        chart_card_open("Preferensi Kategori Berdasarkan Gender")
        gender_category = df.groupby(['product_category', 'customer_gender']).size().reset_index(name='Jumlah')
        # Urutkan kategori berdasarkan total agar lebih rapi
        cat_order = gender_category.groupby('product_category')['Jumlah'].sum().sort_values(ascending=False).index
        fig5 = px.bar(gender_category, x='product_category', y='Jumlah', color='customer_gender', text_auto='.2s',
                      barmode='group', color_discrete_map=GENDER_MAP, category_orders={'product_category': cat_order})
        fig5.update_traces(textfont_size=11, textposition='outside', cliponaxis=False)
        st.plotly_chart(style_bar(fig5, 0.3), use_container_width=True, theme=None)
        chart_card_close()

    with col6:
        chart_card_open("Behavioral Symmetry: Komposisi Keranjang Pria vs Wanita")
        gender_cat_prop = df.groupby(['customer_gender', 'product_category'])['quantity'].sum().reset_index()
        fig6 = px.sunburst(gender_cat_prop, path=['customer_gender', 'product_category'], values='quantity',
                           color='customer_gender', color_discrete_map=GENDER_MAP)
        fig6.update_traces(marker=dict(line=dict(color=BG, width=1.5)))
        st.plotly_chart(fig6, use_container_width=True, theme=None)
        chart_card_close()

# ================= TAB 3 =================
with tab3:
    # INSIGHT PANEL TAB 3
    st.markdown(f"""
        <div style="background-color: {CARD_BG}; border-left: 4px solid {ACCENT_SOFT}; padding: 16px 20px; border-radius: 8px; margin-bottom: 24px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
            <h4 style="color: {INK}; margin-top: 0; margin-bottom: 8px; font-size: 15px; font-weight: 700;">💡 Executive Insights (Promosi & Loyalitas)</h4>
            <p style="color: {SUBTEXT}; margin: 0; font-size: 13px; line-height: 1.6;">
                <b>Efektivitas Diskon:</b> Terdapat korelasi positif di mana diskon yang lebih besar mampu mendorong volume pembelian per pesanan, namun dampaknya terhadap Rating relatif stabil (tidak selalu menjamin rating bintang 5).<br>
                <b>Status Retensi:</b> Sangat disayangkan bahwa basis pelanggan masih didominasi kuat oleh *One-time Buyer*. Memperkuat program *Customer Loyalty* dan kampanye *retargeting* (contoh: promo email khusus pelanggan lama) sangat krusial untuk meningkatkan rasio *Repeat Buyer*.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col7, col8 = st.columns(2)
    with col7:
        chart_card_open("Dampak Rentang Diskon Terhadap Kuantitas")
        def discount_bin(pct):
            if pct == 0: return '1. Tanpa Diskon'
            elif pct <= 10: return '2. Diskon 1-10%'
            elif pct <= 20: return '3. Diskon 11-20%'
            else: return '4. Diskon >20%'
            
        df_discount = df.copy()
        df_discount['discount_group'] = df_discount['discount_percent'].apply(discount_bin)
        # Hilangkan grouping tahun, murni ambil rata-rata kuantitas dari periode yang difilter
        discount_qty = df_discount.groupby('discount_group')['quantity'].mean().reset_index()
        discount_qty = discount_qty.sort_values('discount_group')
        # Buang prefix angka untuk estetika label
        discount_qty['Label'] = discount_qty['discount_group'].apply(lambda x: x.split('. ')[1])
        
        fig7 = px.bar(discount_qty, x='Label', y='quantity', text_auto='.1f',
                      color='quantity', color_continuous_scale=["#1E40AF", PRIMARY])
        fig7.update_coloraxes(showscale=False)
        fig7.update_traces(textfont_size=12, textposition="outside", cliponaxis=False)
        st.plotly_chart(style_bar(fig7, 0.6), use_container_width=True, theme=None)
        chart_card_close()

    with col8:
        chart_card_open("Korelasi Persentase Diskon terhadap Rating")
        discount_rating = df.groupby('discount_percent')['rating'].mean().reset_index().sort_values('discount_percent')
        
        # Scatter/Line Chart yang benar: X = Persentase Diskon, Y = Rating
        fig8 = go.Figure()
        fig8.add_trace(go.Scatter(
            x=discount_rating['discount_percent'], y=discount_rating['rating'],
            mode='lines+markers', name='Rata-rata Rating',
            line=dict(color=ACCENT, width=2.5),
            marker=dict(size=7, color=ACCENT_SOFT)
        ))
        
        # Fokuskan range Y (Rating) agar fluktuasinya terlihat jelas
        y_min = max(1.0, discount_rating['rating'].min() - 0.2)
        y_max = min(5.0, discount_rating['rating'].max() + 0.2)
        fig8.update_layout(margin=dict(l=0, r=0, t=10, b=0),
                           xaxis_title="Besaran Diskon (%)", yaxis_title="Rata-rata Rating (⭐)",
                           yaxis=dict(range=[y_min, y_max], showgrid=True), xaxis=dict(showgrid=True))
                           
        st.plotly_chart(fig8, use_container_width=True, theme=None)
        chart_card_close()
        
    col11, col12 = st.columns(2)
    with col11:
        chart_card_open("Top 5 Pelanggan Teratas (Total Transaksi)")
        top_customers = df.groupby('customer_id')['total_sales'].sum().reset_index()
        top_customers = top_customers.sort_values(by='total_sales', ascending=True).tail(5)
        # Sederhanakan ID Customer agar rapi (ambil 8 karakter)
        top_customers['Customer'] = top_customers['customer_id'].apply(lambda x: str(x)[:8] + '...')
        
        fig11 = px.bar(top_customers, x='total_sales', y='Customer', orientation='h', text_auto='.2s',
                       color='total_sales', color_continuous_scale=["#9A3412", ACCENT])
        fig11.update_coloraxes(showscale=False)
        fig11.update_traces(textfont_size=11, textposition="outside", cliponaxis=False)
        st.plotly_chart(style_bar(fig11, 0.5), use_container_width=True, theme=None)
        chart_card_close()
        
    with col12:
        chart_card_open("Rasio Retensi Pelanggan (Loyalitas)")
        cust_order_counts = df.groupby('customer_id')['order_id'].nunique().reset_index()
        cust_order_counts['Buyer Type'] = cust_order_counts['order_id'].apply(lambda x: 'Repeat Buyer (>1 Order)' if x > 1 else 'One-time Buyer')
        retention_data = cust_order_counts['Buyer Type'].value_counts().reset_index()
        retention_data.columns = ['Tipe Pembeli', 'Jumlah']
        
        fig12 = px.pie(retention_data, names='Tipe Pembeli', values='Jumlah', hole=0.65,
                       color_discrete_map={'Repeat Buyer (>1 Order)': PRIMARY, 'One-time Buyer': PRIMARY_SOFT})
        fig12.update_traces(textfont_size=11, marker=dict(line=dict(color=BG, width=2)))
        st.plotly_chart(fig12, use_container_width=True, theme=None)
        chart_card_close()