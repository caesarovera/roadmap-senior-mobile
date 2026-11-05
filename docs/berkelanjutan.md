# Kebiasaan Berkelanjutan (Sepanjang Roadmap)

[← Kembali ke README](../README.md)

Kebiasaan di bawah ini dijalankan **paralel** dengan semua fase. Inilah yang lama-lama membentuk "insting" seorang senior.

---

## 1. Membaca Kode Orang Lain (1 jam/minggu)

| Fase | Apa yang dibaca |
|---|---|
| 0–1 | Source code fungsi kecil, misalnya implementasi `debounce` di lodash, atau [zustand](https://github.com/pmndrs/zustand) (kodenya pendek) |
| 2 | Contoh resmi [expo/examples](https://github.com/expo/examples), cara TanStack Query menyusun cache |
| 3 | Aplikasi RN open source berskala produksi (cari di GitHub: "react native app" dengan banyak bintang), lalu pelajari struktur folder dan testing-nya |
| 4 | Native module library populer seperti `expo-camera` dan `react-native-mmkv`. Lihat folder `android/` dan `ios/`. |

**Cara membaca:** mulai dari entry point, buat diagram, lalu tulis ringkasan 5 kalimat di catatan Anda.

---

## 2. Menulis (1 tulisan/bulan)

Menulis memaksa Anda benar-benar paham. Contoh topik:
- "Kenapa saya berhenti fetch data pakai useEffect"
- "Membuat absensi offline-first dengan React Native dan Laravel"
- "Mendeteksi fake GPS dengan Expo Modules"

Platform: blog pribadi, Medium, dev.to, LinkedIn, atau folder `blog/` di GitHub.

---

## 3. Kontribusi Open Source

Mulai dari yang kecil:
1. Perbaiki typo atau perjelas dokumentasi library yang Anda pakai
2. Buat **reproduksi minimal** untuk issue yang belum punya reproduksi (sangat dihargai maintainer)
3. Kerjakan issue berlabel `good first issue`
4. Publikasikan library kecil Anda sendiri (Fase 4 Blok D)

---

## 4. Code Review

- Biasakan semua perubahan lewat **Pull Request**, meskipun bekerja sendiri
- Review PR Anda sendiri keesokan harinya, seolah milik orang lain
- Cari partner belajar dan saling review PR setiap minggu
- Gunakan AI reviewer sebagai *second opinion*, tapi pahami setiap saran sebelum menerapkannya

---

## 5. Mengikuti Perkembangan (30 menit/minggu)

- Blog dan changelog **Expo** dan **React Native** (setiap rilis SDK baru)
- Newsletter: *This Week in React* dan *React Native Newsletter*
- Laravel News (untuk sisi backend)
- Konferensi (rekamannya gratis di YouTube): App.js Conf, React Native EU, Chain React

> ⚠️ Jangan kejar setiap library baru. Senior memilih teknologi berdasarkan **kebutuhan dan risiko**, bukan karena sedang tren.

---

## 6. Komunitas Indonesia

- Grup Telegram/Facebook React Native Indonesia dan Laravel Indonesia
- Meetup lokal (misalnya acara komunitas developer di kota Anda)
- Bagikan progres roadmap ini di LinkedIn. Ini juga cara membangun personal branding.

---

## 7. Pengalaman Produksi (Paling Penting)

Skill tanpa pengalaman produksi akan sulit diakui sebagai senior. Cari salah satu (atau lebih):
- **Freelance**: aplikasi untuk UMKM sekitar (kasir, absensi, katalog)
- **Kerja** sebagai mobile developer (mulai melamar posisi mid setelah Fase 3 selesai)
- **Produk sendiri**: aplikasi absensi ini bisa ditawarkan ke kantor kecil, sekolah, atau organisasi

Yang dicari: **pengguna nyata**, **bug nyata**, dan **tanggung jawab nyata**.

---

## Timeline Karier yang Realistis

| Waktu | Target |
|---|---|
| Setelah Fase 1 (±4 bulan) | Bisa mengambil proyek freelance kecil |
| Setelah Fase 3 (±10 bulan) | Siap melamar posisi **Mid-level React Native Developer** |
| Setelah Fase 4 (±15–18 bulan) | Skill setara **Senior awal**; pengakuan formal biasanya butuh 1–2 tahun pengalaman produksi |

---

← [Fase 4](fase-4-topik-senior.md) · [Kembali ke README](../README.md)
