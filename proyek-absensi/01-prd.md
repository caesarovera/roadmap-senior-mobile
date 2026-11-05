# Proyek Absensi — 01. Product Requirements Document (PRD)

[← Kembali ke README](../README.md)

> Proyek portofolio utama yang dibangun dari **Fase 2** sampai **Fase 4**. Dikembangkan bertahap: v1 → v2 → v3.

---

## 1. Latar Belakang

Banyak UMKM, sekolah, dan kantor kecil di Indonesia masih mencatat absensi secara manual atau dengan mesin fingerprint yang mahal. Masalah yang sering muncul:
- **Titip absen** (rekan mengabsenkan karyawan lain)
- Rekap bulanan memakan waktu HR berjam-jam
- Karyawan lapangan atau yang bekerja di beberapa cabang sulit tercatat
- Pengajuan izin masih lewat chat dan sering terlewat

## 2. Tujuan Produk

| Tujuan | Ukuran Keberhasilan |
|---|---|
| Absen cepat | Check-in selesai dalam **< 15 detik** dari aplikasi dibuka |
| Mencegah kecurangan | Wajib berada di radius kantor + selfie; terdeteksi fake GPS (v3) |
| Rekap otomatis | HR bisa ekspor rekap bulanan ke Excel dalam 1 klik |
| Izin terkelola | Pengajuan sampai persetujuan tercatat dan bernotifikasi |
| Andal di lapangan | Tetap bisa absen saat sinyal hilang (v3) |

## 3. Pengguna

| Peran | Platform | Kebutuhan Utama |
|---|---|---|
| **Karyawan** | Aplikasi mobile | Absen masuk/pulang, lihat riwayat, ajukan izin/cuti |
| **Admin / HR** | Panel web (Filament) | Kelola karyawan, kantor, shift; setujui izin; rekap laporan |

### Persona
- **Rina, 26 tahun, staf toko cabang.** HP Android kelas menengah, sinyal di toko sering lemah. Ingin absen cepat lalu langsung kerja.
- **Pak Budi, 45 tahun, pemilik usaha dengan 3 cabang.** Ingin tahu siapa yang terlambat tanpa harus datang ke tiap cabang.

---

## 4. Lingkup Fitur

### v1: MVP (Fase 2)

**Autentikasi**
- [ ] Login dengan email dan password (akun dibuat oleh admin; tidak ada registrasi mandiri)
- [ ] Auto-login, logout
- [ ] Ganti password

**Beranda**
- [ ] Sapaan sesuai waktu ("Selamat pagi, Rina")
- [ ] Info shift hari ini (jam masuk dan pulang) serta nama kantor
- [ ] Status absensi hari ini: belum absen / sudah masuk / sudah pulang
- [ ] Tombol besar **Absen Masuk** / **Absen Pulang**
- [ ] Ringkasan bulan ini: hadir, terlambat, izin, alpha

**Absen Masuk / Pulang**
- [ ] Ambil lokasi GPS dan tampilkan jarak ke kantor
- [ ] Peringatan di aplikasi kalau di luar radius; **validasi final di server**
- [ ] Selfie dengan kamera depan (tidak boleh dari galeri)
- [ ] Kompresi foto sebelum upload
- [ ] Status otomatis: tepat waktu / terlambat (berdasarkan shift + toleransi)
- [ ] Layar sukses dengan jam absen

**Riwayat**
- [ ] Daftar absensi per bulan (infinite scroll)
- [ ] Filter bulan
- [ ] Detail: jam masuk/pulang, durasi kerja, foto, lokasi, status

**Izin & Cuti**
- [ ] Ajukan: jenis (sakit / izin / cuti), tanggal mulai–selesai, alasan, lampiran (foto surat dokter)
- [ ] Daftar pengajuan + status (menunggu / disetujui / ditolak)
- [ ] Batalkan pengajuan yang masih menunggu
- [ ] Sisa kuota cuti

**Notifikasi**
- [ ] Push saat izin disetujui/ditolak
- [ ] Pengingat absen masuk (15 menit sebelum shift, kalau belum absen)
- [ ] Pengingat absen pulang

**Profil**
- [ ] Data diri, kantor, shift
- [ ] Pengaturan tema (terang/gelap/sistem)
- [ ] Versi aplikasi

**Panel Admin (Filament)**
- [ ] CRUD karyawan, kantor (titik koordinat + radius), shift
- [ ] Persetujuan izin
- [ ] Dashboard: hadir/terlambat/belum absen hari ini (**realtime** via Reverb)
- [ ] Ekspor rekap bulanan ke Excel

### v2: Kualitas (Fase 3)
- [ ] Testing lengkap (unit, component, E2E, API)
- [ ] CI/CD + 3 environment
- [ ] OTA update, Sentry
- [ ] **Rilis di Google Play**

### v3: Level Senior (Fase 4)
- [ ] **Absen offline** (outbox + sinkronisasi otomatis)
- [ ] **Deteksi fake GPS** (native module buatan sendiri)
- [ ] Riwayat dengan FlashList + thumbnail
- [ ] Animasi tombol absen, swipe action
- [ ] Feature flag + force update
- [ ] Kantor dengan banyak lokasi (karyawan bisa absen di cabang mana pun yang diizinkan)

### Di Luar Lingkup (Tidak Dikerjakan)
- Penggajian (payroll)
- Face recognition (selfie hanya sebagai bukti visual)
- Pelacakan lokasi di background (masalah privasi + kebijakan Play Store yang ketat)

---

## 5. Aturan Bisnis

| ID | Aturan |
|---|---|
| BR-01 | Absen masuk hanya **sekali** per hari per karyawan |
| BR-02 | Absen pulang hanya bisa dilakukan setelah absen masuk |
| BR-03 | Absen hanya diterima jika jarak ke kantor ≤ `radius_meters` (dihitung di **server**) |
| BR-04 | Terlambat = jam masuk > jam mulai shift + `late_tolerance_minutes` |
| BR-05 | Waktu absen yang berlaku adalah **waktu server**; waktu HP disimpan untuk audit |
| BR-06 | Karyawan yang tidak absen dan tidak punya izin yang disetujui ditandai **alpha** (scheduled job setiap malam) |
| BR-07 | Pengajuan izin tidak boleh tumpang tindih dengan pengajuan lain yang masih aktif |
| BR-08 | Cuti tahunan mengurangi kuota; sakit dan izin tidak |
| BR-09 | Pengajuan yang sudah disetujui/ditolak tidak bisa dibatalkan oleh karyawan |
| BR-10 | Karyawan hanya bisa melihat data miliknya sendiri |
| BR-11 | Foto selfie disimpan di storage privat, hanya bisa diakses pemiliknya dan admin |

---

## 6. Kebutuhan Non-Fungsional

| Aspek | Target |
|---|---|
| Platform | Android 8+ (prioritas), iOS (opsional) |
| Performa | Startup dingin < 2 detik di HP kelas menengah; scroll riwayat 60 fps |
| Ukuran foto | < 300 KB setelah kompresi |
| Jaringan | Tetap bisa dipakai di jaringan 3G / sinyal lemah (timeout dan retry yang wajar) |
| Keamanan | Token di SecureStore, HTTPS, rate limiting, otorisasi per resource |
| Privasi | Lokasi hanya diambil saat absen (bukan di background); kebijakan privasi tersedia |
| Aksesibilitas | Bisa dipakai dengan TalkBack; mendukung ukuran font besar |
| Bahasa | Bahasa Indonesia |

---

[Lanjut → Desain Database](02-database.md)
