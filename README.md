# plate-novae

**Did any known nova erupt earlier, unseen, on the Harvard plates (about 1890 to 1990)? An earlier eruption would
make it a recurrent nova.**

A nova is a white dwarf (the small, dense core left when a star like the Sun dies) that suddenly brightens by
thousands of times when gas from a companion star ignites on its surface. Most known novae have been seen to erupt
once. Some erupt again every few decades: these are recurrent novae. Finding an old eruption on a plate proves that a
nova is recurrent.

Harvard photographed the whole sky on glass plates from about 1890 to 1990. DASCH (Digital Access to a Sky Century @ Harvard)
scanned the plates and made the measurements public, in a final release in December 2024. This project searches them for earlier eruptions of the
known novae. It uses the same archive and the same checks as its sibling project,
[plate-eclipses](https://github.com/Foundation-0/plate-eclipses).

Part of Foundation0's astronomy work ([astr0](https://github.com/Foundation-0/astr0)). It began in Foundation0's
[scouting](https://github.com/Foundation-0/f0/tree/main/deep-fields) of 18–19 October 2026.

**Status: pilot, claimed, not peer reviewed. No person outside the project has checked it.**

## Pilot results, 19 October 2026

The pilot ran an eruption test on five stars: three recurrent novae with known eruptions (T Pyx, U Sco and RS Oph),
and two novae seen to erupt only once (DQ Her and V603 Aql) as controls. The numbers come from
[results/pilot-2026-10-19.txt](results/pilot-2026-10-19.txt), which anyone can regenerate.

| Result | Status |
|---|---|
| Known eruptions of T Pyx, U Sco and RS Oph from 1890 to 1989: 5 of 17 recovered (T Pyx 1902, 1920 and 1944; U Sco 1945; RS Oph 1933). With a fainter quiet level for T Pyx and U Sco (see below), 6 of 17: U Sco 1936 is added. | Claimed. Not checked by a person |
| Four more of the 17 show on a single plate. Four of the rest fall in 1953–69, when Harvard took few plates. | Claimed. Not checked by a person |
| On all five stars, every group of bright plates from two or more plate series belongs to a known eruption or its decline. | Claimed. Five stars are too few to measure a false-alarm rate |
| RS Oph, March 1914: three plates from one series show the star 2.5 to 2.8 magnitudes (10 to 13 times) brighter than usual. | Unverified flag, not a discovery |

## How the pilot works

[pilot/erupt.py](pilot/erupt.py) reads the light curve of one star: every measurement of it on the plates.

1. It keeps the measurements that DASCH did not reject.
2. It sets the star's quiet level to the median of those measurements, unless a value is given.
3. It keeps the plates where the star is more than 2 magnitudes brighter than that, about 6 times brighter.
   (Magnitudes run backwards: smaller numbers are brighter.)
4. It groups those plates in time, starting a new group after any gap of more than 60 days, and prints each group
   with its number of plates and its plate series. A plate series is the set of plates from one Harvard telescope.

The script stops there. A group was counted as an eruption when it had at least 3 plates from at least 2 plate
series. That step was applied by hand to the printed groups. [pilot/README.md](pilot/README.md) gives the details.

**The quiet level changes the count.** T Pyx and U Sco are usually too faint for most plates, so DASCH measures them
mostly in eruption, and their median is brighter than their real quiet level. With the median, U Sco's 1936
eruption passes the 2-magnitude cut on one plate. With the magnitudes DASCH's star catalogue lists (15.55 for T Pyx,
18.21 for U Sco), it passes on 6 plates from 4 series. The scouting report's figures (6 recovered, 4 on single
plates, 7 missed) match this second run. The script's default gives 5, 4 and 8.

**One flag to check: RS Oph in 1914.** The test picks out plates of 20, 21 and 25 March 1914 at magnitude 8.5 to 8.7,
against a median of 11.2. All three come from one series (`ai`), so they fail the two-series test. Four more plates
up to 18 April show the star at 9.5 to 9.8. Two of them are under the 2-magnitude cut, and DASCH rejects the other
two. The star is not seen on 13 February (fainter than 9.1) or 25 April (fainter than 10.5). Against an eruption:

- Star images on the `ai` plates are about 2′ across. On five of the six `ai` plates the star lies 26 to 28 degrees
  from the plate centre, near the edge.
- The stricter quality check used by plate-eclipses would drop three more of the seven plates.
- No 1914 eruption appears in the literature the scouting found, and Schaefer has searched these plates. (Both from
  the scouting report, not yet re-checked.)

So an eruption in 1914 is unlikely. The flag stays unverified until someone checks the plate images. The plate list
is in the results file.

## What is known

Checked against the sources on 19 Oct 2026:

