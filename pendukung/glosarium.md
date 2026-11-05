# 📖 Glosarium

[← Dokumen Pendukung](README.md)

Istilah yang muncul di roadmap, dijelaskan singkat dalam Bahasa Indonesia. Kolom **Fase** menunjukkan kapan istilah itu mulai penting.

---

## A–C

| Istilah | Arti | Fase |
|---|---|---|
| **AAB** (Android App Bundle) | Format unggahan ke Play Store. Google membuat APK yang dioptimasi per perangkat dari file ini. | 3 |
| **AbortController** | Objek untuk membatalkan request/Promise (misalnya `fetch`) lewat `signal`. | 0 |
| **Action (Laravel)** | Class berisi satu use case bisnis, misalnya `CheckInAction`. Menjaga controller tetap tipis. | 2 |
| **ADR** | *Architecture Decision Record*: dokumen singkat berisi satu keputusan arsitektur beserta alasannya. | 3 |
| **API Resource** | Class Laravel yang mengubah model menjadi JSON dengan bentuk terkontrol. | 2 |
| **APK** | File instalasi Android. Bisa dibagikan langsung, tanpa lewat Play Store. | 3 |
| **APNs** | *Apple Push Notification service*: jalur push notification ke iOS. | 2 |
| **AppState** | API React Native untuk mengetahui apakah aplikasi sedang aktif, di background, atau tidak aktif. | 2 |
| **async/await** | Sintaks untuk menulis kode Promise seolah-olah sinkron. | 0 |
| **Backoff (exponential)** | Jeda retry yang terus membesar: 1 detik, 2 detik, 4 detik, dan seterusnya. Supaya server yang sedang bermasalah tidak dibanjiri. | 0 |
| **Bundle (JS)** | Satu file hasil gabungan semua kode JS aplikasi, dibuat oleh Metro. | 1 |
| **Cache invalidation** | Menandai data cache sebagai basi supaya diambil ulang dari server. | 2 |
| **CI/CD** | *Continuous Integration / Delivery*: test dan build otomatis setiap ada perubahan kode. | 3 |
| **Closure** | Fungsi yang mengingat variabel dari tempat ia dibuat. | 0 |
| **CNG** | *Continuous Native Generation*: folder `android/` dan `ios/` dibuat otomatis oleh `expo prebuild`, bukan diedit manual. | 4 |
| **Config plugin** | Kode yang memodifikasi konfigurasi native (Manifest, Info.plist) secara otomatis saat prebuild. | 4 |
| **Crash-free rate** | Persentase sesi/pengguna yang tidak mengalami crash. Metrik utama kesehatan rilis. | 3 |
| **Cursor pagination** | Pagination berbasis penanda posisi (cursor), bukan nomor halaman. Stabil untuk infinite scroll. | 2 |

## D–H

| Istilah | Arti | Fase |
|---|---|---|
| **Debounce** | Menunda aksi sampai input berhenti berubah selama waktu tertentu (misalnya pencarian). | 0 |
| **Deep link** | URL yang membuka layar tertentu di aplikasi, misalnya `absensi://izin/31`. | 1 |
| **Dependency injection** | Memberikan dependensi dari luar (misalnya `fetchImpl`) supaya mudah diganti saat test. | 0 |
| **Design token** | Nilai desain bernama (warna, spacing, radius) yang dipakai konsisten di seluruh UI. | 1 |
| **Development build** | Build aplikasi berisi native module Anda sendiri + dev tools. Pengganti Expo Go untuk proyek serius. | 1 |
| **Discriminated union** | Union type yang dibedakan oleh satu field, misalnya `status: 'loading' \| 'success'`. | 0 |
| **EAS** | *Expo Application Services*: layanan cloud untuk Build, Submit, dan Update. | 3 |
| **Event loop** | Mekanisme JavaScript yang menjalankan kode sinkron, lalu microtask, lalu macrotask. | 0 |
| **Expo Go** | Aplikasi untuk mencoba proyek Expo tanpa build. Terbatas pada native module bawaan Expo. | 1 |
| **Expo Router** | Navigasi berbasis file (folder `app/`). | 1 |
| **Fabric** | Renderer baru React Native (arsitektur baru). | 4 |
| **Feature flag** | Saklar dari server untuk menyalakan/mematikan fitur tanpa rilis ulang. | 4 |
| **FCM** | *Firebase Cloud Messaging*: jalur push notification ke Android. | 2 |
| **Fingerprint (runtime)** | Hash dari semua kode native. Kalau berubah, perlu build baru (OTA tidak cukup). | 3 |
| **FlashList** | Pengganti FlatList dengan view recycling, lebih cepat untuk list panjang. | 4 |
| **Form Request** | Class Laravel untuk validasi + otorisasi request. | 2 |
| **gcTime** | Lama cache TanStack Query disimpan setelah tidak dipakai komponen mana pun. | 2 |
| **Geofence** | Batas area virtual (titik + radius). Absen hanya sah di dalamnya. | 2 |
| **Hermes** | Engine JavaScript yang dioptimasi untuk React Native. | 1 |
| **Hydration (cache)** | Memuat cache tersimpan ke memori saat aplikasi dibuka. | 2 |

