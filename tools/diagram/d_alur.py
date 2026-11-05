"""Diagram alur: autentikasi, check-in, notifikasi & realtime, offline sync, CI/CD."""

from lib import MUTED, TEKS, TEMA, Sekuens, Svg, bungkus, lebar_teks


def _bagian(q: Sekuens, label: str, tema: str, langkah: list, xl: float, xr: float):
    """Gambar bingkai bagian lalu pesan-pesannya. langkah: (dari, ke, label, balas[, warna])."""
    tinggi = 18
    for l in langkah:
        if l[0] == "catat":
            tinggi += 16 * len(bungkus(l[2], 210, 11.5)) + 26
        else:
            tinggi += 46 if l[0] == l[1] else 36
    q.blok(label, tinggi, xl, xr, tema=tema)
    q.jeda(8)
    for l in langkah:
        if l[0] == "catat":
            q.catatan(l[1], l[2], tema=l[3] if len(l) > 3 else "warn")
            continue
        dari, ke, teks, balas, *rest = l
        q.pesan(dari, ke, teks, balas=balas, warna=rest[0] if rest else None)
    q.jeda(22)


def alur_auth():
    s = Svg(1240, 1040, "Alur Autentikasi: Sanctum Token + Expo",
            "Tiga skenario yang wajib benar: aplikasi dibuka, login, dan token dicabut (401).")
    q = Sekuens(s, [("u", "Karyawan", "netral"), ("app", "Aplikasi (RN)", "mobile"),
                    ("ss", "SecureStore", "data"), ("api", "Laravel API", "backend"), ("db", "Database", "data")],
                120, 1120, 96, lebar_kotak=160)
    xl, xr = 40, 1200
    merah = TEMA["danger"].stroke
    hijau = TEMA["data"].stroke

    _bagian(q, "1  APLIKASI DIBUKA", "mobile", [
        ("app", "ss", "getItem('auth_token')", False),
        ("ss", "app", "token (atau null → layar Login)", True),
        ("app", "api", "GET /api/v1/auth/me   Authorization: Bearer <token>", False),
        ("api", "db", "cek personal_access_tokens", False),
        ("api", "app", "200 { data: user }", True, hijau),
        ("app", "app", "status = 'authenticated' → Beranda", False),
    ], xl, xr)

    _bagian(q, "2  LOGIN", "teal", [
        ("u", "app", "isi email + password", False),
        ("app", "api", "POST /auth/login { email, password, device_name }", False),
        ("api", "db", "cek hash password · buat token (30 hari)", False),
        ("api", "app", "200 { data: { token, user } }", True, hijau),
        ("app", "ss", "setItem('auth_token', token)", False),
        ("app", "api", "POST /devices { push_token }  (daftarkan notifikasi)", False),
    ], xl, xr)

    _bagian(q, "3  TOKEN DICABUT ADMIN / KEDALUWARSA", "danger", [
        ("app", "api", "GET /attendances/today", False),
        ("api", "app", "401 { code: 'UNAUTHENTICATED' }", True, merah),
        ("app", "app", "interceptor → signOut() (hanya SEKALI walau ada 3 request)", False),
        ("app", "ss", "deleteItem('auth_token')", False),
        ("app", "app", "queryClient.clear() → layar Login", False),
    ], xl, xr)

    q.tutup(q.y - 10)
    s.catatan(40, q.y - 2, 1160, "Pengecualian: 401 dari /auth/login berarti password salah, BUKAN sesi berakhir, "
              "jadi interceptor tidak boleh memicu logout global untuk endpoint itu.", tema="warn", size=12)
    s.h = int(q.y + 60)
    return "alur-autentikasi.svg", s


