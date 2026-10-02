# 🏭 Industrial IoT: Automasi Streaming Pipeline & Deteksi Anomali Real-Time

Sistem *Predictive Maintenance* dan pemantauan telemetri sensor industri berbasis Machine Learning secara *real-time*, dilengkapi arsitektur streaming otomatis dan *dual monitoring dashboard* (Metabase BI & Modern Web Dashboard).

---

## 📌 Fitur Utama Sistem

1. **Automated Sensor Telemetry Ingestion**: Simulasi aliran telemetri sensor industri (*Air Temperature, Process Temperature, Rotational Speed, Torque, Tool Wear*).
2. **Dual-Engine Machine Learning**:
   - **Unsupervised Anomaly Detection**: Mendeteksi anomali kondisi mesin secara independen (*Isolation Forest*).
   - **Multi-Class Failure Classifier**: Mendiagnosis tipe kerusakan spesifik (*XGBoost / Random Forest*: HDF, PWF, OSF, TWF, RNF).
3. **Structured Storage Layer**: Database SQLite/PostgreSQL terkelola via SQLAlchemy ORM (`sensor_telemetry` & `anomaly_logs`).
4. **Dual Dashboard Monitoring**:
   - **Metabase BI**: Agregasi metrik analitik bisnis & pelaporan riwayat mesin.
   - **Modern Real-Time Web Dashboard**: Pemantauan visual sub-detik via WebSockets dengan tema *Industrial Dark Mode*, animasi *gauge/speedometer*, dan grafik live bergerak.

---

## 📂 Struktur Repositori

```text
Project PSD/
├── data/
│   └── ai4i2020.csv              # Dataset sensor pabrik (UCI AI4I 2020)
├── notebooks/
│   └── 01_eda.ipynb              # Notebook eksplorasi data & analisis pola anomali
├── src/
│   ├── database/
│   │   ├── models.py             # Definisi skema tabel ORM (SQLAlchemy)
│   │   └── connection.py         # Engine & manajemen koneksi database
│   ├── models/                   # Tempat penyimpanan skrip & artefak model ML (.joblib)
│   └── pipeline/                 # Engine streaming, validasi Pydantic, & consumer
├── web/                          # Frontend & server FastAPI WebSocket
├── catatan/
│   ├── road_map.md               # Roadmap pengerjaan 7 hari
│   └── catatan-belajar.md        # Catatan konsep & kamus istilah teknis
├── telemetry.db                  # Database lokal SQLite
└── requirements.txt              # Daftar dependensi Python
```

---

## 🚀 Panduan Memulai Cepat

### 1. Inisialisasi Database
Jalankan perintah berikut untuk membuat file database `telemetry.db` beserta tabel-tabelnya:
```bash
python -m src.database.connection
```

### 2. Eksplorasi Data (EDA)
Buka dan jalankan notebook [notebooks/01_eda.ipynb](notebooks/01_eda.ipynb) pada VS Code / Jupyter Lab untuk memahami karakteristik sensor dan formula *feature engineering*.
