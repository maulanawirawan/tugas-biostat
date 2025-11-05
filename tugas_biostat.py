# -*- coding: utf-8 -*-
"""
Analisis Biostatistik - Data Time Series Medis dengan Eksplorasi & Pembersihan Data
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
# BAGIAN 1: LOADING DATA
# ============================================================================

print("="*80)
print("ANALISIS BIOSTATISTIK - DATA TIME SERIES MEDIS")
print("DENGAN EKSPLORASI & PEMBERSIHAN DATA")
print("="*80)
print()

# Load dataset
print("[1] LOADING DATA")
print("-"*80)
df = pd.read_csv('data biostat.csv')
print(f"✓ Dataset berhasil dimuat")
print(f"✓ Dimensi data: {df.shape[0]} subjek x {df.shape[1]} variabel")
print()

# ============================================================================
# BAGIAN 2: EKSPLORASI STRUKTUR DATA
# ============================================================================

print("[2] EKSPLORASI STRUKTUR DATA")
print("-"*80)

# 2.1 Informasi Tipe Data
print("\n2.1 Tipe Variabel:")
print("-"*40)
print(f"Total kolom: {len(df.columns)}")
print(f"\nKolom Identifikasi (2 kolom):")
print(f"  - subject ID (object): Identifikasi subjek penelitian")
print(f"  - labels (object): Kategori kondisi (normal/abnormal)")
print(f"\nKolom Pengukuran Time Series (682 kolom):")
print(f"  - Kolom 0 hingga 681 (numeric): Data pengukuran fisiologis")
print(f"  - Tipe data: float64")

# 2.2 Sample Data
print(f"\n2.2 Sample Data (5 baris pertama):")
print("-"*40)
print("\nSubject ID | Labels | Sample Pengukuran (kolom 0-5)")
print("-"*60)
for idx in range(min(5, len(df))):
    row = df.iloc[idx]
    sample_values = [f"{row[str(i)]:.1f}" if pd.notna(row[str(i)]) else "NaN" for i in range(6)]
    print(f"{row['subject ID']:10s} | {row['labels']:8s} | {', '.join(sample_values)}")

print()

# ============================================================================
# BAGIAN 3: ANALISIS MISSING VALUES
# ============================================================================

print("[3] ANALISIS MISSING VALUES")
print("-"*80)

# Ambil kolom numerik
numeric_cols = [col for col in df.columns if col not in ['subject ID', 'labels']]

# Hitung missing values per subjek
print("\n3.1 Missing Values per Subjek:")
print("-"*40)
df['missing_count'] = df[numeric_cols].isna().sum(axis=1)
df['missing_percentage'] = (df['missing_count'] / len(numeric_cols)) * 100

print(f"Total kolom pengukuran: {len(numeric_cols)}")
print(f"\nStatistik Missing Values:")
print(f"  Subjek tanpa missing: {(df['missing_count'] == 0).sum()} subjek")
print(f"  Subjek dengan missing: {(df['missing_count'] > 0).sum()} subjek")
print(f"  Rata-rata missing per subjek: {df['missing_count'].mean():.2f} kolom ({df['missing_percentage'].mean():.2f}%)")
print(f"  Median missing per subjek: {df['missing_count'].median():.0f} kolom")
print(f"  Maksimum missing: {df['missing_count'].max():.0f} kolom ({df['missing_percentage'].max():.2f}%)")
print(f"  Minimum missing: {df['missing_count'].min():.0f} kolom ({df['missing_percentage'].min():.2f}%)")

# Missing values per kelompok
print(f"\n3.2 Missing Values per Kelompok:")
print("-"*40)
for label in df['labels'].unique():
    label_df = df[df['labels'] == label]
    print(f"\n{label.upper()}:")
    print(f"  Jumlah subjek: {len(label_df)}")
    print(f"  Rata-rata missing: {label_df['missing_count'].mean():.2f} kolom ({label_df['missing_percentage'].mean():.2f}%)")
    print(f"  Median missing: {label_df['missing_count'].median():.0f} kolom")

# Total missing values
total_cells = len(df) * len(numeric_cols)
total_missing = df[numeric_cols].isna().sum().sum()
print(f"\n3.3 Total Missing Values:")
print("-"*40)
print(f"  Total sel data: {total_cells:,}")
print(f"  Total missing: {total_missing:,} ({(total_missing/total_cells)*100:.2f}%)")
print(f"  Total data valid: {total_cells - total_missing:,} ({((total_cells - total_missing)/total_cells)*100:.2f}%)")

print()

# ============================================================================
# BAGIAN 4: STATISTIK DESKRIPTIF & DATA SUMMARY
# ============================================================================

print("[4] STATISTIK DESKRIPTIF & DATA SUMMARY")
print("-"*80)

# Hitung mean untuk setiap subjek (menghilangkan NaN)
df['mean_value'] = df[numeric_cols].mean(axis=1)
df['median_value'] = df[numeric_cols].median(axis=1)
df['std_value'] = df[numeric_cols].std(axis=1)
df['min_value'] = df[numeric_cols].min(axis=1)
df['max_value'] = df[numeric_cols].max(axis=1)

print("\n4.1 Statistik Deskriptif per Kelompok (Rata-rata per Subjek):")
print("-"*40)

for label in df['labels'].unique():
    label_data = df[df['labels'] == label]
    print(f"\nKelompok: {label.upper()}")
    print("-"*40)
    print(f"  Jumlah subjek        : {len(label_data)}")
    print(f"  Mean (rata-rata)     : {label_data['mean_value'].mean():.4f}")
    print(f"  Median               : {label_data['median_value'].mean():.4f}")
    print(f"  Std Deviasi          : {label_data['std_value'].mean():.4f}")
    print(f"  Minimum              : {label_data['min_value'].min():.4f}")
    print(f"  Maksimum             : {label_data['max_value'].max():.4f}")
    print(f"  Range                : {label_data['max_value'].max() - label_data['min_value'].min():.4f}")

# Statistik keseluruhan untuk semua pengukuran
print(f"\n4.2 Statistik Deskriptif Keseluruhan Data (Semua Pengukuran):")
print("-"*40)

for label in df['labels'].unique():
    label_data = df[df['labels'] == label][numeric_cols]
    all_values = label_data.values.flatten()
    all_values = all_values[~np.isnan(all_values)]

    print(f"\nKelompok: {label.upper()}")
    print("-"*40)
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
# BAGIAN 5: DETEKSI OUTLIER
# ============================================================================

print("[5] DETEKSI OUTLIER")
print("-"*80)

print("\n5.1 Deteksi Outlier dengan Metode IQR (Interquartile Range):")
print("-"*40)
print("Outlier didefinisikan sebagai nilai di luar [Q1 - 1.5*IQR, Q3 + 1.5*IQR]")
print()

outlier_results = {}

for label in df['labels'].unique():
    label_means = df[df['labels'] == label]['mean_value']

    Q1 = label_means.quantile(0.25)
    Q3 = label_means.quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = label_means[(label_means < lower_bound) | (label_means > upper_bound)]
    outlier_indices = outliers.index.tolist()

    outlier_results[label] = {
        'Q1': Q1,
        'Q3': Q3,
        'IQR': IQR,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'n_outliers': len(outliers),
        'outlier_indices': outlier_indices,
        'outlier_values': outliers.values
    }

    print(f"{label.upper()}:")
    print(f"  Q1                   : {Q1:.4f}")
    print(f"  Q3                   : {Q3:.4f}")
    print(f"  IQR                  : {IQR:.4f}")
    print(f"  Batas bawah          : {lower_bound:.4f}")
    print(f"  Batas atas           : {upper_bound:.4f}")
    print(f"  Jumlah outlier       : {len(outliers)} dari {len(label_means)} subjek ({(len(outliers)/len(label_means))*100:.2f}%)")

    if len(outliers) > 0:
        print(f"  Outlier terdeteksi pada indeks: {outlier_indices}")
        print(f"  Nilai outlier: {[f'{v:.2f}' for v in outliers.values]}")
    print()

print("\n5.2 Deteksi Outlier dengan Metode Z-Score:")
print("-"*40)
print("Outlier didefinisikan sebagai nilai dengan |Z-score| > 3")
print()

for label in df['labels'].unique():
    label_means = df[df['labels'] == label]['mean_value']

    mean = label_means.mean()
    std = label_means.std()
    z_scores = np.abs((label_means - mean) / std)

    outliers_z = label_means[z_scores > 3]

    print(f"{label.upper()}:")
    print(f"  Mean                 : {mean:.4f}")
    print(f"  Std Dev              : {std:.4f}")
    print(f"  Jumlah outlier (|Z|>3): {len(outliers_z)} dari {len(label_means)} subjek ({(len(outliers_z)/len(label_means))*100:.2f}%)")

    if len(outliers_z) > 0:
        print(f"  Outlier terdeteksi pada indeks: {outliers_z.index.tolist()}")
        print(f"  Nilai outlier: {[f'{v:.2f}' for v in outliers_z.values]}")
        print(f"  Z-scores: {[f'{z:.2f}' for z in z_scores[z_scores > 3].values]}")
    print()

# ============================================================================
# BAGIAN 6: DISTRIBUSI LABEL
# ============================================================================

print("[6] DISTRIBUSI LABEL")
print("-"*80)
label_counts = df['labels'].value_counts()
for label, count in label_counts.items():
    persen = (count / len(df)) * 100
    print(f"  {label:15s}: {count:3d} subjek ({persen:5.2f}%)")
print(f"  {'TOTAL':15s}: {len(df):3d} subjek (100.00%)")
print()

# ============================================================================
# BAGIAN 7: UJI NORMALITAS
# ============================================================================

print("[7] UJI NORMALITAS (SHAPIRO-WILK TEST)")
print("-"*80)
print("H0: Data berdistribusi normal")
print("H1: Data tidak berdistribusi normal")
print("Alpha: 0.05")
print()

normalitas_hasil = {}
labels_list = df['labels'].unique()

for label in labels_list:
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
# BAGIAN 8: UJI HOMOGENITAS VARIANS
# ============================================================================

print("[8] UJI HOMOGENITAS VARIANS (LEVENE'S TEST)")
print("-"*80)
print("H0: Varians kedua kelompok homogen")
print("H1: Varians kedua kelompok tidak homogen")
print("Alpha: 0.05")
print()

groups = [df[df['labels'] == label]['mean_value'].values for label in labels_list]
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
# BAGIAN 9: UJI HIPOTESIS PERBEDAAN DUA KELOMPOK
# ============================================================================

print("[9] UJI HIPOTESIS PERBEDAAN DUA KELOMPOK")
print("-"*80)

# Tentukan uji yang akan digunakan berdasarkan normalitas
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
    metode_uji = "Independent t-test"

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
    metode_uji = "Welch's t-test"

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
    metode_uji = "Mann-Whitney U Test"

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
# BAGIAN 10: EFFECT SIZE (COHEN'S D)
# ============================================================================

print("[10] EFFECT SIZE (COHEN'S D)")
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
    ukuran_efek = "sangat kecil"
elif abs(cohens_d) < 0.5:
    print("  - Kecil (small)")
    ukuran_efek = "kecil"
elif abs(cohens_d) < 0.8:
    print("  - Sedang (medium)")
    ukuran_efek = "sedang"
else:
    print("  - Besar (large)")
    ukuran_efek = "besar"

print()

# ============================================================================
# BAGIAN 11: CONFIDENCE INTERVAL
# ============================================================================

print("[11] CONFIDENCE INTERVAL (95%)")
print("-"*80)

ci_results = {}
for label in labels_list:
    label_data = df[df['labels'] == label]['mean_value']
    mean = label_data.mean()
    sem = stats.sem(label_data)
    ci = stats.t.interval(0.95, len(label_data)-1, loc=mean, scale=sem)

    ci_results[label] = {'mean': mean, 'ci_lower': ci[0], 'ci_upper': ci[1]}

    print(f"{label.upper()}:")
    print(f"  Mean               : {mean:.4f}")
    print(f"  95% CI             : [{ci[0]:.4f}, {ci[1]:.4f}]")
    print(f"  Interpretasi       : Dengan 95% keyakinan, rata-rata populasi")
    print(f"                       berada di antara {ci[0]:.4f} dan {ci[1]:.4f}")
    print()

# ============================================================================
# BAGIAN 12: REKOMENDASI PEMBERSIHAN DATA
# ============================================================================

print("[12] REKOMENDASI PEMBERSIHAN DATA")
print("-"*80)

print("\n12.1 Analisis Kelengkapan Data:")
print("-"*40)
if df['missing_percentage'].mean() < 10:
    print("✓ Data relatif lengkap (missing < 10%)")
    print("  Rekomendasi: Data dapat digunakan langsung")
elif df['missing_percentage'].mean() < 30:
    print("⚠ Data memiliki missing values moderat (10-30%)")
    print("  Rekomendasi: Pertimbangkan imputasi atau analisis dengan hanya data lengkap")
else:
    print("✗ Data memiliki missing values tinggi (> 30%)")
    print("  Rekomendasi: Perlu investigasi lebih lanjut atau metode imputasi khusus")

print("\n12.2 Analisis Outlier:")
print("-"*40)
total_outliers_pct = sum([outlier_results[label]['n_outliers'] for label in labels_list]) / len(df) * 100
if total_outliers_pct < 5:
    print(f"✓ Outlier minimal ({total_outliers_pct:.2f}% dari total data)")
    print("  Rekomendasi: Outlier dapat dipertahankan atau dihapus sesuai konteks")
elif total_outliers_pct < 10:
    print(f"⚠ Outlier moderat ({total_outliers_pct:.2f}% dari total data)")
    print("  Rekomendasi: Investigasi outlier, pertimbangkan transformasi data atau metode robust")
else:
    print(f"✗ Outlier tinggi ({total_outliers_pct:.2f}% dari total data)")
    print("  Rekomendasi: Perlu investigasi mendalam, mungkin indikasi masalah pengukuran")

print("\n12.3 Kesimpulan Kualitas Data:")
print("-"*40)
print("Berdasarkan analisis eksplorasi data:")
print(f"  - Kelengkapan data: {((total_cells - total_missing)/total_cells)*100:.2f}% data valid")
print(f"  - Outlier terdeteksi: {total_outliers_pct:.2f}% dari subjek")
print(f"  - Distribusi kelompok: Seimbang" if abs(label_counts.iloc[0] - label_counts.iloc[1]) < 5 else "  - Distribusi kelompok: Tidak seimbang")
print()
print("Rekomendasi:")
print("  1. Data cukup baik untuk analisis lanjutan")
print("  2. Pertimbangkan handling missing values sesuai konteks penelitian")
print("  3. Outlier dapat diinvestigasi lebih lanjut atau dipertahankan")
print("  4. Gunakan metode statistik yang sesuai dengan distribusi data")

print()

# ============================================================================
# BAGIAN 13: RINGKASAN HASIL ANALISIS
# ============================================================================

print("[13] RINGKASAN HASIL ANALISIS")
print("="*80)
print()
print("TEMUAN UTAMA:")
print("-"*80)
print(f"1. Dataset terdiri dari {len(df)} subjek dengan {len(numeric_cols)} titik pengukuran")
print(f"2. Distribusi label:")
for label, count in label_counts.items():
    print(f"   - {label}: {count} subjek ({(count/len(df))*100:.1f}%)")
print()
print(f"3. Missing values:")
print(f"   - Total missing: {(total_missing/total_cells)*100:.2f}% dari seluruh data")
print(f"   - Rata-rata missing per subjek: {df['missing_percentage'].mean():.2f}%")
print()
print(f"4. Outlier terdeteksi:")
for label in labels_list:
    n_out = outlier_results[label]['n_outliers']
    total_subj = len(df[df['labels'] == label])
    print(f"   - {label}: {n_out} dari {total_subj} subjek ({(n_out/total_subj)*100:.1f}%)")
print()
print(f"5. Uji normalitas:")
for label in labels_list:
    status = "berdistribusi normal" if normalitas_hasil[label][1] > 0.05 else "tidak berdistribusi normal"
    print(f"   - {label}: {status} (p={normalitas_hasil[label][1]:.4f})")
print()
print(f"6. Uji homogenitas varians:")
status_var = "homogen" if varians_homogen else "tidak homogen"
print(f"   - Varians {status_var} (p={p_levene:.4f})")
print()
print(f"7. Uji perbedaan kelompok ({metode_uji}):")
if p_value_test < 0.05:
    print(f"   - Terdapat perbedaan signifikan (p={p_value_test:.4f})")
else:
    print(f"   - Tidak terdapat perbedaan signifikan (p={p_value_test:.4f})")
print()
print(f"8. Effect size (Cohen's d): {cohens_d:.4f}")
print(f"   - Ukuran efek: {ukuran_efek}")
print()

# ============================================================================
# BAGIAN 14: VISUALISASI DATA
# ============================================================================

print("[14] MEMBUAT VISUALISASI")
print("-"*80)
print("Membuat grafik eksplorasi data dan analisis statistik...")

# Create comprehensive visualization
fig = plt.figure(figsize=(20, 16))

# 1. Boxplot perbandingan
plt.subplot(3, 3, 1)
df.boxplot(column='mean_value', by='labels', ax=plt.gca())
plt.title('Boxplot Perbandingan Rata-rata per Kelompok')
plt.suptitle('')
plt.xlabel('Kelompok')
plt.ylabel('Rata-rata Nilai Pengukuran')

# 2. Histogram
plt.subplot(3, 3, 2)
for label in labels_list:
    data = df[df['labels'] == label]['mean_value']
    plt.hist(data, alpha=0.6, label=label, bins=15, edgecolor='black')
plt.xlabel('Rata-rata Nilai Pengukuran')
plt.ylabel('Frekuensi')
plt.title('Histogram Distribusi Rata-rata per Kelompok')
plt.legend()
plt.grid(True, alpha=0.3)

# 3. Missing values bar chart
plt.subplot(3, 3, 3)
missing_by_group = df.groupby('labels')['missing_percentage'].mean()
plt.bar(missing_by_group.index, missing_by_group.values, color=['skyblue', 'lightcoral'], edgecolor='black')
plt.xlabel('Kelompok')
plt.ylabel('Rata-rata Missing Values (%)')
plt.title('Missing Values per Kelompok')
plt.grid(True, alpha=0.3, axis='y')

# 4. Violin plot
plt.subplot(3, 3, 4)
data_for_violin = [df[df['labels'] == label]['mean_value'].values for label in labels_list]
parts = plt.violinplot(data_for_violin, positions=range(len(labels_list)),
                       showmeans=True, showmedians=True)
plt.xticks(range(len(labels_list)), labels_list)
plt.xlabel('Kelompok')
plt.ylabel('Rata-rata Nilai Pengukuran')
plt.title('Violin Plot Distribusi Data per Kelompok')
plt.grid(True, alpha=0.3)

# 5. Bar plot dengan error bars
plt.subplot(3, 3, 5)
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

# 6. Q-Q plot
plt.subplot(3, 3, 6)
for i, label in enumerate(labels_list):
    data = df[df['labels'] == label]['mean_value']
    stats.probplot(data, dist="norm", plot=plt)
plt.title('Q-Q Plot untuk Uji Normalitas')
plt.grid(True, alpha=0.3)

# 7. Outlier visualization
plt.subplot(3, 3, 7)
for i, label in enumerate(labels_list):
    label_means = df[df['labels'] == label]['mean_value']
    outlier_info = outlier_results[label]

    # Plot all points
    x = [i] * len(label_means)
    plt.scatter(x, label_means, alpha=0.5, s=50, label=f'{label} (normal)')

    # Highlight outliers
    if outlier_info['n_outliers'] > 0:
        outlier_vals = outlier_info['outlier_values']
        x_out = [i] * len(outlier_vals)
        plt.scatter(x_out, outlier_vals, color='red', s=100, marker='x',
                   label=f'{label} (outlier)', zorder=5)

    # Plot IQR bounds
    plt.hlines(outlier_info['lower_bound'], i-0.2, i+0.2, colors='orange', linestyles='dashed')
    plt.hlines(outlier_info['upper_bound'], i-0.2, i+0.2, colors='orange', linestyles='dashed')

plt.xticks(range(len(labels_list)), labels_list)
plt.xlabel('Kelompok')
plt.ylabel('Rata-rata Nilai Pengukuran')
plt.title('Deteksi Outlier (Metode IQR)')
plt.legend(fontsize=8)
plt.grid(True, alpha=0.3, axis='y')

# 8. Time series sample
plt.subplot(3, 3, 8)
for label in labels_list:
    sample = df[df['labels'] == label].iloc[0]
    values = sample[numeric_cols].dropna().values
    plt.plot(values, label=f'{label} ({sample["subject ID"]})', alpha=0.7, linewidth=1.5)
plt.xlabel('Titik Pengukuran (Time Point)')
plt.ylabel('Nilai Pengukuran')
plt.title('Contoh Time Series Data (1 subjek per kelompok)')
plt.legend()
plt.grid(True, alpha=0.3)

# 9. Missing values heatmap (per subjek)
plt.subplot(3, 3, 9)
missing_data = df[['labels', 'missing_percentage']].sort_values('missing_percentage', ascending=False).head(20)
colors = ['skyblue' if label == labels_list[0] else 'lightcoral' for label in missing_data['labels']]
plt.barh(range(len(missing_data)), missing_data['missing_percentage'], color=colors)
plt.yticks(range(len(missing_data)), [f"S{i+1}" for i in range(len(missing_data))])
plt.xlabel('Missing Values (%)')
plt.ylabel('Subjek (20 tertinggi)')
plt.title('Missing Values per Subjek')
plt.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('hasil_analisis_biostatistik.png', dpi=300, bbox_inches='tight')
print("✓ Grafik utama berhasil disimpan: hasil_analisis_biostatistik.png")

# Heatmap time series
fig2, ax = plt.subplots(figsize=(16, 10))
sample_data = df.head(20).copy()
sample_data = sample_data.set_index('subject ID')
sample_data_numeric = sample_data[numeric_cols].iloc[:, ::10]  # Setiap 10 kolom

sns.heatmap(sample_data_numeric, cmap='RdYlBu_r', center=sample_data_numeric.mean().mean(),
            cbar_kws={'label': 'Nilai Pengukuran'}, ax=ax)
plt.title('Heatmap Data Time Series (20 subjek pertama, setiap 10 titik pengukuran)', fontsize=14)
plt.xlabel('Titik Pengukuran')
plt.ylabel('Subjek')
plt.tight_layout()
plt.savefig('heatmap_timeseries.png', dpi=300, bbox_inches='tight')
print("✓ Heatmap berhasil disimpan: heatmap_timeseries.png")

# Scatter plot
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
print("✓ Scatter plot berhasil disimpan: scatter_plot_subjects.png")
print()

# ============================================================================
# BAGIAN 15: EXPORT HASIL
# ============================================================================

print("[15] EXPORT HASIL ANALISIS")
print("-"*80)

# Simpan statistik deskriptif
summary_stats = df.groupby('labels')['mean_value'].describe()
summary_stats.to_csv('statistik_deskriptif.csv')
print("✓ Statistik deskriptif disimpan: statistik_deskriptif.csv")

# Simpan hasil uji hipotesis
hasil_uji = pd.DataFrame({
    'Uji': ['Shapiro-Wilk ('+labels_list[0]+')', 'Shapiro-Wilk ('+labels_list[1]+')',
            'Levene', 'Uji Perbedaan Kelompok'],
    'Statistik': [normalitas_hasil[labels_list[0]][0],
                  normalitas_hasil[labels_list[1]][0],
                  stat_levene, stat_test],
    'P-value': [normalitas_hasil[labels_list[0]][1],
                normalitas_hasil[labels_list[1]][1],
                p_levene, p_value_test],
    'Signifikan (α=0.05)': [normalitas_hasil[labels_list[0]][1] < 0.05,
                            normalitas_hasil[labels_list[1]][1] < 0.05,
                            p_levene < 0.05, p_value_test < 0.05]
})
hasil_uji.to_csv('hasil_uji_statistik.csv', index=False)
print("✓ Hasil uji statistik disimpan: hasil_uji_statistik.csv")

# Simpan data dengan semua variabel turunan
df_export = df[['subject ID', 'labels', 'mean_value', 'median_value', 'std_value',
                'min_value', 'max_value', 'missing_count', 'missing_percentage']]
df_export.to_csv('data_dengan_statistik.csv', index=False)
print("✓ Data dengan statistik disimpan: data_dengan_statistik.csv")

# Simpan informasi outlier
outlier_df_list = []
for label in labels_list:
    if outlier_results[label]['n_outliers'] > 0:
        for idx, val in zip(outlier_results[label]['outlier_indices'],
                           outlier_results[label]['outlier_values']):
            outlier_df_list.append({
                'subject_index': idx,
                'subject_id': df.iloc[idx]['subject ID'],
                'label': label,
                'mean_value': val,
                'lower_bound': outlier_results[label]['lower_bound'],
                'upper_bound': outlier_results[label]['upper_bound']
            })

if outlier_df_list:
    outlier_df = pd.DataFrame(outlier_df_list)
    outlier_df.to_csv('outlier_terdeteksi.csv', index=False)
    print("✓ Outlier terdeteksi disimpan: outlier_terdeteksi.csv")
else:
    print("  (Tidak ada outlier terdeteksi)")

print()

print("="*80)
print("ANALISIS SELESAI!")
print("="*80)
print()
print("File output yang dihasilkan:")
print("  1. hasil_analisis_biostatistik.png - Visualisasi utama (9 grafik)")
print("  2. heatmap_timeseries.png - Heatmap data time series")
print("  3. scatter_plot_subjects.png - Scatter plot per subjek")
print("  4. statistik_deskriptif.csv - Statistik deskriptif per kelompok")
print("  5. hasil_uji_statistik.csv - Hasil semua uji statistik")
print("  6. data_dengan_statistik.csv - Data dengan statistik per subjek")
print("  7. outlier_terdeteksi.csv - Daftar outlier (jika ada)")
print()
print("Semua hasil siap untuk digunakan dalam penulisan paper!")
print("="*80)
