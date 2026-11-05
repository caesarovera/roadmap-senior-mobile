# Proyek Absensi — 03. Spesifikasi API

[← Kembali ke README](../README.md) · [← Database](02-database.md)

Base URL: `/api/v1` · Semua mengikuti [Konvensi API](../arsitektur/03-konvensi-api.md) · 🔒 = butuh `Authorization: Bearer <token>`

## Ringkasan Endpoint

| Method | Endpoint | Auth | Versi | Fungsi |
|---|---|---|---|---|
| `POST` | `/auth/login` | | v1 | Login |
| `POST` | `/auth/logout` | 🔒 | v1 | Logout device ini |
| `GET` | `/auth/me` | 🔒 | v1 | Profil + kantor + shift |
| `PUT` | `/auth/password` | 🔒 | v1 | Ganti password |
| `GET` | `/attendances/today` | 🔒 | v1 | Absensi hari ini + info shift |
| `POST` | `/attendances/check-in` | 🔒 | v1 | Absen masuk |
| `POST` | `/attendances/check-out` | 🔒 | v1 | Absen pulang |
| `GET` | `/attendances` | 🔒 | v1 | Riwayat (cursor pagination) |
| `GET` | `/attendances/{id}` | 🔒 | v1 | Detail absensi |
| `GET` | `/attendances/summary` | 🔒 | v1 | Ringkasan per bulan |
| `GET` | `/leave-requests` | 🔒 | v1 | Daftar pengajuan |
| `POST` | `/leave-requests` | 🔒 | v1 | Ajukan izin/cuti |
| `GET` | `/leave-requests/{id}` | 🔒 | v1 | Detail pengajuan |
| `DELETE` | `/leave-requests/{id}` | 🔒 | v1 | Batalkan (hanya yang `pending`) |
| `GET` | `/leave-requests/quota` | 🔒 | v1 | Sisa kuota cuti |
| `POST` | `/devices` | 🔒 | v1 | Daftarkan push token |
| `DELETE` | `/devices/{token}` | 🔒 | v1 | Hapus push token |
| `GET` | `/config` | | v3 | Versi minimum, feature flag |
| `GET` | `/sync` | 🔒 | v3 | Delta sync untuk offline |

---

## Auth

### `POST /auth/login`

**Request**
```json
{
  "email": "karyawan@demo.test",
  "password": "password",
  "device_name": "Samsung SM-A546E (Android 14)"
}
```

**200 OK**
```json
{
  "data": {
    "token": "1|Xk9fA2...",
    "user": {
      "id": 7,
      "employee_code": "EMP-0007",
      "name": "Rina Lestari",
      "email": "karyawan@demo.test",
      "position": "Staf Toko",
      "avatar_url": null,
      "office": { "id": 1, "name": "Kantor Pusat Jakarta", "latitude": -6.175392, "longitude": 106.827153, "radius_meters": 100, "timezone": "Asia/Jakarta" },
      "shift": { "id": 1, "name": "Shift Pagi", "start_time": "08:00", "end_time": "17:00", "late_tolerance_minutes": 10 }
    }
  }
}
```

**Error:** `401 INVALID_CREDENTIALS` · `403 ACCOUNT_INACTIVE` · `422` validasi · `429`

### `POST /auth/logout` 🔒
**Request** (opsional): `{ "push_token": "ExponentPushToken[xxx]" }` → **204**

### `GET /auth/me` 🔒
**200:** `{ "data": <user seperti di atas> }`

### `PUT /auth/password` 🔒
```json
{ "current_password": "lama", "password": "baru12345", "password_confirmation": "baru12345" }
```
**204** · `422` jika password lama salah

---

## Absensi

### `GET /attendances/today` 🔒

**200**
```json
{
  "data": {
    "date": "2026-11-05",
    "is_work_day": true,
    "shift": { "name": "Shift Pagi", "start_time": "08:00", "end_time": "17:00" },
    "office": { "name": "Kantor Pusat Jakarta", "latitude": -6.175392, "longitude": 106.827153, "radius_meters": 100 },
    "attendance": {
      "id": 120,
      "check_in_at": "2026-11-05T07:58:12+07:00",
      "check_out_at": null,
      "status": "on_time",
      "distance_meters": 23
    },
    "leave": null,
    "can_check_in": false,
    "can_check_out": true
  }
}
```
`attendance` bernilai `null` kalau belum absen. `leave` terisi kalau hari ini sedang izin/cuti.

> Field `can_check_in` / `can_check_out` membuat aturan bisnis tetap di server. Aplikasi tidak perlu menebak.

### `POST /attendances/check-in` 🔒

**Header:** `Content-Type: multipart/form-data` · `Idempotency-Key: <uuid>` (wajib di v3)

| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `latitude` | number | ✅ | |
| `longitude` | number | ✅ | |
| `accuracy` | number | ✅ | Akurasi GPS dalam meter |
| `photo` | file | ✅ | JPEG, maksimal 2 MB |
| `client_recorded_at` | ISO 8601 | ✅ | Waktu di HP |
| `is_mock_location` | boolean | | v3 (dari native module) |

