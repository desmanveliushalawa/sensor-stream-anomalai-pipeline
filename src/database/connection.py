"""
Manajemen Koneksi Database SQLite / SQLAlchemy.
Menyediakan Engine, SessionFactory, serta fungsi inisialisasi tabel.
"""

import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base

# Tentukan lokasi default database SQLite di root project
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = ROOT_DIR / "telemetry.db"

# Dukung environment variable DATABASE_URL jika ingin beralih ke PostgreSQL di masa depan
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH.as_posix()}")

# Buat Engine dengan support multithreading untuk streaming & API
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False  # Ubah ke True jika ingin melihat raw SQL query di terminal saat debug
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Membuat semua tabel database (jika belum ada) sesuai skema Base.metadata.
    """
    print(f"[*] Menginisialisasi skema database pada: {DATABASE_URL} ...")
    Base.metadata.create_all(bind=engine)
    print("[+] Database dan seluruh tabel (sensor_telemetry, anomaly_logs) berhasil diinisialisasi!")


def get_db():
    """
    Generator sesi database untuk FastAPI Depends atau pemakaian context manager.
    Memastikan sesi selalu ditutup setelah selesai digunakan.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
