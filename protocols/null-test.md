# Null-test cohort and rates

Status: preparation for review. No observational result is claimed.

Freeze comparison stars by a documented position and magnitude rule before seeing their eruption-test outputs. Keep each selection, rejected match and variable-star exclusion. Reuse the same quiet-level rule, plate masks, grouping window and two-series acceptance rule as the nova run.

The rate helper takes one row per control star with star_id, plates and passing_groups. It reports flagged stars among stars with plate coverage and passing groups per thousand accepted plates. Zero-coverage stars remain counted separately. A zero numerator is not proof that the false-alarm rate is zero.

Every passing group needs its individual plate IDs and cutout links for inspection. Plate errors cluster by series and time, so confidence intervals should resample control stars or plate groups, not assume every plate is independent. Freeze that uncertainty method before interpreting the sweep.

No control light curves or measured rates are present. The helper provides explicit denominators for the later null run, and rejects duplicate stars and impossible zero-coverage positive groups.
