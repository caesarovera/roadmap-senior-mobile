# ✅ Checklist Rilis

Salin ke `docs/RELEASE.md` di repo proyek. Centang setiap kali rilis.

**Versi:** v_._._ · **Tanggal:** YYYY-MM-DD · **Jenis:** OTA / Build baru

---

## 1. Sebelum Rilis

### Kode
- [ ] Semua PR untuk rilis ini sudah di-merge ke `main`
- [ ] CI hijau (lint, typecheck, unit, component test, Pest)
- [ ] E2E Maestro untuk alur kritis lulus (login, check-in, ajukan izin)
- [ ] Changelog ditulis

### Tentukan jenis rilis
- [ ] Ada perubahan native (library baru, izin baru, versi SDK, config plugin)?
  - **Ya** → build baru (bagian 2B)
  - **Tidak** → OTA (bagian 2A)

### Backend
- [ ] Migrasi database aman untuk aplikasi versi lama (hanya menambah, tidak menghapus/mengganti nama)
- [ ] Endpoint baru sudah di-deploy **sebelum** aplikasi yang memakainya dirilis
- [ ] Backup database terbaru tersedia

## 2A. Rilis OTA
- [ ] `eas update --channel preview --message "vX.Y.Z: ..."`
- [ ] Uji di HP dengan build preview (tutup-buka aplikasi 2x)
- [ ] Pantau Sentry minimal beberapa jam
- [ ] `eas update --channel production --message "vX.Y.Z: ..."`

## 2B. Rilis Build Baru
- [ ] Versi (`version`) dinaikkan sesuai semantic versioning
- [ ] `eas build --profile production --platform android`
- [ ] Uji AAB/APK di HP asli
- [ ] `eas submit --platform android` → track **Internal**
- [ ] Promosikan ke **Closed testing**, lalu ke **Production**
- [ ] Staged rollout: 5% → (pantau) → 20% → 50% → 100%
- [ ] Catatan rilis (*What's new*) diisi dalam Bahasa Indonesia

## 3. Setelah Rilis
- [ ] Crash-free rate di Sentry ≥ target (misalnya 99,5%)
- [ ] Tidak ada error baru yang melonjak
- [ ] Endpoint config: perbarui `latest_version` (dan `min_version` bila perlu force update)
- [ ] Tag git: `git tag vX.Y.Z && git push --tags`

## 4. Kalau Ada Masalah
| Situasi | Tindakan |
|---|---|
| Bug di OTA | Republish update sebelumnya ke channel production (rollback) |
| Bug di build baru | Hentikan staged rollout di Play Console, siapkan hotfix |
| Bug di backend | Rollback deploy / matikan fitur lewat feature flag |
| Bug serius & luas | Tulis [post-mortem](post-mortem.md) |
