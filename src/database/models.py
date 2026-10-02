"""
Skema Database SQLAlchemy untuk Sistem Telemetri Sensor & Deteksi Anomali.
Terdapat dua tabel utama:
1. SensorTelemetry: Menyimpan seluruh aliran data telemetri sensor dan hasil prediksi ML.
2. AnomalyLog: Menyimpan kejadian peringatan ketika terdeteksi adanya anomali atau risiko kerusakan mesin.
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class SensorTelemetry(Base):
    __tablename__ = "sensor_telemetry"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    udi = Column(Integer, nullable=True, index=True, doc="Nomor identitas unik perangkat (UDI)")
    product_id = Column(String(50), nullable=True, index=True, doc="Product ID (misal M14860, L47181)")
    product_type = Column(String(10), nullable=True, doc="Kualitas tipe produk (L, M, H)")

    # Nilai Pembacaan Sensor Fisik
    air_temperature = Column(Float, nullable=False, doc="Suhu udara sekitar mesin [Kelvin]")
    process_temperature = Column(Float, nullable=False, doc="Suhu proses operasional mesin [Kelvin]")
    rotational_speed = Column(Float, nullable=False, doc="Kecepatan putaran poros mesin [RPM]")
    torque = Column(Float, nullable=False, doc="Torsi putaran mesin [Nm]")
    tool_wear = Column(Float, nullable=False, doc="Akumulasi keausan mata pisau mesin [menit]")

    # Fitur Turunan (Feature Engineering)
    temp_difference = Column(Float, nullable=True, doc="Selisih suhu proses - suhu udara [K]")
    mechanical_power = Column(Float, nullable=True, doc="Perhitungan estimasi daya mekanis (Torque x RPM)")

    # Ground Truth / Label Historis (Opsional saat streaming live)
    machine_failure = Column(Integer, default=0, doc="Status ground truth kerusakan (0=Normal, 1=Fail)")
    twf = Column(Integer, default=0, doc="Tool Wear Failure (0/1)")
    hdf = Column(Integer, default=0, doc="Heat Dissipation Failure (0/1)")
    pwf = Column(Integer, default=0, doc="Power Failure (0/1)")
    osf = Column(Integer, default=0, doc="Overstrain Failure (0/1)")
    rnf = Column(Integer, default=0, doc="Random Failure (0/1)")

    # Hasil Inferensi Machine Learning Real-Time
    is_anomaly = Column(Boolean, default=False, index=True, doc="Deteksi anomali oleh model AI (True/False)")
    anomaly_score = Column(Float, default=0.0, doc="Skor keanehan pola dari Isolation Forest")
    predicted_failure = Column(String(50), default="NORMAL", doc="Prediksi jenis kerusakan spesifik")

    timestamp = Column(DateTime, default=datetime.utcnow, index=True, doc="Waktu pencatatan data")

    # Relasi ke tabel log anomali
    anomaly_logs = relationship("AnomalyLog", back_populates="telemetry", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<SensorTelemetry(id={self.id}, udi={self.udi}, is_anomaly={self.is_anomaly}, score={self.anomaly_score:.2f})>"


class AnomalyLog(Base):
    __tablename__ = "anomaly_logs"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    telemetry_id = Column(Integer, ForeignKey("sensor_telemetry.id", ondelete="CASCADE"), nullable=False)
    
    timestamp = Column(DateTime, default=datetime.utcnow, index=True, doc="Waktu anomali terjadi")
    severity = Column(String(20), default="WARNING", doc="Tingkat keparahan: INFO, WARNING, CRITICAL")
    failure_type = Column(String(50), default="UNKNOWN", doc="Tipe kegagalan terdeteksi (HDF, PWF, OSF, TWF, dsb.)")
    anomaly_score = Column(Float, nullable=False, doc="Skor anomali saat kejadian")
    
    description = Column(Text, nullable=False, doc="Deskripsi kondisi abnormal")
    recommended_action = Column(Text, nullable=True, doc="Rekomendasi tindakan mitigasi untuk operator")

    # Relasi balik ke tabel telemetri
    telemetry = relationship("SensorTelemetry", back_populates="anomaly_logs")

    def __repr__(self):
        return f"<AnomalyLog(id={self.id}, severity='{self.severity}', type='{self.failure_type}')>"
