# Tugas Biostatistik - Analisis Data Time Series

## 📋 Deskripsi

Proyek analisis biostatistik komprehensif untuk data time series medis yang membandingkan kelompok normal dan abnormal. Analisis mencakup statistik deskriptif, uji normalitas, uji homogenitas varians, uji perbedaan kelompok, effect size, dan visualisasi data lengkap.

## 📁 File Proyek

- `data biostat.csv` - Dataset penelitian (54 subjek, 682 titik pengukuran)
- `tugas_biostat.py` - Script Python untuk analisis lengkap
- `paper_biostatistik.tex` - Template paper IEEE dalam Bahasa Indonesia
- `README_INSTRUKSI.md` - **BACA INI UNTUK INSTRUKSI LENGKAP!**

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install pandas numpy matplotlib seaborn scipy
```

### 2. Jalankan Analisis

```bash
python tugas_biostat.py
```

### 3. Output yang Dihasilkan

Setelah running, Anda akan mendapatkan:
- 📊 **3 file visualisasi PNG** (grafik analisis)
- 📄 **3 file CSV** (hasil statistik)
- 💬 **Output teks lengkap** di terminal

## 📖 Dokumentasi Lengkap

**Untuk instruksi detail cara menggunakan proyek ini, BACA:**

👉 **[README_INSTRUKSI.md](README_INSTRUKSI.md)**

File tersebut berisi:
- Instalasi lengkap
- Cara running kode
- Cara menggunakan output untuk paper
- Troubleshooting
- FAQ

## 🎯 Fitur Analisis

✅ Statistik deskriptif per kelompok
✅ Uji normalitas (Shapiro-Wilk)
✅ Uji homogenitas varians (Levene's test)
✅ Uji perbedaan kelompok (t-test/Mann-Whitney U)
✅ Effect size (Cohen's d)
✅ Confidence interval 95%
✅ Visualisasi lengkap (6+ grafik)
✅ Export hasil ke CSV
✅ Template paper LaTeX dalam Bahasa Indonesia

## 📊 Output Visualisasi

Kode akan menghasilkan visualisasi meliputi:
1. Boxplot perbandingan kelompok
2. Histogram distribusi
3. Violin plot
4. Bar plot dengan error bars
5. Q-Q plot untuk uji normalitas
6. Time series sample
7. Heatmap data time series
8. Scatter plot per subjek

## 📝 Cara Menulis Paper

1. Jalankan analisis Python
2. Simpan output teks
3. Edit file `paper_biostatistik.tex`
4. Isi nilai-nilai dari output ke dalam tabel LaTeX
5. Upload ke Overleaf dan compile

## 🔧 Requirements

- Python 3.7+
- pandas
- numpy
- matplotlib
- seaborn
- scipy
- LaTeX (untuk compile paper)

## 📞 Support

Untuk bantuan lebih lanjut, baca file **README_INSTRUKSI.md** yang berisi panduan lengkap.

---

**Dibuat untuk keperluan analisis biostatistik**