# Full nova sweep and top-twenty review

Status: preparation for review. No observational result is claimed.

The sweep waits for a versioned target catalogue, quiet-level calibration and null-test output. Record all three hashes and freeze the eruption-test revision before reading new candidates. No fixed count of 402 is assumed until the catalogue export is checked.

Fetch in serial or small bounded batches into an external cache. Every target must finish with success, no coverage, no usable plates or retrieval error. A failed download is not a negative scientific result. Preserve cache hashes and retrieval timestamps.

A passing group needs nova ID, distinct plate IDs, series, dates, magnitudes, quiet-level source, excesses, masks and the exact grouping rule. Exclude known eruptions and their declines using a sourced exclusion window fixed before ranking. Rank deterministically by distinct corroborating series, then distinct plates, then brightness excess, with a stable ID tie-break.

Write every passing group to a machine-readable table. Select the top twenty before image inspection and record the list hash. Apply the RS Oph image/quality/comparison/SkyBoT packet to each, and report the null-test rate beside the list. The 1953–1969 coverage deficit remains a selection effect, not evidence of quietness.

The catalogue, calibration, null products, sweep outputs and twenty image verdicts are outstanding. This protocol supplies the reproducibility contract for a later data-bearing run.
