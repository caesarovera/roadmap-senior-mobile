"""Diagram arsitektur: gambaran sistem, layer mobile, request Laravel, peta state, ERD."""

from lib import MUTED, TEKS, TEMA, Svg, lebar_teks


def sistem():
    s = Svg(1280, 820, "Gambaran Sistem: Aplikasi Absensi",
            "Aplikasi mobile React Native berbicara dengan backend Laravel lewat REST API, WebSocket, dan push notification.")

    # Pengguna
    s.kotak(40, 110, 170, 58, "Karyawan", "pakai HP Android/iOS", tema="netral", judul_size=14)
    s.kotak(690, 110, 170, 58, "Admin / HR", "pakai browser", tema="netral", judul_size=14)

    # ---- Mobile ----
    s.grup(40, 210, 380, 470, "APLIKASI MOBILE  ·  React Native + Expo", tema="mobile")
    s.kotak(64, 240, 332, 66, "Layar (Expo Router)", "Beranda · Absen · Riwayat · Izin · Profil", tema="mobile")
    s.kotak(64, 322, 160, 78, "Server state", "TanStack Query (cache API)", tema="mobile", judul_size=13)
    s.kotak(236, 322, 160, 78, "Client state", "Zustand (sesi, tema)", tema="mobile", judul_size=13)
    s.kotak(64, 416, 332, 58, "Lapisan API", "Axios + interceptor · validasi Zod", tema="mobile", judul_size=13)
    s.kotak(64, 490, 160, 84, "Penyimpanan lokal", "SecureStore (token) · MMKV · SQLite", tema="data", judul_size=13)
    s.kotak(236, 490, 160, 84, "Fitur perangkat", "Kamera · GPS · Notifikasi · Haptics", tema="teal", judul_size=13)
    s.kotak(64, 590, 332, 66, "Native module (Fase 4)", "Deteksi fake GPS · Kotlin / Swift", tema="pink", judul_size=13)

    # ---- Backend ----
    s.grup(500, 210, 380, 470, "BACKEND  ·  Laravel", tema="backend")
    s.kotak(524, 240, 160, 70, "Reverb", "WebSocket realtime", tema="backend", judul_size=13)
    s.kotak(696, 240, 160, 70, "Filament", "panel admin web", tema="backend", judul_size=13)
    s.kotak(524, 326, 332, 90, "REST API  /api/v1", "Sanctum (token) · Form Request · Action · API Resource · Policy",
            tema="backend")
    s.kotak(524, 432, 160, 70, "Scheduler", "pengingat absen, tandai alpha", tema="backend", judul_size=13)
    s.kotak(696, 432, 160, 70, "Queue worker", "thumbnail foto, kirim push", tema="backend", judul_size=13)
    s.kotak(524, 518, 332, 138, "Aturan bisnis di server", "Geofence dihitung di SERVER · waktu absen = waktu "
            "server · satu absen per hari · validasi kuota cuti · otorisasi per data (Policy)", tema="warn",
            judul_size=13, rata="kiri")

    # ---- Data ----
    s.grup(960, 210, 280, 330, "DATA", tema="data")
    s.kotak(984, 240, 232, 70, "MySQL / PostgreSQL", "users, attendances, leave_requests", tema="data", judul_size=13)
    s.kotak(984, 326, 232, 70, "Redis", "antrean queue · cache · rate limit", tema="data", judul_size=13)
    s.kotak(984, 412, 232, 100, "Object storage", "foto selfie & lampiran (privat) · S3 / R2 / disk lokal",
            tema="data", judul_size=13)

    # ---- Eksternal ----
    s.grup(40, 720, 1200, 80, "LAYANAN EKSTERNAL", tema="external")
    for i, (j, isi) in enumerate([
        ("Expo Push / FCM / APNs", "kirim notifikasi ke HP"),
        ("EAS Build · Update", "build APK/AAB, OTA"),
        ("Sentry", "crash & performa"),
        ("Google Play", "distribusi aplikasi"),
        ("GitHub Actions", "CI: lint, test"),
    ]):
        s.kotak(64 + i * 236, 738, 216, 48, j, isi, tema="external", judul_size=12.5, isi_size=11)

    # ---- Panah ----
    s.panah(125, 168, 125, 222, warna=TEMA["mobile"].stroke)
    s.panah(775, 168, 775, 240, warna=TEMA["backend"].stroke)

    s.panah(396, 436, 524, 362, "HTTPS + Bearer token", warna="#334155", lpos=0.42, ldy=-12)
    s.panah(524, 392, 396, 458, "", warna="#94A3B8", dash="6 4")
    s.label(470, 445, "JSON", warna=MUTED)
    s.panah(524, 275, 396, 350, "", warna=TEMA["backend"].stroke, dash="6 4")
    s.label(462, 282, "event realtime", warna=TEMA["backend"].stroke)

    s.panah(856, 352, 984, 278, "SQL", warna=TEMA["data"].stroke, ldy=-4)
    s.panah(856, 398, 984, 460, "simpan foto", warna=TEMA["data"].stroke, lpos=0.5, ldy=-6)

    s.panah(856, 467, 250, 738, "", warna=TEMA["external"].stroke, via=[(912, 467), (912, 700), (250, 700)])
    s.label(560, 696, "push notification (lewat queue)", warna=TEMA["external"].stroke)

    s.legenda(960, 572, [("mobile", "Mobile"), ("backend", "Backend")])
    s.legenda(960, 600, [("data", "Data"), ("external", "Eksternal")])
    s.legenda(960, 628, [("warn", "Aturan penting"), ("pink", "Fase 4")])
    return "sistem-gambaran.svg", s


