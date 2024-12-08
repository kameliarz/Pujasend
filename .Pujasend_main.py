import pandas as pd
import csv
import os
import time
import qrcode
from datetime import datetime
from tabulate import tabulate

#================================================================================
#PENJUAL
#================================================================================

def baca_menu_dari_csv(username): 
    try:
        df = pd.read_csv("stand.csv")
        stand = df[df["Stand"] == username]
        menu = {row["Nama Menu"]: row["Harga"] for index, row in stand.iterrows()}
        return menu
    except FileNotFoundError:
        return {}

def simpan_menu_ke_csv(menu, harga, username):
    nama_stand = username
    menu_baru = {'Stand': nama_stand, 'Nama Menu': menu, 'Harga': harga}
    try:
        df = pd.read_csv('stand.csv', encoding='utf-8-sig')
    except FileNotFoundError:
        print("File tidak ditemukan. Membuat file baru...")
        df = pd.DataFrame(columns=['Stand', 'Nama Menu', 'Harga'])

    menu_baru_df = pd.DataFrame([menu_baru])
    df = pd.concat([df, menu_baru_df], ignore_index=True)
    df.to_csv('stand.csv', index=False, encoding='utf-8-sig')

    print("Menu baru berhasil ditambahkan!")

def kelola_menu(username_km):
    while True:
        menu = baca_menu_dari_csv(username_km)
        header("Penjual > Kelola Menu")
        print("[1] Lihat Menu\n[2] Tambah Menu\n[3] Ubah Menu\n[4] Hapus Menu\n[5] Kembali ke Menu Utama")
        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            header('Penjual > Kelola Menu > Lihat Menu')
            print("\nDaftar Menu:")
            angka = 1
            if menu:
                for nama_menu,harga_menu in menu.items():
                    print(f"{angka}. {nama_menu} - Rp{harga_menu}")
                    angka +=1
            else:
                print("\nMenu masih kosong.")
            input("\n(Enter untuk kembali)")

        elif pilihan == "2":
            header('Penjual > Kelola Menu > Tambah Menu')
            nama_menu = input("Masukkan nama menu: ")
            if nama_menu in menu:
                print(f"{nama_menu} sudah ada di menu.")
            else:
                while True :
                    try:
                        harga_menu = int(input("Masukkan harga menu: "))
                        simpan_menu_ke_csv(nama_menu, harga_menu, username_km)
                        print(f"\n{nama_menu} berhasil ditambahkan!")
                        input('\n(Enter untuk kembali.)')
                        break
                    except ValueError:
                        print("Harga harus berupa angka.")

        elif pilihan == "3":
            header('Penjual > Kelola Menu > Ubah Menu')
            angka = 1
            if menu:
                for nama_menu,harga_menu in menu.items():
                    print(f"{angka}. {nama_menu} - Rp{harga_menu}")
                    angka +=1
                
                nama_menu = input("\nMasukkan nama menu yang ingin diubah: ")
                if nama_menu in menu:
                    print(f"\n| {nama_menu} ditemukan di daftar menu.\n")
                    df = pd.read_csv("stand.csv")
                    hapus_menu_lama = df[df['Nama Menu'] != nama_menu]
                    hapus_menu_lama.to_csv("stand.csv", index=False)
                    ubah = input("Apakah Anda ingin mengubah nama atau harga menu? (y untuk ya, b untuk batal): ").lower()
                
                    if ubah == 'y':
                        nama_baru = input("\nMasukkan nama baru untuk menu: ")
                        while True :
                            try:
                                harga_baru = int(input("Masukkan harga baru untuk menu: "))
                                simpan_menu_ke_csv(nama_baru, harga_baru, username_km)  
                                print(f"Menu {nama_menu} berhasil diubah menjadi {nama_baru} dengan harga Rp{harga_baru}.")
                                input("(Enter untuk kembali.)")
                                break
                            except ValueError:
                                print("Harga harus berupa angka.")
                        
                    elif ubah == 'b':
                        print("Perubahan dibatalkan.")
                        break
                    else:
                        print("Pilihan tidak valid.")
                else:
                    print(f"\n{nama_menu} tidak ditemukan di menu.")
                    input('\n(Enter untuk kembali.)')
            else:
                print("Menu masih kosong.")
                input("(Enter untuk kembali.)")

        elif pilihan == "4":
            header('Penjual > Kelola Menu > Hapus Menu')
            angka = 1
            if menu:
                for nama_menu,harga_menu in menu.items():
                    print(f"{angka}. {nama_menu} - Rp{harga_menu}")
                    angka +=1
            else:
                print("Menu masih kosong.")
            nama_menu = input("\nMasukkan nama menu yang ingin dihapus: ")

            if nama_menu in menu:
                df = pd.read_csv("stand.csv")
                hapus_menu_lama = df[df['Nama Menu'] != nama_menu]
                hapus_menu_lama.to_csv("stand.csv", index=False)
                print(f"{nama_menu} berhasil dihapus!")
            else:
                
                print("\nMenu tidak ditemukan.")
            input('\n(Enter untuk kembali.)')

        elif pilihan == "5":
            break

        else:
            print("Pilihan tidak valid. Coba lagi.")