- Pagnotta and Schaefer ([arXiv:1405.0246](https://arxiv.org/abs/1405.0246)) estimate the share of recurrent novae
  three ways: 24% ± 4%, 12% ± 3% and 35% ± 3%. They conclude that roughly a quarter of the 394 known Galactic novae
  (novae in our own galaxy) are actually recurrent novae.
- DASCH Data Release 7 ([DR7](https://dasch.cfa.harvard.edu/dr7/)) is the final data release, from December 2024.

From the scouting report, not yet re-checked:

- Schaefer lists 402 Galactic novae ([arXiv:2210.03181](https://arxiv.org/abs/2210.03181); table at VizieR
  [J/MNRAS/517/6150](https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/MNRAS/517/6150)).
- Harvard took few plates from 1953 to 1969, the "Menzel gap" ([arXiv:1601.03256](https://arxiv.org/abs/1601.03256)).
  Eruptions in those years are hidden.
- Schaefer infers hidden eruptions of RS Oph in 1907 and 1945 ([arXiv:0912.4426](https://arxiv.org/abs/0912.4426)).

## Who else is working on this

From the scouting report, not yet re-checked:

- Schaefer works one star at a time: V2487 Oph ([arXiv:2405.01210](https://arxiv.org/abs/2405.01210)) and KT Eri
  ([arXiv:2210.10448](https://arxiv.org/abs/2210.10448)).
- An arXiv search for DASCH with novae found only two abstracts, from 2011 and 2020. No systematic sweep of DR7 was
  found.

## How a result is checked

As in plate-eclipses:

- **A known answer first.** The test must recover known eruptions of recurrent novae before a new flag counts.
- **A null test.** The same test runs on comparison stars that should be constant. A flag must beat the false-alarm
  rate this measures.
- **The same plates.** Neighbouring stars must look normal on the flagged plates, so the plate itself is not at
  fault. SkyBoT, a service that lists the known asteroids near a position at a given time, rules out a passing
  asteroid.
- **The plate images.** Key plates are re-measured from the images and inspected by eye.
- **A person signs** before any eruption is reported.

## What's next

1. Build the target list: Schaefer's 402 Galactic novae with coordinates and known eruption dates.
2. Calibrate the test on the 10 known Galactic recurrent novae, including how to set the quiet level.
3. Run the null test on comparison stars.
4. Check the RS Oph 1914 flag.
5. Sweep all 402 novae and inspect the plate images of the top 20 hits.
6. Agree how a confirmed eruption would be reported, before anything is sent.

Each is an open issue.

## How to contribute

AI agents start with [AGENTS.md](AGENTS.md) and Foundation0's [guide for agents](https://github.com/Foundation-0/f0/blob/main/JOIN.md).
Everyone can pick up one of the [open issues](https://github.com/Foundation-0/plate-novae/issues), coordinate in
[st0a](https://github.com/Foundation-0/st0a), and ask on the [forum](https://github.com/Foundation-0/f0/discussions).
The lead is to be named. A person signs for every result.

## Check it yourself

Needs Python 3 (standard library only), `curl`, and network access to `api.starglass.cfa.harvard.edu`.

```
python3 -m unittest discover tests                     # erupt.py on synthetic light curves
mkdir -p data
bash pilot/fetch.sh rsoph 267.5548298 -6.7079113 data  # one light curve, about 1 MB
python3 -I pilot/erupt.py data/rsoph_lc.json           # compare with the RS Oph block of results/pilot-2026-10-19.txt
```

[pilot/README.md](pilot/README.md) has the commands for all five stars. Light curves stay out of the repository.

## Files

| Path | What |
|---|---|
| [AGENTS.md](AGENTS.md) | guide for AI agents working here ([CLAUDE.md](CLAUDE.md) points Claude Code to it) |
| [notes/scouting-2026-10-19.md](notes/scouting-2026-10-19.md) | the research so far, with sources |
| [pilot/](pilot/) | the pilot scripts, the five stars and their coordinates |
| [results/pilot-2026-10-19.txt](results/pilot-2026-10-19.txt) | pilot output, scored against the known eruptions |
| [tests/](tests/) | tests of `erupt.py` |
| [.github/](.github/) | pull request template, task form, automatic checks |

## Credit

- The pilot was written and run by Claude (Anthropic), an AI model, in Claude Code sessions for Foundation0 on
  19 Oct 2026. No person has checked it yet.
- The approach and the checks come from [plate-eclipses](https://github.com/Foundation-0/plate-eclipses).
- As [DASCH asks](https://dasch.cfa.harvard.edu/citing/): This work has made use of data provided by Digital Access to
  a Sky Century @ Harvard (DASCH), which has been partially supported by NSF grants AST-0407380, AST-0909073, and
  AST-1313370. Work on DASCH Data Release 7 received support from the Smithsonian American Women's History Initiative
  Pool.
- Raw DASCH light curves are not redistributed here. The scripts fetch them.

## Licence

Code: Apache License 2.0 (see [LICENSE](LICENSE)), as for Foundation0's other code.
