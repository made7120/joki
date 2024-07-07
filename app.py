import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import os

# Pastikan folder untuk menyimpan foto sampul dan buku digital ada
if not os.path.exists("sampul_buku"):
    os.makedirs("sampul_buku")

if not os.path.exists("buku_digital"):
    os.makedirs("buku_digital")

# Kelas Buku yang dimodifikasi untuk menyertakan atribut foto sampul
class Buku:
    def __init__(self, judul, penulis, tahun_terbit, foto_sampul=None, status="tersedia"):
        self.judul = judul
        self.penulis = penulis
        self.tahun_terbit = tahun_terbit
        self.foto_sampul = foto_sampul
        self.status = status
    
    def info_buku(self):
        status_display = "tidak tersedia" if self.status == "dipinjam" else "tersedia"
        return f"Judul: {self.judul}, Penulis: {self.penulis}, Tahun Terbit: {self.tahun_terbit}, Status: {status_display}, Foto Sampul: {self.foto_sampul}"

class BukuDigital(Buku):
    def __init__(self, judul, penulis, tahun_terbit, ukuran_file, format_file, file_path, foto_sampul=None, status="tersedia"):
        super().__init__(judul, penulis, tahun_terbit, foto_sampul, status)
        self.ukuran_file = ukuran_file
        self.format_file = format_file
        self.file_path = file_path
    
    def info_buku(self):
        info = super().info_buku()
        return f"{info}, Ukuran File: {self.ukuran_file}MB, Format: {self.format_file}, Path: {self.file_path}"

class BukuFisik(Buku):
    def __init__(self, judul, penulis, tahun_terbit, jumlah_halaman, berat, foto_sampul=None, status="tersedia"):
        super().__init__(judul, penulis, tahun_terbit, foto_sampul, status)
        self.jumlah_halaman = jumlah_halaman
        self.berat = berat
    
    def info_buku(self):
        info = super().info_buku()
        return f"{info}, Jumlah Halaman: {self.jumlah_halaman}, Berat: {self.berat} gram"

class Perpustakaan:
    def __init__(self):
        self.daftar_buku = []  # Inisialisasi daftar_buku
        self.load_data()
    
    def tambah_buku(self, buku):
        self.daftar_buku.append(buku)
        self.simpan_data()
    
    def cari_buku(self, judul):
        for buku in self.daftar_buku:
            if buku.judul.lower() == judul.lower():
                return buku
        return None
    
    def tampilkan_semua_buku(self):
        return [buku.info_buku() for buku in self.daftar_buku]
    
    def tampilkan_semua_buku_df(self):
        data = [{
            'Judul': buku.judul,
            'Penulis': buku.penulis,
            'Tahun Terbit': buku.tahun_terbit,
            'Status': "tidak tersedia" if buku.status == "dipinjam" else "tersedia",
            'Ukuran File (MB)': getattr(buku, 'ukuran_file', None),
            'Format File': getattr(buku, 'format_file', None),
            'Jumlah Halaman': getattr(buku, 'jumlah_halaman', None),
            'Berat (gram)': getattr(buku, 'berat', None),
            'Foto Sampul': buku.foto_sampul,
            'File Path': getattr(buku, 'file_path', None)
        } for buku in self.daftar_buku]
        
        df = pd.DataFrame(data)
        return df
    
    def pinjam_buku(self, judul):
        buku = self.cari_buku(judul)
        if buku and buku.status == "tersedia":
            buku.status = "dipinjam"
            self.simpan_data()
            return f"Buku '{judul}' berhasil dipinjam."
        else:
            return f"Buku '{judul}' tidak tersedia untuk dipinjam."
    
    def kembalikan_buku(self, judul):
        buku = self.cari_buku(judul)
        if buku and buku.status == "dipinjam":
            buku.status = "tersedia"
            self.simpan_data()
            return f"Buku '{judul}' berhasil dikembalikan."
        else:
            return f"Buku '{judul}' tidak sedang dipinjam."

    def hapus_buku(self, judul):
        buku = self.cari_buku(judul)
        if buku:
            self.daftar_buku.remove(buku)
            self.simpan_data()
            return f"Buku '{judul}' berhasil dihapus."
        else:
            return f"Buku '{judul}' tidak ditemukan."

    def edit_buku(self, judul_lama, buku_baru):
        buku = self.cari_buku(judul_lama)
        if buku:
            buku.judul = buku_baru.judul
            buku.penulis = buku_baru.penulis
            buku.tahun_terbit = buku_baru.tahun_terbit
            buku.status = buku_baru.status
            buku.foto_sampul = buku_baru.foto_sampul
            if isinstance(buku, BukuDigital):
                buku.ukuran_file = buku_baru.ukuran_file
                buku.format_file = buku_baru.format_file
                buku.file_path = buku_baru.file_path
            elif isinstance(buku, BukuFisik):
                buku.jumlah_halaman = buku_baru.jumlah_halaman
                buku.berat = buku_baru.berat
            self.simpan_data()
            return f"Buku '{judul_lama}' berhasil diupdate."
        else:
            return f"Buku '{judul_lama}' tidak ditemukan."

    def simpan_data(self):
        data = [{
            'Judul': buku.judul,
            'Penulis': buku.penulis,
            'Tahun Terbit': buku.tahun_terbit,
            'Status': buku.status,
            'Ukuran File (MB)': getattr(buku, 'ukuran_file', None),
            'Format File': getattr(buku, 'format_file', None),
            'Jumlah Halaman': getattr(buku, 'jumlah_halaman', None),
            'Berat (gram)': getattr(buku, 'berat', None),
            'Foto Sampul': buku.foto_sampul,
            'File Path': getattr(buku, 'file_path', None)
        } for buku in self.daftar_buku]
        
        df = pd.DataFrame(data)
        df.to_excel('data_perpustakaan.xlsx', index=False)

    def load_data(self):
        try:
            df = pd.read_excel('data_perpustakaan.xlsx')
            for _, row in df.iterrows():
                if pd.notna(row['Ukuran File (MB)']):
                    buku = BukuDigital(
                        row['Judul'],
                        row['Penulis'],  # Pastikan nama penulis dimasukkan dengan benar
                        row['Tahun Terbit'],
                        row['Ukuran File (MB)'],
                        row['Format File'],
                        row['File Path'],
                        row['Foto Sampul'],
                        row['Status']
                    )
                else:
                    buku = BukuFisik(
                        row['Judul'],
                        row['Penulis'],  # Pastikan nama penulis dimasukkan dengan benar
                        row['Tahun Terbit'],
                        row['Jumlah Halaman'],
                        row['Berat (gram)'],
                        row['Foto Sampul'],
                        row['Status']
                    )
                self.daftar_buku.append(buku)
        except FileNotFoundError:
            pass

