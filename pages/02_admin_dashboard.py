# -*- coding: utf-8 -*-
"""
Admin Dashboard - Data management and system configuration
"""

import streamlit as st
import pandas as pd
import json
from modules.graph_utils import load_graph, load_halte_data, load_route_config
from modules.admin_operations import (
    add_halte, update_halte, delete_halte, get_all_haltes,
    update_route_impedance, close_road_segment, reopen_road_segment,
    get_closed_segments, export_configuration, import_configuration,
    calculate_fare
)

st.set_page_config(layout="wide")

st.markdown('<div class="app-title">⚙️ Admin Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Kelola data halte, konfigurasi rute, dan simulasi kondisi jalan</div>', unsafe_allow_html=True)

# Load data
G = load_graph()
if G is None:
    st.stop()

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🚏 Manajemen Halte",
    "🚦 Konfigurasi Rute",
    "🛣️ Simulasi Jalan Tutup",
    "📤 Import/Export"
])

# ============================================================================
# TAB 1: HALTE MANAGEMENT
# ============================================================================
with tab1:
    st.header("🚏 Manajemen Halte")
    
    subtab1, subtab2, subtab3 = st.tabs(["Tambah Halte", "Edit Halte", "Lihat Semua"])
    
    # SUBTAB: Add Halte
    with subtab1:
        st.subheader("➕ Tambah Halte Baru")
        
        col1, col2 = st.columns(2)
        
        with col1:
            halte_name = st.text_input("Nama Halte", placeholder="contoh: Halte Caringin")
            halte_type = st.selectbox("Tipe Lokasi", ["Halte", "Terminal", "Station", "Landmark"])
        
        with col2:
            lat = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=-6.92)
            lon = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=107.60)
        
        moda_options = st.multiselect(
            "Moda Transportasi",
            ["TMP", "Angkot", "KA", "Taksi"],
            default=["Angkot"]
        )
        
        if st.button("✅ Tambah Halte", key="add_halte"):
            if not halte_name:
                st.error("❌ Nama halte tidak boleh kosong")
            else:
                success, message = add_halte(halte_name, lat, lon, halte_type, moda_options)
                if success:
                    st.success(f"✅ {message}")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
    
    # SUBTAB: Edit Halte
    with subtab2:
        st.subheader("✏️ Edit Halte Existing")
        
        halte_data = get_all_haltes()
        halte_list = list(halte_data.keys())
        
        if not halte_list:
            st.info("ℹ️ Tidak ada halte untuk diedit")
        else:
            selected_halte = st.selectbox("Pilih Halte untuk Diedit", halte_list)
            
            if selected_halte:
                current_data = halte_data[selected_halte]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    new_name = st.text_input("Nama Halte", value=selected_halte)
                    halte_type = st.selectbox("Tipe Lokasi", ["Halte", "Terminal", "Station", "Landmark"], 
                                             index=["Halte", "Terminal", "Station", "Landmark"].index(current_data.get("type", "Halte")))
                
                with col2:
                    lat = st.number_input("Latitude", value=float(current_data['lat']))
                    lon = st.number_input("Longitude", value=float(current_data['lon']))
                
                moda_options = st.multiselect(
                    "Moda Transportasi",
                    ["TMP", "Angkot", "KA", "Taksi"],
                    default=current_data.get('moda', [])
                )
                
                if st.button("💾 Simpan Perubahan", key="update_halte"):
                    success, message = update_halte(selected_halte, new_name, lat, lon, halte_type, moda_options)
                    if success:
                        st.success(f"✅ {message}")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
    
    # SUBTAB: View All
    with subtab3:
        st.subheader("📋 Daftar Semua Halte")
        
        halte_data = get_all_haltes()
        
        if halte_data:
            # Display as table
            df_haltes = pd.DataFrame([
                {
                    "Nama Halte": name,
                    "Latitude": f"{data['lat']:.4f}",
                    "Longitude": f"{data['lon']:.4f}",
                    "Tipe": data.get('type', 'Halte'),
                    "Moda": ", ".join(data.get('moda', []))
                }
                for name, data in halte_data.items()
            ])
            
            st.dataframe(df_haltes, use_container_width=True, hide_index=True)
            
            # Delete option
            st.markdown("---")
            st.subheader("🗑️ Hapus Halte")
            
            halte_to_delete = st.selectbox("Pilih Halte untuk Dihapus", list(halte_data.keys()), key="delete_select")
            
            if st.button("🗑️ Hapus", key="delete_halte"):
                success, message = delete_halte(halte_to_delete)
                if success:
                    st.success(f"✅ {message}")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
        else:
            st.info("ℹ️ Tidak ada halte dalam sistem")

