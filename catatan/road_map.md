Berikut adalah cetak biru (*blueprint*) dan **Roadmap 7 Hari (1 Minggu)** pelaksanaan proyek dari nol hingga selesai menjadi sistem utuh yang siap dipresentasikan.

---

## 1. Ringkasan Proyek & Output Akhir

### A. Proyek Ini Tentang Apa?
Proyek ini bertajuk:
> **"Automasi Pipeline Streaming Data Sensor dan Deteksi Anomali Real-Time Berbasis Machine Learning dengan Interactive Dashboard"**

Proyek ini mereplikasi sistem monitoring industri modern (*Industrial IoT & Predictive Maintenance*). Sistem bekerja secara otomatis mengambil aliran data telemetri sensor mesin pabrik (*suhu udara, suhu proses, kecepatan putar, torsi, keausan alat*), melakukan pembersihan dan validasi data secara otomatis (*data pipeline*), memprediksi potensi kegagalan/anomali mesin secara seketika (*Machine Learning inference*), menyimpannya ke database terstruktur, dan memvisualisasikannya ke dashboard interaktif.

### B. Seperti Apa Output Akhirnya?
1. **Automated Streaming Pipeline**: Script penghasil aliran data sensor (meniru sensor fisik pabrik) yang mengirim data secara kontinyu ke sistem pipeline otomatis.
2. **ML Anomaly & Failure Detector**: Model Machine Learning yang berjalan secara otomatis untuk mendeteksi apakah kondisi sensor saat ini normal atau berisiko rusak (*Overheat, Overstrain, Tool Wear, Power Failure*).
3. **Database Terstruktur**: Database lokal (SQLite / DuckDB / PostgreSQL) yang terus terisi data telemetri historis dan log anomali.
4. **Metabase BI Dashboard (Fase Awal)**: Dashboard eksplorasi data analitik bisnis dengan visualisasi agregasi, metrik KPI, tren, dan log kegagalan.
5. **Modern Real-Time Web Dashboard (Fase Akhir / Migrasi)**: Aplikasi web modern (*zero-refresh* via WebSockets) dengan grafik live bergerak, indikator *gauge* kecepatan/suhu, lampu status mesin (Normal / Warning / Critical Danger), serta panel notifikasi anomali seketika.
6. **Laporan & Dokumentasi Proyek**: Panduan instalasi, arsitektur sistem, dan dokumentasi analitik sains data.

---

## 2. Roadmap Harian (7 Hari Kerja)

```
[Day 1] Pondasi Data, Eksplorasi & Skema Database
[Day 2] Pembangunan Engine Machine Learning (Deteksi Anomali)
[Day 3] Pembuatan Data Pipeline & Streaming Engine Otomatis
[Day 4] Setup & Integrasi Dashboard Metabase (Tahap BI)
[Day 5] Pembangunan Backend Web Dashboard Modern (FastAPI + WebSocket)
[Day 6] Pembangunan Frontend Visualisasi Real-Time (UI/UX)
[Day 7] Pengujian End-to-End, Optimasi, & Dokumentasi Akhir
```

---

### **HARI 1: Pondasi Data, Eksplorasi (EDA), & Desain Database**

* **Tujuan**: Memperoleh dataset sensor industri, memahami distribusi serta pola anomali kegagalan mesin, dan merancang skema penyimpanan data yang efisien.
* **Aktivitas**:
  1. Mengunduh dataset **UCI AI4I 2020 Predictive Maintenance**.
  2. Melakukan *Exploratory Data Analysis* (EDA): korelasi antar-fitur (misal hubungan torsi vs RPM, selisih suhu udara vs suhu proses).
  3. Merancang skema tabel database untuk menampung aliran telemetri sensor dan tabel log peringatan anomali.
* **Tools yang Dibutuhkan**: VS Code / Antigravity IDE, DB Browser for SQLite (opsional untuk intip DB).
* **Library Python**: `pandas`, `numpy`, `matplotlib`, `seaborn`, `sqlalchemy`, `sqlite3`.
* **Output Hari 1**: 
  - Notebook/Script EDA yang menghasilkan ringkasan pola data.
  - File skema database (`schema.py` / file `.db`) yang siap menerima data.

---

### **HARI 2: Pengembangan Model Machine Learning (Deteksi Anomali & Prediksi Kegagalan)**

