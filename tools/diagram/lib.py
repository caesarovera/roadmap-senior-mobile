"""
Pustaka kecil untuk membuat diagram SVG dengan gaya yang konsisten.

Semua diagram di assets/diagram/ dibuat dari build.py memakai pustaka ini.
Jalankan:  python3 tools/diagram/build.py
"""

from __future__ import annotations

import html
from dataclasses import dataclass

FONT = "-apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


@dataclass(frozen=True)
class Tema:
    stroke: str
    fill: str
    text: str


TEMA = {
    "mobile": Tema("#2563EB", "#EFF6FF", "#1E3A8A"),
    "backend": Tema("#EA580C", "#FFF7ED", "#7C2D12"),
    "data": Tema("#16A34A", "#F0FDF4", "#14532D"),
    "external": Tema("#7C3AED", "#F5F3FF", "#4C1D95"),
    "netral": Tema("#64748B", "#F8FAFC", "#0F172A"),
    "warn": Tema("#D97706", "#FFFBEB", "#78350F"),
    "danger": Tema("#DC2626", "#FEF2F2", "#7F1D1D"),
    "teal": Tema("#0D9488", "#F0FDFA", "#134E4A"),
    "pink": Tema("#DB2777", "#FDF2F8", "#831843"),
}

TEKS = "#0F172A"
MUTED = "#64748B"
GARIS = "#E2E8F0"
BG = "#FFFFFF"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def lebar_teks(s: str, size: float, bold: bool = False, mono: bool = False) -> float:
    """Perkiraan lebar teks (cukup akurat untuk font sans-serif umum)."""
    if mono:
        return len(s) * size * 0.61
    w = 0.0
    for ch in s:
        if ch in "il.,:;|!'`":
            w += 0.28
        elif ch in "mwMW":
            w += 0.85
        elif ch.isupper():
            w += 0.66
        elif ch == " ":
            w += 0.3
        else:
            w += 0.55
    return w * size * (1.06 if bold else 1.0)


def bungkus(s: str, max_w: float, size: float, bold: bool = False, mono: bool = False) -> list[str]:
    """Pecah teks menjadi beberapa baris agar muat di lebar max_w."""
    hasil: list[str] = []
    for paragraf in s.split("\n"):
        kata = paragraf.split(" ")
        baris = ""
        for k in kata:
            coba = f"{baris} {k}".strip()
            if lebar_teks(coba, size, bold, mono) <= max_w or not baris:
                baris = coba
            else:
                hasil.append(baris)
                baris = k
        hasil.append(baris)
    return hasil


