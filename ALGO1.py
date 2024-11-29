import pandas as pd
import os # os.system('cls')

def login ():
    with open('homepage.txt', 'r', encoding='utf-8') as file:
        homepage = file.read()
    print(homepage)

    df = pd.read_csv('DaftarPengguna.csv')
    daftar_pengguna = df.set_index("username")

    while (True):
        pilihan = input("")
        match pilihan :
            case "1" :
                print("\nMasukkan username : ")
                username = input("")
                if username in daftar_pengguna.index:
                    while(True):
                        print("Masukkan Password : ")
                        password = input("")
                        if password == daftar_pengguna.loc[username, 'password']:
                            print('Anda berhasil masuk')
                            break
                        else :
                            print('Password salah!!!')
                else :
                    print('Maaf, username tidak dikenali')
                break
            case "2" :
                while(True):
                    print("\nMasukkan username : ")
                    username = input("")
                    if username in daftar_pengguna.index:
                        print('Maaf, username sudah ada!!!\nSilahkan masukkan username lain')
                    else:
                        print("\nMasukkan Password : ")
                        password = input("")
                        break
                break
            case _ :
                print("Angka yang anda masukkan tidak sesuai, silahkan coba lagi\n")

login()