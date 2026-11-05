# RFC: [Nama Fitur / Perubahan]

| | |
|---|---|
| **Penulis** | @username |
| **Status** | Draf · Dalam review · Disetujui · Selesai |
| **Tanggal** | YYYY-MM-DD |
| **Reviewer** | @... |
| **Terkait** | Issue #..., ADR NNNN |

> Tulis RFC sebelum membangun fitur yang memakan lebih dari ±1 minggu, menyentuh banyak modul, atau sulit dibatalkan.
> Contoh nyata di roadmap: desain sinkronisasi offline (Fase 4, Blok C).

## 1. Ringkasan
<!-- 3–5 kalimat: apa yang dibangun dan kenapa. -->

## 2. Latar Belakang & Masalah
<!-- Apa yang terjadi sekarang? Siapa yang terdampak? Data/angka bila ada. -->

## 3. Tujuan & Bukan Tujuan
**Tujuan**
- ...

**Bukan tujuan** (sengaja tidak dikerjakan)
- ...

## 4. Ukuran Keberhasilan
| Metrik | Sekarang | Target |
|---|---|---|
| ... | ... | ... |

## 5. Desain yang Diusulkan

### 5.1 Gambaran umum
<!-- Tambahkan diagram (Excalidraw, Mermaid, atau SVG). -->

### 5.2 Perubahan di mobile
<!-- Layar, hooks, penyimpanan lokal, state. -->

### 5.3 Perubahan di backend
<!-- Endpoint baru/berubah, tabel, job, event. -->

### 5.4 Kontrak API
```json
// request / response contoh
```

### 5.5 Skema data
```sql
-- tabel / kolom baru
```

## 6. Alternatif yang Dipertimbangkan
| Alternatif | Kenapa tidak dipilih |
|---|---|
| ... | ... |

## 7. Risiko & Mitigasi
| Risiko | Mitigasi |
|---|---|
| ... | ... |

## 8. Keamanan & Privasi
<!-- Data sensitif apa yang terlibat? Siapa yang boleh mengakses? -->

## 9. Rencana Pengujian
- Unit: ...
- Component: ...
- E2E: ...
- Skenario manual: ...

## 10. Rencana Rilis
- [ ] Di balik feature flag?
- [ ] Butuh build baru atau cukup OTA?
- [ ] Butuh migrasi data?
- [ ] Rencana rollback

## 11. Pertanyaan Terbuka
- ...
