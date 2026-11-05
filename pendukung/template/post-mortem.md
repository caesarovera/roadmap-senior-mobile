# Post-Mortem: [Judul Insiden]

| | |
|---|---|
| **Tanggal insiden** | YYYY-MM-DD HH:MM – HH:MM (WIB) |
| **Durasi** | ... menit |
| **Tingkat keparahan** | SEV1 (semua user) · SEV2 (sebagian besar) · SEV3 (sebagian kecil) |
| **Penulis** | @username |
| **Status** | Draf · Final |

> **Blameless:** fokus pada *sistem dan proses* yang memungkinkan kesalahan terjadi, bukan pada *siapa* yang salah.

## 1. Ringkasan
<!-- 2–3 kalimat: apa yang terjadi, dampaknya, bagaimana diselesaikan. -->

## 2. Dampak
- Pengguna terdampak: ... (± ... %)
- Fitur terdampak: ...
- Data hilang/rusak: ya / tidak

## 3. Kronologi
| Waktu | Kejadian |
|---|---|
| 08:00 | Rilis v1.4.0 (OTA) ke channel production |
| 08:12 | Sentry: lonjakan crash `TypeError ...` di Android 10 |
| 08:15 | ... |
| 08:31 | Rollback ke update sebelumnya |
| 08:40 | Crash-free rate kembali normal |

## 4. Akar Masalah
<!-- Gunakan "5 Whys": kenapa → kenapa → kenapa ... sampai ke akar proses. -->
1. Kenapa aplikasi crash? ...
2. Kenapa ...? ...
3. Kenapa ...? ...

## 5. Apa yang Berjalan Baik
- ...

## 6. Apa yang Perlu Diperbaiki
- ...

## 7. Tindak Lanjut
| Aksi | Jenis | Pemilik | Target |
|---|---|---|---|
| Tambah E2E untuk alur X | Pencegahan | @... | YYYY-MM-DD |
| Rilis OTA ke preview dulu minimal 1 hari | Proses | @... | ... |
| Alert Sentry untuk lonjakan crash | Deteksi | @... | ... |

## 8. Pelajaran
<!-- Apa yang akan Anda lakukan berbeda? -->
