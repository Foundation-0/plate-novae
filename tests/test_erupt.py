"""Tests of pilot/erupt.py on small synthetic light curves. No network needed.

Run from the repository root: python3 -m unittest discover tests
"""
import json
import math
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ERUPT = os.path.join(ROOT, "pilot", "erupt.py")

# The columns erupt.py reads. Real DASCH light curves have many more.
HEADER = "date_jd,series,plate_number,magcal_magdep,limiting_mag_local,reject_flag"
JD_1900 = 2415020.5


def flat_star(n=300, mag=12.0, step=30.0):
    """A constant star seen every `step` days from 1900: small scatter, two plate series, some misses."""
    plates = []
    for i in range(n):
        jd = JD_1900 + i * step
        series = "a" if i % 2 else "b"
        if i % 7 == 0:  # a plate too shallow to show the star: an upper limit
            plates.append((jd, series, i, None, mag - 0.5, ""))
        else:
            plates.append((jd, series, i, mag + 0.2 * math.sin(i), mag + 1.5, "0"))
    return plates


def eruption(start_jd, mags, series, reject="0"):
    """Bright plates one day apart from start_jd, cycling through the given series."""
    return [(start_jd + k, series[k % len(series)], 90000 + k, m, m + 1.0, reject)
            for k, m in enumerate(mags)]


def run(plates, *args):
    """Write plates as a DASCH-style JSON light curve, run erupt.py on it, return its group lines."""
    lines = [HEADER] + [",".join("" if v is None else str(v) for v in p) for p in plates]
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "lc.json")
        with open(path, "w") as f:
            json.dump(lines, f)
        out = subprocess.run([sys.executable, "-I", ERUPT, path, *args],
                             capture_output=True, text=True, check=True).stdout
    return [line.strip() for line in out.splitlines() if line.startswith("  ")]


class TestErupt(unittest.TestCase):
    def test_flat_star_has_no_groups(self):
        self.assertEqual(run(flat_star()), [])

    def test_injected_eruption_is_one_group(self):
        start = JD_1900 + 30 * 365.25 + 10  # early 1930
        groups = run(flat_star() + eruption(start, [8.5, 8.8, 9.2, 9.6, 9.9], ["a", "mc"]))
        self.assertEqual(len(groups), 1)
        self.assertTrue(groups[0].startswith("1930.0"), groups[0])
        self.assertIn("n=5", groups[0])
        self.assertIn("brightest=8.50", groups[0])
        self.assertIn("series=['a', 'mc']", groups[0])

    def test_rejected_plates_are_ignored(self):
        start = JD_1900 + 30 * 365.25
        self.assertEqual(run(flat_star() + eruption(start, [8.5, 8.8, 9.2], ["a", "mc"], reject="5")), [])

    def test_gap_over_60_days_splits_groups(self):
        start = JD_1900 + 30 * 365.25
        plates = flat_star() + eruption(start, [8.5], ["a"]) + eruption(start + 61, [8.6], ["mc"])
        self.assertEqual(len(run(plates)), 2)

    def test_given_quiet_level_replaces_median(self):
        # 1.5 mag above a 12.0 median is under the 2 mag cut; above a quiet level of 14.0 it passes.
        start = JD_1900 + 30 * 365.25
        plates = flat_star() + eruption(start, [10.5, 10.6, 10.7], ["a", "mc"])
        self.assertEqual(run(plates), [])
        self.assertTrue(any("n=3" in g for g in run(plates, "14.0")))


if __name__ == "__main__":
    unittest.main()
