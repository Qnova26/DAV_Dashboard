# 🛍️ Shopnesia Business Performance Report - Executive Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://shopnesia-dashboard-10.streamlit.app/)

Selamat datang di repositori **Shopnesia Executive Dashboard**. Proyek ini merupakan dashboard analitik bisnis interaktif yang dibangun menggunakan Python (Streamlit & Plotly) untuk keperluan evaluasi performa bisnis dari platform e-commerce fiktif *Shopnesia*.

> **🔗 Link Live Dashboard:** [https://shopnesia-dashboard-10.streamlit.app/](https://shopnesia-dashboard-10.streamlit.app/)

---

## 🏆 Identitas Kelompok 10
Proyek ini dikembangkan untuk memenuhi tugas mata kuliah **Data Analytics and Visualization**, oleh:

1. **Carlos Qnova Bha'a Gani** (2305551100)
2. **Made Pradnyan Pranata** (2305551107)
3. **I Made Rangga Harikesa Subhiksa** (2305551150)
4. **Ni Putu Putri Ayu Antari** (2305551163)

---

## 🎯 Target Pengguna (Target Audience)

Dashboard ini dirancang secara khusus sebagai **Strategic Executive Dashboard**. Pengguna utama yang disasar adalah **Manajer Pemasaran (Chief Marketing Officer / CMO)** atau jajaran *C-Level Executives*. 

**Mengapa peruntukan ini yang paling tepat?**
- **Fokus pada Gambaran Besar (*High-Level*):** Eksekutif membutuhkan ringkasan data yang cepat dan padat (*compact single-screen view*) untuk memantau performa bisnis secara keseluruhan (Total Pendapatan, Tren Bulanan, dan Peta Dominasi Geografis) tanpa harus menelusuri data operasional mentah secara manual.
- **Berorientasi pada Strategi Promosi & Retensi:** Analisis mengenai dominasi usia pembeli (Gen Z & Millenials), efektivitas program diskon, dan persentase retensi pelanggan (*Repeat Buyer* vs *One-time Buyer*) adalah "makanan sehari-hari" bagi manajer pemasaran. Metrik ini krusial untuk mengambil keputusan terkait alokasi *budget* iklan (*Ads*), menargetkan promosi musiman, dan merancang program loyalitas pelanggan yang lebih tepat sasaran.

---

## 🚀 Fitur Utama Dashboard

Dashboard ini dirancang secara *compact* (single-screen view) agar *insight* mudah diakses secara cepat, terbagi dalam 3 pilar analitik utama:

1. 📈 **Ringkasan Bisnis & Geografi (Tab 1)**
   - Metrik Utama (Total Penjualan, Transaksi, Volume Terjual, Rating Kepuasan) dengan perbandingan metrik tahunan (YoY).
   - Tren Penjualan Bulanan dengan *Moving Average* (3M).
   - Profil Geografis: *Top 10* Provinsi dan Kota penyumbang penjualan terbesar.

2. 👥 **Demografi & Kategori Produk (Tab 2)**
   - Segmentasi usia pengguna (Gen Z, Millenials, dsb).
   - Volume pembelian spesifik di setiap kategori produk.
   - Analisis preferensi silang (simetri perilaku) kategori produk berdasarkan gender.

3. 🔥 **Promosi & Loyalitas (Tab 3)**
   - Korelasi antara rentang diskon dengan kuantitas yang terjual.
   - Analisis efektivitas diskon terhadap rata-rata *rating* pelanggan (⭐).
   - Metrik Retensi Pelanggan (*Repeat Buyer* vs *One-time Buyer*).

## 🛠️ Teknologi yang Digunakan
- **[Python](https://www.python.org/)** (Bahasa Pemrograman)
- **[Streamlit](https://streamlit.io/)** (Web Dashboard Framework)
- **[Plotly](https://plotly.com/python/)** (Interactive Visualizations)
- **[Pandas](https://pandas.pydata.org/)** (Data Manipulation)

---

## 💻 Cara Menjalankan di Komputer Lokal

Jika Anda ingin menjalankan aplikasi ini di komputer Anda sendiri:

1. **Clone repositori ini:**
   ```bash
   git clone https://github.com/Qnova26/DAV_Dashboard.git
   cd DAV_Dashboard
   ```

2. **Instal dependensi library:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan aplikasi Streamlit:**
   ```bash
   streamlit run shopnesia_dashboard.py
   ```
   *Aplikasi akan otomatis terbuka di browser pada `http://localhost:8501`*

---
*© 2026 Data Analytics and Visualization Project - Kelompok 10.*
