# 🎤 Persiapan Interview Mobile Developer

[← Dokumen Pendukung](README.md)

Pertanyaan yang sering muncul, dikelompokkan per level, beserta **poin jawaban** (bukan jawaban hafalan). Latih menjawab dengan kata-kata sendiri, sebaiknya dengan contoh dari proyek absensi Anda.

> Cara latihan: rekam diri Anda menjawab 3 pertanyaan per hari (maksimal 2 menit per jawaban), lalu dengarkan ulang.

---

## 🟢 Level Junior (setelah Fase 1)

| Pertanyaan | Poin jawaban | Belajar di |
|---|---|---|
| Apa beda `let`, `const`, `var`? | Scope blok vs fungsi, hoisting, TDZ, assign ulang | Fase 0 M1 |
| Jelaskan event loop. | Call stack → microtask (semua) → macrotask (satu). Contoh `Promise.then` vs `setTimeout` | Fase 0 M3 |
| Apa itu closure? Beri contoh nyata. | Fungsi mengingat scope; contoh: counter privat, stale closure di `useEffect` | Fase 0 M1 |
| Kenapa state React harus immutable? | React membandingkan referensi; mutasi tidak memicu render | Fase 0 M4 |
| Bedanya React Native dengan WebView? | RN merender komponen native asli; WebView merender HTML | Fase 1 M1 |
| Kenapa FlatList, bukan ScrollView + map? | Virtualisasi: hanya merender item yang terlihat | Fase 1 M4 |
| Di mana menyimpan token? | SecureStore (terenkripsi), bukan AsyncStorage | Fase 1 M7 |
| Kapan izin lokasi sebaiknya diminta? | Saat fitur dipakai, dengan penjelasan; tangani penolakan | Fase 1 M8 |

## 🟡 Level Mid (setelah Fase 3)

| Pertanyaan | Poin jawaban | Belajar di |
|---|---|---|
| Server state vs client state? | Sumber kebenaran di server vs di HP; Query vs Zustand; jangan disalin | Fase 2 M3–5 |
| Jelaskan `staleTime` dan `gcTime`. | Segar vs disimpan; contoh angka dan alasannya | Fase 2 M3 |
| Bagaimana menangani token kedaluwarsa? | Interceptor 401 → logout sekali → bersihkan cache; pengecualian endpoint login | Fase 2 M2 |
| Bagaimana mendesain API untuk mobile? | Versioning, format error konsisten, cursor pagination, ISO 8601, `code` bisnis | Fase 2 M1 |
| Optimistic update itu apa dan risikonya? | UI duluan → rollback kalau gagal; risiko inkonsistensi | Fase 2 M4 |
| Push notification vs WebSocket? | Aplikasi tertutup vs terbuka; keduanya saling melengkapi | Fase 2 M7–8 |
| Bagaimana struktur folder proyek Anda, dan kenapa? | Berbasis fitur, public API `index.ts`, aturan ESLint | Fase 3 M1–2 |
| Strategi testing Anda? | Piramida; prioritas logika domain; RNTL berbasis perilaku; E2E untuk alur kritis | Fase 3 M3–6 |
| Kapan OTA, kapan build baru? | JS/aset vs native; `runtimeVersion`; kebijakan store | Fase 3 M10 |
| Bagaimana Anda tahu aplikasi crash di production? | Sentry + source map + alert; crash-free rate per rilis | Fase 3 M11 |

## 🔴 Level Senior (setelah Fase 4)

| Pertanyaan | Poin jawaban | Belajar di |
|---|---|---|
| Jelaskan arsitektur baru React Native. | JSI, TurboModules, Fabric; kenapa lebih cepat dari bridge | Fase 4 Blok A |
| List Anda lag. Bagaimana mendiagnosisnya? | Ukur dulu (Profiler, Perf Monitor, build release) → render item, gambar, FlashList → ukur ulang | Fase 4 Blok A |
| Kenapa animasi tersendat saat fetch data? | JS thread sibuk; pindahkan animasi ke UI thread (Reanimated) | Fase 4 Blok B |
| Rancang fitur absen offline. | Outbox, idempotency key, waktu klien vs server, pemicu sync, resolusi konflik, uji skenario | Fase 4 Blok C |
| Pernah menulis native module? Ceritakan. | Masalah → kenapa library tidak cukup → Expo Modules API → test → publikasi | Fase 4 Blok D |
| Bagaimana mencegah kecurangan absen? | Validasi server, deteksi mock location, selfie, audit selisih waktu; HP tidak bisa dipercaya | Fase 4 Blok D–E |
| Bagaimana mengamankan aplikasi mobile? | MASVS; rahasia tidak di bundle; SecureStore; pinning beserta trade-off-nya; Policy di server | Fase 4 Blok E |
| Bagaimana Anda merilis dengan aman? | Feature flag, staged rollout, metrik, rollback, force update | Fase 4 Blok F |
| Ceritakan keputusan teknis yang Anda sesali. | Konteks → keputusan → dampak → pelajaran (jujur, tanpa menyalahkan) | Fase 4 Blok F |
| Bagaimana Anda me-review kode junior? | Fokus pada kebenaran, risiko, keterbacaan; beri alasan; bedakan wajib vs saran | Berkelanjutan |

---

## 🧩 Soal System Design (Senior)

Latih dengan format: **klarifikasi kebutuhan → batasan → desain tingkat tinggi → detail kritis → trade-off → cara mengukur keberhasilan.**

1. **Aplikasi absensi untuk 10.000 karyawan di 200 cabang.** (Gunakan proyek Anda sebagai jawaban dasar, lalu bahas skala: queue, storage, rate limit, laporan.)
2. **Aplikasi chat sederhana** dengan status terkirim/dibaca dan mode offline.
3. **Aplikasi kasir UMKM** yang harus tetap bisa berjualan tanpa internet seharian.
4. **Fitur feed** dengan gambar, infinite scroll, dan pull-to-refresh yang lancar di HP kelas bawah.

---

## 📂 Siapkan Sebelum Interview

- [ ] Portofolio di GitHub dengan README studi kasus ([template](template/readme-portofolio.md))
- [ ] Link aplikasi di Play Store (atau APK + video demo)
- [ ] 3 cerita **STAR** (Situation, Task, Action, Result) dari proyek Anda: satu bug sulit, satu keputusan teknis, satu optimasi dengan angka
- [ ] Bisa menggambar [diagram gambaran sistem](../assets/diagram/sistem-gambaran.svg) dari ingatan dalam 5 menit
- [ ] Pertanyaan balik untuk pewawancara: proses rilis, cara review kode, on-call, metrik kualitas
