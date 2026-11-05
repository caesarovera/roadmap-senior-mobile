# Proyek Absensi — 05. Milestone & Rencana Sprint

[← Kembali ke README](../README.md) · [← Layar & Alur](04-layar-dan-alur.md)

Proyek ini dikembangkan dalam **3 versi** yang mengikuti fase roadmap. Setiap sprint = 1 minggu (±12 jam).

> 💡 **Tips:** buat **GitHub Project** (board Kanban) dan ubah setiap checklist di bawah menjadi *issue*. Kerjakan lewat branch + PR. Dengan begitu Anda terbiasa dengan alur kerja tim profesional.

---

## 🟦 v1: MVP (Fase 2, Minggu 9–12)

### Sprint 1 (Minggu 9): Fondasi & Beranda
**Backend**
- [ ] Migrasi + model + factory: offices, shifts, users, attendances, leave_requests, device_tokens
- [ ] Seeder data demo ([lihat](02-database.md#4-seeder-untuk-development--e2e))
- [ ] Endpoint: `auth/login`, `auth/logout`, `auth/me`, `attendances/today`
- [ ] Format error seragam di `bootstrap/app.php`
- [ ] Scramble aktif di `/docs/api`

**Mobile**
- [ ] Struktur folder sesuai [blueprint](../arsitektur/01-struktur-react-native.md)
- [ ] `env.ts`, `api/client.ts`, `query-client.ts`, `token.ts`
- [ ] Store auth + root layout dengan guard
- [ ] Layar Login (RHF + Zod), lengkap dengan semua state error
- [ ] Bottom tabs + Beranda (data `today` + skeleton + pull to refresh)
- [ ] Komponen UI: Button, Card, Input, Screen, EmptyState, ErrorState

**Definition of Done:** login → Beranda menampilkan data shift asli dari API → logout.

### Sprint 2 (Minggu 10): Absen Masuk & Pulang
**Backend**
- [ ] `GeofenceService` + `CheckInAction` + `CheckOutAction`
- [ ] Endpoint check-in/check-out dengan upload foto
- [ ] Job `GenerateAttendanceThumbnail` (paket image, misalnya Intervention Image)
- [ ] Hitung `work_duration_minutes` saat check-out

**Mobile**
- [ ] Layar Lokasi: izin, GPS, jarak, semua state error
- [ ] Layar Selfie: kamera depan, pratinjau, kompresi
- [ ] Upload dengan progress + retry
- [ ] Layar Sukses + haptic
- [ ] Fungsi domain `distanceMeters`, `isWithinRadius`

**DoD:** absen masuk dari HP asli di dekat titik kantor (atur titik kantor di seeder ke lokasi rumah Anda untuk pengujian), lalu ditolak saat koordinat diubah menjauh.

### Sprint 3 (Minggu 11): Riwayat, Izin, Notifikasi
**Backend**
- [ ] `GET /attendances` (cursor) + `/summary` + detail (dengan Policy)
- [ ] CRUD leave-requests + aturan overlap & kuota
- [ ] `POST/DELETE /devices`
- [ ] `ExpoPushService` + job `SendPushNotification`
- [ ] Scheduled command: pengingat absen masuk dan penanda alpha di malam hari

**Mobile**
- [ ] Riwayat: infinite scroll + filter bulan + detail
- [ ] Izin: kuota, list dengan filter, form (modal), detail, batalkan
- [ ] Optimistic update saat mengajukan izin
- [ ] Registrasi push token setelah login; hapus saat logout
- [ ] Tap notifikasi membuka detail izin (deep link)

**DoD:** admin menyetujui izin dari database/tinker → HP menerima push → tap → membuka detail dengan status baru.

### Sprint 4 (Minggu 12): Admin Panel, Realtime, Polishing
**Backend**
- [ ] Filament: resource Karyawan, Kantor (input koordinat + radius), Shift, Pengajuan Izin (aksi Setujui/Tolak)
- [ ] Dashboard Filament: widget hadir/terlambat/belum absen hari ini
- [ ] Ekspor Excel rekap bulanan (misalnya dengan `maatwebsite/excel` atau `openspout`)
- [ ] Reverb + event `LeaveRequestStatusChanged` dan `AttendanceCheckedIn`

**Mobile**
- [ ] Echo + Reverb: status izin berubah secara live
- [ ] Profil, ganti password, pengaturan tema
- [ ] Dark mode di semua layar
- [ ] Banner offline (NetInfo)
- [ ] Ikon aplikasi + splash screen

**Penutup v1**
- [ ] README kedua repo: deskripsi, GIF demo, arsitektur, cara menjalankan
- [ ] Rekam video demo 2–3 menit
- [ ] Tag rilis `v1.0.0`

---

## 🟩 v2: Kualitas & Rilis (Fase 3, Minggu 1–12)

| Minggu | Pekerjaan di Proyek Absensi |
|---|---|
| 1–2 | Refactor ke struktur fitur + aturan ESLint boundaries + 3 ADR |
| 3 | Unit test: geofence, status kehadiran, format, store auth |
| 4 | Component test: Login, Beranda (semua state), Form Izin (dengan MSW) |
| 5 | E2E Maestro: login, check-in, ajukan izin |
| 6 | Pest: semua endpoint (sukses, validasi, otorisasi, aturan bisnis) |
| 7 | `app.config.ts` + varian dev/preview/production + staging backend |
| 8 | `eas.json` + build preview, lalu bagikan APK ke 3–5 tester |
| 9 | GitHub Actions: CI mobile + CI backend + branch protection |
| 10 | EAS Update + `runtimeVersion` + `docs/RELEASE.md` |
| 11 | Sentry (mobile + Laravel) + Error Boundary |
| 12 | Kebijakan privasi, Data Safety, closed testing, lalu **rilis Google Play** |

**Tag rilis:** `v2.0.0`

---

## 🟥 v3: Fitur Level Senior (Fase 4, Minggu 1–20)

| Blok | Pekerjaan di Proyek Absensi |
|---|---|
| A. Performa | Baseline → FlashList + thumbnail + `expo-image` → startup -20% → laporan |
| B. Animasi | Pulse tombol absen, animasi sukses, swipe di riwayat, bottom sheet filter, audit TalkBack |
| C. Offline | Dokumen desain → SQLite + outbox → idempotency middleware → delta sync → matriks 10 skenario |
| D. Native | Modul `expo-device-integrity` (deteksi mock location + developer mode) → integrasi ke check-in → publikasi ke npm |
| E. Keamanan | Storage privat + `temporaryUrl` untuk foto, token expiry, self-pentest, `docs/security-review.md` |
| F. Rilis | Endpoint `/config`, force update, feature flag "lembur", staged rollout, post-mortem, video presentasi arsitektur |

**Tag rilis:** `v3.0.0`

---

## 📊 Ringkasan Portofolio Akhir

Setelah v3, README proyek Anda bisa menyebutkan, misalnya:

> - Aplikasi absensi **offline-first** dengan React Native (Expo) + Laravel
> - Validasi geofence di server, selfie terkompresi (~4 MB → ~200 KB)
> - **Native module** deteksi fake GPS (Kotlin), dipublikasikan di npm
> - Sinkronisasi offline dengan pola outbox + idempotency key, nol duplikasi dalam 10 skenario uji
> - Startup turun X%, scroll 60 fps pada 10.000 data
> - CI/CD (GitHub Actions + EAS), OTA update, staged rollout, crash-free rate 99,x% (Sentry)
> - Tersedia di **Google Play**

Angka nyata seperti ini yang membedakan portofolio senior dari portofolio tutorial.

---

[← Layar & Alur](04-layar-dan-alur.md) · [Kembali ke README](../README.md)
