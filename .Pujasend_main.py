import pandas as pd
import csv
import os
import time

username = " "
nama_stand = "Rice Bowl Fusion"
#================================================================================
#PENJUAL

def baca_menu_dari_csv(): 
    try:
        df = pd.read_csv("stand.csv")
        stand = df[df["Stand"] == nama_stand]
        menu = {row["Nama Menu"]: row["Harga"] for index, row in stand.iterrows()}
        return menu
    except FileNotFoundError:
        return {}

def simpan_menu_ke_csv(menu, harga):
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

# kelola menu
def kelola_menu():
    while True:
        header("Penjual > Kelola Menu")
        print("[1] Lihat Menu\n[2] Tambah Menu\n[3] Ubah Menu\n[4] Hapus Menu\n[5] Kembali ke Menu Utama")
        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            header('Penjual > Kelola Menu > Lihat Menu')
            print("\nDaftar Menu:")
            angka =1
            if menu:
                for nama_menu,harga_menu in menu.items():
                    print(f"{angka}. {nama_menu}\t\t Rp{harga_menu}")
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
                try:
                    harga_menu = int(input("Masukkan harga menu: "))
                    simpan_menu_ke_csv(nama_menu, harga_menu)
                    print(f"\n{nama_menu} berhasil ditambahkan!")
                    input('\n(Enter untuk kembali.)')
                except ValueError:
                    print("Harga harus berupa angka.")

        elif pilihan == "3":
            header('Penjual > Kelola Menu > Ubah Menu')
            angka = 1
            if menu:
                for nama_menu,harga_menu in menu.items():
                    print(f"{angka}. {nama_menu}\t Rp{harga_menu}")
                    angka +=1
            else:
                print("Menu masih kosong.")
            while(True):
                nama_menu = input("Masukkan nama menu yang ingin diubah: ")
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
                        break
                    else:
                        print("Pilihan tidak valid.")
                else:
                    print(f"\n{nama_menu} tidak ditemukan di menu.")
                    input('\n(Enter untuk kembali.)')

        elif pilihan == "4":
            header('Penjual > Kelola Menu > Hapus Menu')
            angka = 1
            if menu:
                for nama_menu,harga_menu in menu.items():
                    print(f"{angka}. {nama_menu}\t Rp{harga_menu}")
                    angka +=1
            else:
                print("Menu masih kosong.")
            nama_menu = input("\nMasukkan nama menu yang ingin dihapus: ")
            if nama_menu in menu:
                del menu[nama_menu]
                simpan_menu_ke_csv()
                print(f"{nama_menu} berhasil dihapus!")
            else:
                print("\nMenu tidak ditemukan.")
            input('\n(Enter untuk kembali.)')
        elif pilihan == "5":
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

def kelola_orderan():
    while True:
        header('Penjual > Kelola Orderan')
        print("[1] Lihat Orderan Masuk \n[2] Lihat Orderan yang Sedang Diproses \n[3] Kembali ke Menu Utama")
        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            header('Penjual > Kelola Orderan > Lihat Orderan Masuk')
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
            input('\n(Enter untuk kembali.)')

        elif pilihan == "2":
            header('Penjual > Kelola Orderan > Lihat Orderan yang Sedang Diproses')
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
            input('\n(Enter untuk kembali.)')
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
        print("T\nidak ada penjualan yang tercatat.")
    input('(\nEnter untuk kembali.)')

menu = baca_menu_dari_csv()
daftar_orderan = baca_orderan_dari_csv()
daftar_orderan_diproses = []
daftar_orderan_selesai = baca_orderan_selesai_dari_csv()

def penjual():
    while True:
        header("Penjual")
        print("[1] Kelola Menu\n[2] Kelola Orderan\n[3] Lihat Laporan Penjualan\n[4] Keluar")   
        pilihan = input("Masukkan opsi: ")
        if pilihan == "1":
            kelola_menu()
        elif pilihan == "2":
            kelola_orderan()
        elif pilihan == "3":
            lihat_laporan_penjualan()
        elif pilihan == "4":
            logout()
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")
#=========================================================================
#PEMBELI


#=========================================================================

#=========================================================================
#ADMIN

