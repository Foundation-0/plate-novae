# Pilot written on 19 Oct 2026 during Foundation0's scouting
# (https://github.com/Foundation-0/f0/tree/main/deep-fields), by Claude (Anthropic) in a Claude Code session.
# Copied unchanged apart from this header. See pilot/README.md for what the script does and does not do.

"""Flag nova-like eruptions in a DASCH DR7 light curve JSON.

Usage: python3 -I erupt.py LC.json [quiescent_mag]
Prints yearly summary of detections and candidate eruption clusters:
detections at least 2 mag brighter than the median detected mag (or the given
quiescent mag), grouped within 60 days, requiring >= 2 plates.
"""
import csv
import io
import json
import statistics
import sys

JD_1900 = 2415020.5


def year(jd):
    return 1900 + (jd - JD_1900) / 365.25


def main():
    path = sys.argv[1]
    rows = list(csv.DictReader(io.StringIO("\n".join(json.load(open(path))))))
    det, lim = [], []
    for r in rows:
        try:
            jd = float(r["date_jd"])
        except (TypeError, ValueError):
            continue
        m = r.get("magcal_magdep") or ""
        lm = r.get("limiting_mag_local") or ""
        rej = r.get("reject_flag") or "0"
        if m not in ("", "nan") and rej in ("0", ""):
            try:
                det.append((jd, float(m), r.get("series"), r.get("plate_number")))
            except ValueError:
                pass
        elif lm not in ("", "nan"):
            try:
                lim.append((jd, float(lm)))
            except ValueError:
                pass
    det.sort()
    print(f"rows={len(rows)} good_detections={len(det)} upper_limits={len(lim)}")
    if not det:
        return
    q = float(sys.argv[2]) if len(sys.argv) > 2 else statistics.median(m for _, m, _, _ in det)
    print(f"reference (quiescent) mag = {q:.2f}")
    bright = [d for d in det if d[1] < q - 2.0]
    clusters, cur = [], []
    for d in bright:
        if cur and d[0] - cur[-1][0] > 60:
            clusters.append(cur)
            cur = []
        cur.append(d)
    if cur:
        clusters.append(cur)
    for c in clusters:
        mags = [m for _, m, _, _ in c]
        print(f"  {year(c[0][0]):.2f}-{year(c[-1][0]):.2f}  n={len(c)}  brightest={min(mags):.2f}"
              f"  series={sorted(set(s for _, _, s, _ in c))}")


if __name__ == "__main__":
    main()
