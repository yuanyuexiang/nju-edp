# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A Chinese-language deliverable package for Nanjing University EDP (Executive Development Programs) admissions marketing: strategy research, execution plans, spreadsheet templates, compliance checklists, and client-review creative assets (30-second vertical brand videos and posters). It is not a software project. The only executable code is the video renderer at `assets/video/edp-brand-demo-v1/build_video.py`, which belongs to a pre-existing client-review asset. The owner's goal for this package is the marketing strategy and its execution; do not produce new videos or posters unless explicitly asked.

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
python3 assets/video/edp-brand-demo-v1/build_video.py
```

This overwrites that directory's `.mp4` and `招生视频封面.jpg` in place. To produce a new version, copy the whole directory to a new `-vN` slug first. `production/` (intermediate audio, keyframes, `narration.json`) is gitignored. Verify a render by viewing `production/scene-1..5.jpg` and running `ffprobe` on the output.

## How the deliverables fit together

Files are numbered `NN-中文标题.md|csv` and `README.md` is the index: every new deliverable must be added there, and the README's `更新日期` line is bumped on each release of the package. The numbers encode a dependency chain rather than just ordering:

- `01` strategy report is the root. `02` (90-day plan) executes it week by week; `06` (interview guides) is the demand-validation gate that `02` and the README require before paid spend scales. `14` is the scaled-down three-person version of `02` + `08`; it changes cadence and scope only, never thresholds.
- `03` is the 12-week content/activity calendar for `02`. `08` (four-platform study: 公众号, 抖音, 小红书, 微博) is expanded into `09`, its executable 30-day publishing schedule.
- `04` (lead/opportunity sheet), `11` (append-only follow-up log) and `12` (cohort conversion) are the data layer; `05` is the weekly operations dashboard. `08` §3.2 is the channel-code spec that `09`, `04`, `16` and `17` follow: `平台前缀-母题代码-两位序号` (WX/DY/XHS/WB/BD/WEB/EVENT/PARTNER/REF/ALL, paid units prefixed `AD-`), e.g. `DY-AI-01`, `EVENT-AI-01`, `WEB-OFFICIAL-01`.
- `10` (whether to build an admissions system / lightweight CRM) cites `01`, `03`, `05`, `08`, `09`; its §2.1 lists the template limitations that the 2026-09-11 revision of `04`/`05`/`11`/`12` addresses.
- `13` (banned / approval-gated wording) is the checklist every outward-facing text is checked against; `15` holds the landing-page checklist and the B2B one-page hypothesis template referenced from `01` §7 and §10.
- `16` is the evidence-graded channel study (A = author re-verified, B = official page verified by a research line, C = third-party/media, D = self-reported). It refines `01` §6.2 and `08` rather than replacing them; its §8 30-day plan feeds `04`/`05`/`12`. Sources are `07` items 37–82.
- `17` is the system blueprint that turns `10`'s decision into a configurable spec: six tables (联系人/企业/线索/跟进/项目班次/内容渠道; `04` is the 联系人⋈线索 export view, consent lives on 联系人), eight intake channels, stage entry conditions, seven views, twelve automation rules (R1–R12), a permission matrix, and the 30-day build order that mirrors `10` §9. Its acceptance criterion is end-to-end traceability from content/channel to paid enrolment. Keep it platform-neutral; 飞书多维表格 is only the pilot default.
- `18` is the channel-API feasibility study: an official API existing, the school's account being approved for it, and a real call succeeding are three separate checks. `17` §4.4 (interaction inbox) and §4.5 (API gates) follow it. Sources are `07` items 83–114.
- `19` is a separate content-production service plan with a POC spec (one article, three posters, one video). It is a plan; it does not widen `17` §5.4's AI limits, and producing actual creative assets still needs an explicit ask. Sources are `07` items 115–120.
- `20` is the competitor study for 小红书/抖音/公众号/视频号 plus website lead capture only; offline events, institutional partnerships, alumni and search channels stay in `16` §三/§五. Its evidence grades (A/B/C/U) are local to that file and differ from `16`'s. Keep 学院, EE/EDP and MBA layers separate; a procurement notice proves a target, never a result. Sources are `07` items 121–150.
- `21` is the ledger of the center's own channels and accounts. It separates "an account exists" from "it is being operated"; "待确认" means insufficient evidence, never zero. §3.4 lists look-alike third-party pages. It supersedes `16` §二 on current-state facts. Sources are `07` items 151–188.
- `07` is the single source register for all documents. Entries are numbered continuously across sections in the form `N. [title](url)——publish date or "未标日期"/"动态页面". what it supports; caveats`. New research is added as a dated `## …补充（YYYY-MM-DD）` section that continues the numbering and states which document it serves. Re-verification results (dead links, changed pages) also go there. University list pages paginate and drift (a cited `listm4.htm` later stopped containing the item), so cite the article URL rather than the list page, and treat search-engine snippets as leads that must be labelled as not directly read.