def voucher():
    while True :
        header('Admin > Kelola Voucher')
        print("[1] Lihat Voucher \n[2] Tambah Voucher \n[3] Ubah Voucher \n[4] Hapus Voucher \n[5] Kembali")
        pilihan = input("Masukkan opsi: ")
        if pilihan == "1":
            header("Admin > Kelola Voucher > Lihat Voucher")
            voucher = pd.read_csv('voucher.csv')
            print(voucher)
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
            print(voucher)
            nama_voucher = input("\nMasukkan nama voucher yang ingin diubah: ")
            if nama_voucher in voucher["Kode Voucher"].values:
                print(f"{nama_voucher} sudah ada di menu.")
                ubah = input("Apakah Anda ingin mengubah nama atau harga menu? (y untuk ya, b untuk batal): ").lower()
            
                if ubah == 'y':
                    nama_baru = input("Masukkan nama baru untuk voucher: ")
                    try:
                        banyak_diskon = int(input("Masukkan diskon: "))
                        data_baru = {'Kode Voucher' : nama_baru, 'Diskon (%)' : banyak_diskon}
                        hapus_voucher_lama = voucher[voucher['Kode Voucher'] != nama_voucher]
                        hapus_voucher_lama.to_csv("voucher.csv", index=False)
                        data_baru = pd.DataFrame([data_baru])  # Ubah data baru menjadi DataFrame
                        voucher = pd.concat([voucher.reset_index(), data_baru], ignore_index=True)
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
                print(f"\n{nama_voucher} tidak ditemukan di menu.")
            input("\n(Enter untuk kembali.)")
                
                        
        elif pilihan == "4":
            header("Admin > Kelola Voucher > Hapus Voucher")
            voucher = pd.read_csv("voucher.csv")
            print(voucher)
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

def admin():
    while True:
        header("Admin")
        print("[1] Kelola Menu\n[2] Lihat Orderan Masuk\n[3] Kelola Voucher\n[4] Keluar")   
        pilihan = input("Masukkan opsi: ")
        if pilihan == "1":
            kelola_menu()
        elif pilihan == "2":
            baca_orderan_dari_csv()
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
    global username
    header('LOGIN')
    df = pd.read_csv('DaftarPengguna.csv')
    daftar_pengguna = df.set_index("username")
    masukkan_password = True
    while(True):
        print("\nMasukkan username anda : ")
        username = input("")
        if username in daftar_pengguna.index:
            while(masukkan_password):
                print("\nMasukkan Password : ")
                password = input("")
                if password == daftar_pengguna.loc[username, 'password']:
                    print(f'\nAnda masuk sebagai {username}')
                    input("\nTekan Enter untuk melanjutkan.")
                    print(daftar_pengguna.loc[username, 'role'])
                    if daftar_pengguna.loc[username, 'role'] == "Penjual":
                        penjual()
                    elif daftar_pengguna.loc[username, 'role'] == "Admin":
                        admin()
                    masukkan_password = False
                else :
                    print('\n|  Password yang anda masukkan salah!\n| Silahkan coba kembali...')
        else :
            print('\n|  Maaf, username tidak dikenali\n|    Silahkan coba kembali...')
        if masukkan_password == False:
            break

def registrasi():
    header('SIGN IN')
    df = pd.read_csv('DaftarPengguna.csv')
    daftar_pengguna = df.set_index("username")

    while(True):
        username = input("\nMasukkan username : ")
        if username in daftar_pengguna.index:
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
            data_baru = {'username' : username, 'password' : password, 'role' : role}
            data_baru = pd.DataFrame([data_baru])  # Ubah data baru menjadi DataFrame
            daftar_pengguna = pd.concat([daftar_pengguna.reset_index(), data_baru], ignore_index=True)
            daftar_pengguna.to_csv('DaftarPengguna.csv', index=False)
            print(f'\nAnda masuk sebagai {username}')
            input("\nTekan Enter untuk melanjutkan.")
            break

def logout():
    header('LOG OUT')
    kalimat = "Terimakasih sudah menggunakan layanan kami!"
    width = (67-len(kalimat))//2
    print('\n'+" "*width+kalimat+" "*width+'\n\n'+'='*67)

header('',1)