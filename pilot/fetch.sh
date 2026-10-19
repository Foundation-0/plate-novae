#!/bin/bash
# Pilot written on 19 Oct 2026 during Foundation0's scouting
# (https://github.com/Foundation-0/f0/tree/main/deep-fields), by Claude (Anthropic) in a Claude Code session.
# Copied unchanged apart from this header. See pilot/README.md for the stars and their coordinates.
# usage: fetch.sh name ra dec outdir ; picks nearest ATLAS refcat source, saves LC
name=$1; ra=$2; dec=$3; out=$4
curl -sS --max-time 60 -X POST https://api.starglass.cfa.harvard.edu/public/dasch/dr7/querycat -H 'Content-Type: application/json' -d "{\"refcat\": \"atlas\", \"ra_deg\": $ra, \"dec_deg\": $dec, \"radius_arcsec\": 6}" -o $out/${name}_cat.json
read ref gsc mag <<< $(python3 -I -c "
import json,csv,io,math
d=json.load(open('$out/${name}_cat.json'))
rows=list(csv.DictReader(io.StringIO('\n'.join(d))))
rows.sort(key=lambda r: math.hypot(float(r['dra_asec']),float(r['ddec_asec'])))
r=rows[0]; print(r['ref_number'], r['gsc_bin_index'], r['stdmag'])
")
curl -sS --max-time 120 -X POST https://api.starglass.cfa.harvard.edu/public/dasch/dr7/lightcurve -H 'Content-Type: application/json' -d "{\"refcat\": \"atlas\", \"ref_number\": $ref, \"gsc_bin_index\": $gsc}" -o $out/${name}_lc.json
echo "$name ref=$ref stdmag=$mag"
