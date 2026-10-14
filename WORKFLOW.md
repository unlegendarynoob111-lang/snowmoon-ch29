# Production workflow (AI-assisted, fully documented)

> This document IS the "open-source production pipeline" required by the
> [Bring Snowmoon to Life bounty](https://poidh.xyz/mainnet/bounty/34).
> It explains exactly how the film was made, so another creator can build on it.

## Toolchain

| Layer | Tool | Notes |
|---|---|---|
| Screenwriting | GLM (via OpenCode agent) | selected scene + verbatim dialogue |
| Animation code | manim 0.22.0 (Python) | vector motion graphics |
| Render | manim CLI + ffmpeg | CPU-only, no GPU |
| Editing | single manim scene, no cuts | deterministic render |

## Agent prompt log (truthful)

The whole production was done in a single OpenCode session by an AI agent.
These were the exact generation steps:

1. **Read the brief** — downloaded the bounty page (poidh `/data` endpoint),
   confirmed AI filmmaking explicitly allowed, noted deliverables and deadline.
2. **Acquire the source** — fetched all 32 chapters of the novel from
   `vitalik.eth.limo/snowmoon/html/chapter-N.html`, stripped HTML to plain text,
   saved as `ch-NN.txt` files.
3. **Select a scene** — skimmed openings; scored chapters on visual potential,
   emotional arc, and self-containment. Chose chapter 29 (the eve of the
   Elenar Forest battle).
4. **Write the film as code** — produced `snowmoon_ch29.py` in one shot, then
   iterated on 3 small render bugs (missing `math` import, 2D/3D point shape
   in Polygon/VMobject, and a manim API change for color interpolation).
5. **Preview** — rendered `-ql` (480p15) first, verified layout: subtitle
   legibility, sun arc, silhouette readability, cable growth.
6. **Final render** — `-qh --fps 30` (1080p30), combined to single mp4 by ffmpeg
   inside manim.

## Concrete AI prompts used (excerpt)

- "Read bounty page and summarize requirements + constraints"
- "Download all Snowmoon chapters, strip HTML"
- "Pick the most visually adaptable scene — snow, sky arc, swarm, cables"
- "Write a manim Scene for chapter 29: dawn-to-night sky gradient, three
  silhouette figures, pine layers, snow particles, subtitle dialogue from the
  source text, a briefing map overlay, a drone swarm with growing fiber lines,
  credits. Render CPU-only."

## What another creator can reuse

- `snowmoon_ch29.py` — the entire film as code. Change `SKY_*` palette,
  `subtitle(...)` text, or the drone count, re-render, and you have a new cut.
- `README.md` —Why-this-scene + reproduce instructions.
- The pipeline pattern itself: **code-as-film** (manim) is nearly free to
  iterate on CPU, unlike generative video models — well suited to stylized,
  minimal, literary adaptations under GPLv3.

## Assets NOT included (deliberately)

- The novel text itself (GPLv3 — read it at the official site)
- Any image/video stock assets — none were used
- Any pretrained video model — none were used
