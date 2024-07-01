import os
from abc import ABC, abstractmethod
import sqlite3
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import hashlib

# Fungsi untuk memastikan direktori 'images' ada
def ensure_images_directory_exists():
    if not os.path.exists("images"):
        os.makedirs("images")

# Memastikan direktori 'images' ada saat aplikasi dimulai
ensure_images_directory_exists()

# Koneksi ke SQLite
def create_connection():
    conn = sqlite3.connect('peternakan1.db')
    return conn

# Inisialisasi database dan tabel
def init_db():
    conn = create_connection()
    cursor = conn.cursor()
    
    # Inisialisasi tabel hewan
    cursor.execute("PRAGMA table_info(hewan)")
    columns = [column[1] for column in cursor.fetchall()]
    if "gambar" not in columns:
        cursor.execute("ALTER TABLE hewan ADD COLUMN gambar TEXT")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hewan (
            id TEXT PRIMARY KEY,
            nama TEXT,
            umur INTEGER,
            jenis TEXT,
            ras_warna_bulu TEXT,
            berat REAL,
            gambar TEXT
        )
    ''')
    
    # Inisialisasi tabel akun
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS akun (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Fungsi login
def login(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM akun WHERE username = ? AND password = ?', (username, hash_password(password)))
    account = cursor.fetchone()
    cursor.close()
    conn.close()
    return account

# Fungsi daftar akun
def register(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO akun (username, password) VALUES (?, ?)', (username, hash_password(password)))
    conn.commit()
    cursor.close()
    conn.close()

# Kelas Abstrak HewanBase
class HewanBase(ABC):
    def __init__(self, id, nama, umur, jenis, ras_warna_bulu, berat, gambar):
        self.id = id
        self.nama = nama
        self.umur = umur
        self.jenis = jenis
        self.ras_warna_bulu = ras_warna_bulu
        self.berat = berat
        self.gambar = gambar

    @abstractmethod
    def info_hewan(self):
        pass

# Kelas Anjing
class Anjing(HewanBase):
    def __init__(self, id, nama, umur, ras, berat, gambar):
        super().__init__(id, nama, umur, 'Anjing', ras, berat, gambar)
        self.ras = ras

    def info_hewan(self):
        info = f"ID: {self.id}, Nama: {self.nama}, Umur: {self.umur} tahun, Jenis: {self.jenis}"
        return f"{info}, Ras: {self.ras}, Berat: {self.berat} kg"

# Kelas Kucing
class Kucing(HewanBase):
    def __init__(self, id, nama, umur, warna_bulu, berat, gambar):
        super().__init__(id, nama, umur, 'Kucing', warna_bulu, berat, gambar)
        self.warna_bulu = warna_bulu

    def info_hewan(self):
        info = f"ID: {self.id}, Nama: {self.nama}, Umur: {self.umur} tahun, Jenis: {self.jenis}"
        return f"{info}, Warna Bulu: {self.warna_bulu}, Berat: {self.berat} kg"

# Tambahan 10 jenis hewan
class Sapi(HewanBase):
    def __init__(self, id, nama, umur, ras, berat, gambar):
        super().__init__(id, nama, umur, 'Sapi', ras, berat, gambar)
        self.ras = ras

    def info_hewan(self):
        info = f"ID: {self.id}, Nama: {self.nama}, Umur: {self.umur} tahun, Jenis: {self.jenis}"
        return f"{info}, Ras: {self.ras}, Berat: {self.berat} kg"

class Kambing(HewanBase):
    def __init__(self, id, nama, umur, ras, berat, gambar):
        super().__init__(id, nama, umur, 'Kambing', ras, berat, gambar)
        self.ras = ras

    def info_hewan(self):
        info = f"ID: {self.id}, Nama: {self.nama}, Umur: {self.umur} tahun, Jenis: {self.jenis}"
        return f"{info}, Ras: {self.ras}, Berat: {self.berat} kg"

class Ayam(HewanBase):
    def __init__(self, id, nama, umur, ras, berat, gambar):
        super().__init__(id, nama, umur, 'Ayam', ras, berat, gambar)
        self.ras = ras

    def info_hewan(self):
        info = f"ID: {self.id}, Nama: {self.nama}, Umur: {self.umur} tahun, Jenis: {self.jenis}"
        return f"{info}, Ras: {self.ras}, Berat: {self.berat} kg"

class Domba(HewanBase):
    def __init__(self, id, nama, umur, ras, berat, gambar):
        super().__init__(id, nama, umur, 'Domba', ras, berat, gambar)
        self.ras = ras

    def info_hewan(self):
        info = f"ID: {self.id}, Nama: {self.nama}, Umur: {self.umur} tahun, Jenis: {self.jenis}"
        return f"{info}, Ras: {self.ras}, Berat: {self.berat} kg"

class Kelinci(HewanBase):
    def __init__(self, id, nama, umur, warna_bulu, berat, gambar):
        super().__init__(id, nama, umur, 'Kelinci', warna_bulu, berat, gambar)
        self.warna_bulu = warna_bulu

    def info_hewan(self):
        info = f"ID: {self.id}, Nama: {self.nama}, Umur: {self.umur} tahun, Jenis: {self.jenis}"
        return f"{info}, Warna Bulu: {self.warna_bulu}, Berat: {self.berat} kg"

class Bebek(HewanBase):
    def __init__(self, id, nama, umur, ras, berat, gambar):
        super().__init__(id, nama, umur, 'Bebek', ras, berat, gambar)
        self.ras = ras

    def info_hewan(self):
        info = f"ID: {self.id}, Nama: {self.nama}, Umur: {self.umur} tahun, Jenis: {self.jenis}"
        return f"{info}, Ras: {self.ras}, Berat: {self.berat} kg"

class Kuda(HewanBase):
    def __init__(self, id, nama, umur, ras, berat, gambar):
        super().__init__(id, nama, umur, 'Kuda', ras, berat, gambar)
        self.ras = ras

    def info_hewan(self):
        info = f"ID: {self.id}, Nama: {self.nama}, Umur: {self.umur} tahun, Jenis: {self.jenis}"
        return f"{info}, Ras: {self.ras}, Berat: {self.berat} kg"

class Babi(HewanBase):
    def __init__(self, id, nama, umur, ras, berat, gambar):
        super().__init__(id, nama, umur, 'Babi', ras, berat, gambar)
        self.ras = ras

    def info_hewan(self):
        info = f"ID: {self.id}, Nama: {self.nama}, Umur: {self.umur} tahun, Jenis: {self.jenis}"
        return f"{info}, Ras: {self.ras}, Berat: {self.berat} kg"

class Gajah(HewanBase):
    def __init__(self, id, nama, umur, ras, berat, gambar):
        super().__init__(id, nama, umur, 'Gajah', ras, berat, gambar)
        self.ras = ras

    def info_hewan(self):
        info = f"ID: {self.id}, Nama: {self.nama}, Umur: {self.umur} tahun, Jenis: {self.jenis}"
        return f"{info}, Ras: {self.ras}, Berat: {self.berat} kg"

class Singa(HewanBase):
    def __init__(self, id, nama, umur, ras, berat, gambar):
        super().__init__(id, nama, umur, 'Singa', ras, berat, gambar)
        self.ras = ras

    def info_hewan(self):
        info = f"ID: {self.id}, Nama: {self.nama}, Umur: {self.umur} tahun, Jenis: {self.jenis}"
        return f"{info}, Ras: {self.ras}, Berat: {self.berat} kg"

# Kelas Peternakan
class Peternakan:
    def __init__(self):
        self.daftar_hewan = []

    def tambah_hewan(self, hewan):
        conn = create_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO hewan (id, nama, umur, jenis, ras_warna_bulu, berat, gambar) VALUES (?, ?, ?, ?, ?, ?, ?)"
        values = (hewan.id, hewan.nama, hewan.umur, hewan.jenis, hewan.ras_warna_bulu, hewan.berat, hewan.gambar)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()

    def cari_hewan(self, id):
        conn = create_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM hewan WHERE id = ?"
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            jenis_hewan = result[3]
            if jenis_hewan == 'Anjing':
                return Anjing(result[0], result[1], result[2], result[4], result[5], result[6])
            elif jenis_hewan == 'Kucing':
                return Kucing(result[0], result[1], result[2], result[4], result[5], result[6])
            elif jenis_hewan == 'Sapi':
                return Sapi(result[0], result[1], result[2], result[4], result[5], result[6])
            elif jenis_hewan == 'Kambing':
                return Kambing(result[0], result[1], result[2], result[4], result[5], result[6])
            elif jenis_hewan == 'Ayam':
                return Ayam(result[0], result[1], result[2], result[4], result[5], result[6])
            elif jenis_hewan == 'Domba':
                return Domba(result[0], result[1], result[2], result[4], result[5], result[6])
            elif jenis_hewan == 'Kelinci':
                return Kelinci(result[0], result[1], result[2], result[4], result[5], result[6])
            elif jenis_hewan == 'Bebek':
                return Bebek(result[0], result[1], result[2], result[4], result[5], result[6])
            elif jenis_hewan == 'Kuda':
                return Kuda(result[0], result[1], result[2], result[4], result[5], result[6])
            elif jenis_hewan == 'Babi':
                return Babi(result[0], result[1], result[2], result[4], result[5], result[6])
            elif jenis_hewan == 'Gajah':
                return Gajah(result[0], result[1], result[2], result[4], result[5], result[6])
            elif jenis_hewan == 'Singa':
                return Singa(result[0], result[1], result[2], result[4], result[5], result[6])
        return None

    def edit_hewan(self, id, nama=None, umur=None, ras=None, berat=None, warna_bulu=None, gambar=None):
        hewan = self.cari_hewan(id)
        if hewan:
            conn = create_connection()
            cursor = conn.cursor()
            if nama:
                hewan.nama = nama
                cursor.execute("UPDATE hewan SET nama = ? WHERE id = ?", (nama, id))
            if umur:
                hewan.umur = umur
                cursor.execute("UPDATE hewan SET umur = ? WHERE id = ?", (umur, id))
            if isinstance(hewan, (Anjing, Sapi, Kambing, Ayam, Domba, Bebek, Kuda, Babi, Gajah, Singa)) and ras:
                hewan.ras = ras
                cursor.execute("UPDATE hewan SET ras_warna_bulu = ? WHERE id = ?", (ras, id))
            if isinstance(hewan, Kucing) and warna_bulu:
                hewan.warna_bulu = warna_bulu
                cursor.execute("UPDATE hewan SET ras_warna_bulu = ? WHERE id = ?", (warna_bulu, id))
            if berat:
                hewan.berat = berat
                cursor.execute("UPDATE hewan SET berat = ? WHERE id = ?", (berat, id))
            if gambar:
                hewan.gambar = gambar
                cursor.execute("UPDATE hewan SET gambar = ? WHERE id = ?", (gambar, id))
            conn.commit()
            cursor.close()
            conn.close()

    def hapus_hewan(self, id):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM hewan WHERE id = ?", (id,))
        conn.commit()
        cursor.close()
        conn.close()

    def tampilkan_semua_hewan(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nama, umur, jenis, ras_warna_bulu, berat, gambar FROM hewan")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

# Inisialisasi database
init_db()

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

# Session State untuk Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Fungsi untuk menyimpan file yang diunggah
def save_uploaded_file(uploaded_file):
    if not os.path.exists("images"):
        os.makedirs("images")
    with open(os.path.join("images", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return uploaded_file.name

# Login dan Daftar Akun
if not st.session_state.logged_in:
    selected = option_menu(
        menu_title=None,
        options=["Login", "Daftar Akun"],
        icons=["person", "person-plus"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    # Login
    if selected == "Login":
        st.title('Login')
        with st.form('Login'):
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            submitted = st.form_submit_button('Login')

            if submitted:
                account = login(username, password)
                if account:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success('Login berhasil!')
                else:
                    st.error('Username atau password salah.')

    # Daftar Akun
    elif selected == "Daftar Akun":
        st.title('Daftar Akun')
        with st.form('Daftar Akun'):
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            submitted = st.form_submit_button('Daftar')

            if submitted:
                register(username, password)
                st.success('Akun berhasil didaftarkan!')

else:
    st.sidebar.markdown(f"**Logged in as: {st.session_state.username}**")

    # Menu Logout
    if st.sidebar.button('Logout'):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success('Berhasil logout!')

    # Navbar dengan Streamlit Option Menu
    selected = option_menu(
        menu_title=None,
        options=["Tambah Hewan", "Tampilkan Semua Hewan", "Cari dan Edit Hewan", "Hapus Hewan"],
        icons=["plus-circle", "list", "search", "trash"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    # Inisialisasi peternakan
    peternakan = Peternakan()

    # Tambah Hewan
    if selected == "Tambah Hewan":
        st.title('Tambah Hewan')
        with st.form('Tambah Hewan'):
            id = st.text_input('ID')
            nama = st.text_input('Nama')
            umur = st.number_input('Umur', min_value=0)
            jenis = st.selectbox('Jenis', ['Anjing', 'Kucing', 'Sapi', 'Kambing', 'Ayam', 'Domba', 'Kelinci', 'Bebek', 'Kuda', 'Babi', 'Gajah', 'Singa'])
            if jenis in ['Anjing', 'Sapi', 'Kambing', 'Ayam', 'Domba', 'Bebek', 'Kuda', 'Babi', 'Gajah', 'Singa']:
                ras = st.text_input('Ras')
                berat = st.number_input('Berat', min_value=0.0)
            else:
                warna_bulu = st.text_input('Warna Bulu')
                berat = st.number_input('Berat', min_value=0.0)

            gambar = st.file_uploader("Unggah Gambar Hewan", type=["jpg", "png", "jpeg"])
            submitted = st.form_submit_button('Tambah Hewan')

            if submitted:
                if gambar is not None:
                    gambar_name = save_uploaded_file(gambar)
                else:
                    gambar_name = None

                if jenis == 'Anjing':
                    hewan = Anjing(id, nama, umur, ras, berat, gambar_name)
                elif jenis == 'Kucing':
                    hewan = Kucing(id, nama, umur, warna_bulu, berat, gambar_name)
                elif jenis == 'Sapi':
                    hewan = Sapi(id, nama, umur, ras, berat, gambar_name)
                elif jenis == 'Kambing':
                    hewan = Kambing(id, nama, umur, ras, berat, gambar_name)
                elif jenis == 'Ayam':
                    hewan = Ayam(id, nama, umur, ras, berat, gambar_name)
                elif jenis == 'Domba':
                    hewan = Domba(id, nama, umur, ras, berat, gambar_name)
                elif jenis == 'Kelinci':
                    hewan = Kelinci(id, nama, umur, warna_bulu, berat, gambar_name)
                elif jenis == 'Bebek':
                    hewan = Bebek(id, nama, umur, ras, berat, gambar_name)
                elif jenis == 'Kuda':
                    hewan = Kuda(id, nama, umur, ras, berat, gambar_name)
                elif jenis == 'Babi':
                    hewan = Babi(id, nama, umur, ras, berat, gambar_name)
                elif jenis == 'Gajah':
                    hewan = Gajah(id, nama, umur, ras, berat, gambar_name)
                elif jenis == 'Singa':
                    hewan = Singa(id, nama, umur, ras, berat, gambar_name)
                peternakan.tambah_hewan(hewan)
                st.success(f'{jenis} berhasil ditambahkan!')

    # Tampilkan Semua Hewan
    elif selected == "Tampilkan Semua Hewan":
        st.title('Daftar Hewan')
        if st.button('Tampilkan Semua Hewan'):
            results = peternakan.tampilkan_semua_hewan()
            if results:
                df = pd.DataFrame(results, columns=["ID", "Nama", "Umur", "Jenis", "Ras/Warna Bulu", "Berat", "Gambar"])
                st.dataframe(df)
                for index, row in df.iterrows():
                    if row["Gambar"]:
                        image_path = os.path.join("images", row["Gambar"])
                        if os.path.exists(image_path):
                            st.image(image_path, width=100, caption=f"Gambar untuk {row['Nama']}")
                        else:
                            st.write(f"Gambar tidak ditemukan untuk {row['Nama']}")
            else:
                st.write('Tidak ada hewan yang terdaftar.')

    # Cari dan Edit Hewan
    elif selected == "Cari dan Edit Hewan":
        st.title('Cari dan Edit Hewan')
        with st.form('Cari dan Edit Hewan'):
            id_cari = st.text_input('Cari Hewan Berdasarkan ID')
            submit_cari = st.form_submit_button('Cari Hewan')
            if submit_cari:
                hewan = peternakan.cari_hewan(id_cari)
                if hewan:
                    st.write(hewan.info_hewan())
                    if hewan.gambar:
                        image_path = os.path.join("images", hewan.gambar)
                        if os.path.exists(image_path):
                            st.image(image_path, width=100)
                    nama_edit = st.text_input('Edit Nama', value=hewan.nama)
                    umur_edit = st.number_input('Edit Umur', min_value=0, value=hewan.umur)
                    berat_edit = st.number_input('Edit Berat', min_value=0.0, value=hewan.berat)
                    gambar_edit = st.file_uploader("Unggah Gambar Baru", type=["jpg", "png", "jpeg"])
                    if isinstance(hewan, (Anjing, Sapi, Kambing, Ayam, Domba, Bebek, Kuda, Babi, Gajah, Singa)):
                        ras_edit = st.text_input('Edit Ras', value=hewan.ras)
                        warna_bulu_edit = None
                    else:
                        ras_edit = None
                        warna_bulu_edit = st.text_input('Edit Warna Bulu', value=hewan.warna_bulu)

                    submit_edit = st.form_submit_button('Edit Hewan')
                    if submit_edit:
                        if gambar_edit is not None:
                            gambar_name_edit = save_uploaded_file(gambar_edit)
                        else:
                            gambar_name_edit = hewan.gambar
                        peternakan.edit_hewan(id_cari, nama_edit, umur_edit, ras_edit, berat_edit, warna_bulu_edit, gambar_name_edit)
                        st.success('Hewan berhasil diubah!')
                else:
                    st.error('Hewan tidak ditemukan!')

    # Hapus Hewan
    elif selected == "Hapus Hewan":
        st.title('Hapus Hewan')
        with st.form('Hapus Hewan'):
            id_hapus = st.text_input('ID Hewan yang akan Dihapus')
            submit_hapus = st.form_submit_button('Hapus Hewan')
            if submit_hapus:
                peternakan.hapus_hewan(id_hapus)
                st.success('Hewan berhasil dihapus!')

