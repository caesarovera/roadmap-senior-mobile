# 03 — Konvensi API (Kontrak Mobile ↔ Laravel)

[← Kembali ke README](../README.md)

Dokumen ini adalah **kontrak** antara aplikasi mobile dan backend. Aplikasi mobile versi lama bisa tetap terpasang di HP user selama bertahun-tahun, jadi kontrak ini **tidak boleh diubah sembarangan**.

---

## 1. Dasar

| Aturan | Nilai |
|---|---|
| Base URL | `https://api.domain.com/api/v1` |
| Format | JSON (`Accept: application/json` wajib dikirim klien) |
| Nama field | `snake_case` |
| Tanggal + waktu | ISO 8601 dengan offset: `2026-11-05T08:01:23+07:00` |
| Tanggal saja | `YYYY-MM-DD` |
| Uang | Integer dalam satuan terkecil (rupiah): `1500000` |
| ID | Integer (atau ULID/UUID jika ID perlu dibuat di klien) |
| Boolean | `true`/`false` (bukan `1`/`0`) |
| Nilai kosong | `null` (field **tetap dikirim**, jangan dihilangkan) |

---

## 2. Header

### Dikirim klien
| Header | Contoh | Fungsi |
|---|---|---|
| `Authorization` | `Bearer 1\|abc...` | Token Sanctum |
| `Accept` | `application/json` | Memastikan Laravel membalas JSON |
| `Accept-Language` | `id` | Bahasa pesan error |
| `X-Platform` | `android` / `ios` | Analitik, debug |
| `X-App-Version` | `1.4.0` | Debug, dan force update |
| `Idempotency-Key` | UUID v4 | Wajib untuk aksi yang tidak boleh terduplikasi (check-in, pengajuan) |

---

## 3. Format Response Sukses

### Satu item
```json
{
  "data": {
    "id": 42,
    "date": "2026-11-05",
    "check_in_at": "2026-11-05T07:58:12+07:00",
    "check_out_at": null,
    "status": "on_time"
  }
}
```

### List dengan cursor pagination (`cursorPaginate`)
```json
{
  "data": [ { "id": 42 }, { "id": 41 } ],
  "links": {
    "first": null,
    "last": null,
    "prev": null,
    "next": "https://api.domain.com/api/v1/attendances?cursor=eyJpZCI6NDF9"
  },
  "meta": {
    "path": "https://api.domain.com/api/v1/attendances",
    "per_page": 20,
    "next_cursor": "eyJpZCI6NDF9",
    "prev_cursor": null
  }
}
```

Klien membaca `meta.next_cursor`; kalau nilainya `null`, berarti data sudah habis.

```ts
// Contoh di TanStack Query
useInfiniteQuery({
  queryKey: queryKeys.attendance.history(),
  queryFn: ({ pageParam }) => api.get('/attendances', { params: { cursor: pageParam } }).then(r => r.data),
  initialPageParam: null as string | null,
  getNextPageParam: (lastPage) => lastPage.meta.next_cursor,
});
```

### Aksi tanpa data
`204 No Content` (misalnya logout, hapus).

---

## 4. Format Response Error

**Semua error memiliki bentuk yang sama:**
```json
{
  "message": "Pesan yang aman ditampilkan ke user (Bahasa Indonesia).",
  "code": "KODE_MESIN",
  "errors": { },
  "meta": { }
}
```

| Field | Wajib | Keterangan |
|---|---|---|
| `message` | ✅ | Bisa langsung ditampilkan di UI |
| `code` | Untuk error bisnis | Untuk logika di klien (jangan parsing `message`!) |
| `errors` | Untuk 422 validasi | `{ "field": ["pesan", ...] }` (format bawaan Laravel) |
| `meta` | Opsional | Data tambahan, misalnya jarak user dari kantor |

### Contoh: validasi (422)
```json
{
  "message": "Foto selfie wajib diambil.",
  "errors": {
    "photo": ["Foto selfie wajib diambil."]
  }
}
```

