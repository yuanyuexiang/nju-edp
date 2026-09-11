# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A Chinese-language deliverable package for Nanjing University EDP (Executive Development Programs) admissions marketing: strategy research, execution plans, spreadsheet templates, compliance checklists, and client-review creative assets (30-second vertical brand videos and posters). It is not a software project. The only executable code is the video renderer, one copy per version under `assets/video/edp-brand-demo-vN/build_video.py`.

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

Regenerate a brand video (macOS only; needs Python 3, Pillow, NumPy, ffmpeg/ffprobe, the system `Tingting` voice, and the STHeiti/Arial system fonts):

```sh
python3 assets/video/edp-brand-demo-v2/build_video.py
```

This overwrites that directory's `.mp4` and `招生视频封面.jpg` in place. To produce a new version, copy the whole directory to a new `-vN` slug first. `production/` (intermediate audio, keyframes, `narration.json`) is gitignored. Verify a render by viewing `production/scene-1..5.jpg`, running `ffprobe` on the output, and checking the per-scene `tempo` values in `narration.json` stay near 1.0 (see below).

## How the deliverables fit together

Files are numbered `NN-中文标题.md|csv` and `README.md` is the index: every new deliverable must be added there, and the README's `更新日期` line is bumped on each release of the package. The numbers encode a dependency chain rather than just ordering:

- `01` strategy report is the root. `02` (90-day plan) executes it week by week; `06` (interview guides) is the demand-validation gate that `02` and the README require before paid spend scales. `14` is the scaled-down three-person version of `02` + `08`; it changes cadence and scope only, never thresholds.
- `03` is the 12-week content/activity calendar for `02`. `08` (four-platform study: 公众号, 抖音, 小红书, 微博) is expanded into `09`, its executable 30-day publishing schedule.
- `04` (lead/opportunity sheet), `11` (append-only follow-up log) and `12` (cohort conversion) are the data layer; `05` is the weekly operations dashboard. `08` §3.2 is the channel-code spec that `09` and `04` follow: `平台前缀-母题代码-两位序号` (WX/DY/XHS/WB/ALL/EVENT, paid units prefixed `AD-`), e.g. `DY-AI-01`, `EVENT-AI-01`.
- `10` (whether to build an admissions system / lightweight CRM) cites `01`, `03`, `05`, `08`, `09`; its §2.1 lists the template limitations that the 2026-09-11 revision of `04`/`05`/`11`/`12` addresses.
- `13` (banned / approval-gated wording) is the checklist every outward-facing text is checked against; `15` holds the landing-page checklist and the B2B one-page hypothesis template referenced from `01` §7 and §10.
- `07` is the single source register for all documents. Entries are numbered continuously across sections in the form `N. [title](url)——publish date or "未标日期"/"动态页面". what it supports; caveats`. New research is added as a dated `## …补充（YYYY-MM-DD）` section that continues the numbering and states which document it serves. Re-verification results (dead links, changed pages) also go there.

### CSV template gotchas

- One row in `04` = one contact's intent for one project; the same person with two projects is two rows sharing `联系人ID`. `04` keeps only the current snapshot; history goes in `11`. Source is split into 首次/最近/用户自报; consent has time, notice version, purpose and withdrawal columns.
- `05` ratios are same-period ratios (`同期…比`), not conversion rates; cohort conversion lives in `12`, grouped by first-effective-lead month × class. Both use `=IF(denominator=0,"暂无有效样本",…)` rather than `IFERROR(...,0)` so an empty period is not read as 0%.
- Formula columns reference count columns by letter (`05`: P=N−O, S–X reference F/G/H/K/M/P/Q/R; `12`: J=H−I, M–P reference D/E/F/H/J). Inserting or moving a column silently breaks them; fix the letters whenever a header changes.
- Sample rows are marked `示例行请删除` in the last column and must stay clearly labeled. Never commit real lead data.
- Fields containing commas (including every formula, which also contains quoted Chinese) are double-quoted; keep files UTF-8.

### Creative assets

`assets/video/<slug>-vN/` and `assets/posters/<slug>-vN/` each carry a README recording date, specs, what was deliberately excluded, differences from the previous version, and how to regenerate. Posters keep their full generation prompt in `prompt.txt` (v2 is prompt-only, image not yet rendered). Version by copying to a new directory, not by editing in place. v1 is the brand-mood direction; v2 is the problem-type-entry direction from `01` §5.1's alternative claim.

In `build_video.py`, `SCENES` is the single source of truth: each tuple is `(start, end, TTS narration, subtitle lines)` and drives both the per-scene visuals in `scene_layer()` and the voice track in `sound()`. Narration spells letters with spaces (`E D P`, `A I`) so the TTS reads them out; subtitles use the normal spelling. Each voice clip is time-stretched with `atempo` to fit its scene minus 1.15 s, so a longer line gets faster rather than overflowing; `narration.json` records the ratio per scene, and anything above about 1.2 sounds rushed, so shorten the line instead. Headline strings are sized to fit the 900 px column at their font size (roughly 7 CJK characters at size 100); check keyframes after changing copy. `frame(t)` composites background, gold geometry, the scene layer (cross-faded for the first 0.45 s of a scene), and fixed chrome (header, 创意提案 pill, subtitles, progress bar, footer).

## Content rules that apply everywhere

These come from the README, `13`, and the asset READMEs and constrain any edit:

- Tuition, seat counts, start dates, faculty, certificates, and alumni benefits that are not publicly verifiable must be marked as assumptions and deferred to the center's approved wording. Documents distinguish verified facts from operating assumptions explicitly; keep that distinction.
- Run outward-facing copy against `13`: no absolute or ranking terms, no outcome promises, no testimonials as endorsements, no degree/学历 wording for EDP, and price/date/seat/faculty claims only with an approval document.
- Creative assets are proposals: keep the `创意提案` / `非正式招生发布` marks, the `非学历教育` disclaimer, and the `edp.nju.edu.cn` official entry. Do not add the school crest, professor portraits, student testimonials, fabricated campus or classroom imagery, prices, dates, or outcome promises. Program names in them come only from the verified official program list (`07` item 3); regional wording like 长三角 is creative context, not a claim about the center's official scope.
- Any new public source goes into `07-来源清单.md` with its verification date and caveats.
- There is no root `.gitignore`; do not stage `.DS_Store` files.