**201 Created**
```json
{
  "data": {
    "id": 120,
    "date": "2026-11-05",
    "check_in_at": "2026-11-05T07:58:12+07:00",
    "check_out_at": null,
    "status": "on_time",
    "distance_meters": 23,
    "check_in_photo_url": "https://.../selfie.jpg",
    "thumbnail_url": null,
    "work_duration_minutes": null
  }
}
```

**Error**
| Status | `code` | Kapan |
|---|---|---|
| 422 | `OUTSIDE_GEOFENCE` | `meta: { distance_meters, radius_meters }` |
| 422 | `ALREADY_CHECKED_IN` | |
| 422 | `NOT_WORK_DAY` | Hari libur sesuai shift |
| 422 | `ON_LEAVE` | Sedang izin/cuti yang disetujui |
| 422 | `MOCK_LOCATION_DETECTED` | v3 |
| 422 | *(tanpa code)* | Validasi field (`errors`) |
| 409 | `IDEMPOTENCY_IN_PROGRESS` | v3: request dengan key yang sama sedang diproses |

### `POST /attendances/check-out` 🔒
Field sama dengan check-in. **200** → attendance dengan `check_out_at` dan `work_duration_minutes` terisi.
Error: `NOT_CHECKED_IN`, `ALREADY_CHECKED_OUT`, `OUTSIDE_GEOFENCE`.

### `GET /attendances` 🔒

**Query:** `month=2026-11` (opsional) · `status=late` (opsional) · `cursor=...` · `per_page=20` (maks. 50)

**200:** list `AttendanceResource` + `links` + `meta.next_cursor` (lihat [konvensi pagination](../arsitektur/03-konvensi-api.md#list-dengan-cursor-pagination-cursorpaginate))

### `GET /attendances/{id}` 🔒
**200** · **403** jika milik orang lain (Policy) · **404**

### `GET /attendances/summary?month=2026-11` 🔒
```json
{
  "data": {
    "month": "2026-11",
    "work_days": 21,
    "present": 18,
    "on_time": 15,
    "late": 3,
    "leave": 2,
    "absent": 1,
    "total_work_minutes": 8640
  }
}
```

---

## Izin & Cuti

### `GET /leave-requests` 🔒
**Query:** `status=pending|approved|rejected|cancelled` · `cursor`

### `POST /leave-requests` 🔒

**Header:** `multipart/form-data` · `Idempotency-Key` (v3)

| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `type` | `sick` \| `permit` \| `annual_leave` | ✅ | |
| `start_date` | `YYYY-MM-DD` | ✅ | |
| `end_date` | `YYYY-MM-DD` | ✅ | ≥ `start_date` |
| `reason` | string | ✅ | 10–500 karakter |
| `attachment` | file | Wajib jika `sick` > 1 hari | Foto surat dokter |

**201**
```json
{
  "data": {
    "id": 31,
    "type": "annual_leave",
    "type_label": "Cuti Tahunan",
    "start_date": "2026-11-20",
    "end_date": "2026-11-21",
    "total_days": 2,
    "reason": "Acara keluarga di luar kota",
    "attachment_url": null,
    "status": "pending",
    "status_label": "Menunggu Persetujuan",
    "review_note": null,
    "reviewed_at": null,
    "created_at": "2026-11-05T10:12:00+07:00"
  }
}
```
**Error:** `422 LEAVE_OVERLAP` · `422 LEAVE_QUOTA_EXCEEDED` (`meta: { remaining, requested }`)

### `DELETE /leave-requests/{id}` 🔒
**204** · `422 LEAVE_NOT_CANCELLABLE` jika status bukan `pending`

### `GET /leave-requests/quota` 🔒
```json
{ "data": { "year": 2026, "quota": 12, "used": 4, "pending": 2, "remaining": 6 } }
```

---

## Device / Push

### `POST /devices` 🔒
```json
{ "token": "ExponentPushToken[xxxxxxxx]", "platform": "android", "device_name": "Samsung SM-A546E", "app_version": "1.0.0" }
```
**201**. Kalau token sudah ada, server **upsert** (pindahkan ke user ini dan perbarui `last_used_at`).

### `DELETE /devices/{token}` 🔒 → **204**

---

## Realtime (Reverb)

| Channel | Event | Payload | Penerima |
|---|---|---|---|
| `private-user.{id}` | `leave-request.status-changed` | `{ id, status, review_note }` | Karyawan pemilik |
| `private-office.{id}` | `attendance.checked-in` | `{ user_id, name, check_in_at, status }` | Admin (dashboard) |

Otorisasi channel di `routes/channels.php`:
```php
Broadcast::channel('user.{id}', fn ($user, $id) => (int) $user->id === (int) $id);
Broadcast::channel('office.{id}', fn ($user, $id) => $user->role === 'admin');
```

---

## v3: Sinkronisasi Offline

### `GET /sync?since=2026-11-01T00:00:00Z` 🔒
```json
{
  "data": {
    "server_time": "2026-11-05T03:15:00Z",
    "attendances": { "upserted": [ ], "deleted_ids": [ ] },
    "leave_requests": { "upserted": [ ], "deleted_ids": [ ] },
    "profile": { }
  }
}
```
Klien menyimpan `server_time` sebagai nilai `since` untuk sinkronisasi berikutnya. Gunakan waktu server, **bukan** waktu HP.

---

[← Database](02-database.md) · [Lanjut → Layar & Alur](04-layar-dan-alur.md)
