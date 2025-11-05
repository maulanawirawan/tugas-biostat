"""
Analisis Biostatistik - Data Time Series Medis
Author: Analisis untuk Paper Biostatistik
Dataset: data biostat.csv
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import shapiro, mannwhitneyu, ttest_ind, levene
import warnings
warnings.filterwarnings('ignore')

# Set style untuk visualisasi
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# BAGIAN 1: LOADING DAN PREPROCESSING DATA
# ============================================================================

print("="*80)
print("ANALISIS BIOSTATISTIK - DATA TIME SERIES MEDIS")
print("="*80)
print()

# Load dataset
print("[1] LOADING DATA")
print("-"*80)
df = pd.read_csv('data biostat.csv')
print(f" Dataset berhasil dimuat")
print(f" Dimensi data: {df.shape[0]} subjek x {df.shape[1]} variabel")
print()

# Informasi dasar dataset
print("[2] INFORMASI DATASET")
print("-"*80)
print(f"Jumlah subjek total: {len(df)}")
print(f"Jumlah variabel: {df.shape[1]}")
print(f"\nKolom identifikasi:")
print(f"  - subject ID: identifikasi subjek")
print(f"  - labels: kategori kondisi (normal/abnormal)")
print(f"\nKolom pengukuran: 0 hingga 681 (data time series)")
print()

# Distribusi label
print("[3] DISTRIBUSI LABEL")
print("-"*80)
label_counts = df['labels'].value_counts()
for label, count in label_counts.items():
    persen = (count / len(df)) * 100
    print(f"  {label:15s}: {count:3d} subjek ({persen:5.2f}%)")
print(f"  {'TOTAL':15s}: {len(df):3d} subjek (100.00%)")
print()

# ============================================================================
# BAGIAN 2: EKSTRAKSI STATISTIK DESKRIPTIF
# ============================================================================

print("[4] STATISTIK DESKRIPTIF PER KELOMPOK")
print("-"*80)

# Ambil kolom numerik (time series data)
numeric_cols = [col for col in df.columns if col not in ['subject ID', 'labels']]
numeric_data = df[numeric_cols]

# Hitung statistik untuk setiap kelompok
for label in df['labels'].unique():
    print(f"\nKelompok: {label.upper()}")
    print("-"*40)

    # Filter data untuk label tertentu
    label_data = df[df['labels'] == label][numeric_cols]

    # Flatten semua data untuk statistik keseluruhan
    all_values = label_data.values.flatten()
    all_values = all_values[~np.isnan(all_values)]  # Hapus NaN

    print(f"  Jumlah subjek        : {len(label_data)}")
    print(f"  Total pengukuran     : {len(all_values)}")
    print(f"  Rata-rata (mean)     : {np.mean(all_values):.4f}")
    print(f"  Median               : {np.median(all_values):.4f}")
    print(f"  Standar deviasi      : {np.std(all_values, ddof=1):.4f}")
    print(f"  Minimum              : {np.min(all_values):.4f}")
    print(f"  Kuartil 1 (Q1)       : {np.percentile(all_values, 25):.4f}")
    print(f"  Kuartil 3 (Q3)       : {np.percentile(all_values, 75):.4f}")
    print(f"  Maksimum             : {np.max(all_values):.4f}")
    print(f"  Range                : {np.max(all_values) - np.min(all_values):.4f}")
    print(f"  Skewness             : {stats.skew(all_values):.4f}")
    print(f"  Kurtosis             : {stats.kurtosis(all_values):.4f}")

print()

# ============================================================================
# BAGIAN 3: PERHITUNGAN RATA-RATA PER SUBJEK
# ============================================================================

print("[5] ANALISIS RATA-RATA PER SUBJEK")
print("-"*80)

# Hitung mean untuk setiap subjek
df['mean_value'] = df[numeric_cols].mean(axis=1)

# Statistik per kelompok
print("\nStatistik Rata-rata Pengukuran per Subjek:")
print("-"*40)
for label in df['labels'].unique():
    label_means = df[df['labels'] == label]['mean_value']
    print(f"\n{label.upper()}:")
    print(f"  Rata-rata          : {label_means.mean():.4f}")
    print(f"  Standar deviasi    : {label_means.std():.4f}")
    print(f"  Minimum            : {label_means.min():.4f}")
    print(f"  Maksimum           : {label_means.max():.4f}")
    print(f"  Median             : {label_means.median():.4f}")

print()

# ============================================================================
# BAGIAN 4: UJI NORMALITAS
# ============================================================================

print("[6] UJI NORMALITAS (SHAPIRO-WILK TEST)")
print("-"*80)
print("H0: Data berdistribusi normal")
print("H1: Data tidak berdistribusi normal")
print("Alpha: 0.05")
print()

normalitas_hasil = {}
for label in df['labels'].unique():
    label_means = df[df['labels'] == label]['mean_value']
    stat, p_value = shapiro(label_means)
    normalitas_hasil[label] = (stat, p_value)

    print(f"{label.upper()}:")
    print(f"  Statistik W        : {stat:.6f}")
    print(f"  P-value            : {p_value:.6f}")
    if p_value > 0.05:
        print(f"  Kesimpulan         : Data berdistribusi normal (p > 0.05)")
        print(f"  Interpretasi       : Gagal tolak H0")
    else:
        print(f"  Kesimpulan         : Data tidak berdistribusi normal (p < 0.05)")
        print(f"  Interpretasi       : Tolak H0")
    print()

# ============================================================================
# BAGIAN 5: UJI HOMOGENITAS VARIANS
# ============================================================================

print("[7] UJI HOMOGENITAS VARIANS (LEVENE'S TEST)")
print("-"*80)
print("H0: Varians kedua kelompok homogen")
print("H1: Varians kedua kelompok tidak homogen")
print("Alpha: 0.05")
print()

groups = [df[df['labels'] == label]['mean_value'].values for label in df['labels'].unique()]
stat_levene, p_levene = levene(*groups)

print(f"Statistik Levene     : {stat_levene:.6f}")
print(f"P-value              : {p_levene:.6f}")
if p_levene > 0.05:
    print(f"Kesimpulan           : Varians homogen (p > 0.05)")
    print(f"Interpretasi         : Gagal tolak H0")
    varians_homogen = True
else:
    print(f"Kesimpulan           : Varians tidak homogen (p < 0.05)")
    print(f"Interpretasi         : Tolak H0")
    varians_homogen = False
print()

# ============================================================================
# BAGIAN 6: UJI HIPOTESIS PERBEDAAN DUA KELOMPOK
# ============================================================================

print("[8] UJI HIPOTESIS PERBEDAAN DUA KELOMPOK")
print("-"*80)

# Tentukan uji yang akan digunakan berdasarkan normalitas
labels_list = df['labels'].unique()
normal_semua = all([normalitas_hasil[label][1] > 0.05 for label in labels_list])

if normal_semua and varians_homogen:
    print("Metode: Independent t-test (parametrik)")
    print("Alasan: Data berdistribusi normal dan varians homogen")
    print()
    print("H0: Tidak ada perbedaan rata-rata antara kelompok normal dan abnormal")
    print("H1: Ada perbedaan rata-rata antara kelompok normal dan abnormal")
    print("Alpha: 0.05")
    print()

    group1 = df[df['labels'] == labels_list[0]]['mean_value']
    group2 = df[df['labels'] == labels_list[1]]['mean_value']

    stat_test, p_value_test = ttest_ind(group1, group2, equal_var=True)

    print(f"Statistik t          : {stat_test:.6f}")
    print(f"P-value              : {p_value_test:.6f}")
    print(f"Derajat kebebasan    : {len(group1) + len(group2) - 2}")

elif normal_semua and not varians_homogen:
    print("Metode: Welch's t-test (parametrik)")
    print("Alasan: Data berdistribusi normal tetapi varians tidak homogen")
    print()
    print("H0: Tidak ada perbedaan rata-rata antara kelompok normal dan abnormal")
    print("H1: Ada perbedaan rata-rata antara kelompok normal dan abnormal")
    print("Alpha: 0.05")
    print()

    group1 = df[df['labels'] == labels_list[0]]['mean_value']
    group2 = df[df['labels'] == labels_list[1]]['mean_value']

    stat_test, p_value_test = ttest_ind(group1, group2, equal_var=False)

    print(f"Statistik t          : {stat_test:.6f}")
    print(f"P-value              : {p_value_test:.6f}")

else:
    print("Metode: Mann-Whitney U Test (non-parametrik)")
    print("Alasan: Data tidak berdistribusi normal")
    print()
    print("H0: Tidak ada perbedaan median antara kelompok normal dan abnormal")
    print("H1: Ada perbedaan median antara kelompok normal dan abnormal")
    print("Alpha: 0.05")
    print()

    group1 = df[df['labels'] == labels_list[0]]['mean_value']
    group2 = df[df['labels'] == labels_list[1]]['mean_value']

    stat_test, p_value_test = mannwhitneyu(group1, group2, alternative='two-sided')

    print(f"Statistik U          : {stat_test:.6f}")
    print(f"P-value              : {p_value_test:.6f}")

print()
if p_value_test < 0.05:
    print(f"Kesimpulan           : Ada perbedaan signifikan (p < 0.05)")
    print(f"Interpretasi         : Tolak H0")
    print(f"Makna                : Terdapat perbedaan yang signifikan secara")
    print(f"                       statistik antara kelompok normal dan abnormal")
else:
    print(f"Kesimpulan           : Tidak ada perbedaan signifikan (p > 0.05)")
    print(f"Interpretasi         : Gagal tolak H0")
    print(f"Makna                : Tidak terdapat perbedaan yang signifikan secara")
    print(f"                       statistik antara kelompok normal dan abnormal")

print()

# ============================================================================
# BAGIAN 7: EFFECT SIZE (COHEN'S D)
# ============================================================================

print("[9] EFFECT SIZE (COHEN'S D)")
print("-"*80)

group1 = df[df['labels'] == labels_list[0]]['mean_value']
group2 = df[df['labels'] == labels_list[1]]['mean_value']

# Hitung Cohen's d
mean_diff = group1.mean() - group2.mean()
pooled_std = np.sqrt(((len(group1)-1)*group1.std()**2 + (len(group2)-1)*group2.std()**2) / (len(group1)+len(group2)-2))
cohens_d = mean_diff / pooled_std

print(f"Cohen's d            : {cohens_d:.6f}")
print()
print("Interpretasi Effect Size:")
if abs(cohens_d) < 0.2:
    print("  - Sangat kecil (negligible)")
elif abs(cohens_d) < 0.5:
    print("  - Kecil (small)")
elif abs(cohens_d) < 0.8:
    print("  - Sedang (medium)")
else:
    print("  - Besar (large)")

print()

# ============================================================================
# BAGIAN 8: CONFIDENCE INTERVAL
# ============================================================================

print("[10] CONFIDENCE INTERVAL (95%)")
print("-"*80)

for label in labels_list:
    label_data = df[df['labels'] == label]['mean_value']
    mean = label_data.mean()
    sem = stats.sem(label_data)
    ci = stats.t.interval(0.95, len(label_data)-1, loc=mean, scale=sem)

    print(f"{label.upper()}:")
    print(f"  Mean               : {mean:.4f}")
    print(f"  95% CI             : [{ci[0]:.4f}, {ci[1]:.4f}]")
    print(f"  Interpretasi       : Dengan 95% keyakinan, rata-rata populasi")
    print(f"                       berada di antara {ci[0]:.4f} dan {ci[1]:.4f}")
    print()

# ============================================================================
# BAGIAN 9: RINGKASAN HASIL ANALISIS
# ============================================================================

print("[11] RINGKASAN HASIL ANALISIS")
print("="*80)
print()
print("TEMUAN UTAMA:")
print("-"*80)
print(f"1. Dataset terdiri dari {len(df)} subjek dengan {df.shape[1]-2} titik pengukuran")
print(f"2. Distribusi label:")
for label, count in label_counts.items():
    print(f"   - {label}: {count} subjek ({(count/len(df))*100:.1f}%)")
print()
print(f"3. Uji normalitas:")
for label in labels_list:
    status = "berdistribusi normal" if normalitas_hasil[label][1] > 0.05 else "tidak berdistribusi normal"
    print(f"   - {label}: {status} (p={normalitas_hasil[label][1]:.4f})")
print()
print(f"4. Uji homogenitas varians:")
status_var = "homogen" if varians_homogen else "tidak homogen"
print(f"   - Varians {status_var} (p={p_levene:.4f})")
print()
print(f"5. Uji perbedaan kelompok:")
if p_value_test < 0.05:
    print(f"   - Terdapat perbedaan signifikan (p={p_value_test:.4f})")
else:
    print(f"   - Tidak terdapat perbedaan signifikan (p={p_value_test:.4f})")
print()
print(f"6. Effect size (Cohen's d): {cohens_d:.4f}")
if abs(cohens_d) < 0.2:
    ukuran = "sangat kecil"
elif abs(cohens_d) < 0.5:
    ukuran = "kecil"
elif abs(cohens_d) < 0.8:
    ukuran = "sedang"
else:
    ukuran = "besar"
print(f"   - Ukuran efek: {ukuran}")
print()

# ============================================================================
# BAGIAN 10: VISUALISASI DATA
# ============================================================================

print("[12] MEMBUAT VISUALISASI")
print("-"*80)
print("Membuat grafik...")

# Create figure dengan multiple subplots
fig = plt.figure(figsize=(20, 12))

# 1. Boxplot perbandingan
plt.subplot(2, 3, 1)
df.boxplot(column='mean_value', by='labels', ax=plt.gca())
plt.title('Boxplot Perbandingan Rata-rata Pengukuran per Kelompok')
plt.suptitle('')
plt.xlabel('Kelompok')
plt.ylabel('Rata-rata Nilai Pengukuran')

# 2. Histogram
plt.subplot(2, 3, 2)
for label in labels_list:
    data = df[df['labels'] == label]['mean_value']
    plt.hist(data, alpha=0.6, label=label, bins=15, edgecolor='black')
plt.xlabel('Rata-rata Nilai Pengukuran')
plt.ylabel('Frekuensi')
plt.title('Histogram Distribusi Rata-rata per Kelompok')
plt.legend()
plt.grid(True, alpha=0.3)

# 3. Violin plot
plt.subplot(2, 3, 3)
data_for_violin = [df[df['labels'] == label]['mean_value'].values for label in labels_list]
parts = plt.violinplot(data_for_violin, positions=range(len(labels_list)),
                       showmeans=True, showmedians=True)
plt.xticks(range(len(labels_list)), labels_list)
plt.xlabel('Kelompok')
plt.ylabel('Rata-rata Nilai Pengukuran')
plt.title('Violin Plot Distribusi Data per Kelompok')
plt.grid(True, alpha=0.3)

# 4. Bar plot dengan error bars
plt.subplot(2, 3, 4)
means = [df[df['labels'] == label]['mean_value'].mean() for label in labels_list]
stds = [df[df['labels'] == label]['mean_value'].std() for label in labels_list]
x_pos = np.arange(len(labels_list))
plt.bar(x_pos, means, yerr=stds, alpha=0.7, capsize=10,
        color=['skyblue', 'lightcoral'], edgecolor='black')
plt.xticks(x_pos, labels_list)
plt.xlabel('Kelompok')
plt.ylabel('Rata-rata Nilai Pengukuran')
plt.title('Bar Plot dengan Error Bars (Mean ± SD)')
plt.grid(True, alpha=0.3, axis='y')

# 5. Q-Q plot untuk normalitas
plt.subplot(2, 3, 5)
for i, label in enumerate(labels_list):
    data = df[df['labels'] == label]['mean_value']
    stats.probplot(data, dist="norm", plot=plt)
plt.title('Q-Q Plot untuk Uji Normalitas')
plt.grid(True, alpha=0.3)

# 6. Time series sample (subjek pertama dari setiap kelompok)
plt.subplot(2, 3, 6)
for label in labels_list:
    sample = df[df['labels'] == label].iloc[0]
    values = sample[numeric_cols].dropna().values
    plt.plot(values, label=f'{label} (subjek: {sample["subject ID"]})', alpha=0.7, linewidth=1.5)
plt.xlabel('Titik Pengukuran (Time Point)')
plt.ylabel('Nilai Pengukuran')
plt.title('Contoh Time Series Data (1 subjek per kelompok)')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('hasil_analisis_biostatistik.png', dpi=300, bbox_inches='tight')
print(" Grafik berhasil disimpan: hasil_analisis_biostatistik.png")
print()

# Additional visualization - Heatmap
fig2, ax = plt.subplots(figsize=(16, 10))

# Ambil sample data untuk heatmap (20 subjek pertama)
sample_data = df.head(20).copy()
sample_data = sample_data.set_index('subject ID')
sample_data = sample_data.drop('labels', axis=1)
sample_data = sample_data.drop('mean_value', axis=1)

# Hanya ambil setiap 10 kolom untuk readability
sample_data_reduced = sample_data.iloc[:, ::10]

sns.heatmap(sample_data_reduced, cmap='RdYlBu_r', center=sample_data_reduced.mean().mean(),
            cbar_kws={'label': 'Nilai Pengukuran'}, ax=ax)
plt.title('Heatmap Data Time Series (20 subjek pertama, setiap 10 titik pengukuran)', fontsize=14)
plt.xlabel('Titik Pengukuran')
plt.ylabel('Subjek')
plt.tight_layout()
plt.savefig('heatmap_timeseries.png', dpi=300, bbox_inches='tight')
print(" Heatmap berhasil disimpan: heatmap_timeseries.png")
print()

# Scatter plot untuk melihat pola
fig3, ax = plt.subplots(figsize=(12, 6))
for label in labels_list:
    label_data = df[df['labels'] == label]['mean_value']
    plt.scatter(range(len(label_data)), label_data, label=label, alpha=0.6, s=100)

plt.xlabel('Indeks Subjek')
plt.ylabel('Rata-rata Nilai Pengukuran')
plt.title('Scatter Plot Rata-rata Pengukuran per Subjek')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('scatter_plot_subjects.png', dpi=300, bbox_inches='tight')
print(" Scatter plot berhasil disimpan: scatter_plot_subjects.png")
print()

# ============================================================================
# BAGIAN 11: EXPORT HASIL KE CSV
# ============================================================================

print("[13] EXPORT HASIL ANALISIS")
print("-"*80)

# Simpan statistik deskriptif
summary_stats = df.groupby('labels')['mean_value'].describe()
summary_stats.to_csv('statistik_deskriptif.csv')
print(" Statistik deskriptif disimpan: statistik_deskriptif.csv")

# Simpan hasil uji hipotesis
hasil_uji = pd.DataFrame({
    'Uji': ['Shapiro-Wilk (Normal)', 'Shapiro-Wilk (Abnormal)',
            'Levene', 'Uji Perbedaan Kelompok'],
    'Statistik': [normalitas_hasil[labels_list[0]][0],
                  normalitas_hasil[labels_list[1]][0],
                  stat_levene, stat_test],
    'P-value': [normalitas_hasil[labels_list[0]][1],
                normalitas_hasil[labels_list[1]][1],
                p_levene, p_value_test],
    'Signifikan (±=0.05)': [normalitas_hasil[labels_list[0]][1] < 0.05,
                            normalitas_hasil[labels_list[1]][1] < 0.05,
                            p_levene < 0.05, p_value_test < 0.05]
})
hasil_uji.to_csv('hasil_uji_statistik.csv', index=False)
print(" Hasil uji statistik disimpan: hasil_uji_statistik.csv")

# Simpan data dengan mean value
df.to_csv('data_dengan_mean.csv', index=False)
print(" Data dengan mean value disimpan: data_dengan_mean.csv")
print()

print("="*80)
print("ANALISIS SELESAI!")
print("="*80)
print()
print("File output yang dihasilkan:")
print("  1. hasil_analisis_biostatistik.png - Visualisasi utama (6 grafik)")
print("  2. heatmap_timeseries.png - Heatmap data time series")
print("  3. scatter_plot_subjects.png - Scatter plot per subjek")
print("  4. statistik_deskriptif.csv - Statistik deskriptif per kelompok")
print("  5. hasil_uji_statistik.csv - Hasil semua uji statistik")
print("  6. data_dengan_mean.csv - Data lengkap dengan kolom mean value")
print()
print("Semua hasil siap untuk digunakan dalam penulisan paper!")
print("="*80)