class Svg:
    def __init__(self, w: int, h: int, judul: str = "", sub: str = ""):
        self.w, self.h = w, h
        self.el: list[str] = []
        self.marker_warna: set[str] = set()
        self.judul, self.sub = judul, sub
        if judul:
            self.teks(32, 44, judul, size=22, bold=True)
        if sub:
            self.teks(32, 68, sub, size=13.5, warna=MUTED)

    # ---------- primitif ----------
    def teks(self, x, y, s, size=13.0, bold=False, warna=TEKS, anchor="start", mono=False, italic=False):
        fam = MONO if mono else FONT
        w = ' font-weight="700"' if bold else ""
        it = ' font-style="italic"' if italic else ""
        it += ' xml:space="preserve"' if mono else ""
        self.el.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}"{w}{it} '
            f'fill="{warna}" text-anchor="{anchor}">{esc(s)}</text>'
        )

    def teks_multi(self, x, y, baris: list[str], size=12.5, lh=None, **kw):
        lh = lh or size * 1.4
        for i, b in enumerate(baris):
            self.teks(x, y + i * lh, b, size=size, **kw)
        return len(baris) * lh

    def rect(self, x, y, w, h, fill=BG, stroke=GARIS, sw=1.5, r=12, dash=None, opacity=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' fill-opacity="{opacity}"' if opacity is not None else ""
        self.el.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
            f'fill="{fill}"{o} stroke="{stroke}" stroke-width="{sw}"{d}/>'
        )

    def garis(self, x1, y1, x2, y2, warna=MUTED, sw=1.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{warna}" stroke-width="{sw}"{d}/>'
        )

    def lingkaran(self, cx, cy, r, fill, stroke=None, sw=1.5):
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.el.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}"{s}/>')

    def path(self, d, warna=MUTED, sw=1.5, fill="none", dash=None, panah=False):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        m = ""
        if panah:
            self.marker_warna.add(warna)
            m = f' marker-end="url(#p{warna[1:]})"'
        self.el.append(f'<path d="{d}" stroke="{warna}" stroke-width="{sw}" fill="{fill}"{da}{m} stroke-linejoin="round"/>')

    # ---------- komponen ----------
    def kotak(self, x, y, w, h, judul, isi="", tema="netral", ikon="", judul_size=14.0, isi_size=12.0,
              rata="tengah", mono_isi=False, r=12):
        t = TEMA[tema]
        self.rect(x, y, w, h, fill=t.fill, stroke=t.stroke, sw=1.6, r=r)
        cx = x + w / 2
        pad = 14
        baris_judul = bungkus(f"{ikon} {judul}".strip(), w - 2 * pad, judul_size, True)
        baris_isi = bungkus(isi, w - 2 * pad, isi_size, mono=mono_isi) if isi else []
        lh_j, lh_i = judul_size * 1.3, isi_size * 1.45
        tinggi = len(baris_judul) * lh_j + (6 + len(baris_isi) * lh_i if baris_isi else 0)
        if rata == "tengah":
            y0 = y + (h - tinggi) / 2 + judul_size * 0.95
            anchor, tx = "middle", cx
        else:
            y0 = y + pad + judul_size * 0.9
            anchor, tx = "start", x + pad
        for i, b in enumerate(baris_judul):
            self.teks(tx, y0 + i * lh_j, b, size=judul_size, bold=True, warna=t.text, anchor=anchor)
        yi = y0 + len(baris_judul) * lh_j + 4
        for i, b in enumerate(baris_isi):
            self.teks(tx, yi + i * lh_i, b, size=isi_size, warna=TEKS if tema == "netral" else t.text,
                      anchor=anchor, mono=mono_isi)

    def grup(self, x, y, w, h, label, tema="netral", dash="6 5"):
        t = TEMA[tema]
        self.rect(x, y, w, h, fill=t.fill, stroke=t.stroke, sw=1.4, r=16, dash=dash, opacity=0.45)
        lw = lebar_teks(label, 12.5, True) + 22
        self.rect(x + 16, y - 12, lw, 24, fill=BG, stroke=t.stroke, sw=1.4, r=12)
        self.teks(x + 16 + lw / 2, y + 4.5, label, size=12.5, bold=True, warna=t.stroke, anchor="middle")

    def pil(self, x, y, label, tema="netral", size=11.5, anchor="start"):
        t = TEMA[tema]
        w = lebar_teks(label, size, True) + 18
        h = size + 11
        x0 = x - w / 2 if anchor == "middle" else x
        self.rect(x0, y, w, h, fill=t.fill, stroke=t.stroke, sw=1.2, r=h / 2)
        self.teks(x0 + w / 2, y + h / 2 + size * 0.36, label, size=size, bold=True, warna=t.text, anchor="middle")
        return w

    def panah(self, x1, y1, x2, y2, label="", warna="#475569", dash=None, sw=1.7, lpos=0.5, ldx=0, ldy=-7,
              label_size=11.5, lbg=True, via=None):
        if via:
            pts = [(x1, y1), *via, (x2, y2)]
            d = "M " + " L ".join(f"{px:.1f} {py:.1f}" for px, py in pts)
        else:
            d = f"M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}"
        self.path(d, warna=warna, sw=sw, dash=dash, panah=True)
        if label:
            if via:
                seg = [(x1, y1), *via, (x2, y2)]
                i = min(int(lpos * (len(seg) - 1)), len(seg) - 2)
                (ax, ay), (bx, by) = seg[i], seg[i + 1]
                lx, ly = (ax + bx) / 2, (ay + by) / 2
            else:
                lx, ly = x1 + (x2 - x1) * lpos, y1 + (y2 - y1) * lpos
            self.label(lx + ldx, ly + ldy, label, size=label_size, warna=warna, bg=lbg)

    def label(self, x, y, s, size=11.5, warna="#475569", bg=True, anchor="middle", bold=False):
        baris = s.split("\n")
        if bg:
            w = max(lebar_teks(b, size, bold) for b in baris) + 10
            h = len(baris) * size * 1.35 + 4
            x0 = x - w / 2 if anchor == "middle" else x - 5
            self.rect(x0, y - size - 1, w, h, fill=BG, stroke="none", sw=0, r=4)
        for i, b in enumerate(baris):
            self.teks(x, y + i * size * 1.35, b, size=size, warna=warna, anchor=anchor, bold=bold)

    def nomor(self, cx, cy, n, tema="mobile", r=11):
        t = TEMA[tema]
        self.lingkaran(cx, cy, r, t.stroke)
        self.teks(cx, cy + 4.2, str(n), size=12, bold=True, warna="#FFFFFF", anchor="middle")

    def legenda(self, x, y, item: list[tuple[str, str]], size=12):
        cx = x
        for tema, label in item:
            t = TEMA[tema]
            self.rect(cx, y, 14, 14, fill=t.fill, stroke=t.stroke, sw=1.5, r=4)
            self.teks(cx + 20, y + 11.5, label, size=size, warna=MUTED)
            cx += 20 + lebar_teks(label, size) + 22

    def catatan(self, x, y, w, s, tema="warn", size=12):
        t = TEMA[tema]
        baris = bungkus(s, w - 28, size)
        h = len(baris) * size * 1.45 + 18
        self.rect(x, y, w, h, fill=t.fill, stroke=t.stroke, sw=1.2, r=8)
        self.rect(x, y, 5, h, fill=t.stroke, stroke="none", sw=0, r=2)
        self.teks_multi(x + 16, y + 9 + size, baris, size=size, warna=t.text, lh=size * 1.45)
        return h

    # ---------- keluaran ----------
    def render(self) -> str:
        defs = []
        for w in sorted(self.marker_warna):
            defs.append(
                f'<marker id="p{w[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                f'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{w}"/></marker>'
            )
        judul = f"<title>{esc(self.judul)}</title>" if self.judul else ""
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" '
            f'height="{self.h}" role="img">{judul}<defs>{"".join(defs)}</defs>'
            f'<rect x="0.5" y="0.5" width="{self.w - 1}" height="{self.h - 1}" rx="18" fill="{BG}" stroke="{GARIS}"/>'
            + "".join(self.el)
            + "</svg>\n"
        )


