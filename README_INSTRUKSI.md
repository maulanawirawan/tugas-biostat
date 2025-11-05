# Instruksi Lengkap - Analisis Biostatistik

## Daftar Isi
1. [Deskripsi Proyek](#deskripsi-proyek)
2. [Struktur File](#struktur-file)
3. [Persyaratan Sistem](#persyaratan-sistem)
4. [Instalasi](#instalasi)
5. [Cara Menjalankan Analisis](#cara-menjalankan-analisis)
6. [Output yang Dihasilkan](#output-yang-dihasilkan)
7. [Cara Menggunakan Output untuk Paper](#cara-menggunakan-output-untuk-paper)
8. [Penjelasan Kode](#penjelasan-kode)
9. [Troubleshooting](#troubleshooting)

---

## Deskripsi Proyek

Proyek ini berisi analisis biostatistik lengkap untuk data time series medis yang membandingkan kelompok normal dan abnormal. Analisis mencakup:
- Statistik deskriptif
- Uji normalitas (Shapiro-Wilk)
- Uji homogenitas varians (Levene's test)
- Uji perbedaan kelompok (t-test/Mann-Whitney U)
- Effect size (Cohen's d)
- Confidence interval
- Visualisasi data

## Struktur File

```
tugas-biostat/
│
├── data biostat.csv              # Dataset (54 subjek, 682 titik pengukuran)
├── tugas_biostat.py             # Script Python untuk analisis
├── paper_biostatistik.tex       # Template paper dalam Bahasa Indonesia
├── README_INSTRUKSI.md          # File ini (instruksi lengkap)
│
└── Output (akan dibuat setelah running):
    ├── hasil_analisis_biostatistik.png    # Visualisasi utama (6 grafik)
    ├── heatmap_timeseries.png             # Heatmap data time series
    ├── scatter_plot_subjects.png          # Scatter plot per subjek
    ├── statistik_deskriptif.csv           # Statistik deskriptif per kelompok
    ├── hasil_uji_statistik.csv            # Hasil semua uji statistik
    └── data_dengan_mean.csv               # Data lengkap dengan kolom mean
```

---

## Persyaratan Sistem

### Software yang Dibutuhkan:
1. **Python 3.7 atau lebih baru**
2. **pip** (Python package installer)
3. **Text editor** atau IDE (VS Code, PyCharm, dll.)
4. **LaTeX** untuk compile dokumen paper (Overleaf atau TeX distribution lokal)

### Python Libraries yang Dibutuhkan:
- pandas
- numpy
- matplotlib
- seaborn
- scipy

---

## Instalasi

### Langkah 1: Cek Instalasi Python

Buka terminal/command prompt dan jalankan:

```bash
python --version
```

atau

```bash
python3 --version
```

Pastikan versi Python adalah 3.7 atau lebih baru.

### Langkah 2: Install Libraries yang Dibutuhkan

Jalankan perintah berikut di terminal:

```bash
pip install pandas numpy matplotlib seaborn scipy
```

atau jika menggunakan Python 3:

```bash
pip3 install pandas numpy matplotlib seaborn scipy
```

### Verifikasi Instalasi

Untuk memverifikasi bahwa semua library terinstall dengan benar:

```bash
python -c "import pandas, numpy, matplotlib, seaborn, scipy; print('Semua library berhasil diinstall!')"
```

---

## Cara Menjalankan Analisis

### Metode 1: Menggunakan Terminal/Command Prompt

1. **Buka Terminal/Command Prompt**

2. **Navigasi ke Folder Proyek**
   ```bash
   cd /path/to/tugas-biostat
   ```

   Contoh di Windows:
   ```bash
   cd C:\Users\YourName\tugas-biostat
   ```

   Contoh di Mac/Linux:
   ```bash
   cd ~/tugas-biostat
   ```

3. **Jalankan Script Python**
   ```bash
   python tugas_biostat.py
   ```

   atau

   ```bash
   python3 tugas_biostat.py
   ```

4. **Tunggu Hingga Selesai**
   - Script akan menampilkan output teks di terminal
   - Proses biasanya memakan waktu 10-30 detik
   - Anda akan melihat progress analisis secara real-time

### Metode 2: Menggunakan IDE (VS Code, PyCharm, dll.)

1. **Buka folder proyek di IDE**
2. **Buka file `tugas_biostat.py`**
3. **Klik tombol Run/Play** atau tekan **F5**
4. **Lihat output di console/terminal IDE**

### Metode 3: Menggunakan Jupyter Notebook

1. **Install Jupyter** (jika belum):
   ```bash
   pip install jupyter
   ```

2. **Jalankan Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```

3. **Buat notebook baru** dan copy-paste kode dari `tugas_biostat.py`

4. **Jalankan cell-by-cell** untuk melihat output bertahap

---

## Output yang Dihasilkan

Setelah menjalankan script, Anda akan mendapatkan:

### 1. Output Teks di Terminal

Output teks akan menampilkan 13 bagian analisis:

```
[1] LOADING DATA
[2] INFORMASI DATASET
[3] DISTRIBUSI LABEL
[4] STATISTIK DESKRIPTIF PER KELOMPOK
[5] ANALISIS RATA-RATA PER SUBJEK
[6] UJI NORMALITAS (SHAPIRO-WILK TEST)
[7] UJI HOMOGENITAS VARIANS (LEVENE'S TEST)
[8] UJI HIPOTESIS PERBEDAAN DUA KELOMPOK
[9] EFFECT SIZE (COHEN'S D)
[10] CONFIDENCE INTERVAL (95%)
[11] RINGKASAN HASIL ANALISIS
[12] MEMBUAT VISUALISASI
[13] EXPORT HASIL ANALISIS
```

**PENTING:** Catat semua nilai numerik yang muncul di output terminal. Nilai-nilai ini akan Anda masukkan ke dalam dokumen paper.

### 2. File Grafik (PNG)

- **hasil_analisis_biostatistik.png**: Berisi 6 visualisasi dalam 1 gambar
  - Boxplot perbandingan
  - Histogram distribusi
  - Violin plot
  - Bar plot dengan error bars
  - Q-Q plot untuk normalitas
  - Contoh time series

- **heatmap_timeseries.png**: Heatmap menunjukkan pola temporal data

- **scatter_plot_subjects.png**: Scatter plot rata-rata per subjek

### 3. File CSV

- **statistik_deskriptif.csv**: Ringkasan statistik deskriptif
- **hasil_uji_statistik.csv**: Hasil semua uji hipotesis
- **data_dengan_mean.csv**: Dataset asli ditambah kolom mean value

---

## Cara Menggunakan Output untuk Paper

### Langkah 1: Simpan Output Terminal

**Cara menyimpan output ke file teks:**

Di Windows:
```bash
python tugas_biostat.py > hasil_output.txt
```

Di Mac/Linux:
```bash
python3 tugas_biostat.py > hasil_output.txt
```

Atau copy-paste manual dari terminal ke text editor.

### Langkah 2: Ekstrak Nilai untuk Tabel

Buka file `hasil_output.txt` dan cari nilai-nilai berikut:

#### Untuk Tabel Distribusi Label:
```
[3] DISTRIBUSI LABEL
  normal          : XX subjek (XX.XX%)
  abnormal        : XX subjek (XX.XX%)
```

#### Untuk Tabel Statistik Deskriptif:
```
[4] STATISTIK DESKRIPTIF PER KELOMPOK

Kelompok: NORMAL
  Rata-rata (mean)     : XXXX.XXXX
  Median               : XXXX.XXXX
  Standar deviasi      : XXXX.XXXX
  ... (dan seterusnya)

Kelompok: ABNORMAL
  Rata-rata (mean)     : XXXX.XXXX
  ... (dan seterusnya)
```

#### Untuk Tabel Uji Normalitas:
```
[6] UJI NORMALITAS (SHAPIRO-WILK TEST)

NORMAL:
  Statistik W        : X.XXXXXX
  P-value            : X.XXXXXX
  Kesimpulan         : ...

ABNORMAL:
  Statistik W        : X.XXXXXX
  P-value            : X.XXXXXX
  Kesimpulan         : ...
```

#### Untuk Tabel Uji Homogenitas:
```
[7] UJI HOMOGENITAS VARIANS (LEVENE'S TEST)

Statistik Levene     : X.XXXXXX
P-value              : X.XXXXXX
Kesimpulan           : ...
```

#### Untuk Tabel Uji Perbedaan:
```
[8] UJI HIPOTESIS PERBEDAAN DUA KELOMPOK

Metode: [Nama Metode]
Statistik [t/U]      : X.XXXXXX
P-value              : X.XXXXXX
Kesimpulan           : ...
```

#### Untuk Effect Size:
```
[9] EFFECT SIZE (COHEN'S D)

Cohen's d            : X.XXXXXX
Interpretasi         : [Kecil/Sedang/Besar]
```

#### Untuk Confidence Interval:
```
[10] CONFIDENCE INTERVAL (95%)

NORMAL:
  Mean               : XXXX.XXXX
  95% CI             : [XXXX.XXXX, XXXX.XXXX]

ABNORMAL:
  Mean               : XXXX.XXXX
  95% CI             : [XXXX.XXXX, XXXX.XXXX]
```

### Langkah 3: Edit File LaTeX

1. **Buka file `paper_biostatistik.tex`** di text editor atau Overleaf

2. **Cari semua tag `[OUTPUT]` dan `[ISI ...]`** dalam dokumen

3. **Ganti dengan nilai aktual** dari output yang Anda simpan

   Contoh:
   ```latex
   % SEBELUM:
   Normal & [OUTPUT] & [OUTPUT] \\

   % SESUDAH:
   Normal & 30 & 55.56 \\
   ```

4. **Upload gambar ke Overleaf** (atau letakkan di folder yang sama jika compile lokal):
   - hasil_analisis_biostatistik.png
   - heatmap_timeseries.png
   - scatter_plot_subjects.png

5. **Lengkapi bagian interpretasi** yang ditandai dengan `[JELASKAN ...]`

### Langkah 4: Compile Dokumen LaTeX

**Di Overleaf:**
1. Upload file .tex dan gambar-gambar
2. Klik "Recompile"
3. Download PDF

**Di LaTeX lokal:**
```bash
pdflatex paper_biostatistik.tex
bibtex paper_biostatistik
pdflatex paper_biostatistik.tex
pdflatex paper_biostatistik.tex
```

---

## Penjelasan Kode

### Struktur Kode

Kode terbagi dalam 11 bagian utama:

1. **Import Libraries**: Import semua library yang dibutuhkan
2. **Loading Data**: Membaca file CSV
3. **Statistik Deskriptif**: Menghitung mean, median, std, dll.
4. **Rata-rata per Subjek**: Menghitung mean untuk setiap subjek
5. **Uji Normalitas**: Shapiro-Wilk test
6. **Uji Homogenitas**: Levene's test
7. **Uji Perbedaan**: t-test atau Mann-Whitney U
8. **Effect Size**: Cohen's d
9. **Confidence Interval**: CI 95%
10. **Visualisasi**: Membuat grafik
11. **Export**: Simpan hasil ke CSV

### Logika Pemilihan Uji

```
JIKA data normal DAN varians homogen:
    → Gunakan Independent t-test

JIKA data normal DAN varians tidak homogen:
    → Gunakan Welch's t-test

JIKA data tidak normal:
    → Gunakan Mann-Whitney U test
```

### Interpretasi Output

#### P-value:
- **p < 0.05**: Signifikan (tolak H0)
- **p ≥ 0.05**: Tidak signifikan (gagal tolak H0)

#### Cohen's d:
- **|d| < 0.2**: Effect size sangat kecil
- **0.2 ≤ |d| < 0.5**: Effect size kecil
- **0.5 ≤ |d| < 0.8**: Effect size sedang
- **|d| ≥ 0.8**: Effect size besar

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pandas'"

**Solusi:**
```bash
pip install pandas
```

### Error: "FileNotFoundError: 'data biostat.csv'"

**Penyebab:** Script tidak menemukan file dataset

**Solusi:**
1. Pastikan file `data biostat.csv` ada di folder yang sama dengan `tugas_biostat.py`
2. Atau ubah path di kode:
   ```python
   df = pd.read_csv('/full/path/to/data biostat.csv')
   ```

### Error: "PermissionError" saat menyimpan file

**Solusi:**
1. Tutup file yang sedang terbuka (Excel, image viewer, dll.)
2. Jalankan ulang script

### Grafik tidak muncul

**Solusi:**
1. Cek apakah file PNG berhasil dibuat di folder
2. Jika menggunakan server remote, tambahkan:
   ```python
   import matplotlib
   matplotlib.use('Agg')
   ```
   di awal kode sebelum `import matplotlib.pyplot`

### Output terpotong di terminal

**Solusi:**
Simpan output ke file:
```bash
python tugas_biostat.py > output_lengkap.txt
```

### Error: "LaTeX Error: File not found" saat compile

**Solusi:**
1. Pastikan semua gambar (PNG) ada di folder yang sama dengan file .tex
2. Atau upload ke Overleaf

---

## FAQ

**Q: Berapa lama waktu yang dibutuhkan untuk running script?**

A: Biasanya 10-30 detik, tergantung spesifikasi komputer.

---

**Q: Apakah saya bisa menggunakan dataset lain?**

A: Ya, asalkan format file CSV sama:
- Kolom 1: subject ID
- Kolom 2: labels (kategori)
- Kolom 3 dst: data pengukuran

---

**Q: Bagaimana cara mengubah alpha (tingkat signifikansi)?**

A: Ubah nilai 0.05 di bagian uji hipotesis dalam kode.

---

**Q: Apakah saya perlu install LaTeX untuk menjalankan analisis Python?**

A: Tidak. LaTeX hanya dibutuhkan untuk compile dokumen paper (.tex → .pdf).

---

**Q: Apakah saya bisa menjalankan analisis ini tanpa Python?**

A: Tidak. Python adalah requirement utama untuk menjalankan analisis statistik.

---

**Q: Bagaimana cara mendapatkan bantuan lebih lanjut?**

A:
1. Baca dokumentasi library: https://pandas.pydata.org, https://scipy.org
2. Cek error message di Google atau Stack Overflow
3. Konsultasi dengan dosen/pembimbing

---

## Checklist Penggunaan

Gunakan checklist ini untuk memastikan semua langkah sudah dilakukan:

- [ ] Python 3.7+ terinstall
- [ ] Semua library terinstall (pandas, numpy, matplotlib, seaborn, scipy)
- [ ] File `data biostat.csv` tersedia
- [ ] Script `tugas_biostat.py` sudah dijalankan tanpa error
- [ ] Output teks disimpan/dicatat
- [ ] 6 file output berhasil dibuat (3 PNG + 3 CSV)
- [ ] Nilai-nilai dimasukkan ke file LaTeX
- [ ] Gambar diupload ke Overleaf atau folder LaTeX
- [ ] File paper_biostatistik.tex berhasil dicompile
- [ ] PDF paper berhasil dibuat

---

## Kontak dan Support

Untuk pertanyaan teknis atau bantuan:
- Konsultasi dengan dosen/pembimbing
- Dokumentasi Python: https://docs.python.org
- Dokumentasi SciPy: https://docs.scipy.org

---

**Selamat menganalisis data! 🎓📊**

---

## Lampiran: Contoh Alur Kerja Lengkap

```
1. Buka Terminal
   └─→ cd /path/to/tugas-biostat

2. Jalankan Analisis
   └─→ python tugas_biostat.py > output.txt

3. Cek Output
   └─→ Buka file output.txt
   └─→ Catat semua nilai numerik

4. Edit Paper
   └─→ Buka paper_biostatistik.tex
   └─→ Isi semua nilai [OUTPUT]
   └─→ Lengkapi interpretasi

5. Upload ke Overleaf
   └─→ Upload .tex file
   └─→ Upload 3 file PNG
   └─→ Compile

6. Download PDF
   └─→ Review hasil
   └─→ Revisi jika perlu
   └─→ Submit!
```

---

**Versi: 1.0**
**Tanggal: 2025**
**Update terakhir: [Tanggal hari ini]**