def layer_mobile():
    s = Svg(1180, 760, "Arsitektur Aplikasi Mobile: Berbasis Fitur & Berlapis",
            "Setiap fitur punya folder sendiri. Di dalam fitur, kode dibagi per lapisan, dan dependency hanya boleh mengarah ke bawah.")

    # kiri: lapisan
    lap = [
        ("app/  (routing)", "File tipis: hanya me-re-export screen dari fitur", "netral"),
        ("Screen & Komponen", "Menampilkan data & menangani interaksi. Tidak ada logika bisnis.", "mobile"),
        ("Hooks fitur", "useCheckIn, useHistory: menggabungkan query/mutation + logika UI", "mobile"),
        ("API / Repository", "Panggilan HTTP (Axios) atau DB lokal (SQLite) + validasi Zod", "teal"),
        ("Domain", "Fungsi MURNI: hitung jarak, status terlambat. Tanpa React, mudah dites.", "data"),
    ]
    y = 110
    for i, (j, isi, tema) in enumerate(lap):
        s.kotak(40, y, 480, 82, j, isi, tema=tema, rata="kiri", judul_size=14.5, isi_size=12.5)
        if i < len(lap) - 1:
            s.panah(280, y + 82, 280, y + 104, warna="#475569")
        y += 104
    s.label(560, 128, "memanggil", warna=MUTED, anchor="start", bg=False)
    s.path("M 540 140 L 540 600", warna="#475569", sw=2, panah=True)
    s.teks(552, 380, "dependency", size=12, warna=MUTED)
    s.teks(552, 396, "hanya ke bawah", size=12, warna=MUTED)

    # infrastruktur bersama
    s.kotak(40, 640, 480, 90, "Shared: lib/ · components/ui/ · theme/ · utils/",
            "api client, query client, storage, Button/Card/Input, design tokens, format Rupiah & tanggal",
            tema="external", rata="kiri", judul_size=13.5)

    # kanan: struktur folder
    s.grup(680, 110, 460, 620, "src/features/attendance/", tema="mobile")
    baris = [
        ("index.ts", "PUBLIC API fitur: satu-satunya pintu masuk", "warn"),
        ("screens/", "CheckInScreen, HistoryScreen", "mobile"),
        ("components/", "CheckInButton, AttendanceCard", "mobile"),
        ("hooks.ts", "useTodayAttendance, useCheckIn", "mobile"),
        ("api.ts", "getToday(), checkIn(form)", "teal"),
        ("schema.ts", "Zod schema + tipe Attendance", "teal"),
        ("domain/geofence.ts", "distanceMeters(), isWithinRadius()", "data"),
        ("domain/*.test.ts", "unit test fungsi murni", "data"),
    ]
    for i, (f, ket, tema) in enumerate(baris):
        yy = 142 + i * 62
        t = TEMA[tema]
        s.rect(704, yy, 412, 50, fill=t.fill, stroke=t.stroke, sw=1.2, r=8)
        s.teks(720, yy + 21, f, size=13, bold=True, warna=t.text, mono=True)
        s.teks(720, yy + 39, ket, size=11.5, warna=TEKS)

    # aturan
    s.catatan(704, 650, 412, "Fitur lain hanya boleh: import { useCheckIn } from '@/features/attendance'. "
              "Dilarang import file internal fitur lain. Aturan ini ditegakkan dengan ESLint.", tema="warn", size=11.5)
    return "mobile-layer.svg", s


