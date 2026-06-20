
# Menggunakan base image Python yang ringan
FROM python:3.10-slim

# Mencegah Python menulis file .pyc dan membiarkan log langsung muncul
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependensi sistem untuk pemrosesan spasial (GeoPandas/C++ dependencies)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgdal-dev \
    libspatialindex-dev \
    && rm -rf /var/lib/apt/lists/*

# Set direktori kerja
WORKDIR /app

# Copy file requirements dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode aplikasi
COPY . .

# Expose port yang digunakan Streamlit
EXPOSE 8501

# Perintah untuk menjalankan aplikasi
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

