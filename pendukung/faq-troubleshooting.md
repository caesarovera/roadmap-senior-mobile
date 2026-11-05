# 🛠️ FAQ & Troubleshooting

[← Dokumen Pendukung](README.md)

Masalah yang paling sering membuat pemula mentok, beserta cara mengatasinya. Kalau masalah Anda tidak ada di sini, ikuti langkah di [Cara Belajar § Jika Mentok](../docs/00-cara-belajar.md#6-jika-mentok).

---

## 🌐 Koneksi Aplikasi ↔ Laravel Lokal

### "Network request failed" / timeout saat memanggil `http://localhost:8000`
`localhost` di HP/emulator berarti **HP itu sendiri**, bukan laptop Anda.

| Menjalankan di | Pakai URL |
|---|---|
| Emulator Android | `http://10.0.2.2:8000` |
| Simulator iOS | `http://localhost:8000` |
| HP asli (Wi-Fi yang sama) | `http://<IP-laptop>:8000`, misalnya `http://192.168.1.10:8000` |

Jalankan Laravel supaya bisa diakses dari jaringan:
```bash
php artisan serve --host=0.0.0.0 --port=8000
```
Alternatif yang paling mudah: tunnel HTTPS dengan **ngrok** atau **Cloudflare Tunnel**, lalu pakai URL HTTPS-nya.

### Request HTTP (bukan HTTPS) ditolak di Android
Android memblokir HTTP polos secara default. Untuk development, gunakan tunnel HTTPS (disarankan) atau izinkan cleartext **hanya di varian development** lewat config plugin (misalnya `expo-build-properties` → `android.usesCleartextTraffic`). Jangan aktifkan untuk production.

### Selalu 401 padahal sudah login
- [ ] Header `Authorization: Bearer <token>` benar-benar terkirim? Cek di interceptor.
- [ ] Header `Accept: application/json` ada? Tanpa header ini Laravel bisa mengarahkan (redirect) ke halaman login.
- [ ] Token sudah kedaluwarsa (`expires_at`) atau dihapus?
- [ ] Route memakai middleware `auth:sanctum` (bukan `auth`)?

### Laravel mengembalikan HTML, bukan JSON
Pastikan klien mengirim `Accept: application/json` dan `shouldRenderJsonWhen` sudah diatur di `bootstrap/app.php`. Lihat [Struktur Laravel API](../arsitektur/02-struktur-laravel-api.md#bootstrapappphp).

### Upload foto gagal / file kosong di Laravel
- Format file di FormData RN: `{ uri, name: 'selfie.jpg', type: 'image/jpeg' }`
- **Jangan** set `Content-Type` dengan boundary manual; biarkan Axios/fetch yang membuatnya.
- Cek batas ukuran: `upload_max_filesize` & `post_max_size` di PHP, `client_max_body_size` di Nginx.

---

## 📱 Expo & Build

### Library native tidak jalan di Expo Go
Expo Go hanya berisi native module bawaan Expo. Untuk library seperti MMKV, buat **development build**:
```bash
npx expo run:android
```
Atau di cloud: `eas build --profile development`.

### "Invariant Violation" / modul tidak ditemukan setelah install library
```bash
npx expo install --check
```
```bash
npx expo start -c
```
Kalau library punya kode native, **build ulang** development build-nya.

### Versi library tidak cocok dengan SDK
Selalu install dengan `npx expo install <lib>`, bukan `npm install`. Jalankan `npx expo-doctor` untuk mendeteksi masalah.

### Emulator Android lambat / tidak muncul
- Aktifkan virtualisasi (VT-x/AMD-V) di BIOS.
- Pakai image **x86_64** dengan Google APIs.
- Alokasikan RAM ≥ 2 GB untuk emulator. Alternatif: pakai HP asli lewat Expo Go/dev build.

### Perubahan tidak muncul setelah OTA update
- Channel build dan channel update sama?
- `runtimeVersion` build sama dengan update? (Kalau ada perubahan native, OTA tidak akan diterima. Itu memang perilaku yang benar.)
- Update diunduh saat aplikasi dibuka dan biasanya baru diterapkan pada pembukaan **berikutnya**.

---

## ⚛️ React & State

### Komponen render berkali-kali
1. Buka React DevTools → Profiler → aktifkan "Record why each component rendered".
2. Penyebab umum: object/fungsi baru di setiap render yang dikirim sebagai prop, context terlalu besar, selector Zustand yang mengembalikan object baru (pakai `useShallow`).

### State tidak berubah / "terlambat satu langkah"
State update bersifat asinkron dan berlaku pada render **berikutnya**. Kalau bergantung pada nilai sebelumnya, pakai `setX(prev => ...)`.

### `setInterval` di `useEffect` berhenti di angka 1
Itu *stale closure*. Pakai functional update dan cleanup. Lihat latihan `use-detik.ts` di js-ts-playground Minggu 7.

### Data lama muncul sebentar setelah ganti user
Panggil `queryClient.clear()` saat logout. Lihat [Alur Autentikasi](../arsitektur/04-alur-autentikasi.md).

### Data tidak ter-update setelah mutasi
Panggil `queryClient.invalidateQueries({ queryKey: [...] })` di `onSuccess`, dan pastikan query key-nya cocok (gunakan *query key factory*).

---

## 📍 Lokasi, Kamera, Notifikasi

### Lokasi tidak akurat / lama didapat
- Aktifkan GPS dan mode akurasi tinggi.
- Di dalam gedung akurasi bisa ±50 m. Itulah kenapa server memberi toleransi berdasarkan `accuracy`.
- Pakai timeout dan tampilkan tombol "Perbarui lokasi".

### Izin ditolak permanen
`requestPermissionsAsync()` tidak lagi menampilkan dialog. Tampilkan penjelasan + tombol yang memanggil `Linking.openSettings()`.

### Push notification tidak sampai
- Push **tidak** bekerja di emulator tanpa Google Play Services; uji di HP asli.
- Token sudah tersimpan di tabel `device_tokens`?
- Kredensial FCM (Android) sudah diatur di EAS?
- Cek respons dari Expo Push API: tiket error seperti `DeviceNotRegistered` berarti token harus dihapus.

---

## 🧪 Testing

### Test RNTL error "No QueryClient set"
Bungkus komponen dengan `QueryClientProvider` khusus test (dengan `retry: false`) lewat opsi `wrapper`.

### Test async gagal secara acak (flaky)
Gunakan `findBy...` / `waitFor`, bukan `getBy...` + `setTimeout`. Untuk timer, pakai fake timers.

### Test Pest gagal karena waktu
Bekukan waktu dengan `$this->travelTo(now()->setTime(8, 5))` supaya hasil "terlambat/tepat waktu" konsisten.

---

## 🚀 Play Store

### Build ditolak karena target API level
Naikkan versi SDK Expo (setiap SDK baru menaikkan target API) lalu build ulang.

### Tidak bisa langsung rilis ke Production
Akun developer pribadi yang baru wajib menjalankan **closed testing** dengan sejumlah tester selama periode tertentu. Cek syarat terbarunya di Play Console.

### Reviewer tidak bisa login
Sediakan akun demo di formulir *App access*, dan pastikan akun demo bisa absen dari mana saja (misalnya kantor demo dengan radius besar).