def laravel_request():
    s = Svg(1280, 560, "Perjalanan Satu Request di Laravel",
            "Contoh: POST /api/v1/attendances/check-in. Setiap tahap punya satu tanggung jawab.")
    tahap = [
        ("Route", "routes/api.php\nprefix v1", "netral"),
        ("Middleware", "auth:sanctum\nthrottle:api", "backend"),
        ("Form Request", "CheckInRequest\nvalidasi + authorize", "backend"),
        ("Controller", "CheckInController\n(tipis, __invoke)", "backend"),
        ("Action", "CheckInAction\nlogika bisnis", "warn"),
        ("Model", "Attendance\nEloquent + DB", "data"),
        ("Resource", "AttendanceResource\nbentuk JSON", "mobile"),
    ]
    w, gap, x, y = 152, 24, 40, 140
    for i, (j, isi, tema) in enumerate(tahap):
        s.kotak(x, y, w, 96, j, isi, tema=tema, judul_size=14, isi_size=11.5)
        s.nomor(x + 14, y + 14, i + 1, tema=tema if tema != "netral" else "mobile", r=10)
        if i < len(tahap) - 1:
            s.panah(x + w, y + 48, x + w + gap, y + 48, warna="#475569")
        x += w + gap

    # gagal di tiap tahap
    gagal = [
        (1, "401 UNAUTHENTICATED\n429 Too Many Requests"),
        (2, "422 errors per field\n403 tidak berhak"),
        (4, "422 OUTSIDE_GEOFENCE\n422 ALREADY_CHECKED_IN"),
    ]
    for idx, teks in gagal:
        cx = 40 + idx * (w + gap) + w / 2
        s.panah(cx, 236, cx, 290, warna=TEMA["danger"].stroke, dash="5 4")
        s.kotak(cx - 84, 292, 168, 62, "Respons error", teks, tema="danger", judul_size=12, isi_size=10.5)

    s.panah(1172, 236, 1172, 410, "", warna=TEMA["mobile"].stroke)
    s.kotak(960, 410, 280, 84, "201 Created", '{ "data": {\n"id": 120, "status": "on_time"\n} }', tema="mobile",
            judul_size=13, isi_size=11, mono_isi=True)

    s.catatan(40, 400, 880, "Semua error melewati satu tempat: bootstrap/app.php (withExceptions), sehingga "
              "aplikasi mobile SELALU menerima format JSON yang sama: { message, code, errors, meta }. "
              "Aplikasi membaca `code`, bukan teks `message`, untuk menentukan reaksi.", tema="warn", size=12.5)
    s.catatan(40, 476, 880, "Kenapa logika di Action, bukan di Controller? Action bisa dipanggil dari tempat lain "
              "(command, job, test) dan mudah diuji sendiri.", tema="netral", size=12.5)
    return "laravel-request.svg", s


