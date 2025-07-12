import csv
import os
from datetime import datetime

FILE_NAME = "keuangan.csv"

# Struktur Data
transaksi = []  # List untuk data sementara
kategori_pengeluaran = {
    "makan": 0,
    "transport": 0,
    "hiburan": 0,
    "belanja": 0,
    "lainnya": 0
}

# Fungsi bantu
def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["jumlah"] = int(row["jumlah"])
                transaksi.append(row)
    else:
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["id", "tanggal", "jenis", "kategori", "jumlah", "deskripsi"])
            writer.writeheader()

def save_data():
    with open(FILE_NAME, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "tanggal", "jenis", "kategori", "jumlah", "deskripsi"])
        writer.writeheader()
        for t in transaksi:
            writer.writerow(t)

def tampilkan_transaksi():
    if not transaksi:
        print("Belum ada data transaksi.")
        return
    print("\n=== Daftar Transaksi ===")
    for t in transaksi:
        print(f"{t['id']}. [{t['tanggal']}] {t['jenis'].upper()} - {t['kategori']} : Rp{t['jumlah']} ({t['deskripsi']})")

def tambah_transaksi():
    id_baru = str(len(transaksi) + 1)
    tanggal = input("Tanggal (YYYY-MM-DD): ")
    jenis = input("Jenis (pemasukan/pengeluaran): ").lower()
    kategori = input("Kategori: ").lower()
    jumlah = int(input("Jumlah (Rp): "))
    deskripsi = input("Deskripsi: ")

    transaksi.append({
        "id": id_baru,
        "tanggal": tanggal,
        "jenis": jenis,
        "kategori": kategori,
        "jumlah": jumlah,
        "deskripsi": deskripsi
    })
    print("Transaksi berhasil ditambahkan.")
    save_data()

def edit_transaksi():
    tampilkan_transaksi()
    id_edit = input("Masukkan ID transaksi yang ingin diedit: ")
    for t in transaksi:
        if t["id"] == id_edit:
            t["tanggal"] = input(f"Tanggal baru ({t['tanggal']}): ") or t["tanggal"]
            t["jenis"] = input(f"Jenis baru ({t['jenis']}): ") or t["jenis"]
            t["kategori"] = input(f"Kategori baru ({t['kategori']}): ") or t["kategori"]
            t["jumlah"] = int(input(f"Jumlah baru ({t['jumlah']}): ") or t["jumlah"])
            t["deskripsi"] = input(f"Deskripsi baru ({t['deskripsi']}): ") or t["deskripsi"]
            print("Transaksi berhasil diubah.")
            save_data()
            return
    print("ID tidak ditemukan.")

def hapus_transaksi():
    tampilkan_transaksi()
    id_hapus = input("Masukkan ID transaksi yang ingin dihapus: ")
    for i, t in enumerate(transaksi):
        if t["id"] == id_hapus:
            transaksi.pop(i)
            print("Transaksi berhasil dihapus.")
            # Reset ID
            for idx, t in enumerate(transaksi):
                t["id"] = str(idx + 1)
            save_data()
            return
    print("ID tidak ditemukan.")

def laporan_bulanan():
    bulan = input("Masukkan bulan (format MM): ")
    tahun = input("Masukkan tahun (format YYYY): ")
    total_masuk = total_keluar = 0
    for t in transaksi:
        tanggal = datetime.strptime(t["tanggal"], "%Y-%m-%d")
        if tanggal.month == int(bulan) and tanggal.year == int(tahun):
            if t["jenis"] == "pemasukan":
                total_masuk += t["jumlah"]
            elif t["jenis"] == "pengeluaran":
                total_keluar += t["jumlah"]
    print(f"\n=== Laporan Bulan {bulan}/{tahun} ===")
    print(f"Total Pemasukan: Rp{total_masuk}")
    print(f"Total Pengeluaran: Rp{total_keluar}")
    print(f"Saldo Bersih: Rp{total_masuk - total_keluar}")

# Menu CLI
def menu():
    load_data()
    while True:
        print("\n=== Manajemen Keuangan Pribadi ===")
        print("1. Tambah Transaksi")
        print("2. Lihat Transaksi")
        print("3. Edit Transaksi")
        print("4. Hapus Transaksi")
        print("5. Laporan Bulanan")
        print("0. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tambah_transaksi()
        elif pilihan == "2":
            tampilkan_transaksi()
        elif pilihan == "3":
            edit_transaksi()
        elif pilihan == "4":
            hapus_transaksi()
        elif pilihan == "5":
            laporan_bulanan()
        elif pilihan == "0":
            print("Terima kasih! Sampai jumpa.")
            break
        else:
            print("Pilihan tidak valid.")

# Jalankan program
menu()
