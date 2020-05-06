def get_response(response):
    if response == 'peraturan':
        return peraturan
    elif response == 'selamat_datang':
        return selamat_datang
    elif response == 'perbaikan':
        return perbaikan
    elif response == 'choose_role':
        return choose_role
    elif response == 'lobby':
        return lobby
    elif response == 'kelas_sd':
        return kelas_sd
    elif response == 'kelas_smp':
        return kelas_smp
    else:
        return 'Respon tidak ditemukan'

peraturan = '''
**Peraturan Discord Server AHA**
```
- Pilih role sesuai kelas kalian di #📝⫶pendaftaran
- Respect everyone.
- Gunakan channel dengan tepat: 
    •Kategori 💬Berpesan untuk ngobrol menggunakan teks saja. 
    Jika ingin ngobrol dengan sesama teman kelas, masuk kelasnya 
    masing-masing ya
    •Kategori 🏢Fasilitas untuk fasilitas lainnya didukung oleh 
    bot di setiap channelnya (out of topic dan random)
    •Kategori 🔊Bersuara untuk ngobrol dengan suara
- No NSFW, SARA content
```
Udah itu dulu ya. Terima kasih.

    '''

selamat_datang = '''
**Selamat datang di server AHA**
dimana server ini bukanlah official server dari sekolah kita tercinta.
```
- Untuk memulai, pilih kelas (SD/SMP) kalian masing-masing. 
- Jika kalian dari SD dan juga SMP AHA, kalian bisa pilih kedua 
kelas (SD/SMP) tersebut.
- Untuk peraturan dan pengumuman bisa kalian lihat di channel 
#📢⫶pengumuman.
```
Selamat bergabung!:confetti_ball:

    '''

perbaikan = '''
**:warning:Channel sedang dalam perbaikan:warning:**
```Mohon bersabar dan coba lagi nanti ya!```

'''

choose_role = '''
**Pilih Role: Kelas**
Silakan react berdasarkan kelas kalian untuk mendapatkan role.

>>> :orange_square: = SMP

:blue_square: = SD

'''

lobby = '''
```Selamat datang di channel #💬⫶lobby, dimana channel ini digunakan untuk berpesan menggunakan teks oleh semua orang```
'''
kelas_sd = '''
```Selamat datang di channel #🟦⫶kelas-sd, dimana channel ini digunakan untuk berpesan menggunakan teks oleh member SD```
'''
kelas_smp = '''
```Selamat datang di channel #🟧⫶kelas-smp, dimana channel ini digunakan untuk berpesan menggunakan teks oleh member SMP```
'''