def peta_state():
    s = Svg(1200, 760, "Peta State: Data Ini Disimpan di Mana?",
            "Salah memilih tempat penyimpanan adalah sumber bug paling umum. Gunakan pertanyaan di kiri untuk memutuskan.")

    # pohon keputusan
    def tanya(x, y, teks):
        s.kotak(x, y, 250, 56, teks, tema="netral", judul_size=13)

    tanya(40, 110, "Datanya berasal dari server?")
    tanya(40, 230, "Rahasia? (token, kredensial)")
    tanya(40, 350, "Banyak, terstruktur, atau perlu offline?")
    tanya(40, 470, "Perlu bertahan setelah app ditutup?")

    tujuan = [
        (110, "TanStack Query", "Cache data API: profil, absensi hari ini, riwayat, daftar izin", "mobile"),
        (230, "expo-secure-store", "Terenkripsi (Keychain / Keystore). Hanya untuk data kecil yang rahasia.", "danger"),
        (350, "SQLite", "Tabel + query + index. Fondasi offline-first & antrean outbox (Fase 4).", "data"),
        (470, "MMKV (+ Zustand persist)", "Preferensi: tema, bahasa, onboarding sudah dilihat", "teal"),
        (590, "Zustand / useState", "State UI sementara: status sesi, modal terbuka, draft form", "external"),
    ]
    for y, j, isi, tema in tujuan:
        s.kotak(420, y, 330, 72, j, isi, tema=tema, rata="kiri", judul_size=13.5, isi_size=11.5)

    for y in (110, 230, 350, 470):
        s.panah(290, y + 28, 420, y + 30, "Ya", warna=TEMA["data"].stroke, ldy=-8)
    for y in (110, 230, 350):
        s.panah(165, y + 56, 165, y + 120, "Tidak", warna=TEMA["danger"].stroke, ldx=24, ldy=4)
    s.panah(165, 526, 420, 626, "Tidak", warna=TEMA["danger"].stroke, via=[(165, 626)], lpos=0.2, ldx=26)

    # tabel contoh
    s.grup(800, 110, 360, 612, "CONTOH DI APLIKASI ABSENSI", tema="netral")
    rows = [
        ("Token login", "SecureStore", "danger"),
        ("Profil user", "Query", "mobile"),
        ("Absensi hari ini", "Query", "mobile"),
        ("Riwayat absensi", "Query (+ SQLite v3)", "mobile"),
        ("Absen saat offline", "SQLite (outbox)", "data"),
        ("Foto selfie belum terkirim", "FileSystem + SQLite", "data"),
        ("Status sesi (sudah login?)", "Zustand", "external"),
        ("Tema gelap/terang", "Zustand + MMKV", "teal"),
        ("Onboarding sudah dilihat", "MMKV", "teal"),
        ("Isi form izin yang belum dikirim", "React Hook Form", "external"),
    ]
    for i, (data, tempat, tema) in enumerate(rows):
        yy = 142 + i * 57
        s.rect(820, yy, 320, 42, fill="#FFFFFF", stroke="#E2E8F0", sw=1, r=8)
        s.teks(834, yy + 26, data, size=12, warna=TEKS)
        w = lebar_teks(tempat, 10.5, True) + 18
        s.pil(1130 - w, yy + 10, tempat, tema=tema, size=10.5)

    s.catatan(40, 690, 710, "Aturan emas: data dari server JANGAN disalin ke Zustand. Biarkan TanStack Query yang mengelolanya.",
              tema="warn", size=12)
    return "peta-state.svg", s


