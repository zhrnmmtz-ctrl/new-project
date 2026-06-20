🏙️ Bandung Multi-Modal Isochrone & Traffic Simulator
Aplikasi WebGIS canggih berbasis algoritma Dijkstra (Graph Theory) untuk menganalisis aksesibilitas transportasi multi-moda di Kota Bandung. Proyek ini memodelkan jangkauan perjalanan (isochrone) dengan mempertimbangkan hierarki jalan (Bus TMP, Angkot, Jalan Kaki) dan dinamika kemacetan (Traffic Impedance).
🌐 LIVE DEMO: Coba Aplikasinya Di Sini! (Ganti dengan link Streamlit Anda)
✨ Fitur Utama (Industry Standard)
1. Multi-Modal Routing Engine: Menghitung waktu tempuh tidak dengan radius garis lurus, melainkan menelusuri jaringan graf jalan raya secara riil.
2. Temporal Dynamics (Traffic Scenarios): Algoritma dinamis yang menyimulasikan pengerutan area jangkauan berdasarkan 3 skenario kemacetan (Lancar, Normal, Rush Hour).
3. 3D Spatial Visualization: Render poligon isochrone dalam bentuk "Kubah Ekstrusi 3D" (menggunakan PyDeck) untuk memvisualisasikan volume aksesibilitas.
4. Real-time Metrics: Kalkulasi otomatis untuk total panjang jaringan jalan yang terakses (km) dan luasan geografis (km²) menggunakan proyeksi UTM Zone 48S.
🏗️ Arsitektur Data & Metodologi
Proyek ini mengandalkan pemrosesan topologi jaringan dari OpenStreetMap:
1. Data Ingestion: Menarik >12.000 titik simpul (nodes) jaringan jalan Bandung menggunakan OSMnx.
2. Impedance Injection: Menyuntikkan atribut kecepatan berdasarkan klasifikasi jalan (⁠highway⁠ tag):
￼ Arteri/Primer: Proksi Bus Trans Metro Pasundan (20 km/j).
￼ Kolektor/Sekunder: Proksi Angkot (15 km/j).
￼ Lokal/Residential: Proksi Pejalan Kaki (4.5 km/j).
3. Routing Algorithm: Menggunakan ⁠networkx.ego_graph⁠ dengan perhitungan beban (⁠weight⁠) berdasarkan akumulasi waktu tempuh per segmen jalan.
🚀 Cara Menjalankan Secara Lokal (DevOps)
Proyek ini telah dikonfigurasi menggunakan Docker untuk standardisasi environment.
Prasyarat: Pastikan Docker & Docker Compose sudah terpasang.
👨‍💻 Pengembang
Dikembangkan sebagai portofolio Geomatics & Spatial Data Science. Terbuka untuk diskusi, kontribusi, dan kolaborasi!
