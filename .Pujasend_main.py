import pandas as pd
import os # os.system('cls')


def header(isi='', homepage=0):
    os.system('cls')
    with open('homepage.txt', 'r', encoding='utf-8') as file:
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
                    header('KELUAR')
                    kalimat = "Terimakasih sudah menggunakan layanan kami!"
                    width = (67-len(kalimat))//2
                    print('\n'+" "*width+kalimat+" "*width+'\n\n'+'='*67)
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
        username = input("")
        if username in daftar_pengguna.index:
            while(masukkan_password):
                print("\nMasukkan Password : ")
                password = input("")
                if password == daftar_pengguna.loc[username, 'password']:
                    print(f'Anda masuk sebagai {username}') #diarahkan ke program selanjutnya sesuai role
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
            print(f'Anda masuk sebagai {username}')
            break

header('',1)