# Initialize library
perpustakaan = Perpustakaan()

# Streamlit Interface
st.set_page_config(page_title="Sistem Perpustakaan", page_icon="📚", layout="wide")

st.markdown("""
    <style>
    .main {
        background-image: url("data:image/jpeg;base64,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");
        background-size: cover;
    }
    .css-1d391kg {
        background-color: rgba(255, 255, 255, 0.8);
    }
    </style>
    """, unsafe_allow_html=True)

# Logo aplikasi
st.image("data:image/png;base64,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", width=200)

st.title("Sistem Perpustakaan Sederhana")

tabs = st.tabs(["Tambah Buku", "Cari Buku", "Tampilkan Semua Buku", "Pinjam Buku", "Kembalikan Buku", "Hapus Buku", "Edit Buku"])

with tabs[0]:
    st.subheader("Tambah Buku Baru")
    tipe_buku = st.selectbox("Tipe Buku", ["Buku Fisik", "Buku Digital"])
    judul = st.text_input("Judul Buku")
    penulis = st.text_input("Penulis Buku")
    tahun_terbit = st.number_input("Tahun Terbit", min_value=1500, max_value=2024, step=1)
    foto_sampul = st.file_uploader("Unggah Foto Sampul", type=["jpg", "png", "jpeg"])
    
    if foto_sampul is not None:
        foto_sampul_path = os.path.join("sampul_buku", foto_sampul.name)
        with open(foto_sampul_path, "wb") as f:
            f.write(foto_sampul.getbuffer())
    
    if tipe_buku == "Buku Digital":
        ukuran_file = st.number_input("Ukuran File (MB)", min_value=0.1)
        format_file = st.selectbox("Format File", ["PDF", "EPUB", "MOBI"])
        file_buku = st.file_uploader("Unggah File Buku", type=["pdf", "epub", "mobi"])
        
        if file_buku is not None:
            file_path = os.path.join("buku_digital", file_buku.name)
            with open(file_path, "wb") as f:
                f.write(file_buku.getbuffer())
            
        if st.button("Tambah Buku Digital"):
            buku = BukuDigital(judul, penulis, tahun_terbit, ukuran_file, format_file, file_path, foto_sampul_path)
            perpustakaan.tambah_buku(buku)
            st.success(f"Buku digital '{judul}' berhasil ditambahkan.")
    else:
        jumlah_halaman = st.number_input("Jumlah Halaman", min_value=1)
        berat = st.number_input("Berat (gram)", min_value=1)
        if st.button("Tambah Buku Fisik"):
            buku = BukuFisik(judul, penulis, tahun_terbit, jumlah_halaman, berat, foto_sampul_path)
            perpustakaan.tambah_buku(buku)
            st.success(f"Buku fisik '{judul}' berhasil ditambahkan.")
            
