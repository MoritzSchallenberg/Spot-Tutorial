#!/usr/bin/env python3
"""verify-structure.py -- static, source-level checks for the ALeRT Spot
Tutorial's current, Spot-centric navigation structure. Updated from an
earlier topic-based structure this script originally checked -- that
structure's 13 topic directories still exist on disk (as "background
directories", see BACKGROUND_DIRS below) but are no longer top-level
navigation sections in their own right.

Unlike verify-site.py, this needs no build, no server and no browser -- it
reads the Markdown sources in docs/ directly. Run it any time with:

    python3 scripts/verify-structure.py

It checks:

 1. exactly 11 public top-level "primary nav" directories exist, no more,
    no fewer, beyond the background directories they transitively reference,
    and no docs/course/ or docs/prerequisites/ directory exists (the
    pre-migration structure);
 2. every topic directory has an index.md;
 3. every topic's index.md is referenced from docs/index.md's own
    toctrees (the site's single navigation root);
 4. no page anywhere under docs/ contains a numbered-module heading
    ("# 1.", "Module 1", ...), a processing-time estimate ("80-100
    minutes", "80-100 minute", "core learning path"), or a
    Hackathon/Capstone reference (case-insensitive) -- all replaced by
    the topic-based structure and difficulty levels;
 5. no page is orphaned: every .md file under docs/ is reachable from
    some toctree, directly or transitively from docs/index.md;
 6. Robot Manipulation (docs/manipulation/) and Autonomous
    Decision-Making (docs/decision-making/) are distinct directories,
    and no MoveIt-specific content lives under decision-making/ (the
    planning-and-manipulation.md page from the old structure was split:
    RAFCON/PlanSys2/Golog++ stayed in decision-making/, MoveIt moved to
    manipulation/);
 7. ROS 2 installation lives at docs/ros2/installation.md, not under a
    separate prerequisites/getting-started installation page;
 8. no internal link anywhere under docs/ still points at the deleted
    docs/course/ or docs/prerequisites/ paths;
 9. no Carologistics content remains anywhere (carried over from an
    earlier Carologistics-removal commit, still relevant -- a later
    edit could reintroduce it);
10. no page under docs/ is named or titled "Instructor";
11. no video URL (a `grid-item-card` `:link:` on a video page) appears
    more than once across the whole site;
12. every video card carries the channel/duration metadata shape that
    comes from an actually-checked video (a weak proxy for "no video ID
    is unchecked" -- see the note on live oEmbed verification below);
13. only the new difficulty/verification substitutions
    ({{ foundation }}, {{ intermediate }}, {{ advanced }}, {{ research }},
    {{ documented }}, {{ simulation }}, {{ hardwareverified }},
    {{ unverified }}, {{ hwverificationrequired }}, {{ experimental }},
    {{ historical }}) are used -- the old course-era
    {{ core }}/{{ optional }}/{{ platformspecific }} substitutions no
    longer exist in docs/conf.py and must not appear in content either.

Two notes carried over from the previous version of this script, still
true here:

  - Broken/stale cross-references and anchors are exactly what
    `sphinx-build -W --keep-going` already fails on (MyST's
    `local id not found` / `myst.xref_missing` checks). Always run a full
    clean rebuild (`rm -rf docs/_build/html docs/_build/doctrees` first)
    before trusting a "0 warnings" result -- an incremental build can
    silently miss a newly-broken reference in a file that was not itself
    touched in that pass.
  - "No video ID is unchecked" ultimately needs a live call to YouTube's
    oEmbed endpoint per video, which is a network-dependent check unsuited
    to a repo-committed test. Every video already on the site was checked
    manually against oEmbed at authoring time; check 12 above only
    verifies the metadata shape that process produces, not the ID itself.

Exit code is 0 if every check passed, 1 otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"

# The ALeRT Spot Tutorial pivot replaced the 13 independent topics with
# the current Spot-oriented navigation. PRIMARY_NAV_DIRS are the 11
# sections with their own top-level toctree caption in docs/index.md, in
# that order. BACKGROUND_DIRS are the pre-existing topic directories kept
# at their original path (to avoid
# rewriting the ~30 cross-references into docs/platforms/spot/index.md
# alone) and reached transitively through a primary section's own toctree
# instead of being a primary section themselves -- see
# maintainers/spot-tutorial-migration-report.md for the exact mapping.
PRIMARY_NAV_DIRS = [
    "about",
    "safety",
    "operating",
    "architecture",
    "sensors-and-perception",
    "navigation-and-mapping",
    "manipulation",
    "autonomous-behaviors",
    "deployment-and-configuration",
    "integration-testing",
    "reference",
]

BACKGROUND_DIRS = [
    "getting-started",
    "ros2",
    "simulation",
    "platforms",
    "sensors-frames",
    "perception",
    "mapping-world-models",
    "navigation-exploration",
    "decision-making",
    "rescue-projects",
]

TOPIC_DIRS = PRIMARY_NAV_DIRS  # kept for check_topic_index_pages/root-toctree below

REMOVED_DIRS = ["course", "prerequisites"]

TOCTREE_RE = re.compile(r"```\{toctree\}\n(.*?)\n```", re.DOTALL)
VIDEO_LINK_RE = re.compile(
    r":::\{grid-item-card\}[^\n]*\n:link:\s*(https://www\.youtube\.com/watch\?v=[\w-]+)"
)

OLD_SUBSTITUTIONS = ("{{ core }}", "{{ optional }}", "{{ platformspecific }}", "{{ common }}")

NUMBERED_MODULE_RE = re.compile(r"^#\s+\d+\.\s", re.MULTILINE)
MODULE_WORD_RE = re.compile(r"\bmodule\s+\d+\b", re.IGNORECASE)
TIME_ESTIMATE_RE = re.compile(r"80.100 minute|core learning path", re.IGNORECASE)
HACKATHON_CAPSTONE_RE = re.compile(r"\bhackathon\b|\bcapstone\b", re.IGNORECASE)

_CAROLOGISTICS_TERMS = (
    "carologistics",
    "robotino",
    "smart manufacturing league",
    "expertino-rcll",
    "{{ carologistics }}",
)


def all_md_files() -> list[Path]:
    return [p for p in DOCS.rglob("*.md") if "_build" not in p.parts]


_FENCE_RE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)


def strip_code_fences(text: str) -> str:
    """Blank out fenced code blocks (```...```), keeping line numbers and
    surrounding prose intact, so a shell comment like '# 8. do the thing'
    inside a ```bash block is never mistaken for a Markdown heading or a
    real 'module 8' content reference."""
    return _FENCE_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)


def parse_toctree_entries(md_path: Path) -> list[str]:
    """Every entry across ALL toctree blocks in this file (docs/index.md
    has one block per top-level topic), as raw doc-ref strings."""
    text = md_path.read_text(encoding="utf-8")
    entries: list[str] = []
    for m in TOCTREE_RE.finditer(text):
        for line in m.group(1).splitlines():
            line = line.strip()
            if not line or line.startswith(":"):
                continue
            entries.append(line)
    return entries


def doc_ref_to_path(entry: str, from_dir: Path) -> Path:
    return (from_dir / f"{entry}.md").resolve()


def check_topic_directories() -> list[str]:
    failures: list[str] = []
    existing = {p.name for p in DOCS.iterdir() if p.is_dir() and not p.name.startswith("_")}
    for d in REMOVED_DIRS:
        if (DOCS / d).is_dir():
            failures.append(f"pre-migration directory still exists: docs/{d}/")
    allowed = set(PRIMARY_NAV_DIRS) | set(BACKGROUND_DIRS)
    missing = [d for d in PRIMARY_NAV_DIRS if d not in existing]
    for d in missing:
        failures.append(f"expected primary-nav directory missing: docs/{d}/")
    unexpected = existing - allowed - set(REMOVED_DIRS)
    for d in sorted(unexpected):
        failures.append(
            f"unexpected top-level directory under docs/: docs/{d}/ "
            "(not one of the 11 primary-nav sections or their background directories)"
        )
    if len(set(PRIMARY_NAV_DIRS) & existing) != 11 and not missing:
        failures.append(f"expected exactly 11 primary-nav directories, found {len(set(PRIMARY_NAV_DIRS) & existing)}")
    return failures


def check_topic_index_pages() -> list[str]:
    failures: list[str] = []
    for d in TOPIC_DIRS:
        index = DOCS / d / "index.md"
        if not index.is_file():
            failures.append(f"docs/{d}/ has no index.md")
    return failures


def check_topics_in_root_toctree() -> list[str]:
    failures: list[str] = []
    root = DOCS / "index.md"
    if not root.is_file():
        return ["docs/index.md is missing"]
    entries = parse_toctree_entries(root)
    entry_targets = {doc_ref_to_path(e, DOCS) for e in entries}
    for d in TOPIC_DIRS:
        expected = (DOCS / d / "index.md").resolve()
        if expected not in entry_targets:
            failures.append(f"docs/index.md's toctrees do not reference docs/{d}/index.md")
    return failures


def check_no_course_language() -> list[str]:
    failures: list[str] = []
    for p in all_md_files():
        text = strip_code_fences(p.read_text(encoding="utf-8", errors="ignore"))
        rel = p.relative_to(REPO_ROOT)
        if NUMBERED_MODULE_RE.search(text):
            failures.append(f"{rel}: numbered-module-style heading ('# N. ...') found")
        if MODULE_WORD_RE.search(text):
            failures.append(f"{rel}: 'module N' reference found")
        if TIME_ESTIMATE_RE.search(text):
            failures.append(f"{rel}: processing-time estimate or 'core learning path' found")
        if HACKATHON_CAPSTONE_RE.search(text):
            failures.append(f"{rel}: 'Hackathon' or 'Capstone' reference found")
    return failures


def check_no_orphans() -> list[str]:
    """Every .md file under docs/ must be reachable from docs/index.md via
    some chain of toctrees (each topic's index.md toctree, in turn,
    referencing its own subpages)."""
    failures: list[str] = []
    reachable: set[Path] = set()
    queue = [DOCS / "index.md"]
    while queue:
        current = queue.pop()
        if current in reachable or not current.is_file():
            continue
        reachable.add(current)
        for entry in parse_toctree_entries(current):
            target = doc_ref_to_path(entry, current.parent)
            if target not in reachable:
                queue.append(target)

    all_files = set(all_md_files())
    orphans = all_files - reachable
    for p in sorted(orphans):
        failures.append(f"orphaned page, not reachable from docs/index.md via any toctree: {p.relative_to(REPO_ROOT)}")
    return failures


def check_manipulation_decision_making_separate() -> list[str]:
    failures: list[str] = []
    manipulation_dir = DOCS / "manipulation"
    decision_dir = DOCS / "decision-making"
    if not manipulation_dir.is_dir():
        failures.append("docs/manipulation/ does not exist -- Robot Manipulation must be its own topic")
        return failures
    if not decision_dir.is_dir():
        failures.append("docs/decision-making/ does not exist")
        return failures
    if manipulation_dir.resolve() == decision_dir.resolve():
        failures.append("manipulation and decision-making resolve to the same directory")

    # MoveIt-specific headings must not live under decision-making/ --
    # they belong on the manipulation page instead.
    moveit_heading_re = re.compile(r"^#{1,3}\s*MoveIt\b", re.MULTILINE)
    for p in decision_dir.glob("*.md"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        if moveit_heading_re.search(text):
            failures.append(
                f"{p.relative_to(REPO_ROOT)}: has a MoveIt-specific heading -- "
                "MoveIt content belongs under docs/manipulation/, not decision-making/"
            )
    if not (manipulation_dir / "index.md").is_file():
        failures.append("docs/manipulation/index.md is missing")
    return failures


def check_installation_under_ros2() -> list[str]:
    failures: list[str] = []
    expected = DOCS / "ros2" / "installation.md"
    if not expected.is_file():
        failures.append("docs/ros2/installation.md is missing -- installation must live under ROS 2")
    for wrong in (
        DOCS / "prerequisites" / "installation.md",
        DOCS / "getting-started" / "installation.md",
    ):
        if wrong.is_file():
            failures.append(f"installation page found at the wrong location: {wrong.relative_to(REPO_ROOT)}")
    return failures


def check_no_stale_removed_dir_links() -> list[str]:
    failures: list[str] = []
    pattern = re.compile(r"\]\([^)]*\b(?:course|prerequisites)/[^)]*\)")
    linkfield_pattern = re.compile(r"^:link:\s*.*\b(?:course|prerequisites)/", re.MULTILINE)
    for p in all_md_files():
        text = p.read_text(encoding="utf-8", errors="ignore")
        if pattern.search(text) or linkfield_pattern.search(text):
            failures.append(f"{p.relative_to(REPO_ROOT)}: still links into a removed course/ or prerequisites/ path")
    return failures


def check_no_carologistics_content() -> list[str]:
    failures: list[str] = []
    carologistics_page = DOCS / "platforms" / "carologistics-robotino.md"
    if carologistics_page.exists():
        failures.append(f"Carologistics platform page still exists: {carologistics_page.relative_to(REPO_ROOT)}")
    for p in all_md_files():
        text = p.read_text(encoding="utf-8", errors="ignore").lower()
        for term in _CAROLOGISTICS_TERMS:
            if term in text:
                failures.append(f"{p.relative_to(REPO_ROOT)} still mentions {term!r}")
    return failures


def check_no_instructor_page() -> list[str]:
    failures: list[str] = []
    for p in all_md_files():
        if "instructor" in p.name.lower():
            failures.append(f"instructor-named page present in docs/: {p.relative_to(REPO_ROOT)}")
        else:
            text = p.read_text(encoding="utf-8", errors="ignore")
            first_heading = next((l for l in text.splitlines() if l.startswith("# ")), "")
            if "instructor" in first_heading.lower():
                failures.append(f"page titled 'Instructor...': {p.relative_to(REPO_ROOT)}")
    return failures


def check_no_duplicate_video_urls() -> list[str]:
    failures: list[str] = []
    seen: dict[str, Path] = {}
    for videos_md in DOCS.rglob("videos.md"):
        text = videos_md.read_text(encoding="utf-8")
        for url in VIDEO_LINK_RE.findall(text):
            if url in seen and seen[url] != videos_md:
                failures.append(
                    f"video URL used twice: {url} "
                    f"(in {seen[url].relative_to(REPO_ROOT)} and {videos_md.relative_to(REPO_ROOT)})"
                )
            else:
                seen[url] = videos_md
    return failures


def check_video_cards_carry_metadata() -> list[str]:
    failures: list[str] = []
    card_re = re.compile(
        r":::\{grid-item-card\}[^\n]*\n:link:\s*https://www\.youtube\.com/watch\?v=[\w-]+\n\n"
        r"\*\*[^*]+\*\*"
    )
    for videos_md in DOCS.rglob("videos.md"):
        text = videos_md.read_text(encoding="utf-8")
        cards = text.count(":link: https://www.youtube.com/watch?v=")
        metadata_cards = len(card_re.findall(text))
        if cards != metadata_cards:
            failures.append(
                f"{videos_md.relative_to(REPO_ROOT)}: {cards} video card(s) but only "
                f"{metadata_cards} carry the expected channel/duration metadata line "
                "immediately after the link -- looks unchecked"
            )
    return failures


def check_only_new_substitutions_used() -> list[str]:
    failures: list[str] = []
    for p in all_md_files():
        text = p.read_text(encoding="utf-8", errors="ignore")
        for old in OLD_SUBSTITUTIONS:
            if old in text:
                failures.append(f"{p.relative_to(REPO_ROOT)}: uses the removed substitution {old}")
    conf_py = (REPO_ROOT / "docs" / "conf.py").read_text(encoding="utf-8")
    for name in ('"core"', '"optional"', '"platformspecific"', '"common"'):
        if name in conf_py:
            failures.append(f"docs/conf.py still defines the removed substitution {name}")
    return failures


# ---------------------------------------------------------------------------
# ALeRT Spot Tutorial pivot checks.
# ---------------------------------------------------------------------------

EXPECTED_TITLE = "ALeRT Spot Tutorial"

EXPECTED_NAV_CAPTIONS = [
    "About ALeRT and Spot",
    "Safety and Prerequisites",
    "Operating Spot",
    "System Architecture",
    "Sensors and Perception",
    "Navigation and Mapping",
    "Manipulator and MoveIt",
    "Autonomous Behaviors",
    "Deployment and Configuration",
    "Diagnostics and Testing",
    "Reference",
]

HISTORY_PAGES = [
    "about/index.md",
    "about/alert-and-spot.md",
    "about/robocup-rescue.md",
    "about/rescue-challenges.md",
    "about/historical-gallery.md",
]

OPERATING_PAGES = [
    "operating/index.md",
    "operating/system-preparation.md",
    "operating/power-on.md",
    "operating/operator-interface.md",
    "operating/driving-spot.md",
    "operating/operating-the-manipulator.md",
    "operating/safe-shutdown.md",
    "operating/recovery-and-troubleshooting.md",
]

ARCHITECTURE_PAGES = [
    "architecture/index.md",
    "architecture/hardware-overview.md",
    "architecture/computers-and-network.md",
    "architecture/software-components.md",
    "architecture/startup-and-launch-sequence.md",
    "architecture/ros2-interfaces.md",
    "architecture/coordinate-frames.md",
    "architecture/data-flow.md",
]

# Exact strings from the task's Section 16 banned-term list. Case-sensitive
# where the task gave a specific casing (module/session numbers, product
# names); case-insensitive matching is used for the search itself so a
# rephrased heading doesn't slip past by capitalisation alone.
_BANNED_TERMS = (
    "learning robotics crash course",
    "alert advanced robotics tutorial",
    "crash course",
    "module 1",
    "module 2",
    "module 3",
    "module 4",
    "module 5",
    "module 6",
    "module 7",
    "module 8",
    "85 min",
    "90 min",
    "core learning path",
    "hackathon",
    "capstone",
    "carologistics",
    "robotino",
    "rcll",
    "mps",
    "smart manufacturing",
    "thanks to max",
    "credentials are saved",
)

# "MPS" and "RCLL" are short enough to false-positive inside ordinary words
# (timestamps, "jumps", ...) -- match them as whole words only. The rest are
# specific enough as substrings.
_WHOLE_WORD_TERMS = {"mps", "rcll"}
_WHOLE_WORD_RE = {t: re.compile(rf"\b{re.escape(t)}\b", re.IGNORECASE) for t in _WHOLE_WORD_TERMS}

# Historical year mentions (e.g. "RRL2023", "RoboCup 2001") are allowed --
# only the specific old-course-era phrases above are banned.

_PRIVATE_IP_RE = re.compile(
    r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}"
    r"|192\.168\.\d{1,3}\.\d{1,3})\b"
)

MAINTAINERS_MARKER = "Not part of the published website"


def check_new_title() -> list[str]:
    failures: list[str] = []
    conf_py = (REPO_ROOT / "docs" / "conf.py").read_text(encoding="utf-8")
    for field in ('project = "', 'html_title = "'):
        if f'{field}{EXPECTED_TITLE}"' not in conf_py:
            failures.append(f"docs/conf.py: {field.strip(' =\"')} is not {EXPECTED_TITLE!r}")
    index_md = (DOCS / "index.md").read_text(encoding="utf-8")
    first_heading = next((l for l in index_md.splitlines() if l.startswith("# ")), "")
    if first_heading.strip() != f"# {EXPECTED_TITLE}":
        failures.append(f"docs/index.md: first heading is {first_heading!r}, expected '# {EXPECTED_TITLE}'")
    return failures


def check_full_navigation() -> list[str]:
    """The 11 primary-nav captions must appear, in order, as a (not
    necessarily contiguous) subsequence of docs/index.md's toctree
    captions -- allowing a small number of additional entries (e.g.
    "Start Here", added in a later pass) without requiring an exact
    full-list match, while still catching a caption being dropped,
    renamed, or reordered."""
    failures: list[str] = []
    index_md = REPO_ROOT / "docs" / "index.md"
    text = index_md.read_text(encoding="utf-8")
    captions = re.findall(r":caption:\s*(.+)", text)

    search_from = 0
    for expected in EXPECTED_NAV_CAPTIONS:
        try:
            found_at = captions.index(expected, search_from)
        except ValueError:
            failures.append(
                f"docs/index.md toctree captions {captions} are missing or "
                f"misorder the required Section 6 navigation "
                f"{EXPECTED_NAV_CAPTIONS} (expected to find {expected!r} at or "
                f"after position {search_from})"
            )
            break
        search_from = found_at + 1
    return failures


def _check_pages_present(pages: list[str], label: str) -> list[str]:
    failures: list[str] = []
    for rel in pages:
        if not (DOCS / rel).is_file():
            failures.append(f"{label}: expected page missing: docs/{rel}")
    return failures


def check_history_section_present() -> list[str]:
    return _check_pages_present(HISTORY_PAGES, "history section")


def check_operating_pages_present() -> list[str]:
    return _check_pages_present(OPERATING_PAGES, "operating section")


def check_architecture_pages_present() -> list[str]:
    return _check_pages_present(ARCHITECTURE_PAGES, "architecture section")


_MD_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
# Figure/card option lines may be indented when the directive sits inside a
# list item (e.g. a bullet's own nested figure) -- allow leading whitespace
# before the ":" rather than anchoring to column 0.
_FIGURE_BLOCK_RE = re.compile(r":{3,4}\{figure\}[^\n]*\n((?:[ \t]*:.*\n)*)", re.MULTILINE)
_GRID_CARD_IMG_RE = re.compile(
    r":{3,4}\{grid-item-card\}[^\n]*\n((?:[ \t]*:.*\n)*)", re.MULTILINE
)


def check_image_alt_text() -> list[str]:
    failures: list[str] = []
    for p in all_md_files():
        text = p.read_text(encoding="utf-8", errors="ignore")
        rel = p.relative_to(REPO_ROOT)

        for m in _MD_IMAGE_RE.finditer(text):
            alt, target = m.group(1), m.group(2)
            if target.startswith(("http://", "https://")):
                continue
            if not alt.strip():
                failures.append(f"{rel}: image {target!r} has empty alt text")

        for m in _FIGURE_BLOCK_RE.finditer(text):
            options = m.group(1)
            if ":alt:" not in options:
                failures.append(f"{rel}: a {{figure}} directive has no :alt: option")

        for m in _GRID_CARD_IMG_RE.finditer(text):
            options = m.group(1)
            if ":img-top:" in options and ":img-alt:" not in options:
                failures.append(f"{rel}: a grid-item-card with :img-top: has no :img-alt: option")
    return failures


def check_banned_terms() -> list[str]:
    failures: list[str] = []
    for p in all_md_files():
        text = strip_code_fences(p.read_text(encoding="utf-8", errors="ignore"))
        lower = text.lower()
        rel = p.relative_to(REPO_ROOT)
        for term in _BANNED_TERMS:
            if term in _WHOLE_WORD_TERMS:
                if _WHOLE_WORD_RE[term].search(text):
                    failures.append(f"{rel}: banned term found: {term!r}")
            elif term in lower:
                failures.append(f"{rel}: banned term found: {term!r}")
    return failures


def check_no_sensitive_network_data() -> list[str]:
    """Scoped to the Spot-specific sections this task adds (about/, safety/,
    operating/, architecture/), not the whole site -- docs/getting-started/
    and docs/ros2/ predate this task and legitimately use generic private-IP
    examples (e.g. 192.168.1.100 to illustrate subnetting) that have nothing
    to do with the real Spot deployment's actual network."""
    failures: list[str] = []
    scoped_dirs = ("about", "safety", "operating", "architecture")
    for p in all_md_files():
        rel = p.relative_to(REPO_ROOT)
        if rel.parts[1] not in scoped_dirs:  # rel = docs/<dir>/...
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for m in _PRIVATE_IP_RE.finditer(text):
            failures.append(f"{rel}: private IP address literal found: {m.group(0)}")
    return failures


def check_maintainers_not_public() -> list[str]:
    """maintainers/ must never be reachable from docs/ (source) or leak into
    a build (docs/_build/html), and must not appear in Sphinx's own search
    index if a build exists."""
    failures: list[str] = []
    for p in all_md_files():
        text = p.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"\]\([^)]*\.\./maintainers/", text) or re.search(r"\]\(/?maintainers/", text):
            failures.append(f"{p.relative_to(REPO_ROOT)}: links directly into maintainers/, which is not published")

    build_html = DOCS / "_build" / "html"
    if build_html.is_dir():
        for html_file in build_html.rglob("*.html"):
            if MAINTAINERS_MARKER in html_file.read_text(encoding="utf-8", errors="ignore"):
                failures.append(
                    f"{html_file.relative_to(REPO_ROOT)}: contains the maintainers-only marker "
                    f"{MAINTAINERS_MARKER!r} -- an internal document appears to have leaked into the build"
                )
        search_index = build_html / "searchindex.js"
        if search_index.is_file() and "spot-code-audit" in search_index.read_text(encoding="utf-8", errors="ignore"):
            failures.append("docs/_build/html/searchindex.js references an internal maintainers document")
    return failures


def check_banned_terms_in_build() -> list[str]:
    """Same banned-term list as check_banned_terms(), applied to the built
    HTML if one exists (Section 16 requires both source and built-HTML
    coverage). Skipped, not failed, if no build is present -- run
    sphinx-build first for full coverage, as the standard test sequence
    (Section 17) does."""
    failures: list[str] = []
    build_html = DOCS / "_build" / "html"
    if not build_html.is_dir():
        return failures
    for html_file in build_html.rglob("*.html"):
        if ".doctrees" in html_file.parts:
            continue
        lower = html_file.read_text(encoding="utf-8", errors="ignore").lower()
        for term in _BANNED_TERMS:
            if term in _WHOLE_WORD_TERMS:
                continue  # whole-word regex not worth re-running over rendered HTML markup
            if term in lower:
                failures.append(f"{html_file.relative_to(REPO_ROOT)}: banned term found in built HTML: {term!r}")
    return failures


_STALE_IDENTITY_PATTERNS = (
    "Learning-Robotics-Crash-Course",
    "github.io/Learning-Robotics-Crash-Course",
    "MoritzSchallenberg/Learning-Robotics-Crash-Course",
    "/Learning-Robotics-Crash-Course/",
    "docs/course/",
    "Entwicklungsauftrag",
)

# Directories/files this repository actually uses as its own scratch space
# for a throwaway per-check checkout in a test, or that legitimately still
# reference retired names/paths as an explicit historical record rather
# than a live, current claim -- excluded from check_repository_identity()
# by the task's own instruction (maintainers/archive/, .git/, docs/_build/),
# plus this script's own _STALE_IDENTITY_PATTERNS/_BANNED_TERMS definitions,
# which necessarily spell out the exact strings they detect.
_IDENTITY_SCAN_EXCLUDED_DIRS = ("maintainers/archive", ".git", "docs/_build")
_IDENTITY_SCAN_FILE_ALLOWLIST = ("scripts/verify-structure.py",)

_IDENTITY_SCAN_ROOTS = (
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "docs",
    "scripts",
    ".github",
    "requirements.txt",
    "LICENSES.md",
    "DECISIONS_NEEDED.md",
)


def _identity_scan_files() -> list[Path]:
    files: list[Path] = []
    for root_name in _IDENTITY_SCAN_ROOTS:
        root = REPO_ROOT / root_name
        if not root.exists():
            continue
        candidates = [root] if root.is_file() else list(root.rglob("*"))
        for p in candidates:
            if not p.is_file():
                continue
            rel = p.relative_to(REPO_ROOT).as_posix()
            if any(rel.startswith(f"{excluded}/") for excluded in _IDENTITY_SCAN_EXCLUDED_DIRS):
                continue
            if rel in _IDENTITY_SCAN_FILE_ALLOWLIST:
                continue
            files.append(p)
    return files


def check_repository_identity() -> list[str]:
    """The repository was renamed from Learning-Robotics-Crash-Course to
    Spot-Tutorial, and the internal Entwicklungsauftrag task-numbering
    scheme used during development should never leak into active,
    reader-facing or maintainer-facing content. Catches a regression --
    a copy-pasted old link, a stale example path -- before it ships."""
    failures: list[str] = []
    for p in _identity_scan_files():
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = p.relative_to(REPO_ROOT).as_posix()
        for pattern in _STALE_IDENTITY_PATTERNS:
            if pattern in text:
                failures.append(f"{rel}: stale reference found: {pattern!r}")

    # Positive assertions: the correct current values are actually present
    # where it matters most, not just that the wrong ones are absent.
    conf_py = DOCS / "conf.py"
    if conf_py.is_file():
        text = conf_py.read_text(encoding="utf-8")
        if "https://moritzschallenberg.github.io/Spot-Tutorial/" not in text:
            failures.append("docs/conf.py: html_baseurl does not point to the current Spot-Tutorial Pages URL")

    index_md = DOCS / "index.md"
    if index_md.is_file():
        text = index_md.read_text(encoding="utf-8")
        if "github.com/MoritzSchallenberg/Spot-Tutorial/issues" not in text:
            failures.append("docs/index.md: GitHub issue link does not point to MoritzSchallenberg/Spot-Tutorial")

    readme = REPO_ROOT / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        if "https://moritzschallenberg.github.io/Spot-Tutorial/" not in text:
            failures.append("README.md: documentation link does not point to the current Spot-Tutorial Pages URL")

    pages_yml = REPO_ROOT / ".github" / "workflows" / "pages.yml"
    if pages_yml.is_file():
        text = pages_yml.read_text(encoding="utf-8")
        if "Learning-Robotics-Crash-Course" in text or "learning-robotics-crash-course" in text.lower():
            failures.append(".github/workflows/pages.yml: references the old repository path")

    verify_site_py = REPO_ROOT / "scripts" / "verify-site.py"
    if verify_site_py.is_file():
        text = verify_site_py.read_text(encoding="utf-8")
        if "localhost:8899/Spot-Tutorial" not in text:
            failures.append("scripts/verify-site.py: default base URL does not use the current /Spot-Tutorial subpath")

    return failures


def main() -> int:
    all_failures: list[str] = []

    all_failures.extend(check_topic_directories())
    all_failures.extend(check_topic_index_pages())
    all_failures.extend(check_topics_in_root_toctree())
    all_failures.extend(check_no_course_language())
    all_failures.extend(check_no_orphans())
    all_failures.extend(check_manipulation_decision_making_separate())
    all_failures.extend(check_installation_under_ros2())
    all_failures.extend(check_no_stale_removed_dir_links())
    all_failures.extend(check_no_carologistics_content())
    all_failures.extend(check_no_instructor_page())
    all_failures.extend(check_new_title())
    all_failures.extend(check_full_navigation())
    all_failures.extend(check_history_section_present())
    all_failures.extend(check_operating_pages_present())
    all_failures.extend(check_architecture_pages_present())
    all_failures.extend(check_image_alt_text())
    all_failures.extend(check_banned_terms())
    all_failures.extend(check_no_sensitive_network_data())
    all_failures.extend(check_maintainers_not_public())
    all_failures.extend(check_banned_terms_in_build())
    all_failures.extend(check_no_duplicate_video_urls())
    all_failures.extend(check_video_cards_carry_metadata())
    all_failures.extend(check_only_new_substitutions_used())
    all_failures.extend(check_repository_identity())

    print("=== verify-structure.py results ===")
    if all_failures:
        for f in all_failures:
            print(f"  [FAIL] {f}")
        print(f"\n{len(all_failures)} failure(s)")
        return 1

    print(
        f"All structural checks passed for {len(PRIMARY_NAV_DIRS)} primary-nav "
        f"sections ({len(BACKGROUND_DIRS)} background directories)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
