# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A Chinese-language deliverable package for Nanjing University EDP (Executive Development Programs) admissions marketing: strategy research, execution plans, spreadsheet templates, and client-review creative assets (a 30-second vertical brand video and a poster). It is not a software project. The only executable code is the video renderer at `assets/video/edp-brand-demo-v1/build_video.py`.

All content is written in simplified Chinese. `AGENTS.md` holds additional conventions (commit/PR style, research handling) and should be read alongside this file.

## Commands

There is no build, lint, or test suite. Useful checks:

```sh
git diff --check                       # whitespace errors before committing
rg '^#{1,3} ' -- *.md                  # heading structure of the documents
```

Validate every CSV after editing (all nonblank rows must match the header's column count):

```sh
python3 - <<'EOF'
import csv, glob
for p in sorted(glob.glob("*.csv")):
    rows = list(csv.reader(open(p, encoding="utf-8")))
    n = len(rows[0])
    bad = [(i + 1, len(r)) for i, r in enumerate(rows) if r and len(r) != n]
    print(p, "OK" if not bad else f"BAD (line, cols): {bad}")
EOF
```

Regenerate the brand video (macOS only; needs Python 3, Pillow, NumPy, ffmpeg/ffprobe, the system `Tingting` voice, and the STHeiti/Arial system fonts):

```sh
python3 assets/video/edp-brand-demo-v1/build_video.py
```

This overwrites the `.mp4` and `招生视频封面.jpg` in place. To produce a new version, copy the whole directory to a new `-vN` slug first. `production/` (intermediate audio, keyframes, `narration.json`) is gitignored.

## How the deliverables fit together

Files are numbered `NN-中文标题.md|csv` and `README.md` is the index: every new deliverable must be added there, and the README's `更新日期` line is bumped on each release of the package. The numbers encode a dependency chain rather than just ordering:

- `01` strategy report is the root. `02` (90-day plan) executes it week by week; `06` (interview guides) is the demand-validation gate that `02` and the README require before paid spend scales.
- `03` is the 12-week content/activity calendar for `02`. `08` (four-platform study: 公众号, 抖音, 小红书, 微博) is expanded into `09`, its executable 30-day publishing schedule.
- `04` (lead CRM template) and `05` (metrics dashboard) are the data layer everything else reports into. `09`'s `渠道码` column (platform prefix + theme + sequence, e.g. `DY-AI-01`, `WX-AI-01`, `ALL-OFFICIAL-01`) is what lands in `04`'s `来源一级/来源二级/渠道码` columns.
- `10` (whether to build an admissions system / lightweight CRM) cites `01`, `03`, `05`, `08`, `09` and the README's launch sequence step 6.
- `07` is the single source register for all documents. Entries are numbered continuously across sections in the form `N. [title](url)——publish date or "未标日期"/"动态页面". what it supports; caveats`. New research is added as a dated `## …专项补充（YYYY-MM-DD）` section that continues the numbering and states which document it serves (see the 2026-09-07 section for `10`).

### CSV template gotchas

- `05` formula columns (`有效线索率` through `营销回收倍数`, columns Q–V) reference count columns by letter (`=IFERROR(G2/F2,0)`, `(O2+P2)/M2`, etc.). Inserting or moving a column silently breaks them; fix the letters whenever the header changes.
- Sample rows are marked `示例行请删除` in the last column and must stay clearly labeled. Never commit real lead data into `04`.
- Fields containing commas (including every formula) are double-quoted; keep files UTF-8.

### Creative assets

`assets/video/<slug>-vN/` and `assets/posters/<slug>-vN/` each carry a README recording date, specs, what was deliberately excluded, and how to regenerate. The poster keeps its full generation prompt in `prompt.txt`. Version by copying to a new directory, not by editing in place.

In `build_video.py`, `SCENES` is the single source of truth: each tuple is `(start, end, TTS narration, subtitle lines)` and drives both the per-scene visuals in `scene_layer()` and the voice track in `sound()`. Narration text spells `E D P` with spaces so the TTS pronounces the letters; subtitles use `EDP`. Each voice clip is time-stretched with `atempo` to fit its scene minus 1.15 s, so lengthening a line makes it faster rather than overflowing. `frame(t)` composites background, gold geometry, the scene layer (cross-faded for the first 0.45 s of a scene), and fixed chrome (header, 创意提案 pill, subtitles, progress bar, footer).

## Content rules that apply everywhere

These come from the README and the asset READMEs and constrain any edit:

- Tuition, seat counts, start dates, faculty, certificates, and alumni benefits that are not publicly verifiable must be marked as assumptions and deferred to the center's approved wording. Documents distinguish verified facts from operating assumptions explicitly; keep that distinction.
- Creative assets are proposals: keep the `创意提案` / `非正式招生发布` marks, the `非学历教育` disclaimer, and the `edp.nju.edu.cn` official entry. Do not add the school crest, professor portraits, student testimonials, fabricated campus or classroom imagery, prices, dates, or outcome promises. Only claims verified on the official EDP site (个人提升, 企业定制, official consultation entry) appear in them.
- Any new public source goes into `07-来源清单.md` with its verification date and caveats.
- There is no root `.gitignore`; do not stage `.DS_Store` files.