* **Tujuan**: Membangun model cerdas yang mampu membedakan pembacaan sensor normal dari anomali/gejala kerusakan mesin.
* **Aktivitas**:
  1. *Feature Engineering*: Menghitung fitur turunan penting seperti $\Delta T$ (*selisih suhu*), rasio daya mekanik ($Power = Torque \times Speed$), dan indikator keausan.
  2. Melatih model:
     - **Unsupervised Anomaly Detection**: *Isolation Forest* / *One-Class SVM* (untuk menemukan keanehan pola tanpa label).
     - **Supervised Classification**: *Random Forest* / *XGBoost* (untuk mengklasifikasikan jenis kegagalan spesifik: *Heat Dissipation, Power Failure, Overstrain*).
  3. Evaluasi performa model (*Precision, Recall, F1-Score, ROC-AUC*) terutama pada kelas minoritas (kondisi rusak).
  4. Menyimpan (*serialize*) model terlatih menjadi file siap pakai (`.joblib` / `.pkl`).
* **Tools yang Dibutuhkan**: Script Python / Model Registry lokal.
* **Library Python**: `scikit-learn`, `xgboost`, `joblib`.
* **Output Hari 2**:
  - Model ML siap pakai (`anomaly_detector.joblib` & `failure_classifier.joblib`).
  - Laporan metrik performa model.

---

### **HARI 3: Otomasi Data Pipeline & Streaming Engine**

* **Tujuan**: Menghubungkan aliran data sensor tiruan (*streamer*) ke pipeline pembersihan, *feature extraction*, prediksi ML otomatis, dan penyimpanan database secara *background*.
* **Aktivitas**:
  1. Membuat **Sensor Streamer Simulator**: Script yang membaca baris dataset dan memancarkannya satu per satu dengan jeda waktu tertentu (misal tiap 1-2 detik) layaknya sensor nyata.
  2. Membuat **Pipeline Consumer/Processor**:
     - Menerima raw payload data sensor.
     - Melakukan validasi tipe data dan penanganan *missing values*.
     - Menghitung fitur turunan secara dinamis.
     - Memanggil model ML untuk menyematkan skor anomali (`is_anomaly: True/False`, `risk_level: High/Med/Low`).
     - Menyimpan record hasil olahan ke database secara otomatis (*automated ingestion*).
* **Tools yang Dibutuhkan**: Terminal / Background worker.
* **Library Python**: `pydantic` (validasi skema data), `sqlalchemy`, `asyncio`, `time`.
* **Output Hari 3**:
  - Pipeline otomatis yang berjalan mandiri: data sensor terkirim $\to$ diproses $\to$ dianalisis ML $\to$ tersimpan rapi di database secara kontinyu.

---

### **HARI 4: Implementasi Dashboard BI dengan Metabase**

* **Tujuan**: Menyediakan antarmuka visual pertama menggunakan platform Business Intelligence (Metabase) untuk memantau data yang mengalir ke database.
* **Aktivitas**:
  1. Menjalankan Metabase (menggunakan standalone JAR atau Docker ringan).
  2. Mengkoneksikan Metabase ke database pipeline yang sudah dibuat di Hari 3.
  3. Membangun panel visualisasi analitik di Metabase:
     - *Card KPI*: Total Pembacaan Sensor, Jumlah Anomali Terdeteksi Hari Ini, Rata-rata Suhu Mesin.
     - *Line Chart*: Fluktuasi Torsi vs Kecepatan Putar (RPM) terhadap waktu.
     - *Pie/Bar Chart*: Distribusi jenis kegagalan mesin (*Heat Dissipation vs Power vs Tool Wear*).
     - *Table View*: Log kejadian anomali terbaru (*Live Failure Logs*).
  4. Mengatur konfigurasi *Auto-Refresh* untuk simulasi monitoring.
* **Tools yang Dibutuhkan**: Metabase (JAR file / Docker).
* **Output Hari 4**:
  - Dashboard analitik operasional di Metabase yang siap digunakan untuk laporan manajemen atau analisis mendalam.

---

### **HARI 5: Backend Web Dashboard Modern (FastAPI + WebSocket)**

