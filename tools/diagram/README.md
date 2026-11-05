# Generator Diagram

Semua diagram di [`assets/diagram/`](../../assets/diagram/) dibuat dari kode Python di folder ini, **tanpa library tambahan** (cukup Python 3.10+).

## Cara membuat ulang

```bash
python3 tools/diagram/build.py
```

Hanya diagram tertentu (berdasarkan potongan nama file):

```bash
python3 tools/diagram/build.py alur
```

## Struktur

| File | Isi |
|---|---|
| `lib.py` | Komponen gambar: `Svg`, `kotak`, `grup`, `panah`, `catatan`, `legenda`, `Sekuens` (sequence diagram) |
| `d_arsitektur.py` | Gambaran sistem, layer mobile, request Laravel, peta state, ERD |
| `d_alur.py` | Autentikasi, check-in, notifikasi & realtime, offline outbox, CI/CD |
| `d_belajar.py` | Timeline roadmap, event loop, thread RN, piramida testing, siklus TanStack Query |
| `build.py` | Menjalankan semuanya dan menulis file SVG |

## Warna (tema)

| Tema | Dipakai untuk |
|---|---|
| `mobile` (biru) | Aplikasi React Native |
| `backend` (oranye) | Laravel |
| `data` (hijau) | Database, storage, fungsi domain murni |
| `external` (ungu) | Layanan pihak ketiga |
| `warn` (kuning) | Aturan penting, peringatan |
| `danger` (merah) | Error, kegagalan |
| `teal` | Perangkat & fitur native |
| `pink` | Topik Fase 4 |
| `netral` (abu-abu) | Lainnya |

## Menambah diagram baru

1. Tulis fungsi baru di salah satu file `d_*.py` yang mengembalikan `("nama-file.svg", svg)`.
2. Tambahkan fungsi itu ke daftar `SEMUA` di file tersebut.
3. Jalankan `build.py`, lalu tampilkan di dokumen: `![Judul](../assets/diagram/nama-file.svg)`.

Setiap SVG punya latar putih sendiri, jadi tetap terbaca di GitHub mode gelap.