def alur_checkin():
    s = Svg(1280, 1020, "Alur Absen Masuk (Check-in) End-to-End",
            "Cek jarak di HP hanya untuk UX. Keputusan akhir selalu di SERVER, karena aplikasi mobile tidak bisa dipercaya.")
    q = Sekuens(s, [("u", "Karyawan", "netral"), ("app", "Aplikasi (RN)", "mobile"), ("dev", "GPS & Kamera", "teal"),
                    ("api", "Laravel API", "backend"), ("job", "Queue & Storage", "external"),
                    ("db", "Database", "data")], 110, 1170, 96, lebar_kotak=150)
    xl, xr = 36, 1244
    merah = TEMA["danger"].stroke
    hijau = TEMA["data"].stroke

    _bagian(q, "DI HP", "mobile", [
        ("u", "app", "tap 'Absen Masuk'", False),
        ("app", "dev", "minta izin lokasi → getCurrentPosition", False),
        ("dev", "app", "lat, lng, accuracy", True),
        ("app", "app", "distanceMeters() → tampilkan jarak (UX saja)", False),
        ("app", "dev", "buka kamera depan", False),
        ("dev", "app", "foto selfie (~4 MB)", True),
        ("app", "app", "kompres & resize → ~200 KB", False),
    ], xl, xr)

    _bagian(q, "KIRIM KE SERVER", "backend", [
        ("app", "api", "POST /attendances/check-in  (multipart + Idempotency-Key)", False),
        ("api", "api", "FormRequest: validasi · hitung geofence di server", False),
    ], xl, xr)

    _bagian(q, "ALT: DI LUAR RADIUS / SUDAH ABSEN", "danger", [
        ("api", "app", "422 { code: 'OUTSIDE_GEOFENCE', meta: { distance_meters: 340 } }", True, merah),
    ], xl, xr)

    _bagian(q, "ALT: VALID", "data", [
        ("api", "job", "simpan foto ke storage privat", False),
        ("api", "db", "INSERT attendance (check_in_at = waktu SERVER)", False),
        ("api", "job", "dispatch GenerateThumbnail (afterCommit)", False),
        ("api", "app", "201 { data: { status: 'on_time', ... } }", True, hijau),
        ("app", "app", "setQueryData(today) → layar Sukses + haptic", False),
    ], xl, xr)
    q.tutup(q.y - 10)
    s.h = int(q.y + 10)
    return "alur-checkin.svg", s


def notifikasi_realtime():
    s = Svg(1240, 860, "Push Notification vs Realtime (WebSocket)",
            "Contoh: admin menyetujui izin. Dua jalur dipakai bersamaan, tergantung apakah aplikasi sedang dibuka.")

    # Pemicu
    s.kotak(470, 100, 300, 64, "Admin menyetujui izin", "di Filament (web)", tema="netral")
    s.kotak(470, 196, 300, 64, "event LeaveRequestStatusChanged", "Laravel Event", tema="backend", judul_size=13)
    s.panah(620, 164, 620, 196)

    def kolom(x, judul, sub, tema, langkah):
        s.grup(x, 300, 520, 530, judul, tema=tema)
        s.teks(x + 260, 336, sub, size=12.5, warna=MUTED, anchor="middle")
        y = 356
        for i, (j, isi, tm) in enumerate(langkah):
            s.kotak(x + 60, y, 420, 58, j, isi, tema=tm, judul_size=13, isi_size=11.5)
            s.nomor(x + 36, y + 29, i + 1, tema=tema)
            if i < len(langkah) - 1:
                s.panah(x + 270, y + 58, x + 270, y + 74)
            y += 74

    kolom(40, "APLIKASI DITUTUP / DI BACKGROUND", "→ Push notification", "external", [
        ("Job SendPushNotification masuk queue", "jangan kirim di dalam request (lambat)", "backend"),
        ("Expo Push API → FCM (Android) / APNs (iOS)", "pakai token dari tabel device_tokens", "external"),
        ("Notifikasi muncul di HP", "\"Pengajuan izin Anda disetujui\"", "external"),
        ("User tap notifikasi", "data: { url: 'absensi://izin/31' }", "mobile"),
        ("Deep link membuka layar detail izin", "Expo Router: app/(app)/izin/[id].tsx", "mobile"),
        ("Data diambil ulang", "useQuery(['leave','detail',31])", "mobile"),
    ])
    kolom(680, "APLIKASI SEDANG DIBUKA", "→ WebSocket (Laravel Reverb)", "backend", [
        ("Event ShouldBroadcast", "channel privat: private-user.7", "backend"),
        ("Reverb mengirim lewat WebSocket", "otorisasi channel pakai token Sanctum", "backend"),
        ("Laravel Echo di aplikasi menerima event", "listener terdaftar saat login", "mobile"),
        ("invalidateQueries(['leave'])", "atau setQueryData untuk update instan", "mobile"),
        ("UI langsung berubah", "badge 'Menunggu' → 'Disetujui'", "mobile"),
        ("Reconnect saat kembali dari background", "AppState 'active' → echo.connect()", "warn"),
    ])
    s.panah(540, 260, 420, 300, "", warna=TEMA["external"].stroke)
    s.panah(700, 260, 1000, 300, "", warna=TEMA["backend"].stroke)
    return "notifikasi-realtime.svg", s