## I–N

| Istilah | Arti | Fase |
|---|---|---|
| **Idempotency key** | ID unik per aksi; request yang sama dikirim berkali-kali tetap diproses sekali. | 4 |
| **IDOR** | *Insecure Direct Object Reference*: user mengakses data orang lain dengan mengganti ID. Dicegah dengan Policy. | 4 |
| **Immutability** | Tidak mengubah data asli; selalu membuat salinan baru. Wajib untuk state React. | 0 |
| **Interceptor** | Fungsi Axios yang dijalankan sebelum request atau sesudah response (misalnya menambah token, menangani 401). | 2 |
| **Jank** | UI patah-patah karena frame terlewat (> 16 ms per frame). | 4 |
| **JSI** | *JavaScript Interface*: JS memanggil C++/native secara langsung tanpa serialisasi JSON. | 4 |
| **Macrotask** | Antrean tugas seperti `setTimeout`, I/O. Dijalankan setelah semua microtask habis. | 0 |
| **Memoization** | Menyimpan hasil komputasi supaya tidak dihitung ulang (`useMemo`, `memo`). | 0 |
| **Metro** | Bundler JavaScript untuk React Native. | 1 |
| **Microtask** | Antrean prioritas tinggi: `Promise.then`, lanjutan setelah `await`, `queueMicrotask`. | 0 |
| **MMKV** | Penyimpanan key-value yang sangat cepat dan sinkron. | 1 |
| **Mock location** | Lokasi palsu dari aplikasi fake GPS. | 4 |
| **MSW** | *Mock Service Worker*: me-mock API di level jaringan untuk testing. | 3 |
| **Native module** | Kode Kotlin/Swift yang bisa dipanggil dari JavaScript. | 4 |

## O–S

| Istilah | Arti | Fase |
|---|---|---|
| **Offline-first** | UI membaca dari data lokal; sinkronisasi ke server berjalan di belakang. | 4 |
| **Optimistic update** | UI diubah dulu sebelum server menjawab, lalu dibatalkan kalau gagal. | 2 |
| **OTA update** | *Over-the-air*: memperbarui bundle JS tanpa lewat store. | 3 |
| **Outbox pattern** | Aksi disimpan di tabel antrean lokal, lalu dikirim saat memungkinkan. | 4 |
| **Policy (Laravel)** | Class otorisasi: "bolehkah user ini melakukan aksi pada data ini?" | 2 |
| **Prebuild** | `npx expo prebuild`: membuat folder `android/` dan `ios/` dari konfigurasi. | 4 |
| **Query key** | Identitas cache di TanStack Query, misalnya `['attendance', 'today']`. | 2 |
| **Race condition** | Hasil bergantung pada urutan selesainya proses async; sering menyebabkan data lama menimpa data baru. | 0 |
| **Re-render** | Komponen React dipanggil ulang karena state, props, atau context berubah. | 0 |
| **Reverb** | Server WebSocket resmi Laravel. | 2 |
| **runtimeVersion** | Penanda kecocokan antara bundle OTA dan kode native aplikasi. | 3 |
| **Sanctum** | Paket autentikasi Laravel; di mobile memakai personal access token. | 2 |
| **SecureStore** | Penyimpanan terenkripsi (Keychain di iOS, Keystore di Android). | 1 |
| **Server state** | Data yang sumber kebenarannya di server (profil, absensi). Dikelola TanStack Query. | 2 |
| **Source map** | Peta dari kode yang di-bundle ke kode asli, supaya stack trace di Sentry terbaca. | 3 |
| **Stale closure** | Closure yang memegang nilai state lama dari render sebelumnya. | 0 |
| **staleTime** | Lama data TanStack Query dianggap segar (tidak di-refetch). | 2 |
| **Staged rollout** | Rilis bertahap ke sebagian persen pengguna. | 4 |

## T–Z

| Istilah | Arti | Fase |
|---|---|---|
| **Testing pyramid** | Banyak unit test, sedikit E2E test. | 3 |
| **Thumbnail** | Versi kecil gambar untuk ditampilkan di list. | 4 |
| **Tree-shaking** | Menghapus kode yang tidak dipakai saat bundling. | 0 |
| **TurboModules** | Sistem native module baru: dimuat lazy, bertipe, lewat JSI. | 4 |
| **Type guard** | Fungsi yang mempersempit tipe: `function isX(v: unknown): v is X`. | 0 |
| **UI thread** | Thread utama native yang menggambar layar. | 4 |
| **Versioning API** | Menjaga versi API (`/v1`, `/v2`) supaya aplikasi lama tidak rusak. | 2 |
| **Worklet** | Fungsi kecil yang dijalankan Reanimated di UI thread. | 4 |
| **Zod** | Library validasi data saat runtime + inferensi tipe TypeScript. | 0 |
| **Zustand** | Library state management client yang ringan. | 2 |
