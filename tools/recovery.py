"""Classify cached detections in a fixed sixty-day recovery window."""
import math

def classify(plates,start,quiet):
    if not all(math.isfinite(x) for x in (start,quiet)):raise ValueError('finite start and quiet magnitude required')
    unique={}
    for p in plates:
        jd=float(p['jd']);mag=float(p['magnitude'])
        if not math.isfinite(jd) or not math.isfinite(mag):continue
        if 0<=jd-start<=60 and p.get('quality','0')=='0':
            key=(p['series'],p['plate_id'])
            if key in unique and unique[key]!=p:raise ValueError('conflicting duplicate plate')
            unique[key]=p
    good=list(unique.values());bright=[p for p in good if float(p['magnitude'])<quiet-2]
    series={p['series'] for p in bright}
    outcome='recovered' if len(bright)>=3 and len(series)>=2 else 'single plate' if len(bright)==1 else 'insufficient corroboration' if bright else 'missed'
    return dict(good_plates=len(good),bright_plates=len(bright),series=sorted(series),outcome=outcome,quiet_mag=quiet,window_days=60,coverage='has plates' if good else 'no good detections')