def _ketupat(s: Svg, cx, cy, w, h, teks, tema="warn"):
    t = TEMA[tema]
    s.path(f"M {cx} {cy - h / 2} L {cx + w / 2} {cy} L {cx} {cy + h / 2} L {cx - w / 2} {cy} Z",
           warna=t.stroke, fill=t.fill, sw=1.6)
    baris = bungkus(teks, w * 0.62, 12.5, True)
    y0 = cy - (len(baris) - 1) * 8 + 4
    for i, b in enumerate(baris):
        s.teks(cx, y0 + i * 16, b, size=12.5, bold=True, warna=t.text, anchor="middle")


def offline_outbox():
    s = Svg(1240, 900, "Offline-First dengan Pola Outbox (Fase 4)",
            "Aksi user disimpan dulu di HP, lalu dikirim saat online. Idempotency-Key mencegah data ganda.")

    s.grup(40, 110, 560, 760, "DI HP", tema="mobile")
    s.grup(660, 110, 540, 760, "DI SERVER (Laravel)", tema="backend")

    # HP
    s.kotak(80, 140, 480, 58, "User tap 'Absen Masuk' (sedang offline)", tema="netral")
    s.kotak(80, 226, 480, 78, "Simpan ke tabel outbox (SQLite)",
            "id = UUID (= Idempotency-Key) · type = check_in · payload · file_uri foto · status = pending",
            tema="data", judul_size=13.5)
    s.kotak(80, 332, 480, 58, "UI: \"Tersimpan, menunggu sinkronisasi\"", tema="mobile")
    s.panah(320, 198, 320, 226)
    s.panah(320, 304, 320, 332)

    s.kotak(80, 420, 480, 96, "Pemicu sync engine",
            "aplikasi dibuka · koneksi kembali (NetInfo) · interval berkala · background task (dibatasi OS)",
            tema="teal", judul_size=13.5)
    s.panah(320, 390, 320, 420)
    s.kotak(80, 546, 480, 58, "Ambil item pending tertua → status = sending", tema="mobile", judul_size=13)
    s.panah(320, 516, 320, 546)
    s.kotak(80, 634, 480, 58, "POST /attendances/check-in  +  Idempotency-Key", tema="mobile", judul_size=13)
    s.panah(320, 604, 320, 634)

    # hasil
    s.kotak(80, 760, 140, 80, "2xx", "status = done · refresh cache", tema="data", judul_size=13, isi_size=11)
    s.kotak(240, 760, 150, 80, "Jaringan / 5xx", "attempts++ · tunggu (backoff) · ulangi", tema="warn",
            judul_size=13, isi_size=11)
    s.kotak(410, 760, 150, 80, "4xx", "status = failed · tampilkan ke user", tema="danger", judul_size=13,
            isi_size=11)
    s.panah(320, 692, 150, 760, via=[(320, 726), (150, 726)])
    s.panah(320, 692, 315, 760)
    s.panah(320, 692, 485, 760, via=[(320, 726), (485, 726)])
    s.path("M 315 840 L 315 856 L 60 856 L 60 575 L 80 575", warna=TEMA["warn"].stroke, panah=True, dash="5 4")
    s.label(66, 700, "ulangi", warna=TEMA["warn"].stroke, anchor="start")

    # server
    s.panah(560, 663, 700, 190, "", warna="#334155", via=[(620, 663), (620, 190)])
    s.label(626, 420, "request", warna="#334155", anchor="start")
    s.kotak(700, 140, 460, 100, "Middleware EnsureIdempotency",
            "cari key di tabel idempotency_keys (per user)", tema="backend")
    _ketupat(s, 930, 330, 300, 120, "Key sudah pernah diproses?")
    s.panah(930, 240, 930, 270)

    s.kotak(700, 440, 210, 110, "Belum", "kunci key → jalankan CheckInAction → simpan response ke tabel",
            tema="data", judul_size=13, isi_size=11.5)
    s.kotak(950, 440, 210, 110, "Sudah", "kembalikan response yang TERSIMPAN (tanpa membuat data baru)",
            tema="warn", judul_size=13, isi_size=11.5)
    s.panah(860, 352, 805, 440, "tidak", lpos=0.4, ldx=-14)
    s.panah(1000, 352, 1055, 440, "ya", lpos=0.4, ldx=14)

    s.kotak(700, 590, 460, 96, "Waktu klien vs waktu server",
            "simpan check_in_client_at (jam HP) DAN check_in_at (jam server). Selisih besar → tandai untuk diaudit.",
            tema="netral", judul_size=13)
    s.catatan(700, 712, 460, "Hasilnya: request yang terkirim 3x (sinyal putus-sambung) tetap menghasilkan TEPAT "
              "1 data absensi.", tema="warn", size=12.5)
    return "offline-outbox.svg", s