### Contoh: error bisnis (422)
```json
{
  "message": "Anda berada di luar area kantor.",
  "code": "OUTSIDE_GEOFENCE",
  "meta": { "distance_meters": 340, "radius_meters": 100 }
}
```

### Status Code

| Kode | Arti | Reaksi di aplikasi |
|---|---|---|
| `200` | OK | |
| `201` | Data dibuat | |
| `204` | Sukses tanpa body | |
| `401` | Token tidak valid/kedaluwarsa | **Logout otomatis** → layar login |
| `403` | Tidak punya akses | Tampilkan pesan, jangan logout |
| `404` | Tidak ditemukan | Layar "data tidak ditemukan" |
| `409` | Konflik (misalnya idempotency key sedang diproses) | Retry sebentar lagi |
| `422` | Validasi / aturan bisnis | Tampilkan error per field atau pesan bisnis |
| `426` | Versi aplikasi terlalu lama | Layar **wajib update** |
| `429` | Terlalu banyak request | Tampilkan "coba lagi dalam X detik" (header `Retry-After`) |
| `500`–`503` | Error server | Pesan umum + retry; laporkan ke Sentry |
| *(tanpa response)* | Offline / timeout | Banner offline, simpan ke antrean (Fase 4) |

### Daftar Kode Error Bisnis

| `code` | Kapan |
|---|---|
| `UNAUTHENTICATED` | Token tidak valid |
| `INVALID_CREDENTIALS` | Email/password salah |
| `ACCOUNT_INACTIVE` | Akun dinonaktifkan admin |
| `ALREADY_CHECKED_IN` | Sudah absen masuk hari ini |
| `NOT_CHECKED_IN` | Mencoba absen pulang sebelum absen masuk |
| `OUTSIDE_GEOFENCE` | Di luar radius kantor |
| `MOCK_LOCATION_DETECTED` | Terdeteksi fake GPS (Fase 4) |
| `LEAVE_OVERLAP` | Tanggal izin bertabrakan dengan izin lain |
| `LEAVE_QUOTA_EXCEEDED` | Kuota cuti habis |
| `APP_VERSION_UNSUPPORTED` | Versi aplikasi di bawah minimum |

---

## 5. Aturan Perubahan API (Versioning)

### ✅ Boleh dilakukan di `v1` (tidak merusak aplikasi lama)
- Menambah endpoint baru
- Menambah field baru di response
- Menambah field **opsional** di request
- Menambah nilai enum baru (**dengan syarat** klien sudah menangani nilai yang tidak dikenal)

### ❌ Harus membuat `v2` (merusak aplikasi lama)
- Menghapus atau mengganti nama field
- Mengubah tipe field (string → object)
- Menambah field **wajib** di request
- Mengubah arti sebuah nilai

### Kebijakan Deprecation
1. Umumkan endpoint lama sebagai *deprecated* (header `Deprecation` + `Sunset`)
2. Pantau versi aplikasi yang masih memanggilnya (dari `X-App-Version` di log)
3. Naikkan `min_version` lewat endpoint config (force update)
4. Matikan endpoint lama setelah pemakaiannya mendekati nol

---

## 6. Endpoint Config (Fase 4)

`GET /api/v1/config`, dipanggil setiap aplikasi dibuka:
```json
{
  "data": {
    "min_version": { "android": "1.2.0", "ios": "1.2.0" },
    "latest_version": { "android": "1.5.0", "ios": "1.5.0" },
    "store_url": { "android": "https://play.google.com/store/apps/details?id=com.caesarovera.absensi" },
    "features": {
      "overtime": false,
      "offline_check_in": true
    },
    "maintenance": { "enabled": false, "message": null }
  }
}
```

---

[← Struktur Laravel](02-struktur-laravel-api.md) · [Lanjut → Alur Autentikasi](04-alur-autentikasi.md)
