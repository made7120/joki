import streamlit as st
import pandas as pd
import os
from abc import ABC, abstractmethod
import pickle

# Kelas Abstrak BukuBase
class BukuBase(ABC):
    def __init__(self, judul, penulis, tahun_terbit, status="tersedia"):
        self.judul = judul
        self.penulis = penulis
        self.tahun_terbit = tahun_terbit
        self.status = status

    @abstractmethod
    def info_buku(self):
        pass

class BukuDigital(BukuBase):
    def __init__(self, judul, penulis, tahun_terbit, ukuran_file, format_file, status="tersedia"):
        super().__init__(judul, penulis, tahun_terbit, status)
        self.ukuran_file = ukuran_file
        self.format_file = format_file

    def info_buku(self):
        return (f"Judul: {self.judul}\nPenulis: {self.penulis}\nTahun Terbit: {self.tahun_terbit}\n"
                f"Status: {self.status}\nUkuran File: {self.ukuran_file} MB\nFormat File: {self.format_file}")

class BukuFisik(BukuBase):
    def __init__(self, judul, penulis, tahun_terbit, jumlah_halaman, berat, status="tersedia"):
        super().__init__(judul, penulis, tahun_terbit, status)
        self.jumlah_halaman = jumlah_halaman
        self.berat = berat

    def info_buku(self):
        return (f"Judul: {self.judul}\nPenulis: {self.penulis}\nTahun Terbit: {self.tahun_terbit}\n"
                f"Status: {self.status}\nJumlah Halaman: {self.jumlah_halaman}\nBerat: {self.berat} gram")

class Perpustakaan:
    def __init__(self, file_path="data_perpustakaan.pkl"):
        self.file_path = file_path
        self.daftar_buku = []
        self.buku_id_counter = 1
        self.load_data()

    def tambah_buku(self, buku):
        buku.id = self.buku_id_counter
        self.daftar_buku.append(buku)
        self.buku_id_counter += 1
        self.save_data()
        st.success(f"Buku '{buku.judul}' berhasil ditambahkan dengan ID {buku.id}.")

    def cari_buku(self, judul):
        for buku in self.daftar_buku:
            if buku.judul.lower() == judul.lower():
                return buku
        return None

    def tampilkan_semua_buku(self):
        if not self.daftar_buku:
            st.write("Perpustakaan kosong.")
        else:
            for buku in self.daftar_buku:
                with st.expander(buku.judul):
                    st.markdown(buku.info_buku())

    def pinjam_buku(self, judul):
        buku = self.cari_buku(judul)
        if buku and buku.status == "tersedia":
            buku.status = "dipinjam"
            self.save_data()
            st.success(f"Buku '{judul}' berhasil dipinjam.")
        elif buku:
            st.warning(f"Buku '{judul}' tidak tersedia untuk dipinjam.")
        else:
            st.error(f"Buku '{judul}' tidak ditemukan di perpustakaan.")

    def kembalikan_buku(self, judul):
        buku = self.cari_buku(judul)
        if buku and buku.status == "dipinjam":
            buku.status = "tersedia"
            self.save_data()
            st.success(f"Buku '{judul}' berhasil dikembalikan.")
        elif buku:
            st.warning(f"Buku '{judul}' tidak sedang dipinjam.")
        else:
            st.error(f"Buku '{judul}' tidak ditemukan di perpustakaan.")

    def hapus_buku(self, judul):
        buku = self.cari_buku(judul)
        if buku:
            self.daftar_buku.remove(buku)
            self.save_data()
            st.success(f"Buku '{judul}' berhasil dihapus dari perpustakaan.")
        else:
            st.error(f"Buku '{judul}' tidak ditemukan di perpustakaan.")

    def edit_buku(self, judul, judul_baru=None, penulis_baru=None, tahun_terbit_baru=None, status_baru=None):
        buku = self.cari_buku(judul)
        if buku:
            buku.judul = judul_baru or buku.judul
            buku.penulis = penulis_baru or buku.penulis
            buku.tahun_terbit = tahun_terbit_baru or buku.tahun_terbit
            buku.status = status_baru or buku.status
            self.save_data()
            st.success(f"Buku '{judul}' berhasil diperbarui.")
        else:
            st.error(f"Buku '{judul}' tidak ditemukan di perpustakaan.")

    def save_data(self):
        with open(self.file_path, 'wb') as f:
            pickle.dump(self.daftar_buku, f)

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'rb') as f:
                self.daftar_buku = pickle.load(f)
            self.buku_id_counter = max([buku.id for buku in self.daftar_buku], default=0) + 1

# Fungsi untuk halaman login
def login(users):
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state["username"] = username
            st.session_state["logged_in"] = True
            st.success("Login berhasil!")
        else:
            st.error("Username atau password salah!")

# Fungsi untuk halaman daftar
def daftar(users):
    st.title("Daftar")
    new_username = st.text_input("Username baru")
    new_password = st.text_input("Password baru", type="password")
    if st.button("Daftar"):
        if new_username in users:
            st.error("Username sudah ada!")
        else:
            users[new_username] = {"password": new_password}
            with open("users.pkl", "wb") as f:
                pickle.dump(users, f)
            st.success("Pendaftaran berhasil!")

