"""Diagram konsep belajar: timeline roadmap, event loop, thread RN, piramida testing, siklus TanStack Query."""

from lib import BG, MUTED, TEKS, TEMA, Svg, bungkus, lebar_teks


def timeline():
    s = Svg(1280, 600, "Peta Perjalanan 18 Bulan",
            "Setiap fase menghasilkan proyek nyata. Kebiasaan berkelanjutan dijalankan sepanjang jalan.")
    x0, x1 = 60, 1240
    minggu_total = 78
    px = (x1 - x0) / minggu_total

    def X(m):
        return x0 + m * px

    # sumbu bulan
    for b in range(0, 19):
        x = X(b * 78 / 18)
        s.garis(x, 120, x, 470, warna="#F1F5F9", sw=1)
        if b < 18:
            s.teks(X((b + 0.5) * 78 / 18), 116, f"B{b + 1}", size=11, warna=MUTED, anchor="middle")

    fase = [
        (0, 8, "Fase 0", "JS · TS · React", "Mini proyek katalog", "external"),
        (8, 18, "Fase 1", "Dasar React Native", "App keuangan offline", "mobile"),
        (18, 30, "Fase 2", "Aplikasi nyata + Laravel", "Absensi v1", "backend"),
        (30, 42, "Fase 3", "Kualitas · CI/CD · Rilis", "Rilis Google Play (v2)", "teal"),
        (42, 62, "Fase 4", "Topik senior", "Offline + native module (v3)", "pink"),
        (62, 78, "Buffer", "pendalaman & proyek nyata", "Portofolio studi kasus", "netral"),
    ]
    for i, (a, b, j, isi, hasil, tema) in enumerate(fase):
        y = 140 + (i % 2) * 0
        t = TEMA[tema]
        s.rect(X(a) + 2, 140, X(b) - X(a) - 4, 92, fill=t.fill, stroke=t.stroke, sw=1.6, r=10)
        s.teks(X(a) + 12, 164, j, size=14, bold=True, warna=t.text)
        s.teks(X(a) + 12, 182, f"{b - a} minggu", size=11, warna=MUTED)
        for k, baris in enumerate(bungkus(isi, X(b) - X(a) - 24, 12)):
            s.teks(X(a) + 12, 202 + k * 15, baris, size=12, warna=t.text)
        # hasil
        s.rect(X(a) + 2, 246, X(b) - X(a) - 4, 50, fill=BG, stroke=t.stroke, sw=1.2, r=8, dash="4 3")
        for k, baris in enumerate(bungkus("→ " + hasil, X(b) - X(a) - 20, 11.5)):
            s.teks(X(a) + 10, 266 + k * 15, baris, size=11.5, warna=TEKS, bold=k == 0)

    # berkelanjutan
    s.rect(X(0) + 2, 312, X(78) - X(0) - 4, 40, fill=TEMA["warn"].fill, stroke=TEMA["warn"].stroke, sw=1.4, r=10)
    s.teks(X(0) + 14, 337, "Berkelanjutan: baca kode orang lain · menulis 1 artikel/bulan · kontribusi open source · "
           "code review · ikuti changelog Expo & RN", size=12.5, warna=TEMA["warn"].text, bold=False)

    # tonggak karier
    tonggak = [(18, "Bisa ambil freelance kecil", "mobile"), (42, "Siap melamar Mid-level", "teal"),
               (62, "Skill setara Senior awal", "pink")]
    for m, label, tema in tonggak:
        x = X(m)
        t = TEMA[tema]
        s.garis(x, 360, x, 410, warna=t.stroke, sw=2, dash="4 3")
        s.lingkaran(x, 418, 8, t.stroke)
        w = lebar_teks(label, 12.5, True) + 24
        s.rect(x - w / 2, 436, w, 30, fill=t.stroke, stroke="none", sw=0, r=15)
        s.teks(x, 456, label, size=12.5, bold=True, warna="#FFFFFF", anchor="middle")
    s.garis(X(0), 418, X(78), 418, warna="#CBD5E1", sw=2)
    s.teks(X(0), 412, "Karier", size=11.5, warna=MUTED, bold=True)

    s.catatan(60, 500, 1180, "Ritme yang disarankan: 10–15 jam/minggu (lihat docs/00-cara-belajar.md). Lebih lambat "
              "tidak masalah. Yang penting setiap checkpoint benar-benar lulus sebelum lanjut ke fase berikutnya.",
              tema="netral", size=12.5)
    return "roadmap-timeline.svg", s


