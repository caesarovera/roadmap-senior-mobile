# 00 — Cara Belajar dengan Roadmap Ini

[← Kembali ke README](../README.md)

## 1. Format Setiap Minggu

Setiap minggu di dokumen fase punya struktur yang sama:

| Bagian | Isi |
|---|---|
| 🎯 **Tujuan** | Apa yang harus bisa Anda lakukan di akhir minggu |
| 📚 **Materi** | Topik yang dipelajari plus link dokumentasi resmi |
| 🛠 **Latihan** | Tugas praktik (wajib dikerjakan, bukan sekadar dibaca) |
| ✅ **Checkpoint** | Pertanyaan atau tugas untuk menguji pemahaman |

## 2. Jadwal Mingguan yang Disarankan (±12 jam)

| Hari | Aktivitas | Durasi |
|---|---|---|
| Senin | Baca materi + catat konsep kunci | 1,5 jam |
| Selasa | Latihan kecil (ikuti contoh dokumentasi) | 1,5 jam |
| Rabu | Baca materi lanjutan | 1,5 jam |
| Kamis | Latihan kecil | 1,5 jam |
| Sabtu | **Latihan utama minggu itu** (proyek) | 4 jam |
| Minggu | Review: jawab checkpoint, tulis catatan belajar, push ke GitHub | 2 jam |

> Kalau waktu Anda lebih sedikit, perpanjang durasi fase, **jangan kurangi latihannya**.

## 3. Aturan Belajar

1. **Praktik > tonton.** Tutorial video maksimal 30% dari waktu belajar. Sisanya menulis kode.
2. **Dokumentasi resmi adalah sumber utama.** Tutorial pihak ketiga sering tertinggal versi.
3. **Ketik sendiri, jangan copy-paste.** Terutama di Fase 0–1.
4. **Rusak dengan sengaja.** Setelah sesuatu berhasil, ubah dan lihat apa yang rusak. Dari situ Anda paham *kenapa* sesuatu bekerja.
5. **Tulis catatan dengan kata-kata sendiri.** Buat file `CATATAN.md` di setiap repo latihan.
6. **Pakai AI sebagai mentor, bukan sebagai pengganti.** Minta penjelasan dan review kode Anda, bukan "buatkan kodenya". Setelah AI menjelaskan, tutup jendelanya dan tulis ulang dari ingatan.
7. **Commit setiap hari belajar.** Kebiasaan kecil, dampaknya besar untuk portofolio.

## 4. Setup Alat (Lakukan Sebelum Fase 0)

### Wajib
- [ ] **Node.js LTS** (pakai `nvm` / `fnm` agar mudah ganti versi)
- [ ] **VS Code** + ekstensi: ESLint, Prettier, Error Lens, GitLens, Expo Tools
- [ ] **Git** + akun GitHub (sudah ✅)
- [ ] **Android Studio** (untuk emulator Android dan nantinya profiler)
- [ ] **HP Android** dengan aplikasi **Expo Go** (untuk tes cepat di perangkat asli)
- [ ] **PHP + Composer + Laravel** (Anda sudah punya: Laravel Herd, Sail, atau Laragon)
- [ ] **Bruno** atau **Postman** untuk mengetes API

### Opsional
- [ ] **Mac** (dibutuhkan untuk simulator iOS dan build iOS lokal; build iOS di cloud bisa lewat EAS tanpa Mac)
- [ ] Akun **Expo** (gratis) untuk EAS Build
- [ ] Akun **Google Play Console** (bayar sekali, dibutuhkan di Fase 3)

## 5. Struktur Repo Latihan yang Disarankan

Buat repo terpisah di GitHub Anda:

| Repo | Fase | Isi |
|---|---|---|
| `js-ts-playground` | 0 | Latihan JavaScript/TypeScript per minggu |
| `react-web-latihan` | 0 | Aplikasi React web kecil |
| `rn-keuangan` | 1 | Aplikasi keuangan pribadi offline |
| `absensi-api` | 2–4 | Backend Laravel untuk proyek absensi |
| `absensi-mobile` | 2–4 | Aplikasi React Native untuk proyek absensi |
| `expo-<nama>-module` | 4 | Native module buatan sendiri |

Setiap repo wajib punya `README.md` berisi: deskripsi, screenshot/GIF, tech stack, cara menjalankan, dan **keputusan teknis** yang Anda ambil.

## 6. Jika Mentok

1. Baca pesan error sampai habis, lalu cari pesan persisnya.
2. Cek dokumentasi resmi dan **GitHub Issues** library terkait.
3. Buat **reproduksi minimal**: proyek baru sekecil mungkin yang tetap memunculkan error.
4. Kalau lewat 2 jam belum ketemu, tanya di komunitas (Discord Reactiflux, Expo Discord, grup Telegram/Facebook developer Indonesia) **dengan reproduksi minimal tadi**.
5. Tulis solusinya di `CATATAN.md`. Masalah yang sama hampir pasti datang lagi.

---

Lanjut ke → [Fase 0: JavaScript, TypeScript, React](fase-0-javascript-typescript.md)