def baca_data_orderan():
    try:
        return pd.read_csv("orderan.csv")
    except FileNotFoundError:
        print("File 'orderan.csv' tidak ditemukan.")
        return pd.DataFrame(columns=["Stand", "Nama Menu", "Jumlah", "Harga", "Status"])

def tampilkan_pesanan_belum_diproses(stand):
    df = baca_data_orderan()
    df_stand = df[(df["Stand"] == stand) & (df["Status"] == "Belum")]

    if df_stand.empty:
        print(f"\nTidak ada pesanan yang belum diproses.")
    else:
        print(f"\nPesanan belum diproses :")
        for i, row in df_stand.iterrows():
            print(f"{row['Nama Menu']} - {row['Jumlah']} pcs - Rp{row['Harga']}")
    input("\n(Enter untuk kembali.)")

def ubah_status_pesanan(stand):
    df = baca_data_orderan()
    df_stand = df[(df["Stand"] == stand) & (df["Status"] == "Belum")]

    if df_stand.empty:
        print(f"\nTidak ada pesanan yang belum diproses.")
        return

    print(f"\nPesanan belum diproses :")
    for i, row in df_stand.iterrows():
        print(f"{i}. {row['Nama Menu']} - {row['Jumlah']} pcs - Rp{row['Harga']}")

    try:
        index = int(input("\nMasukkan nomor pesanan yang ingin diubah statusnya: "))
        if index not in df_stand.index:
            print("Nomor pesanan tidak valid.")
            return

        df.loc[index, "Status"] = "Sudah"
        df.to_csv("orderan.csv", index=False)
        print(f"Status pesanan nomor {index} berhasil diubah menjadi 'Sudah'.")
    except ValueError:
        print("Input harus berupa angka.")
    input("\n(Enter untuk kembali.)")

def tampilkan_arsip_pesanan(stand):
    df = baca_data_orderan()
    df_stand = df[(df["Stand"] == stand) & (df["Status"] == "Sudah")]

    if df_stand.empty:
        print(f"\nTidak ada arsip pesanan.")
    else:
        print(f"\nArsip pesanan :")
        for i, row in df_stand.iterrows():
            print(f"{i}. {row['Nama Menu']} - {row['Jumlah']} pcs - Rp{row['Harga']}")
    input("\n(Enter untuk kembali.)")

def kelola_orderan(username_ko):
    while True:
        header("Penjual > Kelola Orderan")
        print("[1] Lihat Pesanan Belum Diproses\n[2] Ubah Status Pesanan\n[3] Lihat Arsip Pesanan\n[4] Keluar")
        pilihan = input("Masukkan opsi: ")
        if pilihan == "1":
            header("Penjual > Kelola Orderan > Lihat Pesanan Belum Diproses")
            tampilkan_pesanan_belum_diproses(username_ko)
        elif pilihan == "2":
            header("Penjual > Kelola Orderan > Ubah Status Pesanan")
            ubah_status_pesanan(username_ko)
        elif pilihan == "3":
            header("Penjual > Kelola Orderan > Lihat Arsip Pesanan")
            tampilkan_arsip_pesanan(username_ko)
        elif pilihan == "4":
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def penjual(username):
    while True:
        header("Penjual")
        print("[1] Kelola Menu\n[2] Kelola Orderan\n[3] Keluar")   
        pilihan = input("Masukkan opsi: ")
        if pilihan == "1":
            kelola_menu(username)
        elif pilihan == "2":
            kelola_orderan(username)
        elif pilihan == "3":
            logout()
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

#=========================================================================
#PEMBELI
#=========================================================================

def baca_menu_dari_csv_pembeli():
    try:
        menu_df = pd.read_csv("stand.csv")
        return menu_df
    except FileNotFoundError:
        print("File 'stand.csv' tidak ditemukan.")
        return pd.DataFrame(columns=["Stand", "Nama Menu", "Harga"])

