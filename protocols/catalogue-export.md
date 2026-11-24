# Galactic nova catalogue export

Status: preparation for review. No observational result is claimed.

Use the named VizieR catalogue J/MNRAS/517/6150 as the starting snapshot. Save the raw response, catalogue version, exact query, UTC retrieval time and SHA-256 before normalizing names or coordinates. The scouting count 402 remains a comparison target, not an accepted row count.

The normalized nova table needs nova_id, original_name, aliases, ra_deg, dec_deg, coordinate_frame, epoch and source_table_row. Store eruptions in a separate one-to-many table: nova_id, eruption_start, date_precision, time_scale, primary_reference and source_location. A missing date is unknown, not evidence of no eruption.

Record name merges and duplicate decisions in a separate reconciliation table. The query must preserve the full source table rather than silently dropping rows with incomplete dates. Cross-check ten deterministic random positions with SIMBAD and record positional offsets and epoch differences.

No catalogue response is bundled in this branch. Acceptance needs the downloader, normalized outputs, count reconciliation and independent position checks; these cannot be supplied by copying the scouting total.