# Fungsi untuk halaman logout
def logout():
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.sidebar.success("Logout berhasil!")

# Fungsi utama untuk aplikasi Streamlit
def main():
    # Load data pengguna
    if os.path.exists("users.pkl"):
        with open("users.pkl", "rb") as f:
            users = pickle.load(f)
    else:
        users = {}

    # Inisialisasi status login
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Halaman login dan daftar
    if not st.session_state["logged_in"]:
        st.sidebar.title("Perpustakaan")
        menu = st.sidebar.selectbox("Menu", ["Login", "Daftar"])
        if menu == "Login":
            login(users)
        elif menu == "Daftar":
            daftar(users)
    else:
        # Inisialisasi objek perpustakaan
        perpustakaan = Perpustakaan()

        # Tampilkan judul aplikasi
        st.title("MyLibrary")

        # Menampilkan sidebar untuk menu
        menu = st.sidebar.radio(
            "Menu",
            [
                "📚 Tambah Buku",
                "📖 Daftar Buku",
                "📤 Pinjam Buku",
                "📥 Kembalikan Buku",
                "🔍 Cek Status Buku",
                "🗑️ Hapus Buku",
                "✏️ Edit Buku",
                "Logout"
            ]
        )

        if menu == "📚 Tambah Buku":
            st.header("Tambah Buku Baru")
            jenis_buku = st.selectbox("Jenis Buku:", ("Buku Digital", "Buku Fisik"))

            col1, col2 = st.columns(2)
            with col1:
                judul = st.text_input("Judul Buku:")
                penulis = st.text_input("Nama Penulis:")
            with col2:
                tahun_terbit = st.number_input("Tahun Terbit:", min_value=0, step=1, format="%d")

            if jenis_buku == "Buku Digital":
                ukuran_file = st.number_input("Ukuran File (MB):", min_value=0.0, step=0.1, format="%.1f")
                format_file = st.text_input("Format File:")
                if st.button("Tambah Buku"):
                    buku = BukuDigital(judul, penulis, tahun_terbit, ukuran_file, format_file)
                    perpustakaan.tambah_buku(buku)

            elif jenis_buku == "Buku Fisik":
                jumlah_halaman = st.number_input("Jumlah Halaman:", min_value=0, step=1, format="%d")
                berat = st.number_input("Berat (gram):", min_value=0.0, step=1.0, format="%.1f")
                if st.button("Tambah Buku"):
                    buku = BukuFisik(judul, penulis, tahun_terbit, jumlah_halaman, berat)
                    perpustakaan.tambah_buku(buku)

        elif menu == "📖 Daftar Buku":
            st.header("Daftar Buku di Perpustakaan")
            perpustakaan.tampilkan_semua_buku()

        elif menu == "📤 Pinjam Buku":
            st.header("Pinjam Buku")
            judul_pinjam = st.text_input("Masukkan judul buku yang ingin dipinjam:")
            if st.button("Pinjam"):
                perpustakaan.pinjam_buku(judul_pinjam)

        elif menu == "📥 Kembalikan Buku":
            st.header("Kembalikan Buku")
            judul_kembali = st.text_input("Masukkan judul buku yang ingin dikembalikan:")
            if st.button("Kembalikan"):
                perpustakaan.kembalikan_buku(judul_kembali)

        elif menu == "🔍 Cek Status Buku":
            st.header("Cek Status Buku")
            judul_status = st.text_input("Masukkan judul buku yang ingin diperiksa statusnya:")
            if st.button("Cek Status"):
                buku = perpustakaan.cari_buku(judul_status)
                if buku:
                    st.info(f"Status buku '{judul_status}': {buku.status}")
                else:
                    st.error(f"Buku '{judul_status}' tidak ditemukan di perpustakaan.")

        elif menu == "🗑️ Hapus Buku":
            st.header("Hapus Buku")
            judul_hapus = st.text_input("Masukkan judul buku yang ingin dihapus:")
            if st.button("Hapus Buku"):
                perpustakaan.hapus_buku(judul_hapus)

        elif menu == "✏️ Edit Buku":
            st.header("Edit Buku")
            judul_edit = st.text_input("Masukkan judul buku yang ingin diedit:")
            judul_baru = st.text_input("Judul Baru (opsional):")
            penulis_baru = st.text_input("Penulis Baru (opsional):")
            tahun_terbit_baru = st.number_input("Tahun Terbit Baru (opsional):", min_value=0, step=1, format="%d")
            status_baru = st.selectbox("Status Baru (opsional):", ["", "tersedia", "dipinjam"])
            if st.button("Edit Buku"):
                perpustakaan.edit_buku(judul_edit, judul_baru, penulis_baru, tahun_terbit_baru if tahun_terbit_baru > 0 else None, status_baru if status_baru else None)

        elif menu == "Logout":
            logout()

# CSS untuk background hijau muda
st.markdown(
    """
    <style>
    .main {
        background-color: #DFF2E1;
    }
    </style>
    <style>
    .st-emotion-cache-6qob1r {
        background-color: #DFF2E1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if __name__ == "__main__":
    main()