def event_loop():
    s = Svg(1240, 700, "Event Loop JavaScript",
            "Kenapa Promise.then() selalu jalan sebelum setTimeout(..., 0)? Karena microtask dikosongkan dulu.")

    # kode
    s.rect(40, 100, 400, 300, fill="#0F172A", stroke="#0F172A", r=12)
    kode = [
        ("console.log('A');", "#E2E8F0"),
        ("setTimeout(() => console.log('B'), 0);", "#FDBA74"),
        ("Promise.resolve().then(() => console.log('C'));", "#86EFAC"),
        ("queueMicrotask(() => console.log('D'));", "#86EFAC"),
        ("console.log('E');", "#E2E8F0"),
    ]
    s.teks(60, 130, "// Tebak urutan output-nya", size=12.5, warna="#64748B", mono=True)
    for i, (k, w) in enumerate(kode):
        s.teks(60, 168 + i * 34, k, size=12.5, warna=w, mono=True)
    s.teks(60, 372, "putih = sinkron · hijau = microtask · oranye = macrotask", size=11, warna="#94A3B8")

    # diagram
    s.kotak(520, 100, 300, 170, "Call Stack", "kode sinkron dijalankan di sini, satu per satu", tema="mobile",
            rata="kiri")
    for i, f in enumerate(["console.log('E')", "main()"]):
        s.rect(540, 170 + i * 40, 260, 32, fill=BG, stroke=TEMA["mobile"].stroke, sw=1.2, r=6)
        s.teks(670, 191 + i * 40, f, size=12, mono=True, anchor="middle", warna=TEMA["mobile"].text)

    s.kotak(880, 100, 320, 170, "Web API / Runtime", "timer, fetch, I/O berjalan di luar JS. Setelah selesai, "
            "callback-nya dimasukkan ke antrean.", tema="netral", rata="kiri")
    s.rect(900, 200, 280, 40, fill=BG, stroke="#94A3B8", sw=1.2, r=6)
    s.teks(1040, 225, "timer 0 ms → callback B", size=12, mono=True, anchor="middle")

    s.kotak(520, 310, 680, 110, "Microtask queue  (prioritas TINGGI)", "", tema="data", rata="kiri")
    for i, f in enumerate(["() => log('C')", "() => log('D')"]):
        s.rect(840 + i * 180, 356, 160, 40, fill=BG, stroke=TEMA["data"].stroke, sw=1.2, r=6)
        s.teks(920 + i * 180, 381, f, size=12, mono=True, anchor="middle", warna=TEMA["data"].text)
    s.teks(540, 372, "Promise.then, await, queueMicrotask", size=11.5, warna=TEMA["data"].text)
    s.teks(540, 392, "(1) dikosongkan SEMUA dulu", size=11.5, bold=True, warna=TEMA["data"].text)

    s.kotak(520, 450, 680, 100, "Macrotask queue", "", tema="warn", rata="kiri")
    s.rect(840, 490, 160, 40, fill=BG, stroke=TEMA["warn"].stroke, sw=1.2, r=6)
    s.teks(920, 515, "() => log('B')", size=12, mono=True, anchor="middle", warna=TEMA["warn"].text)
    s.teks(540, 506, "setTimeout, setInterval, I/O", size=11.5, warna=TEMA["warn"].text)
    s.teks(540, 526, "(2) baru ambil SATU, lalu ulangi", size=11.5, bold=True, warna=TEMA["warn"].text)

    s.panah(1160, 240, 1160, 450, "", warna=TEMA["warn"].stroke, dash="5 4")
    s.path("M 516 365 C 482 365 482 200 518 200", warna=TEMA["data"].stroke, sw=2, panah=True)
    s.path("M 516 500 C 458 500 458 230 518 230", warna=TEMA["warn"].stroke, sw=2, panah=True)
    s.nomor(490, 300, 1, tema="data", r=10)
    s.nomor(467, 420, 2, tema="warn", r=10)

    # hasil
    s.teks(40, 600, "Output:", size=14, bold=True)
    urutan = [("A", "sinkron", "mobile"), ("E", "sinkron", "mobile"), ("C", "microtask", "data"),
              ("D", "microtask", "data"), ("B", "macrotask", "warn")]
    for i, (h, ket, tema) in enumerate(urutan):
        x = 120 + i * 140
        t = TEMA[tema]
        s.rect(x, 576, 120, 60, fill=t.fill, stroke=t.stroke, sw=1.6, r=10)
        s.teks(x + 60, 603, h, size=20, bold=True, warna=t.text, anchor="middle")
        s.teks(x + 60, 624, ket, size=11, warna=t.text, anchor="middle")
        if i < 4:
            s.panah(x + 120, 606, x + 140, 606)
    s.catatan(840, 572, 360, "Di React Native: state update, hasil fetch, dan event semuanya melewati antrean ini. "
              "Kode sinkron yang berat memblokir seluruh JS thread.", tema="netral", size=11.5)
    return "event-loop.svg", s


