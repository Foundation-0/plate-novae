# Pilot, 19 October 2026

Two scripts written during Foundation0's scouting on 19 Oct 2026, copied here unchanged apart from a header:

- [`fetch.sh`](fetch.sh) looks up a position in DASCH's copy of the ATLAS star catalogue, takes the nearest star
  within 6″, and downloads its light curve: every measurement of that star on the Harvard plates. It needs `curl`
  and `python3`.
- [`erupt.py`](erupt.py) flags possible eruptions in one light curve. It uses only the Python standard library.

The output of both runs, and how each known eruption scored, is in
[`results/pilot-2026-10-19.txt`](../results/pilot-2026-10-19.txt).

## What erupt.py does

1. It reads every plate row. A row counts as a measurement when DASCH gives a calibrated magnitude
   (`magcal_magdep`) and its `reject_flag` is 0 or empty. DASCH's other quality bits (`aflags`) are not used.
   Rows without a measurement are counted as upper limits and otherwise ignored.
2. It sets the star's quiet level to the median of the measurements, or to the number given as the second
   argument.
3. It keeps the measurements more than 2 magnitudes brighter than the quiet level. Magnitudes run backwards:
   smaller numbers are brighter, and 2 magnitudes is a factor of about 6 in brightness.
4. It sorts them by date and groups them. A new group starts whenever more than 60 days pass between one bright
   plate and the next, so one group can span more than 60 days.
5. It prints each group: first and last date as decimal years, number of plates, brightest magnitude, and plate
   series. A plate series is the set of plates from one Harvard telescope, named by a short code such as `ai`.

It prints groups of every size, including single plates. Its docstring says it requires at least 2 plates, but
the code does not enforce that. The pilot's eruption test was applied by hand to the printed groups: at least
3 plates from at least 2 plate series.

**The quiet level.** T Pyx and U Sco are usually too faint for most plates, so DASCH measures them mostly in
eruption. Their median is then brighter than their real quiet level, and fewer plates pass the 2-magnitude cut.
Run B in the results file sets their quiet level to the magnitude DASCH's ATLAS catalogue lists for them:
15.55 for T Pyx and 18.21 for U Sco. With that, U Sco's 1936 eruption passes the test.

## The five stars

| Star | Role | RA (deg) | Dec (deg) | DASCH catalogue entry | `refcat` | `ref_number` | `gsc_bin_index` |
|---|---|---|---|---|---|---|---|
| T Pyx | recurrent nova | 136.1729423 | -32.3798619 | APASS_J090441.5-322248 | apass | 409044152322248 | 39233375 |
| U Sco | recurrent nova | 245.6282465 | -17.8786575 | ATLAS2_563839755 | atlas | 9563839755 | 58544554 |
| RS Oph | recurrent nova | 267.5548298 | -6.7079113 | ATLAS2_650056559 | atlas | 9650056559 | 74615911 |
| DQ Her | control: one eruption, 1934 | 271.8760460 | 45.8590458 | ATLAS2_910534029 | atlas | 9910534029 | 145107751 |
| V603 Aql | control: one eruption, 1918 | 282.2276541 | 0.5841270 | ATLAS2_693013898 | atlas | 9693013898 | 85353694 |

Coordinates: SIMBAD, which takes them from Gaia EDR3 (ICRS, epoch J2000), looked up through the
[Sesame](https://cds.unistra.fr/cgi-bin/Sesame) name resolver on 19 Oct 2026. Each DASCH entry lies within 0.1″ of
these positions.

## Fetching the light curves

Keep them in `data/`, which git ignores. Please don't commit light curves.

```
mkdir -p data
bash pilot/fetch.sh usco    245.6282465 -17.8786575 data
bash pilot/fetch.sh rsoph   267.5548298  -6.7079113 data
bash pilot/fetch.sh dqher   271.8760460  45.8590458 data
bash pilot/fetch.sh v603aql 282.2276541   0.5841270 data
```

T Pyx needs a different call. The pilot used DASCH's APASS catalogue entry for it, while `fetch.sh` picks the ATLAS
entry (ATLAS2_388903450). That is a different light curve of the same star: 288 measurements instead of 352. Its
groups from two or more series fall in the same years (1902, 1920, 1944–45), but its single-plate groups differ.
To fetch the light curve the pilot used:

```
curl -sS -X POST https://api.starglass.cfa.harvard.edu/public/dasch/dr7/lightcurve \
  -H 'Content-Type: application/json' \
  -d '{"refcat": "apass", "ref_number": 409044152322248, "gsc_bin_index": 39233375}' \
  -o data/tpyx_lc.json
```

The same call, with the values from the table, fetches any of the five. The light curves total about 4 MB. On
19 Oct 2026, U Sco fetched with `fetch.sh` and T Pyx fetched with the call above gave the same `erupt.py` output as
the results file. The API returned the rows in a different order, which does not change the output.

## Re-running

```
for s in tpyx usco rsoph dqher v603aql; do python3 -I pilot/erupt.py data/${s}_lc.json; done   # Run A
python3 -I pilot/erupt.py data/tpyx_lc.json 15.55                                             # Run B
python3 -I pilot/erupt.py data/usco_lc.json 18.21                                             # Run B
```

Compare each output with its block in [`results/pilot-2026-10-19.txt`](../results/pilot-2026-10-19.txt).