# ============================================================================
# TAB 2: ROUTE CONFIGURATION
# ============================================================================
with tab2:
    st.header("🚦 Konfigurasi Rute & Tarif")
    
    route_config = load_route_config()
    
    st.info("ℹ️ Atur parameter operasional untuk setiap moda transportasi")
    
    # Create tabs for each mode
    config_tabs = st.tabs([f"🚌 {moda}" for moda in route_config.keys()])
    
    for idx, (moda, tab) in enumerate(zip(route_config.keys(), config_tabs)):
        with tab:
            st.subheader(f"Konfigurasi {moda}")
            
            moda_config = route_config[moda]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Kecepatan & Waktu**")
                
                base_speed = st.number_input(
                    f"Kecepatan Dasar ({moda}) - km/h",
                    value=float(moda_config.get('base_speed', 15)),
                    min_value=1.0,
                    step=0.5,
                    key=f"speed_{moda}"
                )
                
                headway = st.number_input(
                    f"Waktu Tunggu ({moda}) - menit",
                    value=int(moda_config.get('headway_time', 5)),
                    min_value=0,
                    step=1,
                    key=f"headway_{moda}"
                )
                
                if 'ngetem_penalty' in moda_config:
                    ngetem = st.number_input(
                        f"Penalti Ngetem ({moda}) - menit tambahan",
                        value=int(moda_config.get('ngetem_penalty', 0)),
                        min_value=0,
                        step=1,
                        key=f"ngetem_{moda}"
                    )
            
            with col2:
                st.write("**Tarif**")
                
                base_fare = st.number_input(
                    f"Tarif Dasar ({moda}) - IDR",
                    value=int(moda_config.get('base_fare', 5000)),
                    min_value=0,
                    step=100,
                    key=f"fare_{moda}"
                )
                
                fare_per_km = st.number_input(
                    f"Tarif per KM ({moda}) - IDR/km",
                    value=int(moda_config.get('fare_per_km', 500)),
                    min_value=0,
                    step=100,
                    key=f"fare_km_{moda}"
                )
            
            # Save button
            if st.button(f"💾 Simpan Konfigurasi {moda}", key=f"save_config_{moda}"):
                try:
                    update_route_impedance(moda, 'base_speed', base_speed)
                    update_route_impedance(moda, 'headway_time', headway)
                    update_route_impedance(moda, 'base_fare', base_fare)
                    update_route_impedance(moda, 'fare_per_km', fare_per_km)
                    
                    if 'ngetem_penalty' in moda_config:
                        update_route_impedance(moda, 'ngetem_penalty', ngetem)
                    
                    st.success(f"✅ Konfigurasi {moda} berhasil disimpan")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Fare calculator
    st.markdown("---")
    st.subheader("🧮 Kalkulator Tarif")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_moda = st.selectbox("Pilih Moda", list(route_config.keys()), key="fare_calc_moda")
    
    with col2:
        distance = st.number_input("Jarak (km)", min_value=0.1, step=0.1, value=1.0, key="fare_calc_distance")
    
    estimated_fare = calculate_fare(selected_moda, distance)
    st.metric("Estimasi Tarif", f"Rp {estimated_fare:,.0f}")

# ============================================================================
# TAB 3: ROAD CLOSURE SIMULATION
# ============================================================================
with tab3:
    st.header("🛣️ Simulasi Penutupan Jalan")
    
    st.info("⚠️ Simulasikan dampak penutupan jalan terhadap aksesibilitas transportasi")
    
    # Get graph edges for selection
    st.subheader("➕ Tutup Segmen Jalan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        u = st.number_input("Node Awal (U)", min_value=0, step=1, key="close_u")
    
    with col2:
        v = st.number_input("Node Akhir (V)", min_value=0, step=1, key="close_v")
    
    with col3:
        duration = st.number_input("Durasi (menit)", min_value=0, step=30, value=60, key="close_duration")
    
    reason = st.text_area("Alasan Penutupan", placeholder="contoh: CFD Dago, Banjir di Pasteur", key="close_reason")
    
    if st.button("⛔ Tutup Segmen Jalan", key="close_segment"):
        if reason:
            success, message = close_road_segment(u, v, reason, duration)
            if success:
                st.success(f"✅ {message}")
                st.rerun()
            else:
                st.error(f"❌ {message}")
        else:
            st.error("❌ Alasan penutupan harus diisi")
    
    # View closed segments
    st.markdown("---")
    st.subheader("📋 Segmen Jalan yang Ditutup")
    
    closed_segments = get_closed_segments()
    
    if closed_segments:
        df_closed = pd.DataFrame(closed_segments)
        st.dataframe(df_closed, use_container_width=True, hide_index=True)
        
        # Reopen option
        st.markdown("---")
        st.subheader("🔓 Buka Kembali Segmen")
        
        col1, col2 = st.columns(2)
        
        with col1:
            u_reopen = st.number_input("Node Awal", min_value=0, step=1, key="reopen_u")
        
        with col2:
            v_reopen = st.number_input("Node Akhir", min_value=0, step=1, key="reopen_v")
        
        if st.button("✅ Buka Segmen", key="reopen_segment"):
            success, message = reopen_road_segment(u_reopen, v_reopen)
            if success:
                st.success(f"✅ {message}")
                st.rerun()
            else:
                st.error(f"❌ {message}")
    else:
        st.info("ℹ️ Tidak ada segmen jalan yang ditutup")

# ============================================================================
# TAB 4: IMPORT/EXPORT
# ============================================================================
with tab4:
    st.header("📤 Import/Export Konfigurasi")
    
    st.info("💾 Backup dan restore konfigurasi sistem secara keseluruhan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📥 Export Konfigurasi")
        
        config_json = export_configuration()
        
        st.download_button(
            label="⬇️ Download Konfigurasi (JSON)",
            data=config_json,
            file_name="bandung_transit_config.json",
            mime="application/json"
        )
        
        st.code(config_json[:500] + "...", language="json")
    
    with col2:
        st.subheader("📤 Import Konfigurasi")
        
        uploaded_file = st.file_uploader("Pilih file JSON", type="json")
        
        if uploaded_file is not None:
            try:
                json_str = uploaded_file.read().decode()
                
                if st.button("✅ Import Konfigurasi"):
                    success, message = import_configuration(json_str)
                    if success:
                        st.success(f"✅ {message}")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # System info
    st.markdown("---")
    st.subheader("ℹ️ Informasi Sistem")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Halte", len(get_all_haltes()))
    
    with col2:
        st.metric("Total Moda", len(route_config))
    
    with col3:
        st.metric("Jalan Ditutup", len(get_closed_segments()))

st.markdown("---")
st.caption("⚠️ Semua perubahan disimpan secara otomatis. Gunakan fitur Export untuk backup.")