def cicd():
    s = Svg(1280, 760, "Alur Rilis: Dari Kode ke Tangan Pengguna",
            "Setiap perubahan lewat PR + CI. Perubahan JS saja bisa dikirim lewat OTA; perubahan native butuh build baru.")

    langkah = [
        ("Branch fitur", "feat/check-in-offline", "netral"),
        ("Pull Request", "review + deskripsi", "mobile"),
        ("CI (GitHub Actions)", "lint · tsc · jest · pest", "teal"),
        ("Merge ke main", "branch protection", "mobile"),
    ]
    x = 40
    for i, (j, isi, tema) in enumerate(langkah):
        s.kotak(x, 120, 200, 70, j, isi, tema=tema, judul_size=13.5)
        if i < len(langkah) - 1:
            s.panah(x + 200, 155, x + 230, 155)
        x += 230
    s.label(500, 214, "CI merah → tidak bisa merge", warna=TEMA["danger"].stroke)
    s.path("M 600 190 L 600 222 L 300 222 L 300 190", warna=TEMA["danger"].stroke, dash="5 4", panah=True)

    _ketupat(s, 1100, 155, 220, 120, "Ada perubahan native? (fingerprint)")
    s.panah(960, 155, 990, 155)

    # Jalur OTA
    s.grup(40, 290, 580, 300, "JALUR A · HANYA JS / ASET  →  OTA UPDATE", tema="teal")
    ota = [
        ("eas update --channel preview", "tester menerima update", "teal"),
        ("Uji di build preview", "cek Sentry, coba alur kritis", "netral"),
        ("eas update --channel production", "user menerima saat buka app", "teal"),
    ]
    for i, (j, isi, tm) in enumerate(ota):
        s.kotak(80, 330 + i * 84, 500, 62, j, isi, tema=tm, judul_size=13, mono_isi=False)
        if i < 2:
            s.panah(330, 392 + i * 84, 330, 414 + i * 84)
    s.panah(1100, 215, 620, 360, "", warna=TEMA["teal"].stroke, via=[(1100, 240), (650, 240), (650, 360)])
    s.label(870, 234, "tidak → OTA", warna=TEMA["teal"].stroke)

    # Jalur build
    s.grup(660, 290, 580, 300, "JALUR B · ADA PERUBAHAN NATIVE  →  BUILD BARU", tema="backend")
    build = [
        ("eas build --profile production", "versionCode otomatis naik", "backend"),
        ("eas submit → Play Console", "Internal → Closed testing", "backend"),
        ("Staged rollout 5% → 20% → 50% → 100%", "naikkan bertahap sambil memantau crash-free rate", "warn"),
    ]
    for i, (j, isi, tm) in enumerate(build):
        s.kotak(700, 330 + i * 84, 500, 62, j, isi, tema=tm, judul_size=13)
        if i < 2:
            s.panah(950, 392 + i * 84, 950, 414 + i * 84)
    s.panah(1210, 155, 1150, 290, "", warna=TEMA["backend"].stroke, via=[(1258, 155), (1258, 262), (1150, 262)])
    s.label(1232, 147, "ya", warna=TEMA["backend"].stroke)

    # Monitoring
    s.kotak(360, 630, 560, 90, "Pantau dengan Sentry", "crash-free rate · error baru · performa layar · per versi rilis",
            tema="external")
    s.panah(330, 590, 500, 630, warna=TEMA["external"].stroke)
    s.panah(950, 590, 780, 630, warna=TEMA["external"].stroke)
    s.kotak(40, 640, 280, 70, "Masalah di OTA?", "republish update sebelumnya (rollback)", tema="danger",
            judul_size=13)
    s.kotak(960, 640, 280, 70, "Masalah di build?", "hentikan rollout + hotfix", tema="danger", judul_size=13)
    s.panah(360, 675, 320, 675, warna=TEMA["danger"].stroke, dash="5 4")
    s.panah(920, 675, 960, 675, warna=TEMA["danger"].stroke, dash="5 4")
    return "alur-rilis-cicd.svg", s


SEMUA = [alur_auth, alur_checkin, notifikasi_realtime, offline_outbox, cicd]
