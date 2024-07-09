import streamlit as st
from abc import ABC, abstractmethod
import pandas as pd
from streamlit_option_menu import option_menu
import shelve

# Styling
st.markdown(
    """
    <style>
    .main {
        background-color: #AED9DA;
        font-family: 'Arial', sans-serif;
    }
    h1 {
        color: #333333;
    }
    .stButton>button {
        background-color: #3DDAD7;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2A93D5;
    }
    .stSelectbox>div>div>div>div {
        background-color: #fff;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True
)

class BukuBase(ABC):
    def __init__(self, id_buku, judul, penulis, tahun_terbit):
        self.id_buku = id_buku
        self.judul = judul
        self.penulis = penulis
        self.tahun_terbit = tahun_terbit
        self.status = "tersedia"

    @abstractmethod
    def info_buku(self):
        pass

class BukuDigital(BukuBase):
    def __init__(self, id_buku, judul, penulis, tahun_terbit, ukuran_file, format_file):
        super().__init__(id_buku, judul, penulis, tahun_terbit)
        self.ukuran_file = ukuran_file
        self.format_file = format_file

    def info_buku(self):
        return {
            "ID": self.id_buku,
            "Judul": self.judul,
            "Penulis": self.penulis,
            "Tahun Terbit": self.tahun_terbit,
            "Status": self.status,
            "Ukuran File": self.ukuran_file,
            "Format": self.format_file,
            "Jumlah Halaman": None,
            "Berat": None
        }

class BukuFisik(BukuBase):
    def __init__(self, id_buku, judul, penulis, tahun_terbit, jumlah_halaman, berat):
        super().__init__(id_buku, judul, penulis, tahun_terbit)
        self.jumlah_halaman = jumlah_halaman
        self.berat = berat

    def info_buku(self):
        return {
            "ID": self.id_buku,
            "Judul": self.judul,
            "Penulis": self.penulis,
            "Tahun Terbit": self.tahun_terbit,
            "Status": self.status,
            "Ukuran File": None,
            "Format": None,
            "Jumlah Halaman": self.jumlah_halaman,
            "Berat": self.berat
        }

class Perpustakaan:
    def __init__(self):
        self.daftar_buku = []
        self.laporan_peminjaman = []
        self.muat_data()

    def simpan_data(self):
        with shelve.open('data_perpustakaan') as db:
            db['daftar_buku'] = self.daftar_buku
            db['laporan_peminjaman'] = self.laporan_peminjaman

    def muat_data(self):
        with shelve.open('data_perpustakaan') as db:
            self.daftar_buku = db.get('daftar_buku', [])
            self.laporan_peminjaman = db.get('laporan_peminjaman', [])

    def tambah_buku(self, buku):
        self.daftar_buku.append(buku)
        self.simpan_data()
        st.success(f"Buku '{buku.judul}' berhasil ditambahkan dengan ID {buku.id_buku}.")
        self.tampilkan_semua_buku()

    def cari_buku(self, id_buku):
        for buku in self.daftar_buku:
            if buku.id_buku == id_buku:
                return buku
        return None

    def tampilkan_semua_buku(self):
        data = [buku.info_buku() for buku in self.daftar_buku]
        df = pd.DataFrame(data)
        st.table(df)

    def hitung_buku_tersedia(self):
        return sum(1 for buku in self.daftar_buku if buku.status == "tersedia")

    def pinjam_buku(self, id_buku, nama_peminjam):
        buku = self.cari_buku(id_buku)
        if buku and buku.status == "tersedia":
            buku.status = "dipinjam"
            self.laporan_peminjaman.append({
                "ID Buku": buku.id_buku,
                "Judul": buku.judul,
                "Nama Peminjam": nama_peminjam,
                "Status": "dipinjam"
            })
            self.simpan_data()
            st.success(f"Buku '{buku.judul}' berhasil dipinjam oleh {nama_peminjam}.")
        else:
            st.error(f"Buku dengan ID {id_buku} tidak tersedia untuk dipinjam.")

    def kembalikan_buku(self, id_buku):
        buku = self.cari_buku(id_buku)
        if buku and buku.status == "dipinjam":
            buku.status = "tersedia"
            for laporan in self.laporan_peminjaman:
                if laporan["ID Buku"] == id_buku and laporan["Status"] == "dipinjam":
                    laporan["Status"] = "dikembalikan"
                    break
            self.simpan_data()
            st.success(f"Buku '{buku.judul}' berhasil dikembalikan.")
        else:
            st.error(f"Buku dengan ID {id_buku} tidak sedang dipinjam.")

    def hapus_buku(self, id_buku):
        buku = self.cari_buku(id_buku)
        if buku:
            self.daftar_buku.remove(buku)
            self.simpan_data()
            st.success(f"Buku dengan ID {id_buku} berhasil dihapus.")
            self.tampilkan_semua_buku()
        else:
            st.error(f"Buku dengan ID {id_buku} tidak ditemukan.")

    def edit_buku(self, id_buku, **kwargs):
        buku = self.cari_buku(id_buku)
        if buku:
            for key, value in kwargs.items():
                if hasattr(buku, key):
                    setattr(buku, key, value)
            self.simpan_data()
            st.success(f"Buku dengan ID {id_buku} berhasil diperbarui.")
            self.tampilkan_semua_buku()
        else:
            st.error(f"Buku dengan ID {id_buku} tidak ditemukan.")

    def tampilkan_laporan_peminjaman(self):
        df = pd.DataFrame(self.laporan_peminjaman)
        st.table(df)

    def simpan_ke_excel(self):
        data = []
        for buku in self.daftar_buku:
            if isinstance(buku, BukuDigital):
                data.append([buku.id_buku, buku.judul, buku.penulis, buku.tahun_terbit, buku.status, buku.ukuran_file, buku.format_file, None, None])
            elif isinstance(buku, BukuFisik):
                data.append([buku.id_buku, buku.judul, buku.penulis, buku.tahun_terbit, buku.status, None, None, buku.jumlah_halaman, buku.berat])

        df = pd.DataFrame(data, columns=['ID', 'Judul', 'Penulis', 'Tahun Terbit', 'Status', 'Ukuran File', 'Format File', 'Jumlah Halaman', 'Berat'])
        df.to_excel('aplikasi_perpustakaan.xlsx', index=False)

# Inisialisasi perpustakaan dalam session state
if 'perpustakaan' not in st.session_state:
    st.session_state.perpustakaan = Perpustakaan()

# Antarmuka pengguna dengan Streamlit
st.title("Aplikasi Perpustakaan")

# Sidebar untuk navigasi
with st.sidebar:
    page = option_menu(
        "Perpustakaan digital",
        ["Tambah Buku", "Daftar Buku", "Pinjam Buku", "Kembalikan Buku", "Edit Buku", "Hapus Buku", "Cari Buku", "Laporan Peminjaman"],
        icons=["book", "list", "download", "upload", "upload", "trash", "search", "clipboard"],
        menu_icon="cast",
        default_index=0,
    )

if page == "Tambah Buku":
    st.header("Tambah Buku")
    id_buku = st.number_input("ID Buku", min_value=1, step=1)
    judul = st.text_input("Judul Buku")
    penulis = st.text_input("Penulis")
    tahun_terbit = st.number_input("Tahun Terbit", min_value=1000, step=1)
    jenis_buku = st.selectbox("Jenis Buku", ["Digital", "Fisik"])

    if jenis_buku == "Digital":
        ukuran_file = st.number_input("Ukuran File (MB)", min_value=0.0, step=0.1)
        format_file = st.text_input("Format File")
        if st.button("Tambah Buku Digital"):
            if judul and penulis and tahun_terbit and ukuran_file and format_file:
                buku = BukuDigital(id_buku, judul, penulis, tahun_terbit, ukuran_file, format_file)
                st.session_state.perpustakaan.tambah_buku(buku)
            else:
                st.error("Harap isi semua kolom.")

    elif jenis_buku == "Fisik":
        jumlah_halaman = st.number_input("Jumlah Halaman", min_value=1, step=1)
        berat = st.number_input("Berat (gram)", min_value=0.0, step=0.1)
        if st.button("Tambah Buku Fisik"):
            if judul and penulis and tahun_terbit and jumlah_halaman and berat:
                buku = BukuFisik(id_buku, judul, penulis, tahun_terbit, jumlah_halaman, berat)
                st.session_state.perpustakaan.tambah_buku(buku)
            else:
                st.error("Harap isi semua kolom.")

elif page == "Daftar Buku":
    st.header("Daftar Buku di Perpustakaan")
    if st.button("Tampilkan Semua Buku"):
        st.session_state.perpustakaan.tampilkan_semua_buku()
    st.write(f"Jumlah buku tersedia: {st.session_state.perpustakaan.hitung_buku_tersedia()}")

elif page == "Pinjam Buku":
    st.header("Pinjam Buku")
    id_pinjam = st.number_input("ID Buku untuk Dipinjam", min_value=1, step=1)
    nama_peminjam = st.text_input("Nama Peminjam")
    if st.button("Pinjam Buku"):
        st.session_state.perpustakaan.pinjam_buku(id_pinjam, nama_peminjam)

elif page == "Kembalikan Buku":
    st.header("Kembalikan Buku")
    id_kembali = st.number_input("ID Buku untuk Dikembalikan", min_value=1, step=1)
    if st.button("Kembalikan Buku"):
        st.session_state.perpustakaan.kembalikan_buku(id_kembali)

elif page == "Edit Buku":
    st.header("Edit Buku")
    id_edit = st.number_input("ID Buku untuk Diedit", min_value=1, step=1)
    field_to_edit = st.selectbox("Field yang akan Diedit", ["judul", "penulis", "tahun_terbit", "ukuran_file", "format_file", "jumlah_halaman", "berat"])
    new_value = st.text_input(f"Nilai baru untuk {field_to_edit}")
    if st.button("Edit Buku"):
        if new_value:
            st.session_state.perpustakaan.edit_buku(id_edit, **{field_to_edit: new_value})
        else:
            st.error("Harap isi nilai baru untuk field yang akan diedit.")

elif page == "Hapus Buku":
    st.header("Hapus Buku")
    id_hapus = st.number_input("ID Buku untuk Dihapus", min_value=1, step=1)
    if st.button("Hapus Buku"):
        st.session_state.perpustakaan.hapus_buku(id_hapus)

elif page == "Cari Buku":
    st.header("Cari Buku")
    id_cari = st.number_input("ID Buku untuk Dicari", min_value=1, step=1)
    if st.button("Cari Buku"):
        buku = st.session_state.perpustakaan.cari_buku(id_cari)
        if buku:
            st.write(buku.info_buku())
        else:
            st.error(f"Buku dengan ID {id_cari} tidak ditemukan.")

elif page == "Laporan Peminjaman":
    st.header("Laporan Peminjaman Buku")
    if st.button("Tampilkan Laporan Peminjaman"):
        st.session_state.perpustakaan.tampilkan_laporan_peminjaman()
