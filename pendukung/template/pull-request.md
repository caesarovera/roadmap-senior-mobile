<!--
Simpan file ini sebagai .github/pull_request_template.md di repo proyek Anda.
GitHub akan otomatis mengisinya setiap kali PR dibuat.
-->

## Apa yang Berubah

<!-- Ringkasan 1–3 kalimat. -->

## Kenapa

<!-- Masalah / issue yang diselesaikan. Tautkan issue: Closes #123 -->

## Tangkapan Layar / Video

| Sebelum | Sesudah |
|---|---|
| | |

## Cara Menguji

1. ...
2. ...

## Checklist

- [ ] Lint & typecheck lulus (`npm run lint`, `npx tsc --noEmit`)
- [ ] Test ditambahkan/diperbarui dan lulus
- [ ] Diuji di HP Android asli
- [ ] Mode gelap & ukuran layar kecil sudah dicek
- [ ] State loading / kosong / error ditangani
- [ ] Tidak ada rahasia (API key, password) di kode
- [ ] Butuh perubahan native? → **build baru**, bukan OTA
- [ ] Kontrak API berubah? → backend & mobile sudah disesuaikan, dan versi lama tetap jalan
- [ ] Dokumentasi / ADR diperbarui bila perlu