def baca_voucher_dari_csv():
    try:
        voucher_df = pd.read_csv("voucher.csv", header=None, names=["Kode Voucher", "Diskon"])
        return voucher_df
    except FileNotFoundError:
        print("Voucher tidak ditemukan. Pastikan file 'voucher.csv' tersedia.")
        return pd.DataFrame(columns=["Kode Voucher", "Diskon"])

def simpan_orderan_ke_csv(orderan):
    with open("orderan.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(orderan)

def tampilkan_stand(stand_df):
    print("\n=== Daftar Stand ===")
    stands = stand_df["Stand"].unique()
    stand_list = [[i + 1, stand] for i, stand in enumerate(stands)]
    print(tabulate(stand_list, headers=["No", "Stand"], tablefmt="grid"))
    return stands

def pilih_stand(stand_df):
    stands = tampilkan_stand(stand_df)
    while True:
        try:
            pilihan = int(input("\nPilih nomor stand: "))
            if 1 <= pilihan <= len(stands):
                return stands[pilihan - 1]
            else:
                print("Pilihan tidak valid. Coba lagi.")
        except ValueError:
            print("Input harus berupa angka. Coba lagi.")

def animasi_proses():
    print("\nPesanan sedang diproses...", end="", flush=True)
    time.sleep(1)
    print(".", end="", flush=True)
    time.sleep(1)
    print(".", flush=True)
    time.sleep(1)
    print("\nPesanan sedang dibuat dan akan dikirimkan ke alamatmu jika sudah siap!")

def pilih_kecamatan():
    tarif = {
        "kaliwates": {"cepat": 15000, "standar": 13000, "hemat": 11000},
        "sumbersari": {"cepat": 10000, "standar": 8000, "hemat": 6000},
        "patrang": {"cepat": 12000, "standar": 10000, "hemat": 8000},
    }
    while True:
        lokasi = input("Masukkan kecamatan (Kaliwates/Sumbersari/Patrang): ").lower()
        if lokasi in tarif:
            while True:
                print("\nOpsi pengiriman:")
                print("1. Cepat (lebih mahal, lebih cepat)")
                print("2. Standar (seimbang)")
                print("3. Hemat (lebih murah, lebih lama)")
                try:
                    metode = int(input("Pilih metode pengiriman (1/2/3): "))
                    if metode == 1:
                        return lokasi, tarif[lokasi]["cepat"]
                    elif metode == 2:
                        return lokasi, tarif[lokasi]["standar"]
                    elif metode == 3:
                        return lokasi, tarif[lokasi]["hemat"]
                    else:
                        print("Pilihan tidak valid. Coba lagi.")
                except ValueError:
                    print("Input harus berupa angka. Coba lagi.")
        else:
            print("Kecamatan tidak tersedia. Silakan pilih antara Kaliwates, Sumbersari, atau Patrang.")

def hitung_total(keranjang, ongkir, voucher_df, kode_voucher=None):
    subtotal = sum(data["total_harga"] for data in keranjang.values()) 
    diskon = 0
    if kode_voucher:
        if kode_voucher.upper() in voucher_df["Kode Voucher"].values:
            diskon_persen = voucher_df.loc[voucher_df["Kode Voucher"] == kode_voucher.upper(), "Diskon"].values[0]
            diskon = subtotal * (float(diskon_persen) / 100)
            print(f"Voucher {kode_voucher.upper()} diterapkan! Anda mendapatkan diskon {diskon_persen}%.")
        else:
            print("Voucher tidak valid atau tidak berlaku.")
    total = subtotal - diskon + ongkir
    return subtotal, diskon, total
        
def tampilkan_menu(menu_df, stand):
    header("Daftar Stand > Lihat Menu dan Buat Pesanan")
    print(f"\n=== Menu di Stand {stand.capitalize()} ===")
    stand_menu = menu_df[menu_df["Stand"].str.lower() == stand.lower()]
    if not stand_menu.empty:
        menu_list = [[idx + 1, row["Nama Menu"], f"Rp{row['Harga']}"] for idx, (_, row) in enumerate(stand_menu.iterrows())]
        print(tabulate(menu_list, headers=["No", "Nama Menu", "Harga"], tablefmt="grid"))
    else:
        print("Menu kosong. Tidak ada data untuk ditampilkan.")
        
def cetak_struk(keranjang, kecamatan, ongkir, kode_voucher, subtotal, diskon, total):
    header('Struk Belanja')
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n" + "=" * 55)
    print(f"{'Struk Pembelian':^55}")
    print("=" * 55)
    print(f"Tanggal     : {waktu}")
    print(f"Kecamatan   : {kecamatan.capitalize()}")
    print("-" * 55)
    print(f"{'Nama Menu':<30}{'Qty':<6}{'Total':>15}")
    print("-" * 55)
    for nama_menu, data in keranjang.items():
        print(f"{nama_menu:<30}{data['jumlah']:<6}{data['total_harga']:>15}")
    print("-" * 55)
    print(f"{'Subtotal':30}{'':<6}{subtotal:>15}")
    if diskon > 0:
        print(f"{'Diskon':<30}{'':<6}{int(diskon):>15}")
    print(f"{'Ongkir':<30}{'':<6}{ongkir:>15}")
    print("=" * 55)
    print(f"{'Total':<30}{'':<6}{total:>15}")
    print("=" * 55)
    print(f"{'Terima Kasih Telah Berbelanja!':^55}")
    print("=" * 55)

def buat_pesanan(menu_df):
    keranjang = {}
    voucher_df = baca_voucher_dari_csv()
    while True:
        stand = pilih_stand(menu_df)
        header("Daftar Stand > Lihat Menu dan Buat Pesanan")
        tampilkan_menu(menu_df, stand)
        while True:
            try:
                pilihan_menu = int(input("\nMasukkan nomor menu (atau ketik 'selesai' untuk checkout): "))
                stand_menu = menu_df[menu_df["Stand"].str.lower() == stand.lower()]
                if 1 <= pilihan_menu <= len(stand_menu):
                    nama_menu = stand_menu.iloc[pilihan_menu - 1]["Nama Menu"]
                    harga = int(stand_menu.iloc[pilihan_menu - 1]["Harga"])
                    jumlah = int(input(f"Masukkan jumlah {nama_menu}: "))

                    if nama_menu in keranjang:
                        keranjang[nama_menu]["jumlah"] += jumlah
                        keranjang[nama_menu]["total_harga"] += int(harga) * jumlah
                    else:
                        keranjang[nama_menu] = {"jumlah": jumlah, "harga_satuan": harga, "total_harga": harga * jumlah}

                    print(f"{jumlah} {nama_menu} ditambahkan ke keranjang.")
                else:
                    print("Menu tidak ditemukan. Coba lagi.")
            except ValueError:
                if input("\n Apakah anda sudah yakin?(y/t) ").lower() == "y":
                    break
                else:
                    print("Pilihan tidak valid. Coba lagi.")

        if input("Pilih stand lain? (y/n): ").lower() != "y":
            break

    if keranjang:
        header("Daftar Stand > Lihat Menu dan Buat Pesanan > Ringkasan Pesanan")
        ringkasan = [[nama_menu, data["jumlah"], int(data["total_harga"])] for nama_menu, data in keranjang.items()]
        print(tabulate(ringkasan, headers=["Nama Menu", "Jumlah", "Total Harga"], tablefmt="grid"))
        print('\n')
        kecamatan, ongkir = pilih_kecamatan()
        print(f"Ongkir ke kecamatan {kecamatan.capitalize()}: Rp{ongkir}\n")

        kode_voucher = input("Masukkan kode voucher (jika ada) atau tekan Enter: ").upper()

        subtotal, diskon, total = hitung_total(keranjang, ongkir, voucher_df, kode_voucher)

        print(f"\nSubtotal                : Rp{subtotal}")
        if diskon > 0:
            print(f"Diskon                  : Rp{int(diskon)}")
        print(f"Ongkir                  : Rp{ongkir}")
        print(f"Total yang harus dibayar: Rp{total}")

        simpan = input("\nKonfirmasi pesanan? (y/n): ").lower()
        if simpan == "y":
            for nama_menu, data in keranjang.items():
                stand_order = menu_df[menu_df["Nama Menu"].str.lower() == nama_menu.lower()]["Stand"].iloc[0]
                simpan_orderan_ke_csv([stand_order, nama_menu, data["jumlah"], data["total_harga"], "Belum"])
            header("Pembayaran")
            bayar = input('Silahkan pilih metode pembayaran (QRIS/cash): ').lower()
            if bayar == 'cash':
                print(f'Silahkan siapkan uang tunai sebesar {total} ya! ^^')
            elif bayar == 'qris':
                data = "bayar woi"
                qr = qrcode.QRCode(version=1, box_size=1, border=1)  
                qr.add_data(data)
                qr.make(fit=True)
                qr_matrix = qr.get_matrix()
                ascii_qr = "\n".join(
                   "".join("██" if cell else "  " for cell in row) for row in qr_matrix
                )
                print(f'Silahkan scan qrcode berikut dengan total {total}')
                print(ascii_qr)
                while True:
                    validasi_bayar = input("Tekan 'enter' jika telah selesai melakukan pembayaran: ")
                    if validasi_bayar == "":
                        break
                    else:
                        print("Input tidak valid. Harap tekan 'enter' setelah selesai melakukan pembayaran.")
            animasi_proses()
            cetak_struk(keranjang, kecamatan, ongkir, kode_voucher, subtotal, diskon, total)
            print("\nPesanan berhasil disimpan. Terima kasih!")
            input("\nTekan 'Enter' untuk kembali ke menu utama...")
        else:
            print("Pesanan dibatalkan.")
    else:
        print("Tidak ada item yang dipesan.")
        
def pembeli():
    header("Daftar Stand")
    menu_df = baca_menu_dari_csv_pembeli()
    if menu_df.empty:
        return
    buat_pesanan(menu_df)
    
def main_pembeli():
    while True:
        header("PEMBELI")
        print("\n=== Selamat Datang di Pujasend ===")
        print("1. Lihat menu dan pesan")
        print("2. Keluar")
        
        try:
            pilihan_user = int(input("Pilih menu (1/2): "))
            if pilihan_user == 1:
                pembeli()
            elif pilihan_user == 2:
                header("", homepage=1)
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
        except ValueError:
            print("Input harus berupa angka. Silakan coba lagi.")

#================================================================================
#ADMIN
#================================================================================

def ringkasan_penjualan(df):
    laporan = df.groupby("Stand").agg(
        Total_Penjualan=("Harga", "sum"),
        Jumlah_Transaksi=("Jumlah", "sum")
    ).reset_index()

    stand_terlaris = laporan.sort_values(by="Total_Penjualan", ascending=False).iloc[0]

    kalimat = "=== RINGKASAN PENJUALAN ==="
    width = (67-len(kalimat))//2
    print(" "*width+kalimat+" "*width)
    print(tabulate(laporan, headers=["Stand", "Total Penjualan", "Jumlah Transaksi"], tablefmt="fancy_grid", showindex=False))

    print(f"\nStand Terlaris: {stand_terlaris['Stand']} dengan penjualan Rp {stand_terlaris['Total_Penjualan']:,}")
    input("\n(Enter untuk Kembali.)")

def detail_penjualan_per_stand(df):
    kalimat = "=== DETAIL PENJUALAN PER STAND ==="
    width = (67-len(kalimat))//2
    print(" "*width+kalimat+" "*width)
    stands = df["Stand"].unique()

    for stand in stands:
        print(f"\n{stand}:")
        stand_data = df[df["Stand"] == stand]
        laporan_menu = stand_data.groupby("Nama Menu").agg(
            Jumlah_Terjual=("Jumlah", "sum"),
            Total_Pendapatan=("Harga", "sum")
        ).reset_index()

        print(tabulate(laporan_menu, headers=["Menu", "Jumlah Terjual", "Total Pendapatan"], tablefmt="fancy_grid", showindex=False))
    input("\n(Enter untuk Kembali.)")

def statistik(df):
    total_penjualan = df["Harga"].sum()
    rata_rata_penjualan = df.groupby("Stand")["Harga"].sum().mean()

    kontribusi = df.groupby("Stand")["Harga"].sum().reset_index()
    kontribusi["Kontribusi (%)"] = (kontribusi["Harga"] / total_penjualan) * 100
    
    kalimat = "=== STATISTIK ==="
    width = (67-len(kalimat))//2
    print(" "*width+kalimat+" "*width)
    print(f"Total Penjualan: Rp {total_penjualan:,}")
    print(f"Rata-rata Penjualan per Stand: Rp {rata_rata_penjualan:,.2f}")
    
    print(f"\n\nKontribusi Penjualan per Stand:\n")
    print(tabulate(kontribusi, headers=["Stand", "Total Penjualan", "Kontribusi (%)"], tablefmt="fancy_grid", showindex=False))

    input("\n(Enter untuk Kembali.)")

def catatan_penjualan():  
    while True : 
        header("Admin > Catatan Penjualan")
        print("[1] Ringkasan Penjualan\n[2] Detail Penjualan per Stand\n[3] Statistik\n[4] Kembali")
        df = pd.read_csv("orderan.csv")
        pilihan = input("Masukkan opsi: ")
        if pilihan == '1':
            header("Admin > Catatan Penjualan > Ringkasan Penjualan")
            ringkasan_penjualan(df)
        elif pilihan == "2":
            header("Admin > Catatan Penjualan > Detail Penjualan per Stand")
            detail_penjualan_per_stand(df)
        elif pilihan == "3" :
            header("Admin > Catatan Penjualan > Statistik")
            statistik(df)
        elif pilihan == "4" :
            break
        else :
            print("Pilihan tidak valid.")

def voucher():
    while True :
        header('Admin > Kelola Voucher')
        print("[1] Lihat Voucher \n[2] Tambah Voucher \n[3] Ubah Voucher \n[4] Hapus Voucher \n[5] Kembali")
        pilihan = input("Masukkan opsi: ")
        if pilihan == "1":
            header("Admin > Kelola Voucher > Lihat Voucher")
            voucher = pd.read_csv('voucher.csv')
            print(tabulate(voucher, headers="keys", tablefmt="fancy_grid", showindex=False))
            input("\n(Enter untuk kembali.)")
        elif pilihan == "2":
            header("Admin > Kelola Voucher > Tambah Voucher")
            voucher = pd.read_csv("voucher.csv")
            nama_voucher = input("Masukkan nama voucher: ")
            if nama_voucher in voucher:
                print(f"{nama_voucher} sudah ada di menu.")
            else:
                try:
                    banyak_diskon = int(input("Masukkan diskon: "))
                    data_baru = {'Kode Voucher' : nama_voucher, 'Diskon (%)' : banyak_diskon}
                    data_baru = pd.DataFrame([data_baru])  # Ubah data baru menjadi DataFrame
                    voucher = pd.concat([voucher, data_baru], ignore_index=True)
                    voucher.to_csv('voucher.csv', index=False)
                    print(f"\n{nama_voucher} berhasil ditambahkan!")
                    input('\n(Enter untuk kembali.)')
                except ValueError:
                    print("Persentase harus berupa angka.")
        elif pilihan == "3":
            header("Admin > Kelola Voucher > Ubah Voucher")
            voucher = pd.read_csv("voucher.csv")
            print(tabulate(voucher, headers="keys", tablefmt="fancy_grid", showindex=False))
            nama_voucher = input("\nMasukkan nama voucher yang ingin diubah: ")
            if nama_voucher in voucher["Kode Voucher"].values:
                print(f"{nama_voucher} sudah ada di menu.")
                ubah = input("Apakah Anda ingin mengubah nama kode voucher atau banyak diskon? (y untuk ya, b untuk batal): ").lower()
            
                if ubah == 'y':
                    nama_baru = input("Masukkan nama baru untuk voucher: ")
                    try:
                        banyak_diskon = int(input("Masukkan diskon: "))
                        data_baru = {'Kode Voucher' : nama_baru, 'Diskon (%)' : banyak_diskon}
                        hapus_voucher_lama = voucher[voucher['Kode Voucher'] != nama_voucher]
                        hapus_voucher_lama.to_csv("voucher.csv", index=False)
                        data_baru = pd.DataFrame([data_baru])  # Ubah data baru menjadi DataFrame
                        voucher = pd.concat([hapus_voucher_lama, data_baru], ignore_index=True)
                        voucher.to_csv('voucher.csv', index=False)
                        print(f"Voucher {nama_voucher} berhasil diubah menjadi {nama_baru} dengan potongan harga {banyak_diskon}%.")
                    except ValueError:
                        print("Harga harus berupa angka.")
                    
                elif ubah == 'b':
                    print("Perubahan dibatalkan.")
                    break
                else:
                    print("Pilihan tidak valid.")
            else:
                print(f"\nVoucher '{nama_voucher}' tidak ditemukan di menu.")
            input("\n(Enter untuk kembali.)")
                 
        elif pilihan == "4":
            header("Admin > Kelola Voucher > Hapus Voucher")
            voucher = pd.read_csv("voucher.csv")
            print(tabulate(voucher, headers="keys", tablefmt="fancy_grid", showindex=False))
            nama_voucher = input("\nMasukkan nama voucher yang ingin dihapus: ")
            if nama_voucher in voucher["Kode Voucher"].values:
                hapus_voucher_lama = voucher[voucher['Kode Voucher'] != nama_voucher]
                hapus_voucher_lama.to_csv("voucher.csv", index=False)
                print(f"{nama_voucher} berhasil dihapus!")
            else:
                print("\nVoucher tidak ditemukan.")
            input('\n(Enter untuk kembali.)')
        elif pilihan == "5":
            break 
        else:
            print("Pilihan tidak valid. Coba lagi.")

def kelola_user_penjual():
    while True :
        daftar_pengguna = pd.read_csv('DaftarPengguna.csv')
        header('Admin > Kelola User')
        print("[1] Lihat Daftar Pengguna \n[2] Ubah Penjual \n[3] Hapus Penjual \n[4] Kembali")
        pilihan = input("Masukkan opsi: ")

        while pilihan == "1":
            header("Admin > Kelola User Penjual > Lihat Daftar Pengguna")
            print("[1] Lihat Daftar Penjual \n[2] Lihat Daftar Pembeli \n[3] Kembali")
            masukkan = input("Masukkan opsi: ")
            if masukkan == "1":
                header("Admin > Kelola User Penjual > Lihat Daftar Pengguna > Lihat Daftar Penjual")
                daftar_penjual = daftar_pengguna[daftar_pengguna['role'] == 'Penjual']
                print(tabulate(daftar_penjual, headers="keys", tablefmt="fancy_grid", showindex=False))
                input("\n(Enter untuk kembali.)")
            elif masukkan == "2":
                header("Admin > Kelola User Penjual > Lihat Daftar Pengguna > Lihat Daftar Pembeli")
                daftar_pembeli = daftar_pengguna[daftar_pengguna['role'] == 'Pembeli']
                print(tabulate(daftar_pembeli, headers="keys", tablefmt="fancy_grid", showindex=False))
                input("\n(Enter untuk kembali.)")
            elif masukkan == "3" :
                break
            else :
                print("Pilihan tidak valid.")
                input("")

        if pilihan == "2":
            header("Admin > Kelola User Penjual > Ubah Penjual")
            daftar_penjual = daftar_pengguna[daftar_pengguna['role'] == 'Penjual']
            daftar_stand = pd.read_csv("stand.csv")
            print(daftar_penjual)
            nama_penjual = input("\nMasukkan nama user yang ingin diubah: ")
            if nama_penjual in daftar_penjual["username"].values:
                print(f"{nama_penjual} sudah ada di daftar.")
                ubah = input("Apakah Anda ingin mengubah nama user? (y untuk ya, b untuk batal): ").lower()
                if ubah == 'y':
                    nama_baru = input("Masukkan nama yang baru untuk user : ")
                    daftar_pengguna.loc[daftar_pengguna["username"] == nama_penjual, "username"] = nama_baru
                    daftar_pengguna.to_csv("DaftarPengguna.csv", index=False)
                    daftar_stand.loc[daftar_stand["Stand"] == nama_penjual, "Stand"] = nama_baru
                    daftar_stand.to_csv("stand.csv", index=False)
                    print(f"User Penjual {nama_penjual} berhasil diubah menjadi {nama_baru}.")
                elif ubah == 'b':
                    print("Perubahan dibatalkan.")
                    break
                else:
                    print("Pilihan tidak valid.")
            else:
                print(f"\n{nama_penjual} tidak ditemukan di daftar.")
            input("\n(Enter untuk kembali.)")
                             
        elif pilihan == "3":
            header("Admin > Kelola Penjual > Hapus Penjual")
            daftar_penjual = daftar_pengguna[daftar_pengguna['role'] == 'Penjual']
            daftar_stand = pd.read_csv("stand.csv")
            print(daftar_penjual)
            nama_penjual = input("\nMasukkan nama user yang ingin dihapus: ")
    
            if nama_penjual in daftar_penjual["username"].values:
                print(f"{nama_penjual} ditemukan dalam daftar.")
                hapus = input("Apakah Anda yakin ingin menghapus penjual ini? (y untuk ya, b untuk batal): ").lower()
                if hapus == 'y':
                    daftar_pengguna = daftar_pengguna[daftar_pengguna["username"] != nama_penjual]
                    daftar_pengguna.to_csv("DaftarPengguna.csv", index=False)
                    daftar_stand = daftar_stand[daftar_stand["Stand"] != nama_penjual]
                    daftar_stand.to_csv("stand.csv", index=False)
                    print(f"Penjual {nama_penjual} berhasil dihapus dari semua file terkait.")
                elif hapus == 'b':
                    print("Penghapusan dibatalkan.")
                else:
                    print("Pilihan tidak valid. Kembali ke menu sebelumnya.")
            else:
                print(f"{nama_penjual} tidak ditemukan dalam daftar.")
                input('\n(Enter untuk kembali.)')
        
        elif pilihan == "4":
            break

        else:
            print("Pilihan tidak valid. Coba lagi.")

def admin():
    while True:
        header("Admin")
        print("[1] Kelola User\n[2] Catatan Penjualan\n[3] Kelola Voucher\n[4] Keluar")   
        pilihan = input("Masukkan opsi: ")
        if pilihan == "1":
            kelola_user_penjual()
        elif pilihan == "2":
            catatan_penjualan()
        elif pilihan == "3":
            voucher()
        elif pilihan == "4":
            logout()
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

#=========================================================================
def header(isi='', homepage=0):
    os.system('cls')
    with open('Header.txt', 'r', encoding='utf-8') as file:
        filetxt = file.read()
    print(filetxt)
    width = (67-len(isi))//2
    print(" "*width+isi+" "*width)
    print('='*67)
    if homepage == 1:
        kalimat = "Selamat Datang di aplikasi kami! ^-^"
        width = (67-len(kalimat))//2
        print(" "*width+kalimat+" "*width)
        kalimat = "Untuk masuk silahkan pilih opsi dibawah ini"
        width = (67-len(kalimat))//2
        print(" "*width+kalimat+" "*width)
        print("[1] Log in\n[2] Sign in\n[0] Keluar")
        while (True):
            pilihan = input("")
            match pilihan:
                case '1':
                    login()
                    break
                case '2':
                    registrasi()
                    break
                case '0':
                    logout()
                    break
                case _ :
                    print('Maaf, silahkan masukkan pilihan yang tersedia.')

def login():
    header('LOGIN')
    df = pd.read_csv('DaftarPengguna.csv')
    daftar_pengguna = df.set_index("username")
    i = 0
    j = 0
    while (i<3):
        print("\nMasukkan username anda : ")
        username1 = input("")
        if username1 in daftar_pengguna.index:
            i = 3
            while (j <3):
                print("\nMasukkan Password : ")
                password = input("")
                if password == daftar_pengguna.loc[username1, 'password']:
                    print(f'\n| Anda masuk sebagai {username1}')
                    input("\n(Tekan Enter untuk melanjutkan.)")
                    print(daftar_pengguna.loc[username1, 'role'])
                    if daftar_pengguna.loc[username1, 'role'] == "Penjual":
                        penjual(username1)
                        j = 3
                    elif daftar_pengguna.loc[username1, 'role'] == "Pembeli":
                        main_pembeli()
                        j = 3
                    elif daftar_pengguna.loc[username1, 'role'] == "Admin":
                        admin()
                        j = 3
                else :
                    j +=1
                    if j < 2:
                        print('\n|  Password yang anda masukkan salah!\n| Silahkan coba kembali...')
                    else :
                        print('\n| Anda salah memasukkan password sebanyak tiga kali.\n| Anda akan diarahkan ke menu utama.')
                        input('\n\n(Enter untuk melanjutkan.)')
        else :
            i += 1
            if i < 2:
                print('\n|  Maaf, username tidak dikenali\n|    Silahkan coba kembali...')
            else :
                print("\n| Maaf, kami tidak mengenali anda.\n| Silahkan daftarkan akun anda untuk masuk.")
                input("\n(Enter untuk kembali.)")
                header('',1)

def registrasi():
    header('SIGN IN')
    df = pd.read_csv('DaftarPengguna.csv')
    daftar_pengguna = df.set_index("username")

    while(True):
        username2 = input("\nMasukkan username : ")
        if username2 in daftar_pengguna.index:
            print('Maaf, username sudah ada!!!\nSilahkan masukkan username lain')
        else:
            password = input("\nMasukkan Password : ")
            print("Anda bisa memilih peran yang akan dijalankan\n[1]Pembeli\n[2]Penjual")
            while(True):
                role = input("Masukkan peran : ")
                if role == '1' :
                    role = 'Pembeli'
                    break
                elif role == '2' :
                    role = 'Penjual'
                    break
                else :
                    print('Tolong masukkan 1 atau 2')
            data_baru = {'username' : username2, 'password' : password, 'role' : role}
            data_baru = pd.DataFrame([data_baru])  # Ubah data baru menjadi DataFrame
            daftar_pengguna = pd.concat([daftar_pengguna.reset_index(), data_baru], ignore_index=True)
            daftar_pengguna.to_csv('DaftarPengguna.csv', index=False)
            print(f'\nAnda masuk sebagai {username2}')
            input("\nTekan Enter untuk melanjutkan.")
            if role == 'Penjual' :
                penjual(username2)
            elif role == 'Pembeli':
                pembeli()
                print()
            break

def logout():
    header('LOG OUT')
    kalimat = "Terimakasih sudah menggunakan layanan kami!"
    width = (67-len(kalimat))//2
    print('\n'+" "*width+kalimat+" "*width+'\n\n'+'='*67)

header('',1)