### CSV template gotchas

- One row in `04` = one contact's intent for one project; the same person with two projects is two rows sharing `联系人ID`. `04` keeps only the current snapshot; history goes in `11`. Source is split into 首次/最近/用户自报; consent has time, notice version, purpose and withdrawal columns.
- `05` ratios are same-period ratios (`同期…比`), not conversion rates; cohort conversion lives in `12`, grouped by first-effective-lead month × class. Both use `=IF(denominator=0,"暂无有效样本",…)` rather than `IFERROR(...,0)` so an empty period is not read as 0%.
- Formula columns reference count columns by letter (`05`: P=N−O, S–X reference F/G/H/K/M/P/Q/R; `12`: J=H−I, M–P reference D/E/F/H/J). Inserting or moving a column silently breaks them; fix the letters whenever a header changes.
- Sample rows are marked `示例行请删除` in the last column and must stay clearly labeled. Never commit real lead data.
- Fields containing commas (including every formula, which also contains quoted Chinese) are double-quoted; keep files UTF-8.

### Creative assets

`assets/video/<slug>-vN/` and `assets/posters/<slug>-vN/` each carry a README recording date, specs, what was deliberately excluded, differences from the previous version, and how to regenerate. Posters keep their full generation prompt in `prompt.txt`. Version by copying to a new directory, not by editing in place.

In `build_video.py`, `SCENES` is the single source of truth: each tuple is `(start, end, TTS narration, subtitle lines)` and drives both the per-scene visuals in `scene_layer()` and the voice track in `sound()`. Narration spells letters with spaces (`E D P`) so the TTS reads them out; subtitles use the normal spelling. Each voice clip is time-stretched with `atempo` to fit its scene minus 1.15 s, so a longer line gets faster rather than overflowing; keep narration lines about the length of the existing ones or they sound rushed. Headline strings are sized to fit the 900 px column at their font size (roughly 7 CJK characters at size 100); check keyframes after changing copy. `frame(t)` composites background, gold geometry, the scene layer (cross-faded for the first 0.45 s of a scene), and fixed chrome (header, 创意提案 pill, subtitles, progress bar, footer).

## Content rules that apply everywhere

These come from the README, `13`, and the asset READMEs and constrain any edit:

- Tuition, seat counts, start dates, faculty, certificates, and alumni benefits that are not publicly verifiable must be marked as assumptions and deferred to the center's approved wording. Documents distinguish verified facts from operating assumptions explicitly; keep that distinction.
- Run outward-facing copy against `13`: no absolute or ranking terms, no outcome promises, no testimonials as endorsements, no degree/学历 wording for EDP, and price/date/seat/faculty claims only with an approval document.
- Creative assets are proposals: keep the `创意提案` / `非正式招生发布` marks, the `非学历教育` disclaimer, and the `edp.nju.edu.cn` official entry. Do not add the school crest, professor portraits, student testimonials, fabricated campus or classroom imagery, prices, dates, or outcome promises. Program names in them come only from the verified official program list (`07` item 3); regional wording like 长三角 is creative context, not a claim about the center's official scope.
- Any new public source goes into `07-来源清单.md` with its verification date and caveats.
- There is no root `.gitignore`; do not stage `.DS_Store` files.
