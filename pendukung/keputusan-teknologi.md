# 🧭 Keputusan Teknologi

[← Dokumen Pendukung](README.md) · [Dokumen Arsitektur § ADR](../arsitektur/00-dokumen-arsitektur.md#9-keputusan-arsitektur-adr)

Dokumen ini menjelaskan **kenapa** stack di roadmap dipilih. Senior tidak memilih teknologi karena tren, melainkan karena **konteks, kebutuhan, dan risiko**. Pakai pola berpikir di sini saat Anda harus memilih teknologi di proyek nyata.

---

## 1. Kerangka Berpikir

Untuk setiap keputusan, tanyakan:

1. **Masalah apa** yang mau diselesaikan? (Bukan "library apa yang keren?")
2. **Apa batasannya?** Skill tim, waktu, anggaran, platform target, aturan store.
3. **Apa saja opsinya?** Minimal 2–3, termasuk opsi "tidak memakai apa-apa".
4. **Apa trade-off-nya?** Setiap pilihan punya biaya.
5. **Seberapa mudah dibatalkan?** Keputusan yang sulit dibatalkan butuh analisis lebih dalam.
6. **Tulis sebagai ADR** supaya alasannya tidak hilang.

---

## 2. Framework Mobile

| Kriteria | React Native + Expo | Flutter | Native (Kotlin + Swift) | Kotlin Multiplatform |
|---|---|---|---|---|
| Bahasa | TypeScript | Dart | Kotlin & Swift | Kotlin (+ Swift untuk UI iOS) |
| Satu codebase | ✅ UI + logika | ✅ UI + logika | ❌ dua codebase | Logika ✅ · UI pilihan (native atau Compose MP) |
| Kurva belajar (dari JS) | **Rendah** | Sedang | Tinggi | Tinggi |
| Tampilan | Komponen native asli | Engine render sendiri (konsisten di semua platform) | Native asli | Native / Compose |
| Akses fitur native | Lewat module; bisa tulis sendiri | Lewat plugin; bisa tulis sendiri | Penuh | Penuh |
| Ekosistem | npm (sangat besar) | pub.dev (besar) | Resmi platform | Sedang tumbuh |
| OTA update | ✅ (EAS Update) | Terbatas | ❌ | ❌ |
| Berbagi kode dengan web | ✅ (React) | Terbatas | ❌ | Sebagian |

**Keputusan:** React Native + Expo.
**Alasan:** skill JavaScript bisa langsung dipakai, satu codebase, OTA update, dan EAS mengurangi beban build. Developer yang juga menguasai Laravel bisa memegang produk dari ujung ke ujung.
**Kapan pilihan lain lebih tepat:** tim sudah ahli Dart (Flutter); aplikasi sangat bergantung pada fitur native terbaru, grafis berat, atau AR (Native); perusahaan ingin berbagi logika bisnis dengan aplikasi Android native yang sudah ada (KMP).

> 💡 Belajar Kotlin & Swift di Fase 4 tetap penting: senior React Native harus bisa turun ke native.

---

## 3. Manajemen State

| Opsi | Cocok untuk | Kekurangan |
|---|---|---|
| **TanStack Query** | Server state: cache, refetch, retry, pagination | Bukan untuk state client murni |
| **Zustand** | Client state global kecil–menengah | Tidak menangani cache server |
| Redux Toolkit (+ RTK Query) | Tim besar, butuh pola yang ketat & devtools | Lebih banyak boilerplate |
| Context API | Nilai yang jarang berubah (tema, i18n) | Semua consumer re-render saat nilai berubah |
| Jotai / Valtio | State atomik / berbasis proxy | Pola berbeda; tim perlu menyesuaikan |

**Keputusan:** TanStack Query (server state) + Zustand (client state).
**Alasan:** hampir semua state di aplikasi absensi berasal dari server. Sisa state client sangat kecil.

---

## 4. Penyimpanan Lokal

| Opsi | Tipe | Kecepatan | Enkripsi | Cocok untuk |
|---|---|---|---|---|
| `expo-secure-store` | Key-value | Lambat | ✅ | Token, kredensial |
| `react-native-mmkv` | Key-value | Sangat cepat (sinkron) | Opsional | Preferensi, cache kecil |
| `AsyncStorage` | Key-value | Lambat (async) | ❌ | Data kecil sederhana; berjalan di Expo Go |
| `expo-sqlite` (+ Drizzle) | Relasional | Cepat | Opsional (SQLCipher) | Data terstruktur, offline, outbox |
| `op-sqlite` | Relasional | Sangat cepat (JSI) | Opsional | Data besar, butuh performa |
| WatermelonDB | Relasional + reaktif + sync | Cepat | — | Offline-first dengan protokol sync bawaan |

**Keputusan:** SecureStore (token), MMKV (preferensi), expo-sqlite (offline/outbox).

---

## 5. Backend & Realtime

| Kebutuhan | Pilihan | Alternatif | Alasan |
|---|---|---|---|
| Framework | **Laravel** | Node (NestJS), Go, BaaS (Supabase/Firebase) | Skill sudah ada; ekosistem lengkap (queue, scheduler, broadcasting) |
| Auth mobile | **Sanctum token** | Passport (OAuth2), JWT | Sederhana; cukup untuk aplikasi first-party |
| Realtime | **Reverb** | Pusher, Ably, Soketi | Resmi Laravel, self-hosted, protokol kompatibel dengan Pusher |
| Admin panel | **Filament** | Nova, buat sendiri | Cepat, gratis, kaya fitur |
| Push | **Expo Push API** | FCM/APNs langsung, OneSignal | Satu API untuk Android & iOS; bisa beralih ke FCM langsung nanti |

---

## 6. Kualitas & Operasional

| Kebutuhan | Pilihan | Alternatif |
|---|---|---|
| Unit/component test | Jest + RNTL | Vitest (belum menjadi standar di RN) |
| E2E | **Maestro** | Detox (lebih kuat, setup lebih rumit), Appium |
| Mock API | MSW | Mock manual |
| CI | GitHub Actions | GitLab CI, Bitrise, Codemagic |
| Build | EAS Build | Build lokal, Fastlane |
| Monitoring | Sentry | Firebase Crashlytics, Bugsnag |

---

## 7. Template ADR untuk Keputusan Anda

Gunakan [template ADR](template/adr.md). Contoh judul ADR yang layak ditulis:
- 0011-memakai-flashlist-untuk-riwayat
- 0012-outbox-alih-alih-watermelondb
- 0013-foto-disimpan-di-r2-dengan-temporary-url
