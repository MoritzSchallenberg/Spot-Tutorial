# Historical asset migration record

**Not part of the published website.** Internal working document for
Entwicklungsauftrag 9, Section 5.3. Excluded from the Sphinx build
(outside `docs/`) and not linked from any published toctree.

## Method

Every image requested by the task and actually found in the old Spot
tutorial (`00-02 Quelle 2 Spot Tutorial/Website Code`) was copied
byte-for-byte (no recompression, no resizing) into
`docs/_static/images/history/`, using the copy that was actually
embedded in a page (the `..._files/` copy) wherever a file existed in
more than one place. SHA-256 of source and destination was compared
for every file; all 24 matched exactly (see the table below). Two
files (`award_ceremony.jpg`, `spot_gravel_sitting.jpg`) existed as two
byte-identical copies in the source material (a top-level copy and the
`..._files/` copy embedded by the page) — only one copy of each was
migrated.

`wifi.png`, `kinova_web.png`, and `kinova_faults.png` (from the old
Spot Startup page) were **not** on the task's requested image list and
were excluded per `maintainers/spot-security-audit.md`: they show a
real private IP address and a list of real local WiFi network names.

Faces are visible in `award_ceremony.jpg` and `rrl_eindhoven_group.png`
but no names are attached to them anywhere in the old site's HTML (no
alt text, no caption naming an individual) — new alt text and captions
describe the scene without naming anyone, since no name attribution
exists in the source to be accurate about. Image rights for these
photographs were not established by the old site and are not asserted
here; no license is claimed for any migrated image beyond "the former
ALeRT tutorial's own published material."

## Migration table

