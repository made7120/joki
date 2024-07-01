import streamlit as st
import sqlite3
import json
import os
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.utils.exceptions import InvalidFileException

class Buku:
    def __init__(self, judul, penulis, tahun_terbit, status="tersedia"):
        self.judul = judul
        self.penulis = penulis
        self.tahun_terbit = tahun_terbit
        self.status = status

    def info_buku(self):
        return {
            "Judul": self.judul,
            "Penulis": self.penulis,
            "Tahun Terbit": self.tahun_terbit,
            "Status": self.status
        }

class BukuDigital(Buku):
    def __init__(self, judul, penulis, tahun_terbit, ukuran_file, format_file, status="tersedia"):
        super().__init__(judul, penulis, tahun_terbit, status)
        self.ukuran_file = ukuran_file
        self.format_file = format_file

    def info_buku(self):
        info = super().info_buku()
        info.update({"Ukuran File (MB)": self.ukuran_file, "Format File": self.format_file})
        return info

class BukuFisik(Buku):
    def __init__(self, judul, penulis, tahun_terbit, jumlah_halaman, berat, status="tersedia"):
        super().__init__(judul, penulis, tahun_terbit, status)
        self.jumlah_halaman = jumlah_halaman
        self.berat = berat

    def info_buku(self):
        info = super().info_buku()
        info.update({"Jumlah Halaman": self.jumlah_halaman, "Berat (gram)": self.berat})
        return info

class Perpustakaan:
    def __init__(self, data_file="data_buku.json"):
        self.data_file = data_file
        self.daftar_buku = self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as file:
                    data = json.load(file)
                    daftar_buku = []
                    for item in data:
                        if "Ukuran File (MB)" in item:
                            buku = BukuDigital(
                                judul=item["Judul"],
                                penulis=item["Penulis"],
                                tahun_terbit=item["Tahun Terbit"],
                                ukuran_file=item["Ukuran File (MB)"],
                                format_file=item["Format File"],
                                status=item["Status"]
                            )
                        elif "Jumlah Halaman" in item:
                            buku = BukuFisik(
                                judul=item["Judul"],
                                penulis=item["Penulis"],
                                tahun_terbit=item["Tahun Terbit"],
                                jumlah_halaman=item["Jumlah Halaman"],
                                berat=item["Berat (gram)"],
                                status=item["Status"]
                            )
                        else:
                            buku = Buku(
                                judul=item["Judul"],
                                penulis=item["Penulis"],
                                tahun_terbit=item["Tahun Terbit"],
                                status=item["Status"]
                            )
                        daftar_buku.append(buku)
                    return daftar_buku
            except json.JSONDecodeError:
                st.warning("File JSON kosong atau tidak valid. Menginisialisasi dengan daftar kosong.")
                return []
        return []

    def save_data(self):
        data = [buku.info_buku() for buku in self.daftar_buku]
        with open(self.data_file, "w") as file:
            json.dump(data, file)

    def tambah_buku(self, buku):
        self.daftar_buku.append(buku)
        self.save_data()
        st.success(f"Buku '{buku.judul}' berhasil ditambahkan.")  

        # Menyimpan data ke file Excel
        self.save_to_excel()

    def save_to_excel(self):
        try:
            if os.path.exists("daftar_buku.xlsx"):
                wb = load_workbook("daftar_buku.xlsx")
                ws = wb.active
            else:
                wb = Workbook()
                ws = wb.active
                ws.append(["Judul", "Penulis", "Tahun Terbit", "Status"])

            # Clear the existing data
            for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
                for cell in row:
                    cell.value = None

            # Add new data
            for buku in self.daftar_buku:
                ws.append([buku.judul, buku.penulis, buku.tahun_terbit, buku.status])
            wb.save("daftar_buku.xlsx")
        except PermissionError:
            st.error("Gagal menyimpan ke 'daftar_buku.xlsx'. Pastikan file tidak sedang terbuka di program lain.")
        except InvalidFileException:
            st.error("Format file tidak valid atau rusak.")
        except Exception as e:
            st.error(f"Gagal menyimpan ke 'daftar_buku.xlsx'. Kesalahan: {e}")

    def hapus_buku(self, judul):
        buku_dihapus = None
        for buku in self.daftar_buku:
            if buku.judul.lower() == judul.lower():
                buku_dihapus = buku
                break

        if buku_dihapus:
            self.daftar_buku.remove(buku_dihapus)
            self.save_data()
            self.save_to_excel()
            st.success(f"Buku '{judul}' berhasil dihapus.")
        else:
            st.warning(f"Buku '{judul}' tidak ditemukan.")

    def cari_buku(self, judul):
        for buku in self.daftar_buku:
            if buku.judul.lower() == judul.lower():
                return buku
        return None

    def tampilkan_semua_buku(self):
        return [buku.info_buku() for buku in self.daftar_buku]

    def pinjam_buku(self, judul):
        buku = self.cari_buku(judul)
        if buku and buku.status == "tersedia":
            buku.status = "dipinjam"
            self.save_data()
            self.save_to_excel()
            return f"Buku '{judul}' berhasil dipinjam."
        else:
            return f"Buku '{judul}' tidak tersedia untuk dipinjam."

    def kembalikan_buku(self, judul):
        buku = self.cari_buku(judul)
        if buku and buku.status == "dipinjam":
            buku.status = "tersedia"
            self.save_data()
            self.save_to_excel()
            return f"Buku '{judul}' berhasil dikembalikan."
        else:
            return f"Buku '{judul}' tidak sedang dipinjam."

    def tampilkan_buku_dipinjam(self):
        return [buku.info_buku() for buku in self.daftar_buku if buku.status == "dipinjam"]

    def tampilkan_buku_dikembalikan(self):
        return [buku.info_buku() for buku in self.daftar_buku if buku.status == "tersedia"]

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Cek apakah tabel 'hewan' sudah ada
    if not table_exists(conn, 'hewan'):
        # Jika tidak, buat tabel 'hewan'
        cursor.execute("""
            CREATE TABLE hewan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT,
                jenis TEXT
            );
        """)
        conn.commit()

    # Cek apakah kolom 'gambar' sudah ada
    if not column_exists(conn, 'hewan', 'gambar'):
        cursor.execute("ALTER TABLE hewan ADD COLUMN gambar TEXT")
        conn.commit()

    conn.close()

