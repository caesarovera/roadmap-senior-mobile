"""Bangun semua diagram SVG ke assets/diagram/.

    python3 tools/diagram/build.py            # semua
    python3 tools/diagram/build.py sistem     # hanya yang namanya mengandung 'sistem'
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import d_alur  # noqa: E402
import d_arsitektur  # noqa: E402
import d_belajar  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parents[2] / "assets" / "diagram"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    filter_ = sys.argv[1] if len(sys.argv) > 1 else ""
    for fn in [*d_arsitektur.SEMUA, *d_alur.SEMUA, *d_belajar.SEMUA]:
        nama, svg = fn()
        if filter_ and filter_ not in nama:
            continue
        (OUT / nama).write_text(svg.render(), encoding="utf-8")
        print("✓", nama)


if __name__ == "__main__":
    main()