* **Tujuan**: Memulai migrasi ke dashboard modern dengan membangun API server yang mendukung *real-time push updates* (tanpa perlu reload halaman).
* **Aktivitas**:
  1. Membangun server backend menggunakan **FastAPI**.
  2. Mengimplementasikan endpoint **WebSocket (`/ws/telemetry`)** yang mem-broadcast data sensor dan prediksi ML terbaru langsung ke client setiap kali data baru masuk.
  3. Membuat endpoint REST API untuk mengambil data historis (misal: 100 titik terakhir untuk render grafik awal).
  4. Mengintegrasikan pipeline streaming langsung ke antrean WebSocket broadcast.
* **Tools yang Dibutuhkan**: FastAPI dev server, browser / Postman untuk testing WebSocket.
* **Library Python**: `fastapi`, `uvicorn`, `websockets`.
* **Output Hari 5**:
  - Backend server real-time yang memancarkan data sensor dan status ML melalui koneksi WebSocket berlatensi rendah.

---

### **HARI 6: Frontend Web Dashboard Modern (Interaktif & Real-Time)**

* **Tujuan**: Membangun tampilan antarmuka web kustom yang modern, estetik, dan responsif dengan visualisasi dinamis tanpa refresh.
* **Aktivitas**:
  1. Merancang UI/UX bertema **Industrial Dark Mode / Sci-Fi Monitoring**:
     - *Status Bar*: Indikator status mesin (HIJAU = Normal, KUNING = Warning, MERAH = Critical Anomaly).
     - *Speedometer / Gauges*: Menampilkan RPM dan Suhu Proses secara visual.
     - *Real-time Streaming Charts*: Grafik garis yang bergerak ke kiri secara dinamis saat data baru masuk.
     - *Alert Feed*: Notifikasi pop-up seketika saat anomali terdeteksi model ML.
  2. Menghubungkan frontend ke WebSocket backend yang dibangun di Hari 5.
  3. Menyediakan kontrol tombol: *Start Stream*, *Pause Stream*, *Inject Anomaly* (untuk demo uji coba).
* **Tools & Library**: HTML5, CSS modern (Glassmorphism & Flexbox/Grid), JavaScript murni, library grafik interaktif (`Chart.js` atau `Plotly.js`).
* **Output Hari 6**:
  - Aplikasi Web Dashboard Real-Time mandiri yang interaktif, mulus, dan memukau secara visual.

---

### **HARI 7: Pengujian End-to-End, Evaluasi, & Dokumentasi Akhir**

* **Tujuan**: Memastikan seluruh sistem dari streaming hingga kedua dashboard (Metabase & Web Dashboard) berjalan tanpa error, serta menyusun dokumentasi komprehensif.
* **Aktivitas**:
  1. *Stress Testing*: Menguji sistem jika aliran sensor dipercepat atau jika anomali berturut-turut terjadi.
  2. Perbandingan Hasil: Mendokumentasikan kelebihan dashboard Metabase (untuk analitik historis/bisnis) vs Web Dashboard Modern (untuk monitoring *real-time/sub-detik*).
  3. Menyusun file dokumentasi utama:
     - `README.md`: Panduan instalasi, arsitektur sistem, dan cara menjalankan seluruh komponen dengan 1-2 perintah sederhana.
     - Presentasi / Ringkasan Proyek: Ringkasan teknis dan bisnis untuk portofolio.
* **Output Hari 7**:
  - Proyek selesai 100% (*ready-to-demo*).
  - Repositori proyek terstruktur rapi dan terdokumentasi penuh.

---

## 3. Matriks Kebutuhan Tools & Library Lengkap

| Kategori | Nama Tools / Library | Fungsi Utama |
| :--- | :--- | :--- |
| **Bahasa & Environment** | Python 3.10+ | Bahasa pemrograman utama seluruh pipeline & ML |
| **Manipulasi & Analisis Data** | `pandas`, `numpy` | Pengolahan array, data cleaning, & transformasi |
| **Machine Learning** | `scikit-learn`, `xgboost`, `joblib` | Model deteksi anomali, klasifikasi kerusakan, & serialisasi |
| **Database & ORM** | SQLite / DuckDB, `sqlalchemy` | Penyimpanan data sensor dan log kejadian anomali |
| **Backend & Streaming** | `fastapi`, `uvicorn`, `websockets`, `pydantic` | Server API real-time, validasi data, & WebSocket broadcasting |
| **BI Dashboard (Fase 1)** | Metabase | Dashboard visualisasi data analitik & laporan bisnis |
| **Web UI (Fase 2)** | HTML, CSS, JavaScript, `Chart.js` | Tampilan dashboard monitoring real-time kustom yang estetik |

---
