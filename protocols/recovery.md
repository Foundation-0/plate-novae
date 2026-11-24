# Known-eruption calibration

Status: preparation for review. No observational result is claimed.

The classifier uses a fixed sixty-day window after a sourced eruption start, a brightness excess strictly greater than two magnitudes, and at least three distinct plates from two series for recovery. Two same-series detections remain insufficient corroboration rather than being counted as a recovery or a single plate.

Supply a literature-backed quiet level in a compatible passband, with uncertainty and reference. The detected-magnitude median can be biased toward eruptions; it is a sensitivity run, not the only accepted baseline. Report both rules for U Sco and the other recurrent novae.

The input needs one row per plate with jd, magnitude, series, plate_id and quality. Preserve limiting observations separately; the helper's good-detection count is not the number of all covering plates. Compute recovery rates over all known eruptions and over independently established covered windows separately.

Actual ten-star eruption lists, plate limits, data fetching and calibrated output tables remain pending. Synthetic classifier checks do not establish an observational recovery rate.