| Original file | Destination | Used on | Checksum equal | Privacy checked | Rights clarified | Remark |
| --- | --- | --- | --- | --- | --- | --- |
| `Website Code/.../General Information..._files/arena.png` | `docs/_static/images/history/arena.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes — no people, no credentials, no network info | Not established (old tutorial's own material; no license asserted) | Exploration-challenge arena |
| `Website Code/.../General Information..._files/arena2.png` | `docs/_static/images/history/arena2.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes | Not established | "Smaller teams" ruleset arena |
| `Website Code/.../General Information..._files/arena3.png` | `docs/_static/images/history/arena3.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes | Not established | 2019 rulebook arena |
| `Website Code/ALeRT Team Page..._files/award_ceremony.jpg` | `docs/_static/images/history/award_ceremony.jpg` | about/alert-and-spot.md, about/historical-gallery.md, docs/index.md (via link) | Yes | Yes — faces visible, no names attached in source, none added | Not established | Duplicate top-level copy not migrated (byte-identical) |
| `Website Code/.../General Information..._files/Dexterity_board.png` | `docs/_static/images/history/Dexterity_board.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes | Not established | |
| `Website Code/.../General Information..._files/door.png` | `docs/_static/images/history/door.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes | Not established | |
| `Website Code/.../General Information..._files/Emergency.png` | `docs/_static/images/history/Emergency.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes | Not established | |
| `Website Code/.../General Information..._files/Exploration1.png` | `docs/_static/images/history/Exploration1.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes | Not established | |
| `Website Code/.../General Information..._files/Exploration2.png` | `docs/_static/images/history/Exploration2.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes | Not established | |
| `Website Code/.../General Information..._files/Exploration3.png` | `docs/_static/images/history/Exploration3.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes | Not established | |
| `Website Code/.../General Information..._files/Exploration4.png` | `docs/_static/images/history/Exploration4.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes | Not established | |
| `Website Code/.../General Information..._files/maneuvering.png` | `docs/_static/images/history/maneuvering.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes | Not established | |
| `Website Code/.../General Information..._files/objective1.png` | `docs/_static/images/history/objective1.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes | Not established | |
| `Website Code/.../General Information..._files/objective2.png` | `docs/_static/images/history/objective2.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes | Not established | |
| `Website Code/.../General Information..._files/readiness.png` | `docs/_static/images/history/readiness.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes | Not established | |
| `Website Code/.../General Information..._files/resuceleague_teams.png` | `docs/_static/images/history/resuceleague_teams.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes | Not established | Filename typo ("resuceleague") preserved as-is; original filename kept for traceability |
| `Website Code/Tutorials/01 Introduction..._files/RRL_arena.png` | `docs/_static/images/history/RRL_arena.png` | about/alert-and-spot.md, about/historical-gallery.md | Yes | Yes | Not established | |
| `Website Code/Tutorials/01 Introduction..._files/rrl_eindhoven_group.png` | `docs/_static/images/history/rrl_eindhoven_group.png` | about/alert-and-spot.md, about/historical-gallery.md | Yes | Yes — faces visible, no names attached in source, none added | Not established | |
| `Website Code/ALeRT Team Page..._files/spot_gravel_sitting.jpg` | `docs/_static/images/history/spot_gravel_sitting.jpg` | about/alert-and-spot.md, about/historical-gallery.md, docs/index.md | Yes | Yes — no people, no credentials, no network info | Not established | Duplicate top-level copy not migrated (byte-identical); also used as the homepage's historical Spot image |
| `Website Code/.../General Information..._files/terrain1.png` | `docs/_static/images/history/terrain1.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes | Not established | |
| `Website Code/.../General Information..._files/terrain2.png` | `docs/_static/images/history/terrain2.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes | Not established | |
| `Website Code/.../General Information..._files/terrain3.png` | `docs/_static/images/history/terrain3.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes | Not established | |
| `Website Code/.../General Information..._files/terrain4.png` | `docs/_static/images/history/terrain4.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes | Not established | |
| `Website Code/.../General Information..._files/tests.png` | `docs/_static/images/history/tests.png` | about/robocup-rescue.md, about/historical-gallery.md | Yes | Yes | Not established | |

Full path for every `.../General Information..._files/` row above:
`00-02 Quelle 2 Spot Tutorial/Website Code/Spot Documentation/00 General
Information/General Information — ALeRT - RoboCup Rescue Team Page
1.0-r1 documentation_files/<filename>`. Full path for every
`Tutorials/01 Introduction..._files/` row:
`00-02 Quelle 2 Spot Tutorial/Website Code/Tutorials/01
Introduction/Introduction — ALeRT - RoboCup Rescue Team Page 1.0-r1
documentation_files/<filename>`. Full path for the `ALeRT Team
Page..._files/` rows:
`00-02 Quelle 2 Spot Tutorial/Website Code/ALeRT Team Page — ALeRT -
RoboCup Rescue Team Page 1.0-r1 documentation_files/<filename>`.
Shortened above for table width; SHA-256 values for every file are
recorded in `/tmp/history-image-checksums.csv` at migration time (not
committed — regenerate with `sha256sum` against the paths above if
re-verification is needed).

## Historical interface screenshots (Section 9.3)

Four operating-interface screenshots requested by Section 9.3, from
`Spot Documentation/08 Spot Startup/..._files/`, migrated into
`docs/_static/images/historical-interface/`, checksums verified equal:

| File | Checksum equal | Visually reviewed | Disposition |
| --- | --- | --- | --- |
| `spot_buttons.jpg` | Yes | Yes — a labeled photo of the power/motor-cutoff button panel, no sensitive content | Kept, labeled `Historical interface`, used in `operating/power-on.md` |
| `rviz.png` | Yes | Yes — RViz + rqt dashboard; tab labels ("BASIC/PLUS/BW/EXP/NAV"), the "Estop" slider, and the "Start" button visible in the screenshot match literal strings in the current `spot_estop_rqt.py` source; no sensitive content | Kept, labeled `Historical interface`, used in `operating/operator-interface.md` |
| `spot_control.png` | Yes | Yes — a Steam Deck control schematic; describes Steam Deck native controls, which do not match the DualSense mapping found in the current teleop code | Kept, labeled `Historical interface`, explicit mismatch noted in `operating/driving-spot.md` |
| `manipulator_control.png` | Yes | Yes — a Steam Deck manipulator-control schematic; same mismatch as above | Kept, labeled `Historical interface`, explicit mismatch noted in `operating/operating-the-manipulator.md` |

Per Section 9.3, three other screenshots from the same source
directory — `wifi.png`, `kinova_web.png`, `kinova_faults.png` — were
excluded entirely rather than labeled, because they show real network
information (see "Excluded images" below and `spot-security-audit.md`),
not because their depicted interface is out of date.

## Excluded images

| Original file | Category | Reason excluded |
| --- | --- | --- |
| `.../08 Spot Startup..._files/wifi.png` | Screenshot | Shows a real list of local WiFi network names; not on the task's requested list |
| `.../08 Spot Startup..._files/kinova_web.png` | Screenshot | Shows a real private IP address in a browser UI; not on the task's requested list |
| `.../08 Spot Startup..._files/kinova_faults.png` | Screenshot | Shows the same private IP address; not on the task's requested list |

## Summary

24 images migrated, all checksums verified equal, none recompressed or
resized, none showing sensitive information. 3 images excluded for
showing real network/IP information. No image license is asserted;
rights remain unestablished for all migrated images, consistent with
this repository's existing `LICENSES.md` position on source material
from the old tutorial.
