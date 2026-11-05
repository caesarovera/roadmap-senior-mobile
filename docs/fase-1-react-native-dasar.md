# Fase 1 — Dasar React Native + Expo

[← Kembali ke README](../README.md) · **Durasi: 10 minggu** · Repo latihan: `rn-playground`, `rn-keuangan`

## Tujuan Fase

Membangun aplikasi mobile yang **terasa native**: layout benar di berbagai ukuran layar, navigasi lancar, form nyaman dipakai, data tersimpan di perangkat, dan memakai fitur HP (kamera, lokasi).

**Hasil akhir fase:** aplikasi **Catatan Keuangan Pribadi** yang berjalan offline.

> 📌 Dokumentasi utama fase ini: [docs.expo.dev](https://docs.expo.dev/) dan [reactnative.dev](https://reactnative.dev/docs/getting-started)

---

## Minggu 1 — Setup & Cara Kerja React Native

🎯 **Tujuan:** proyek pertama berjalan di emulator **dan** HP asli, dan Anda paham apa yang terjadi di baliknya.

📚 **Materi**
- Membuat proyek: `npx create-expo-app@latest rn-playground`
- Struktur proyek Expo: `app/`, `app.json`, `package.json`, `assets/`
- **Cara kerja RN secara garis besar:** kode JS berjalan di engine Hermes, lalu React Native merender **komponen native asli** (bukan WebView)
- **Expo Go vs Development Build**: Expo Go untuk belajar cepat; dev build (`npx expo run:android` atau EAS) saat butuh native module kustom
- Metro bundler, fast refresh, dev menu, dan React Native DevTools
- Setup ESLint + Prettier, aktifkan TypeScript `strict`

🛠 **Latihan**
1. Jalankan proyek di emulator Android **dan** di HP via Expo Go.
2. Ubah layar utama menjadi kartu profil Anda (foto, nama, bio).
3. Buka React Native DevTools, pasang breakpoint, lalu inspeksi komponen.

✅ **Checkpoint**
- Apa bedanya React Native dengan aplikasi WebView (misalnya Cordova)?
- Kapan Expo Go tidak cukup dan Anda butuh development build?

---

## Minggu 2 — Komponen Inti & Styling

🎯 **Tujuan:** menguasai blok bangunan UI.

📚 **Materi**
- `View`, `Text`, `Image` (pertimbangkan `expo-image`), `ScrollView`, `Pressable`, `TextInput`, `ActivityIndicator`, `Switch`, `Modal`
- `StyleSheet.create` dan kenapa tidak ada CSS cascading
- **Flexbox di RN:** default `flexDirection: 'column'`, `flex: 1`, `gap`, `alignItems`, `justifyContent`
- Unit tanpa `px`; satuan berbasis density-independent pixel
- Teks harus selalu berada di dalam `<Text>`
- Sumber: [reactnative.dev: Core Components](https://reactnative.dev/docs/components-and-apis) · [Flexbox](https://reactnative.dev/docs/flexbox)

🛠 **Latihan**
Tiru 3 layar dari aplikasi yang Anda pakai sehari-hari (misalnya halaman login, profil, dan detail produk), **hanya UI statis**. Fokus pada ketepatan layout.

Buat juga komponen reusable: `Button` (varian primary/secondary/ghost, state loading/disabled), `Card`, `Input` (label + pesan error).

✅ **Checkpoint**
- Bagaimana membuat elemen menempel di bawah layar sementara konten di atasnya bisa di-scroll?

---

## Minggu 3 — Layout Lanjutan & Adaptasi Platform

🎯 **Tujuan:** UI tetap benar di HP kecil, HP besar, Android, iOS, mode gelap, dan saat keyboard muncul.

📚 **Materi**
- `react-native-safe-area-context` (notch, status bar, navigation bar)
- `useWindowDimensions` untuk layout responsif
- `Platform.OS`, `Platform.select`, file `.android.tsx`/`.ios.tsx`
- `KeyboardAvoidingView` (atau `react-native-keyboard-controller`)
- Dark mode: `useColorScheme`, sistem **design token** (warna, spacing, radius, font)
- Font kustom dengan `expo-font`

🛠 **Latihan**
1. Buat file `theme.ts` berisi token light/dark, lalu terapkan ke komponen Minggu 2.
2. Buat layar form panjang yang tidak tertutup keyboard di Android maupun iOS.
3. Uji di emulator dengan ukuran layar kecil dan tablet.

✅ **Checkpoint**
- Kenapa hardcode warna di setiap komponen menyulitkan dark mode, dan bagaimana token menyelesaikannya?

---

## Minggu 4 — List & Performa Dasar

🎯 **Tujuan:** menampilkan data dalam jumlah besar dengan lancar.

📚 **Materi**
- **Kenapa `ScrollView` + `.map()` buruk untuk list panjang** (semua item dirender sekaligus)
- `FlatList`: `data`, `renderItem`, `keyExtractor`, `ListEmptyComponent`, `ListHeaderComponent`, `ItemSeparatorComponent`
- `SectionList` untuk data berkelompok (misalnya per tanggal)
- Pull to refresh (`refreshing`, `onRefresh`) dan infinite scroll (`onEndReached`)
- Dasar optimasi: `renderItem` yang stabil, `React.memo` untuk item, `getItemLayout`
- Kenalan dengan [FlashList](https://shopify.github.io/flash-list/) (akan didalami di Fase 4)

🛠 **Latihan**
1. Tampilkan 5.000 item dummy dengan `ScrollView`, lalu dengan `FlatList`. Rasakan bedanya.
2. Buat `SectionList` transaksi yang dikelompokkan per tanggal (pakai fungsi dari Fase 0 Minggu 4).
3. Tambahkan pull-to-refresh dan state kosong yang informatif.

✅ **Checkpoint**
- Apa yang terjadi kalau `keyExtractor` mengembalikan nilai yang tidak unik?

---

## Minggu 5 — Navigasi dengan Expo Router

🎯 **Tujuan:** membangun struktur navigasi aplikasi nyata.

📚 **Materi**
- **File-based routing**: `app/index.tsx`, `app/(tabs)/_layout.tsx`, `app/transaksi/[id].tsx`
- Stack, Tabs, Modal
- `Link`, `router.push`, `router.replace`, `router.back`
- Route params: `useLocalSearchParams`
- **Route group** `(auth)` dan `(app)`, beserta pola **protected route** (redirect kalau belum login)
- Deep link: `scheme` di `app.json`, lalu buka dengan `npx uri-scheme open`
- Sumber: [Expo Router docs](https://docs.expo.dev/router/introduction/)

🛠 **Latihan**
Buat kerangka navigasi aplikasi keuangan:
```
app/
├── _layout.tsx              ← root stack
├── (tabs)/
│   ├── _layout.tsx          ← bottom tabs
│   ├── index.tsx            ← Beranda (ringkasan)
│   ├── transaksi.tsx        ← Daftar transaksi
│   └── pengaturan.tsx
├── transaksi/
│   ├── [id].tsx             ← Detail
│   └── baru.tsx             ← Form (presentation: modal)
└── +not-found.tsx
```

✅ **Checkpoint**
- Apa bedanya `push` dan `replace`? Kapan memakai `replace` (petunjuk: setelah login)?
- Bagaimana membuka detail transaksi langsung lewat link `rnkeuangan://transaksi/12`?

---

## Minggu 6 — Form & Validasi

🎯 **Tujuan:** membuat form yang nyaman dipakai di HP.

📚 **Materi**
- [React Hook Form](https://react-hook-form.com/): `useForm`, `Controller` (wajib di RN), `formState`
- Validasi dengan **Zod** + `@hookform/resolvers`
- UX form mobile: `keyboardType`, `returnKeyType`, `autoComplete`, `secureTextEntry`, fokus ke input berikutnya (`ref.focus()`)
- Input khusus: date picker (`@react-native-community/datetimepicker`), input mata uang (format Rupiah)

🛠 **Latihan**
Form **Tambah Transaksi**: jenis (masuk/keluar), jumlah (format `Rp 1.500.000`), kategori (picker), tanggal, catatan.
- Validasi: jumlah > 0, kategori wajib diisi, tanggal tidak boleh di masa depan
- Tombol "Simpan" nonaktif selama form belum valid
- Tekan "Next" di keyboard untuk pindah ke input berikutnya

✅ **Checkpoint**
- Kenapa input mata uang sebaiknya disimpan sebagai angka (integer, satuan rupiah) dan hanya diformat saat ditampilkan?

---

## Minggu 7 — Penyimpanan Lokal

🎯 **Tujuan:** memilih penyimpanan yang tepat untuk tiap jenis data.

📚 **Materi**

| Penyimpanan | Untuk apa | Catatan |
|---|---|---|
| `expo-secure-store` | Token, kredensial | Terenkripsi (Keychain/Keystore) |
| `react-native-mmkv` | Preferensi, cache kecil | Sinkron dan sangat cepat; butuh dev build |
| `AsyncStorage` | Data kecil sederhana | Async, lebih lambat; jalan di Expo Go |
| `expo-sqlite` | Data terstruktur, query, data besar | Fondasi offline-first (Fase 4) |
| `expo-file-system` | File, foto, cache gambar | |

- Dasar SQL di SQLite: `CREATE TABLE`, `INSERT`, `SELECT ... WHERE ... ORDER BY`, index
- Migrasi skema sederhana (simpan versi skema dengan `PRAGMA user_version`)
- Opsional: ORM ringan seperti **Drizzle** untuk expo-sqlite

🛠 **Latihan**
1. Simpan transaksi di `expo-sqlite`: buat repository `transaksiRepo` dengan `getAll`, `getById`, `create`, `update`, `remove`, `getSummaryByMonth`.
2. Simpan preferensi (tema, mata uang) di MMKV atau AsyncStorage.
3. Buat migrasi versi 2: tambah kolom `foto_struk` di tabel transaksi.

✅ **Checkpoint**
- Kenapa token **tidak boleh** disimpan di AsyncStorage?
- Apa yang terjadi pada user lama saat Anda mengubah skema database tanpa migrasi?

---

## Minggu 8 — Fitur Perangkat & Izin Akses

🎯 **Tujuan:** memakai kemampuan HP dengan alur izin yang benar.

📚 **Materi**
- Alur izin (permission): cek → minta → tangani kalau ditolak → arahkan ke Settings (`Linking.openSettings()`)
- `expo-image-picker` (galeri dan kamera) dan `expo-camera`
- `expo-location`: izin *foreground*, akurasi, `getCurrentPositionAsync`
- `expo-haptics`, `expo-sharing`, `expo-clipboard`
- Konfigurasi izin di `app.json` (pesan izin iOS, permission Android)

🛠 **Latihan**
1. Lampirkan **foto struk** ke transaksi (kamera atau galeri), simpan file di `FileSystem.documentDirectory`.
2. Simpan **lokasi** saat transaksi dibuat (opsional, minta izin dengan sopan).
3. Tangani semua kondisi: izin ditolak, ditolak permanen, GPS mati.

✅ **Checkpoint**
- Kenapa sebaiknya izin diminta **saat fitur dipakai**, bukan saat aplikasi pertama kali dibuka?

---

## Minggu 9–10 — 🏁 Proyek Akhir Fase: Catatan Keuangan Pribadi

### Fitur Wajib
- [ ] Onboarding singkat (2–3 layar), hanya tampil sekali
- [ ] Beranda: saldo, total pemasukan/pengeluaran bulan ini, 5 transaksi terakhir
- [ ] Daftar transaksi per tanggal (`SectionList`), filter bulan dan kategori, pencarian
- [ ] Tambah, edit, dan hapus transaksi (dengan konfirmasi hapus)
- [ ] Foto struk (kamera/galeri)
- [ ] Kategori kustom (CRUD)
- [ ] Grafik sederhana pengeluaran per kategori (misalnya `victory-native` atau `react-native-gifted-charts`)
- [ ] Dark mode
- [ ] **Semua data offline** di SQLite
- [ ] Ekspor data ke CSV lalu bagikan (`expo-sharing`)

### Nilai Tambah
- [ ] Kunci aplikasi dengan sidik jari (`expo-local-authentication`)
- [ ] Pengingat harian dengan notifikasi lokal (`expo-notifications`)

### Struktur Folder
Gunakan struktur dari [arsitektur/01-struktur-react-native.md](../arsitektur/01-struktur-react-native.md). Versi sederhananya cukup untuk fase ini.

### README Proyek Wajib Berisi
- Screenshot atau GIF demo
- Alasan memilih SQLite dibanding penyimpanan lain
- Kendala terbesar dan cara Anda mengatasinya

✅ **Checkpoint Fase 1**
- [ ] Aplikasi berjalan lancar di HP Android asli
- [ ] Tidak ada warning merah atau kuning di console
- [ ] Layout benar di HP kecil dan besar, di mode terang maupun gelap
- [ ] Bisa menjelaskan pilihan penyimpanan untuk setiap jenis data
- [ ] Repo `rn-keuangan` di GitHub lengkap dengan README dan screenshot

---

← [Fase 0](fase-0-javascript-typescript.md) · Lanjut ke → [Fase 2: Aplikasi Nyata dengan Laravel](fase-2-aplikasi-nyata-laravel.md)