class Sekuens:
    """Pembantu diagram sekuens (sequence diagram)."""

    def __init__(self, svg: Svg, peserta: list[tuple[str, str, str]], x0: float, x1: float, y_kepala: float,
                 lebar_kotak: float = 150, tinggi_kotak: float = 50):
        self.s = svg
        n = len(peserta)
        jarak = (x1 - x0) / (n - 1) if n > 1 else 0
        self.x = {}
        self.y_kepala = y_kepala
        self.tinggi_kotak = tinggi_kotak
        self.lebar_kotak = lebar_kotak
        self.peserta = peserta
        for i, (kunci, nama, tema) in enumerate(peserta):
            self.x[kunci] = x0 + i * jarak
        self.y = y_kepala + tinggi_kotak + 48
        self.idx = len(svg.el)

    def tutup(self, y_akhir: float):
        """Gambar garis hidup (di bawah semua elemen) dan kotak peserta (di atas)."""
        garis_awal = len(self.s.el)
        for kunci, nama, tema in self.peserta:
            cx = self.x[kunci]
            self.s.garis(cx, self.y_kepala + self.tinggi_kotak, cx, y_akhir, warna="#CBD5E1", sw=1.5, dash="5 5")
        garis = self.s.el[garis_awal:]
        del self.s.el[garis_awal:]
        self.s.el[self.idx:self.idx] = garis
        for kunci, nama, tema in self.peserta:
            cx = self.x[kunci]
            self.s.kotak(cx - self.lebar_kotak / 2, self.y_kepala, self.lebar_kotak, self.tinggi_kotak, nama,
                         tema=tema, judul_size=13)

    def pesan(self, dari, ke, label, balas=False, warna=None, jarak=36, nomor=None, tema_nomor="mobile"):
        x1, x2 = self.x[dari], self.x[ke]
        y = self.y
        warna = warna or ("#64748B" if balas else "#334155")
        if dari == ke:
            self.s.path(f"M {x1:.1f} {y:.1f} h 40 v 18 h -38", warna=warna, panah=True, dash="5 4" if balas else None)
            self.s.label(x1 + 48, y + 13, label, anchor="start", warna=warna)
            self.y += jarak + 10
            return
        arah = 1 if x2 > x1 else -1
        self.s.panah(x1 + 4 * arah, y, x2 - 4 * arah, y, warna=warna, dash="6 4" if balas else None)
        self.s.label((x1 + x2) / 2, y - 7, label, warna=warna)
        if nomor is not None:
            self.s.nomor(x1 + 16 * arah if arah > 0 else x1 - 16, y - 13, nomor, tema=tema_nomor, r=9)
        self.y += jarak

    def blok(self, label, tinggi, x_kiri, x_kanan, tema="netral"):
        """Bingkai alt/opt. Panggil SEBELUM pesan-pesan di dalamnya; kembalikan y awal."""
        t = TEMA[tema]
        y = self.y - 22
        self.s.rect(x_kiri, y, x_kanan - x_kiri, tinggi, fill=t.fill, stroke=t.stroke, sw=1.2, r=8, dash="4 4",
                    opacity=0.5)
        w = lebar_teks(label, 11.5, True) + 14
        self.s.rect(x_kiri, y, w, 20, fill=t.stroke, stroke="none", sw=0, r=6)
        self.s.teks(x_kiri + 7, y + 14, label, size=11.5, bold=True, warna="#FFFFFF")
        self.y += 8
        return y

    def jeda(self, dy):
        self.y += dy

    def catatan(self, di, label, tema="warn", lebar=230):
        cx = self.x[di]
        t = TEMA[tema]
        baris = bungkus(label, lebar - 20, 11.5)
        h = len(baris) * 16 + 12
        self.s.rect(cx - lebar / 2, self.y - 16, lebar, h, fill=t.fill, stroke=t.stroke, sw=1.2, r=6)
        self.s.teks_multi(cx, self.y + 0, baris, size=11.5, warna=t.text, anchor="middle", lh=16)
        self.y += h + 14