def table_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    return cursor.fetchone() is not None

def column_exists(conn, table_name, column_name):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [col[1] for col in cursor.fetchall()]
    return column_name in columns

def main():
    st.title("Selamat Datang di Perpustakaan Digital")
    
    st.markdown(
        """
        <style>
        body {
            background-color: #ff8c00;
        }
        .stApp {
            background-color: #c2dfff;
        }
        .css-1544g2n {
            display: flex;
            flex-direction: row-reverse;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    with col1:
        if st.button("💻️ Tambah Buku Digital"):
            st.session_state['menu'] = "Tambah Buku Digital"
    with col2:
        if st.button("📚️ Tambah Buku Fisik"):
            st.session_state['menu'] = "Tambah Buku Fisik"
    with col3:
        if st.button("📖️ Tampilkan Semua Buku"):
            st.session_state['menu'] = "Tampilkan Semua Buku"
    with col4:
        if st.button("📝️ Pinjam Buku"):
            st.session_state['menu'] = "Pinjam Buku"
    with col5:
        if st.button("📚️‍♂️ Kembalikan Buku"):
            st.session_state['menu'] = "Kembalikan Buku"
    with col6:
        if st.button("📊️ Tampilkan Buku yang Dipinjam"):
            st.session_state['menu'] = "Tampilkan Buku yang Dipinjam"
    with col7:
        if st.button("📈️ Tampilkan Buku yang Dikembalikan"):
            st.session_state['menu'] = "Tampilkan Buku yang Dikembalikan"
    
    choice = st.session_state.get('menu', 'Tampilkan Semua Buku')

    if choice == "Tambah Buku Digital":
        st.subheader("Tambah Buku Digital")
        st.image("digital_book.jpg", width=200)
        judul = st.text_input("Judul", label_visibility="visible")
        penulis = st.text_input("Penulis", label_visibility="visible")
        tahun_terbit = st.number_input("Tahun Terbit", min_value=0, max_value=2024, step=1, label_visibility="visible")
        ukuran_file = st.number_input("Ukuran File (MB)", min_value=0.0, step=0.1, label_visibility="visible")
        format_file = st.selectbox("Format File", ["PDF", "EPUB", "MOBI"], label_visibility="visible")
        if st.button("Tambah Buku", key="tambah_digital"):
            buku = BukuDigital(judul, penulis, tahun_terbit, ukuran_file, format_file)
            perpustakaan.tambah_buku(buku)

    elif choice == "Tambah Buku Fisik":
        st.subheader("Tambah Buku Fisik")
        st.image("physical_book.jpg", width=200)
        judul = st.text_input("Judul", label_visibility="visible")
        penulis = st.text_input("Penulis", label_visibility="visible")
        tahun_terbit = st.number_input("Tahun Terbit", min_value=0, max_value=2024, step=1, label_visibility="visible")
        jumlah_halaman = st.number_input("Jumlah Halaman", min_value=1, step=1, label_visibility="visible")
        berat = st.number_input("Berat (gram)", min_value=0.0, step=0.1, label_visibility="visible")
        if st.button("Tambah Buku", key="tambah_fisik"):
            buku = BukuFisik(judul, penulis, tahun_terbit, jumlah_halaman, berat)
            perpustakaan.tambah_buku(buku)

    elif choice == "Tampilkan Semua Buku":
        st.subheader("Tampilkan Semua Buku")
        st.image("all_books.jpg", width=200)
        buku_list = perpustakaan.tampilkan_semua_buku()
        if buku_list:
            df = pd.DataFrame(buku_list)
            st.table(df)
            judul_hapus = st.text_input("Judul Buku yang Ingin Dihapus", label_visibility="visible")
            if st.button("Hapus Buku"):
                perpustakaan.hapus_buku(judul_hapus)
                st.success(f"Buku '{judul_hapus}' berhasil dihapus.")
                st.experimental_rerun()
        else:
            st.write("Tidak ada buku di perpustakaan.")
    
    elif choice == "Pinjam Buku":
        st.subheader("Pinjam Buku")
        st.image("borrow_book.jpg", width=200)
        judul = st.text_input("Judul Buku yang Akan Dipinjam", label_visibility="visible")
        if st.button("Pinjam Buku", key="pinjam"):
            pesan = perpustakaan.pinjam_buku(judul)
            st.info(pesan)

    elif choice == "Kembalikan Buku":
        st.subheader("Kembalikan Buku")
        st.image("return_book.jpg", width=200)
        judul = st.text_input("Judul Buku yang Akan Dikembalikan", label_visibility="visible")
        if st.button("Kembalikan Buku", key="kembalikan"):
            pesan = perpustakaan.kembalikan_buku(judul)
            st.info(pesan)
        
    elif choice == "Tampilkan Buku yang Dipinjam":
        st.subheader("Buku yang Sedang Dipinjam")
        st.image("gambar.jpg", width=200)
        buku_dipinjam = perpustakaan.tampilkan_buku_dipinjam()
        if buku_dipinjam:
            df = pd.DataFrame(buku_dipinjam)
            st.table(df)
        else:
            st.info("Tidak ada buku yang sedang dipinjam.")

    elif choice == "Tampilkan Buku yang Dikembalikan":
        st.subheader("Buku yang Telah Dikembalikan")
        st.image("hasil.jpg", width=200)
        buku_dikembalikan = perpustakaan.tampilkan_buku_dikembalikan()
        if buku_dikembalikan:
            df = pd.DataFrame(buku_dikembalikan)
            st.table(df)
        else:
            st.info("Belum ada buku yang dikembalikan.")

if __name__ == "__main__":
    init_db()
    main()