def erd():
    s = Svg(1240, 760, "Desain Database: Aplikasi Absensi",
            "PK = primary key · FK = foreign key · UQ = unique. Garis menunjukkan relasi satu-ke-banyak (1 ─< N).")

    def tabel(x, y, nama, kolom, tema, lebar=260):
        t = TEMA[tema]
        h = 40 + len(kolom) * 24 + 10
        s.rect(x, y, lebar, h, fill="#FFFFFF", stroke=t.stroke, sw=1.6, r=10)
        s.rect(x, y, lebar, 36, fill=t.stroke, stroke=t.stroke, sw=1.6, r=10)
        s.rect(x, y + 20, lebar, 16, fill=t.stroke, stroke="none", sw=0, r=0)
        s.teks(x + 14, y + 24, nama, size=14, bold=True, warna="#FFFFFF", mono=True)
        for i, (k, tipe, tag) in enumerate(kolom):
            yy = y + 60 + i * 24
            if i % 2 == 0:
                s.rect(x + 1.5, yy - 16, lebar - 3, 24, fill=t.fill, stroke="none", sw=0, r=0)
            s.teks(x + 14, yy, k, size=12, warna=TEKS, mono=True, bold=tag == "PK")
            s.teks(x + lebar - 14, yy, tipe, size=11, warna=MUTED, anchor="end", mono=True)
            if tag:
                warna = {"PK": "warn", "FK": "mobile", "UQ": "external"}[tag]
                s.pil(x + lebar - 14 - len(tipe) * 6.9 - 44, yy - 13, tag, tema=warna, size=9)
        return h

    tabel(40, 110, "offices", [
        ("id", "bigint", "PK"), ("name", "string", ""), ("latitude", "decimal", ""), ("longitude", "decimal", ""),
        ("radius_meters", "int", ""), ("timezone", "string", "")], "data")
    tabel(40, 330, "shifts", [
        ("id", "bigint", "PK"), ("name", "string", ""), ("start_time", "time", ""), ("end_time", "time", ""),
        ("late_tolerance_minutes", "int", ""), ("work_days", "json", "")], "data")
    tabel(490, 200, "users", [
        ("id", "bigint", "PK"), ("office_id", "bigint", "FK"), ("shift_id", "bigint", "FK"),
        ("employee_code", "string", "UQ"), ("name", "string", ""), ("email", "string", "UQ"),
        ("role", "enum", ""), ("is_active", "bool", ""), ("annual_leave_quota", "int", "")], "mobile", 270)
    tabel(940, 110, "attendances", [
        ("id", "bigint", "PK"), ("user_id", "bigint", "FK"), ("office_id", "bigint", "FK"), ("date", "date", ""),
        ("check_in_at", "timestamp", ""), ("check_in_distance", "int", ""), ("check_in_photo_path", "string", ""),
        ("check_out_at", "timestamp", ""), ("status", "enum", ""), ("is_mock_location", "bool", ""),
        ("idempotency_key", "uuid", "UQ")], "backend")
    tabel(940, 470, "leave_requests", [
        ("id", "bigint", "PK"), ("user_id", "bigint", "FK"), ("type", "enum", ""), ("start_date", "date", ""),
        ("end_date", "date", ""), ("status", "enum", ""), ("reviewed_by", "bigint", "FK")], "warn")
    tabel(490, 560, "device_tokens", [
        ("id", "bigint", "PK"), ("user_id", "bigint", "FK"), ("token", "string", "UQ"), ("platform", "enum", "")],
        "external", 270)

    def rel(x1, y1, x2, y2, via=None, label=""):
        s.panah(x1, y1, x2, y2, label, warna="#475569", via=via, lpos=0.5)

    rel(300, 160, 490, 268, via=[(400, 160), (400, 268)], label="1 ─< N")
    rel(300, 380, 490, 292, via=[(420, 380), (420, 292)], label="1 ─< N")
    rel(760, 245, 940, 196, via=[(850, 245), (850, 196)], label="1 ─< N")
    rel(760, 268, 940, 556, via=[(880, 268), (880, 556)], label="1 ─< N")
    rel(625, 446, 625, 560, label="1 ─< N")

    s.catatan(40, 560, 400, "UNIQUE(user_id, date) di attendances menegakkan aturan \"satu absen per hari\" "
              "langsung di level database, bukan hanya di kode.", tema="warn", size=12)
    s.catatan(40, 650, 400, "check_in_at = waktu SERVER. Waktu dari HP disimpan terpisah (check_in_client_at) "
              "hanya untuk audit, karena jam HP bisa diubah.", tema="netral", size=12)
    return "erd-absensi.svg", s


SEMUA = [sistem, layer_mobile, laravel_request, peta_state, erd]