def rn_thread():
    s = Svg(1240, 700, "Cara Kerja React Native (Arsitektur Baru)",
            "Kode Anda berjalan di JS thread. Layar digambar oleh UI thread. JSI menghubungkan keduanya tanpa serialisasi JSON.")

    s.grup(40, 110, 400, 420, "JS THREAD  ·  Hermes", tema="mobile")
    for i, (j, isi) in enumerate([
        ("Kode Anda", "komponen, hooks, logika"),
        ("React", "render → tree elemen baru"),
        ("TanStack Query · Zustand", "state & cache"),
        ("Event handler", "onPress, onChangeText"),
    ]):
        s.kotak(64, 140 + i * 92, 352, 74, j, isi, tema="mobile", judul_size=13.5)

    s.kotak(500, 200, 240, 240, "JSI", "C++ interface: JS bisa memanggil fungsi native secara LANGSUNG "
            "(sinkron), tanpa bridge JSON seperti arsitektur lama.", tema="netral")

    s.grup(800, 110, 400, 420, "UI THREAD (main)  ·  native", tema="backend")
    s.kotak(824, 140, 352, 74, "Fabric renderer", "menghitung perubahan, menerapkan ke view native", tema="backend",
            judul_size=13.5)
    s.kotak(824, 232, 352, 74, "View native asli", "android.view.View · UIView (bukan WebView)", tema="backend",
            judul_size=13.5)
    s.kotak(824, 324, 352, 74, "Reanimated worklet", "animasi & gesture langsung di UI thread", tema="pink",
            judul_size=13.5)
    s.kotak(824, 416, 352, 90, "TurboModules", "kamera, GPS, SecureStore, modul buatan Anda (Expo Modules API)",
            tema="teal", judul_size=13.5)

    s.panah(440, 260, 500, 290, "render", lpos=0.4)
    s.panah(740, 290, 824, 190, "commit", lpos=0.5)
    s.panah(824, 460, 740, 400, "hasil", lpos=0.5, warna=MUTED, dash="5 4")
    s.panah(740, 360, 824, 450, "", lpos=0.5)
    s.panah(500, 380, 440, 420, "event", lpos=0.5, warna=MUTED, dash="5 4")

    # anggaran frame
    s.teks(40, 576, "Anggaran per frame (60 fps)", size=14, bold=True)
    s.rect(40, 590, 760, 34, fill="#F1F5F9", stroke="#E2E8F0", sw=1, r=8)
    s.rect(40, 590, 520, 34, fill=TEMA["data"].fill, stroke=TEMA["data"].stroke, sw=1.4, r=8)
    s.teks(300, 612, "≤ 16 ms: halus", size=12.5, bold=True, warna=TEMA["data"].text, anchor="middle")
    s.rect(560, 590, 240, 34, fill=TEMA["danger"].fill, stroke=TEMA["danger"].stroke, sw=1.4, r=8)
    s.teks(680, 612, "> 16 ms: frame terlewat (jank)", size=12, bold=True, warna=TEMA["danger"].text,
           anchor="middle")
    s.teks(40, 648, "Kalau JS thread sibuk (loop berat, render berlebih), interaksi & animasi berbasis JS tersendat.",
           size=12, warna=MUTED)
    s.catatan(840, 566, 360, "Solusi: kurangi kerja di JS thread (memo, FlashList), pindahkan animasi ke UI thread "
              "(Reanimated), dan ukur di build release.", tema="warn", size=12)
    return "rn-arsitektur-thread.svg", s


