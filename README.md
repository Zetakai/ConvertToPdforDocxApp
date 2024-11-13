Buku Panduan Pengguna
### Buku Panduan Pengguna
**Nama Aplikasi**: Aplikasi Manajemen Pengguna & Konversi File
---
#### 1. Ikhtisar
Aplikasi ini adalah program desktop yang memungkinkan pengguna untuk:
- Mendaftar dan masuk dengan akun pengguna.
- Mengonversi berbagai format file (DOCX, CSV, TXT, XLSX, XLS, PNG, JPG, JPEG, PDF) ke PDF atau DOCX.
- Mengakses dan mengelola data pengguna dalam database SQLite lokal.
Aplikasi ini dibuat dengan Python, menggunakan PyQt6 untuk antarmuka grafis dan pustaka seperti `pandas`, `pdfkit`, `reportlab`, dan `docx` untuk penanganan dan konversi file.
---
#### 2. Instalasi
1. **Persyaratan**:
   - Pastikan Python telah terinstal di sistem Anda.
   - Instal pustaka yang diperlukan dengan menjalankan:
     ```bash
     pip install PyQt6 pandas pdfkit markdown2 python-docx reportlab pdfplumber pillow
     ```
2. **Menjalankan Aplikasi**:
   - Untuk memulai program, buka direktori aplikasi dan jalankan:
     ```bash
     python app.py
     ```
   - Jendela login utama akan muncul.
---
#### 3. Fitur
**3.1 Pendaftaran Pengguna**
   - Buka jendela **Register**.
   - Masukkan username dan password unik.
   - Klik **Register** untuk membuat akun Anda.
   - Jika pendaftaran berhasil, pesan konfirmasi akan muncul. Jika tidak, akan muncul notifikasi jika username sudah digunakan.
**3.2 Masuk Pengguna**
   - Masukkan username dan password terdaftar Anda di jendela **Login**.
   - Klik **Login** untuk mengakses aplikasi.
   - Login yang berhasil akan mengarahkan Anda ke jendela **Menu**, di mana Anda dapat mengakses fitur konversi file.
**3.3 Konversi File**
   - Di jendela **Menu**, pilih file dengan mengklik **Select File**. Tipe file yang didukung termasuk DOCX, CSV, TXT, XLSX, XLS, PNG, JPG, JPEG, dan PDF.
   - Pilih format konversi (baik **Convert to PDF** atau **Convert to DOCX**) dari dropdown.
   - Klik **Convert** untuk memulai proses konversi. Bar progres akan menunjukkan kemajuan konversi.
   - Setelah selesai, file yang dikonversi akan disimpan di direktori yang sama dengan file asli dengan format baru.
---
#### 4. Rincian Teknis
**4.1 Pengaturan Database**
   - Aplikasi ini menggunakan database SQLite bernama `users.db`.
   - Database diinisialisasi secara otomatis pada penggunaan pertama, membuat tabel `users` untuk menyimpan username dan password.
**4.2 Konversi File yang Didukung**
   - **CSV ke PDF/DOCX**: Mengonversi file CSV ke PDF atau DOCX dengan setiap baris ditampilkan dalam dokumen.
   - **DOCX ke PDF**: Mengonversi dokumen DOCX ke format PDF.
   - **TXT ke PDF/DOCX**: Membaca file teks biasa dan menyimpan kontennya dalam format yang dipilih.
   - **Excel (XLSX, XLS) ke PDF/DOCX**: Menangani spreadsheet, menampilkan setiap baris di file yang dikonversi.
   - **Gambar (PNG, JPG, JPEG) ke PDF**: Mengonversi gambar ke format PDF.
   - **PDF ke DOCX**: Mengekstrak teks dari halaman PDF dan menyimpannya ke dokumen DOCX.
**4.3 Alur Konversi File**
   - Setelah memilih file dan format konversi, aplikasi menggunakan metode khusus untuk menangani setiap jenis file.
   - Penanganan kesalahan diimplementasikan untuk memberi tahu pengguna jika file tidak didukung atau konversi gagal.
---
#### 5. Pemecahan Masalah
- **Masalah Login**: Pastikan username dan password Anda benar. Jika belum terdaftar, gunakan jendela **Register** terlebih dahulu.
- **Kesalahan Konversi File**: Jika konversi gagal, periksa apakah tipe file didukung dan file dapat diakses. Lihat pesan kesalahan untuk panduan lebih lanjut.
---
Buku panduan ini memberikan gambaran umum untuk pengaturan dan operasi, membantu pengguna memahami dan menggunakan setiap fitur dengan efektif. Untuk pertanyaan tambahan, konsultasikan dengan dukungan IT Anda.