with tabs[1]:
    st.subheader("Cari Buku")
    judul = st.text_input("Masukkan Judul Buku")
    if st.button("Cari"):
        buku = perpustakaan.cari_buku(judul)
        if buku:
            st.write(buku.info_buku())
            if buku.foto_sampul:
                st.image(buku.foto_sampul, caption=buku.judul)
        else:
            st.warning("Buku tidak ditemukan.")

with tabs[2]:
    st.subheader("Daftar Semua Buku")
    df_buku = perpustakaan.tampilkan_semua_buku_df()
    st.dataframe(df_buku)

with tabs[3]:
    st.subheader("Pinjam Buku")
    judul = st.text_input("Masukkan Judul Buku yang Akan Dipinjam")
    if st.button("Pinjam"):
        pesan = perpustakaan.pinjam_buku(judul)
        st.write(pesan)

with tabs[4]:
    st.subheader("Kembalikan Buku")
    judul = st.text_input("Masukkan Judul Buku yang Akan Dikembalikan")
    if st.button("Kembalikan"):
        pesan = perpustakaan.kembalikan_buku(judul)
        st.write(pesan)

with tabs[5]:
    st.subheader("Hapus Buku")
    judul = st.text_input("Masukkan Judul Buku yang Akan Dihapus")
    if st.button("Hapus"):
        pesan = perpustakaan.hapus_buku(judul)
        st.write(pesan)

with tabs[6]:
    st.subheader("Edit Buku")
    judul_lama = st.text_input("Masukkan Judul Buku yang Akan Diedit")
    if st.button("Cari Buku untuk Diedit"):
        buku = perpustakaan.cari_buku(judul_lama)
        if buku:
            judul = st.text_input("Judul Buku", value=buku.judul)
            penulis = st.text_input("Penulis Buku", value=buku.penulis)
            tahun_terbit = st.number_input("Tahun Terbit", min_value=1500, max_value=2024, step=1, value=buku.tahun_terbit)
            foto_sampul = st.file_uploader("Unggah Foto Sampul Baru", type=["jpg", "png", "jpeg"])
            
            if foto_sampul is not None:
                foto_sampul_path = os.path.join("sampul_buku", foto_sampul.name)
                with open(foto_sampul_path, "wb") as f:
                    f.write(foto_sampul.getbuffer())
            else:
                foto_sampul_path = buku.foto_sampul
            
            if isinstance(buku, BukuDigital):
                ukuran_file = st.number_input("Ukuran File (MB)", min_value=0.1, value=buku.ukuran_file)
                format_file = st.selectbox("Format File", ["PDF", "EPUB", "MOBI"], index=["PDF", "EPUB", "MOBI"].index(buku.format_file))
                file_buku = st.file_uploader("Unggah File Buku Baru", type=["pdf", "epub", "mobi"])
                
                if file_buku is not None:
                    file_path = os.path.join("buku_digital", file_buku.name)
                    with open(file_path, "wb") as f:
                        f.write(file_buku.getbuffer())
                else:
                    file_path = buku.file_path
                
                buku_baru = BukuDigital(judul, penulis, tahun_terbit, ukuran_file, format_file, file_path, foto_sampul_path)
            else:
                jumlah_halaman = st.number_input("Jumlah Halaman", min_value=1, value=buku.jumlah_halaman)
                berat = st.number_input("Berat (gram)", min_value=1, value=buku.berat)
                
                buku_baru = BukuFisik(judul, penulis, tahun_terbit, jumlah_halaman, berat, foto_sampul_path)
            
            if st.button("Update Buku"):
                pesan = perpustakaan.edit_buku(judul_lama, buku_baru)
                st.write(pesan)
        else:
            st.warning("Buku tidak ditemukan.")