def piramida_testing():
    s = Svg(1240, 640, "Piramida Testing",
            "Banyak test kecil yang cepat di bawah, sedikit test besar yang lambat di atas.")
    cx, top, base_y, half = 360, 110, 560, 300

    def lebar_pada(y):
        return half * (y - top) / (base_y - top)

    lapis = [
        (top, 230, "E2E", "Maestro", "pink"),
        (230, 390, "Component", "React Native Testing Library + MSW", "mobile"),
        (390, base_y, "Unit", "Jest (fungsi domain, hooks, store) · Pest (API)", "data"),
    ]
    for y1, y2, j, isi, tema in lapis:
        t = TEMA[tema]
        w1, w2 = lebar_pada(y1), lebar_pada(y2)
        s.path(f"M {cx - w1:.1f} {y1} L {cx + w1:.1f} {y1} L {cx + w2:.1f} {y2} L {cx - w2:.1f} {y2} Z",
               warna=t.stroke, fill=t.fill, sw=1.8)
        ym = (y1 + y2) / 2
        s.teks(cx, ym + (6 if j == "E2E" else -4), j, size=17 if j != "E2E" else 15, bold=True, warna=t.text,
               anchor="middle")
        if j != "E2E":
            for k, b in enumerate(bungkus(isi, 2 * lebar_pada(ym) - 60, 12)):
                s.teks(cx, ym + 18 + k * 15, b, size=12, warna=t.text, anchor="middle")
        else:
            s.teks(cx, ym + 24, isi, size=11.5, warna=t.text, anchor="middle")

    # panah samping
    s.path(f"M 30 {base_y} L 30 {top + 10}", warna=MUTED, sw=1.6, panah=True)
    s.label(30, (top + base_y) / 2, "lebih\nlambat\n& mahal", warna=MUTED, size=11)

    # contoh
    contoh = [
        ("E2E · ±3–5 flow", "login → check-in → riwayat → logout · ajukan izin · check-in dengan lokasi mock",
         "pink"),
        ("Component · ±10–20", "LoginScreen: field kosong, password salah, sukses · Beranda: loading / kosong / "
         "error / data · Form izin: validasi tanggal", "mobile"),
        ("Unit · sebanyak mungkin", "distanceMeters, isWithinRadius, status terlambat, formatRupiah, store auth "
         "(login/logout) · Pest: setiap endpoint (sukses, 422, 403, aturan bisnis)", "data"),
    ]
    y = 110
    for j, isi, tema in contoh:
        s.kotak(720, y, 480, 100, j, isi, tema=tema, rata="kiri", judul_size=14, isi_size=12)
        y += 150
    s.teks(720, 98, "Contoh di aplikasi absensi", size=13, bold=True, warna=MUTED)
    s.catatan(40, 584, 1160, "Prioritas: uji LOGIKA BISNIS dulu (murah, nilainya tinggi). Jangan mengejar angka "
              "coverage. Uji perilaku yang dilihat user, bukan detail implementasi.", tema="warn", size=12.5)
    return "piramida-testing.svg", s


def siklus_query():
    s = Svg(1240, 620, "Siklus Hidup Cache TanStack Query",
            "Memahami fresh, stale, dan inactive menjelaskan kapan data diambil ulang dari server, dan kapan tidak.")
    status = [
        (60, "fetching", "request berjalan · isLoading / isFetching = true", "mobile"),
        (330, "fresh", "data dianggap terbaru. TIDAK ada refetch selama staleTime", "data"),
        (600, "stale", "data ditampilkan, tapi akan di-refetch saat ada pemicu", "warn"),
        (870, "inactive", "tidak ada komponen yang memakai query ini", "netral"),
    ]
    for x, j, isi, tema in status:
        s.kotak(x, 130, 230, 110, j, isi, tema=tema, judul_size=16, isi_size=12)
    s.panah(290, 185, 330, 185, "sukses", ldy=-10)
    s.panah(560, 185, 600, 185, "staleTime\nhabis", ldy=-22)
    s.panah(830, 185, 870, 185, "unmount", ldy=-10)
    s.kotak(1120, 140, 90, 90, "hapus", "gcTime habis", tema="danger", judul_size=13, isi_size=11)
    s.panah(1100, 185, 1120, 185)

    # pemicu refetch
    s.path("M 715 240 L 715 300 L 175 300 L 175 240", warna=TEMA["warn"].stroke, sw=1.8, panah=True)
    s.label(445, 296, "refetch otomatis", warna=TEMA["warn"].stroke, bold=True)
    pemicu = [
        ("Komponen baru mount", "useQuery dipanggil lagi"),
        ("Aplikasi kembali aktif", "focusManager + AppState"),
        ("Koneksi kembali", "onlineManager + NetInfo"),
        ("invalidateQueries()", "setelah mutasi berhasil"),
    ]
    for i, (j, isi) in enumerate(pemicu):
        s.kotak(60 + i * 270, 330, 250, 64, j, isi, tema="warn", judul_size=12.5, isi_size=11.5)

    # contoh konfigurasi
    s.rect(60, 430, 640, 160, fill="#0F172A", stroke="#0F172A", r=12)
    kode = [
        ("useQuery({", "#E2E8F0"),
        ("  queryKey: ['attendance', 'today'],", "#E2E8F0"),
        ("  queryFn: getToday,", "#E2E8F0"),
        ("  staleTime: 30_000,   // 30 detik dianggap fresh", "#86EFAC"),
        ("  gcTime: 5 * 60_000,  // cache dibuang 5 menit setelah tak dipakai", "#FDBA74"),
        ("});", "#E2E8F0"),
    ]
    for i, (k, w) in enumerate(kode):
        s.teks(84, 462 + i * 21, k, size=12.5, warna=w, mono=True)

    s.kotak(740, 430, 440, 160, "Memilih staleTime", "Absensi hari ini: 30 detik · Riwayat: 5 menit · "
            "Profil: 5–10 menit · Data master (kantor, shift): 1 jam. Semakin jarang berubah, semakin panjang.",
            tema="netral", rata="kiri", judul_size=13.5, isi_size=12)
    return "siklus-tanstack-query.svg", s


SEMUA = [timeline, event_loop, rn_thread, piramida_testing, siklus_query]
