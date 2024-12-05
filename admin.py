import pandas as pd
import csv
import os

#=========================================================================
#ADMIN

def ringkasan_penjualan(df):
    laporan = df.groupby("Stand").agg(
        Total_Penjualan=("Total Harga", "sum"),
        Jumlah_Transaksi=("Jumlah", "sum")
    ).reset_index()

    stand_terlaris = laporan.sort_values(by="Total_Penjualan", ascending=False).iloc[0]

    print("\n===RINGKASAN PENJUALAN===")
    print(f"{'Stand':<20} {'Total Penjualan':<20} {'Jumlah Transaksi':<20}")
    print("-" * 60)
    for index, row in laporan.iterrows():
        print(f"{row['Stand']:<20} Rp {row['Total_Penjualan']:<20} {row['Jumlah_Transaksi']:<20}")
    
    print(f"\nStand Terlaris: {stand_terlaris['Stand']} dengan penjualan Rp {stand_terlaris['Total_Penjualan']:,}")
    input("\n(Enter untuk Kembali.)")

def detail_penjualan_per_stand(df):
    print("\n===DETAIL PENJUALAN PER STAND===")
    stands = df["Stand"].unique()

    for stand in stands:
        print(f"\n{stand}:")
        stand_data = df[df["Stand"] == stand]
        laporan_menu = stand_data.groupby("Nama Menu").agg(
            Jumlah_Terjual=("Jumlah", "sum"),
            Total_Pendapatan=("Total Harga", "sum")
        ).reset_index()

        print(f"{'Menu':<30} {'Jumlah Terjual':<15} {'Total Pendapatan':<15}")
        print("-" * 60)
        for index, row in laporan_menu.iterrows():
            print(f"{row['Nama Menu']:<30} {row['Jumlah_Terjual']:<15} Rp {row['Total_Pendapatan']:<15}")
    input("\n(Enter untuk Kembali.)")

def statistik(df):
    total_penjualan = df["Total Harga"].sum()
    rata_rata_penjualan = df.groupby("Stand")["Total Harga"].sum().mean()

    kontribusi = df.groupby("Stand")["Total Harga"].sum().reset_index()
    kontribusi["Kontribusi (%)"] = (kontribusi["Total Harga"] / total_penjualan) * 100
    
    print("\n===STATISTIK===")
    print(f"Total Penjualan: Rp {total_penjualan:,}")
    print(f"Rata-rata Penjualan per Stand: Rp {rata_rata_penjualan:,.2f}")
    
    print(f"\n\nKontribusi Penjualan per Stand:\n")
    print(f"{'Stand':<20} {'Kontribusi (%)':<20}")
    print("-" * 40)
    for index, row in kontribusi.iterrows():
        print(f"{row['Stand']:<20} {row['Kontribusi (%)']:<20.2f}")

    input("\n(Enter untuk Kembali.)")

def catatan_penjualan():  
    while True : 
        header("Admin > Catatan Penjualan")
        print("[1] Ringkasan Penjualan\n[2] Detail Penjualan per Stand\n[3] Statistik\n[4] Keluar")
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
                ubah = input("Apakah Anda ingin mengubah nama kode voucher atau banyak diskon? (y untuk ya, b untuk batal): ").lower()
            
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
                print(f"\nVoucher '{nama_voucher}' tidak ditemukan di menu.")
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

def kelola_user_penjual():
    while True :
        daftar_pengguna = pd.read_csv('DaftarPengguna.csv')
        header('Admin > Kelola User')
        print("[1] Lihat Daftar Pengguna \n[2] Ubah Penjual \n[3] Hapus Penjual \n[4] Kembali")
        pilihan = input("Masukkan opsi: ")

        if pilihan == "1":
            header("Admin > Kelola User Penjual > Lihat Daftar Pengguna")
            print("[1] Lihat Daftar Penjual \n[2] Lihat Daftar Pembeli \n[3] Kembali")
            masukkan = input("Masukkan opsi: ")
            if masukkan == "1":
                header("Admin > Kelola User Penjual > Lihat Daftar Pengguna > Lihat Daftar Penjual")
                daftar_penjual = daftar_pengguna[daftar_pengguna['role'] == 'Penjual']
                print(daftar_penjual)
            elif masukkan == "2":
                header("Admin > Kelola User Penjual > Lihat Daftar Pengguna > Lihat Daftar Pembeli")
                daftar_pembeli = daftar_pengguna[daftar_pengguna['role'] == 'Pembeli']
                print(daftar_pembeli)
            else :
                print("Pilihan tidak valid.")
            input("(Enter untuk kembali.)")

        elif pilihan == "2":
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
    masukkan_password = True
    while(True):
        print("\nMasukkan username anda : ")
        username1 = input("")
        if username1 in daftar_pengguna.index:
            while(masukkan_password):
                print("\nMasukkan Password : ")
                password = input("")
                if password == daftar_pengguna.loc[username1, 'password']:
                    print(f'\nAnda masuk sebagai {username1}')
                    input("\nTekan Enter untuk melanjutkan.")
                    print(daftar_pengguna.loc[username1, 'role'])
                    if daftar_pengguna.loc[username1, 'role'] == "Admin":
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
            # if role == 'Penjual' :
            #     penjual(username2)
            # elif role == 'Pembeli':
            #     pembeli()
            #     print()
            break

def logout():
    header('LOG OUT')
    kalimat = "Terimakasih sudah menggunakan layanan kami!"
    width = (67-len(kalimat))//2
    print('\n'+" "*width+kalimat+" "*width+'\n\n'+'='*67)

header('',1)