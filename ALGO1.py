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
                            print('Anda berhasil masuk') #diarahkan ke program selanjutnya sesuai role
                            break
                        else :
                            print('Password salah!!! Silahkan masukkan kembali')
                else :
                    print('Maaf, username tidak dikenali\nSilahkan coba lagi...')
                break
            case "2" :
                while(True):
                    username = input("\nMasukkan username : ")
                    if username in daftar_pengguna.index:
                        print('Maaf, username sudah ada!!!\nSilahkan masukkan username lain')
                    else:
                        password = input("\nMasukkan Password : ")
                        print("Anda bisa memilih peran yang akan dijalankan\n[1]Pembeli\n[2]Penjual")
                        while(True):
                            role = input("Masukkan peran : ")
                            if role == 1 :
                                role = 'Pembeli'
                                break
                            elif role == 2 :
                                role = 'Penjual'
                                break
                            else :
                                print('Tolong masukkan angka 1 atau 2')
                        data_baru = {'username' : username, 'password' : password, 'role' : role}
                        data_baru_df = pd.DataFrame([data_baru])  # Ubah data baru menjadi DataFrame
                        daftar_pengguna = pd.concat([daftar_pengguna.reset_index(), data_baru_df], ignore_index=True)
                        daftar_pengguna.to_csv('DaftarPengguna.csv', index=False)
                        break
                break
            case _ :
                print("Angka yang anda masukkan tidak sesuai, silahkan coba lagi\n")

login()