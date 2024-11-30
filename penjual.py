import csv

def baca_menu_dari_csv():
    try:
        with open("menu.csv", "r") as file:
            reader = csv.reader(file)
            menu = {
                "nasi goreng" : 15000 ,
                "mi goreng" : 10000 ,
                "nasi empal" : 13000 ,
            }
            for baris in reader:
                nama_menu, harga_menu = baris
                menu[nama_menu] = int(harga_menu)
            return menu
    except FileNotFoundError:
        return {}

def simpan_menu_ke_csv():
    with open("menu.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for nama_menu, harga_menu in menu.items():
            writer.writerow([nama_menu, harga_menu])

def baca_orderan_dari_csv():
    try:
        with open("orderan.csv", "r") as file:
            reader = csv.reader(file)
            return [baris for baris in reader]
    except FileNotFoundError:
        return []  # Jika file belum ada, kembalikan list kosong

def simpan_orderan_ke_csv():
    with open("orderan.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for orderan in daftar_orderan:
            writer.writerow(orderan)

def baca_orderan_selesai_dari_csv():
    try:
        with open("orderan_selesai.csv", "r") as file:
            reader = csv.reader(file)
            return [baris for baris in reader]
    except FileNotFoundError:
        return []  # Jika file belum ada, kembalikan list kosong

def simpan_orderan_selesai_ke_csv():
    with open("orderan_selesai.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for orderan_selesai in daftar_orderan_selesai:
            writer.writerow(orderan_selesai)

# menu utama
def menu_utama():
    print("\n=== Selamat Datang ===")
    print("1. Kelola Menu")
    print("2. Kelola Orderan")
    print("3. Lihat Laporan Penjualan")
    print("4. Keluar")

# kelola menu
def kelola_menu():
    while True:
        print("\n=== Kelola Menu ===")
        print("1. Lihat Menu")
        print("2. Tambah Menu")
        print("3. Ubah Menu")
        print("4. Hapus Menu")
        print("5. Kembali ke Menu Utama")
        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            print("\nDaftar Menu:")
            if menu:
                for nama_menu, harga_menu in menu.items():
                    print(f"- {nama_menu}: Rp{harga_menu}")
            else:
                print("Menu masih kosong.")

        elif pilihan == "2":
            nama_menu = input("Masukkan nama menu: ")
            if nama_menu in menu:
                print(f"{nama_menu} sudah ada di menu.")
            else:
                try:
                    harga_menu = int(input("Masukkan harga menu: "))
                    menu[nama_menu] = harga_menu
                    simpan_menu_ke_csv()
                    print(f"{nama_menu} berhasil ditambahkan!")
                except ValueError:
                    print("Harga harus berupa angka.")

        elif pilihan == "3":
            nama_menu = input("Masukkan nama menu: ")
            if nama_menu in menu:
                print(f"{nama_menu} sudah ada di menu.")
                ubah = input("Apakah Anda ingin mengubah nama atau harga menu? (y untuk ya, b untuk batal): ").lower()
        
                if ubah == 'y':
                    nama_baru = input("Masukkan nama baru untuk menu: ")
                    try:
                        harga_baru = int(input("Masukkan harga baru untuk menu: "))
                        menu[nama_baru] = harga_baru  # Mengubah nama dan harga menu 
                        del menu[nama_menu]  # Menghapus menu lama
                        simpan_menu_ke_csv()  
                        print(f"Menu {nama_menu} berhasil diubah menjadi {nama_baru} dengan harga Rp{harga_baru}.")
                    except ValueError:
                        print("Harga harus berupa angka.")
                
                elif ubah == 'b':
                    print("Perubahan dibatalkan.")
                else:
                    print("Pilihan tidak valid.")
            else:
                print(f"{nama_menu} tidak ditemukan di menu.")

        elif pilihan == "4":
            nama_menu = input("Masukkan nama menu yang ingin dihapus: ")
            if nama_menu in menu:
                del menu[nama_menu]
                simpan_menu_ke_csv()
                print(f"{nama_menu} berhasil dihapus!")
            else:
                print("Menu tidak ditemukan.")
        elif pilihan == "5":
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

def kelola_orderan():
    while True:
        print("\n=== Kelola Orderan ===")
        print("1. Lihat Orderan Masuk")
        print("2. Lihat Orderan yang Sedang Diproses")
        print("3. Kembali ke Menu Utama")
        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            print("\nOrderan Masuk:")
            if daftar_orderan:
                for indeks, orderan in enumerate(daftar_orderan):
                    print(f"{indeks + 1}. Pesanan: {orderan[0]}, Status: {orderan[1]}")
                    keputusan = input("Terima (TE) atau Tolak (TO)? (TE untuk Terima, TO untuk Tolak): ").lower()
                    if keputusan == 'te':
                        # Jika diterima, pindahkan ke daftar orderan sedang diproses
                        orderan[1] = "Diproses"
                        daftar_orderan_diproses.append(orderan)
                        daftar_orderan.remove(orderan)
                        simpan_orderan_ke_csv()
                        print(f"Orderan {orderan[0]} diterima dan sedang diproses.")
                    elif keputusan == 'to':
                        daftar_orderan.remove(orderan)
                        simpan_orderan_ke_csv()
                        print(f"Orderan {orderan[0]} ditolak.")
                    else:
                        print("Pilihan tidak valid. Kembali ke menu.")
            else:
                print("Tidak ada orderan masuk.")
        elif pilihan == "2":
            print("\nOrderan yang Sedang Diproses:")
            if daftar_orderan_diproses:
                for orderan in daftar_orderan_diproses:
                    print(f"Pesanan: {orderan[0]}, Status: {orderan[1]}")
                    keputusan = input("Selesai diproses (S) atau belum (B)? (S untuk Selesai, B untuk Belum): ").lower()
                    if keputusan == 's':
                        orderan[1] = "Selesai"
                        daftar_orderan_selesai.append(orderan)
                        daftar_orderan_diproses.remove(orderan)
                        simpan_orderan_selesai_ke_csv()
                        simpan_orderan_ke_csv()
                        print(f"Orderan {orderan[0]} selesai dan dipindahkan ke laporan penjualan.")
                    elif keputusan == 'b':
                        print(f"Orderan {orderan[0]} belum selesai diproses.")
                    else:
                        print("Pilihan tidak valid. Kembali ke menu.")
            else:
                print("Tidak ada orderan yang sedang diproses.")
        elif pilihan == "3":
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

def lihat_laporan_penjualan():
    print("\n=== Laporan Penjualan ===")
    if daftar_orderan_selesai:
        for orderan_selesai in daftar_orderan_selesai:
            print(f"Pesanan: {orderan_selesai[0]}, Status: {orderan_selesai[1]}")
    else:
        print("Tidak ada penjualan yang tercatat.")

menu = baca_menu_dari_csv()
daftar_orderan = baca_orderan_dari_csv()
daftar_orderan_diproses = []
daftar_orderan_selesai = baca_orderan_selesai_dari_csv()

while True:
    menu_utama()
    pilihan = input("Pilih menu: ")
    if pilihan == "1":
        kelola_menu()
    elif pilihan == "2":
        kelola_orderan()
    elif pilihan == "3":
        lihat_laporan_penjualan()
    elif pilihan == "4":
        print("Terima kasih telah menggunakan program ini!")
        break
    else:
        print("Pilihan tidak valid. Coba lagi.")
