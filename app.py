import streamlit as st
import pandas as pd
import plotly.express as px

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="ShopNesia Analytics Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 ShopNesia Executive Dashboard (2021-2023)")
st.markdown("Dashboard interaktif untuk menganalisis performa penjualan, demografi, dan loyalitas pelanggan.")

# 2. FUNGSI LOAD DATA (Agar data di-cache dan tidak loading berulang kali)
@st.cache_data
def load_data():
    df = pd.read_csv('shopnesia_all_data.csv')
    # Pastikan order_date terbaca sebagai format tanggal (datetime)
    df['order_date'] = pd.to_datetime(df['order_date'])
    # Ekstrak Tahun dan Bulan-Tahun untuk mempermudah analisis waktu
    df['Year'] = df['order_date'].dt.year
    df['Month_Year'] = df['order_date'].dt.to_period('M').astype(str)
    return df

df = load_data()

# 3. SIDEBAR FILTER
st.sidebar.header("⚙️ Filter Data")
# Menambahkan opsi 'Semua Tahun' di awal list
tahun_options = ['Semua Tahun'] + list(df['Year'].unique())
selected_year = st.sidebar.selectbox("Pilih Tahun:", tahun_options)

# Terapkan filter ke dataframe
if selected_year != 'Semua Tahun':
    df_filtered = df[df['Year'] == selected_year]
else:
    df_filtered = df.copy()

# 4. KPI SCORECARDS (Metrik Utama di Bagian Atas)
col1, col2, col3, col4 = st.columns(4)
total_transaksi = len(df_filtered)
total_revenue = df_filtered['final_price'].sum()
rata_rating = df_filtered['rating'].mean()
total_pelanggan = df_filtered['customer_id'].nunique()

col1.metric("Total Transaksi", f"{total_transaksi:,.0f}")
col2.metric("Total Pendapatan", f"Rp {total_revenue/1e9:,.2f} Miliar")
col3.metric("Rata-rata Rating", f"{rata_rating:.2f} ⭐")
col4.metric("Total Pelanggan Unik", f"{total_pelanggan:,.0f}")

st.markdown("---")

# 5. PEMBAGIAN TAB
tab1, tab2, tab3 = st.tabs([
    "📈 Ringkasan Bisnis & Geografi", 
    "👥 Demografi & Performa Produk", 
    "🎁 Promosi & Loyalitas"
])

# ==========================================
# ISI TAB 1: RINGKASAN BISNIS & GEOGRAFI
# ==========================================
with tab1:
    st.subheader("Tren Penjualan Waktu")
    col_waktu1, col_waktu2 = st.columns(2)
    
    with col_waktu1:
        # Chart 1: Penjualan Per Tahun (Bar Chart)
        transaksi_per_tahun = df.groupby('Year').size().reset_index(name='Total')
        fig_tahun = px.bar(transaksi_per_tahun, x='Year', y='Total', 
                           title="Total Transaksi per Tahun", text_auto=True, color_discrete_sequence=['#4C72B0'])
        fig_tahun.update_xaxes(type='category') # Agar tahun tidak berkoma
        st.plotly_chart(fig_tahun, use_container_width=True)
        
    with col_waktu2:
        # Chart 2: Penjualan Per Bulan (Line Chart)
        transaksi_per_bulan = df_filtered.groupby('Month_Year').size().reset_index(name='Total')
        fig_bulan = px.line(transaksi_per_bulan, x='Month_Year', y='Total', markers=True,
                            title="Tren Transaksi Bulanan", color_discrete_sequence=['#DD8452'])
        st.plotly_chart(fig_bulan, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Kinerja Wilayah (Geografi)")
    col_geo1, col_geo2 = st.columns(2)
    
    with col_geo1:
        # Chart 3: Top 10 Provinsi (Horizontal Bar Chart)
        top_provinsi = df_filtered['customer_province'].value_counts().head(10).reset_index()
        top_provinsi.columns = ['Provinsi', 'Total Transaksi']
        fig_prov = px.bar(top_provinsi, x='Total Transaksi', y='Provinsi', orientation='h',
                          title="Top 10 Provinsi dengan Transaksi Terbanyak", color_discrete_sequence=['#55A868'])
        fig_prov.update_layout(yaxis={'categoryorder':'total ascending'}) # Urutkan dari terbesar di atas
        st.plotly_chart(fig_prov, use_container_width=True)
        
    with col_geo2:
        # Chart 4: Top 10 Kota (Horizontal Bar Chart)
        top_kota = df_filtered['customer_city'].value_counts().head(10).reset_index()
        top_kota.columns = ['Kota', 'Total Transaksi']
        fig_kota = px.bar(top_kota, x='Total Transaksi', y='Kota', orientation='h',
                          title="Top 10 Kota dengan Transaksi Terbanyak", color_discrete_sequence=['#C44E52'])
        fig_kota.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_kota, use_container_width=True)

# Placeholder untuk Tab 2 dan Tab 3
with tab2:
    st.info("Visualisasi Demografi (Usia & Gender) dan Performa Kategori Produk akan diletakkan di sini.")

with tab3:
    st.info("Visualisasi Dampak Diskon dan Analisis Pelanggan Loyal akan diletakkan di sini.")