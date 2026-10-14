# Snowmoon â€” Chapter 29: "The Eve of Battle" (motion graphics adaptation)

> An audiovisual adaptation of a scene from Vitalik Buterin's *Snowmoon* (GPLv3).
> Submitted to the ["Bring Snowmoon to Life" bounty](https://poidh.xyz/mainnet/bounty/34)
> on poidh.xyz.

**Source scene:** [Chapter 29 â€” Elenar Forest, Veridia](https://vitalik.eth.limo/snowmoon/html/chapter-29.html)

**What this is:** a ~55-second motion-graphics short depicting the night before
the Veridian counteroffensive â€” Zei, Mu and Bai on a snowy hill while the drone
armies and their fiber-optic tether networks wait for sundown.

## Watch

- Video: (link to public X post â€” filled after posting)
- Claim: https://poidh.xyz/mainnet/bounty/34 (claim link after submission)

## Why AI-assisted filmmaking is allowed here

The bounty explicitly welcomes "AI-assisted or AI-generated filmmaking". The
novel itself is GPLv3 and Vitalik asks only that meaningful production materials
be open-sourced â€” which is exactly what this repository is for.

## How this was made (the open pipeline)

Everything below was produced by an AI agent (OpenCode running GLM), with the
following transparent process:

### 1. Scene selection
The agent downloaded all 32 chapters from the official site
(`vitalik.eth.limo/snowmoon`), skimmed chapter openings, and picked Chapter 29
for its visual clarity (snow hill, dawn-to-night arc, drone swarm, fiber optic
cables), emotional completeness (three characters, one quiet moment), and
self-contained dialogue (no external context needed).

### 2. Screenwriting / shot list
Adapted directly from Buterin's text â€” dialogue lines are verbatim from the
chapter. The agent wrote the shot list in the file header
(`snowmoon_ch29.py` docstring):
1. cold-open title (place + date)
2. hill dialogue (Mu/Zei)
3. Bai's arrival + hug
4. briefing overlay (Operation Order, 4 groups)
5. drone swarm + fiber-optic lines at dusk
6. nightfall + the "training for tonight" line
7. credits

### 3. Code as film (manim)
The `snowmoon_ch29.py` file IS the film. Layout, palettes (SKY_DAWN â†’ SKY_NIGHT),
character silhouettes, snow particles, drone field, cable segments, subtitles
and the map overlay are all code. No image assets, no pretrained video model.
Rendering is deterministic (`random.seed(3725)`).

### 4. Rendering
```
python -m manim -qh --fps 30 --disable_caching snowmoon_ch29.py EveOfBattle
```
Output: `media/videos/snowmoon_ch29/1080p30/EveOfBattle.mp4`
CPU-only (Intel UHD 620 laptop) â€” no GPU required, that is the point of the
code-as-film approach.

## Reproduce

```bash
pip install manim          # requires ffmpeg on PATH
python -m manim -qh --fps 30 --disable_caching snowmoon_ch29.py EveOfBattle
```

## License

This adaptation is released under **GPLv3**, same as Snowmoon. The source
novel is Â© Vitalik Buterin, GPLv3: https://vitalik.eth.limo/snowmoon/

