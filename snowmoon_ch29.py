"""
Snowmoon — Chapter 29: "The Eve of Battle"
An audiovisual adaptation of a scene from Vitalik Buterin's Snowmoon (GPLv3).
Scene: https://vitalik.eth.limo/snowmoon/html/chapter-29.html
Bounty: https://poidh.xyz/mainnet/bounty/34

Style: minimal motion graphics. Silhouette figures, layered pines, snow, sky
color graded from sunrise to dusk. Subtitled dialogue from the source text.
Render:  python -m manim -qh --disable_caching snowmoon_ch29.py EveOfBattle
"""
from manim import *
import math
import random

# ---- palette (cool nordic, graded by time of day) --------------------------
SKY_DAWN   = "#2c3550"
SKY_DAY    = "#7a94ad"
SKY_DUSK   = "#5d4a63"
SKY_NIGHT  = "#141824"
SUN_COLOR  = "#f2d9a0"
PINE_DARK  = "#0f1f1a"
PINE_MID   = "#17352b"
PINE_LIGHT = "#22493c"
SNOW       = "#e8eef4"
SILVER     = "#c8d2dc"
TEXT_COLOR = "#e6edf3"
WARM_ACC   = "#d9a06b"

random.seed(3725)  # chapter year


def pine_polygon(cx: float, base_y: float, w: float, h: float, color) -> Polygon:
    """A stylized pine: three stacked triangles + trunk."""
    pts = []
    for i, (ww, hh) in enumerate([(1.0, 0.45), (0.78, 0.40), (0.52, 0.35)]):
        level = h * (0.30 + 0.35 * i)
        pts += [
            [cx - w * ww / 2, base_y + level, 0.0],
            [cx + w * ww / 2, base_y + level, 0.0],
            [cx, base_y + level + h * hh * 1.6, 0.0],
        ]
    return Polygon(
        *pts,
        stroke_width=0,
        fill_color=color,
        fill_opacity=1,
    )


def pine_row(count, x0, x1, base_y, w_max, h_max, color, depth_jitter=0.25):
    group = VGroup()
    step = (x1 - x0) / count
    for i in range(count + 2):
        cx = x0 + step * i + random.uniform(-step * 0.35, step * 0.35)
        w = w_max * random.uniform(0.6, 1.15)
        h = h_max * random.uniform(0.6, 1.15) * (1 + depth_jitter * random.uniform(-1, 1))
        group.add(pine_polygon(cx, base_y + random.uniform(-0.1, 0.1), w, h, color))
    return group


def snow_field(width, base_y, color=SNOW, opacity=0.9):
    return Rectangle(width=width, height=10, stroke_width=0,
                     fill_color=color, fill_opacity=opacity).move_to([0, base_y - 5, 0])


class EveOfBattle(Scene):
    def construct(self):
        self.camera.background_color = SKY_DAWN
        W = config.frame_width
        H = config.frame_height

        # ---------------------------------------------------------- sky cycle
        sky = Rectangle(width=W * 2, height=H * 2, stroke_width=0)
        sky.move_to(ORIGIN)
        sky.set_fill(SKY_DAWN, opacity=1)
        self.add(sky)

        def sky_color(t):
            """t in [0,1]: dawn -> day -> dusk -> night."""
            keys = [(0.0, SKY_DAWN), (0.35, SKY_DAY), (0.7, SKY_DUSK), (1.0, SKY_NIGHT)]
            for (t0, c0), (t1, c1) in zip(keys, keys[1:]):
                if t0 <= t <= t1:
                    local = (t - t0) / (t1 - t0)
                    return ManimColor.interpolate(ManimColor(c0), ManimColor(c1), local)
            return ManimColor(SKY_NIGHT)

        # ------------------------------------------------------- ground/snow
        snow_near = snow_field(W * 1.4, -2.6)
        snow_far  = snow_field(W * 1.4, -1.4, opacity=0.75)
        hill      = Arc(radius=6, start_angle=-math.pi / 2, angle=math.pi / 2,
                        stroke_width=0, fill_color=SNOW, fill_opacity=0.95)\
                     .scale([1.4, 0.35, 1]).move_to([-2.0, -2.3, 0])

        pines_back  = pine_row(14, -W, W, -1.3, 1.6, 1.9, PINE_MID).set_opacity(0.55)
        pines_mid   = pine_row(11, -W, W, -2.2, 2.2, 2.8, PINE_LIGHT)
        pines_near  = pine_row(8, -W, W, -3.1, 3.0, 3.6, PINE_DARK)
        self.add(snow_far, hill, snow_near, pines_back, pines_mid, pines_near)

        # ------------------------------------------------------ sun position
        sun = Circle(radius=0.32, stroke_width=0, fill_color=SUN_COLOR, fill_opacity=0.95)
        glow = Circle(radius=0.85, stroke_width=0, fill_color=SUN_COLOR, fill_opacity=0.20)
        sun.add_updater(lambda m: None)
        glow.add_updater(lambda m: None)
        sun.move_to([-4.0, -0.2, 0]); glow.move_to(sun)
        self.add(glow, sun)

        def set_time(t):
            # sky
            sky.set_fill(sky_color(t), 1)
            # sun arc across the sky (left dawn -> center noon -> right set)
            ang = math.pi * (1 - t)          # pi (left) -> 0 (right)
            radius = 4.2
            cx = -1.0
            sun.move_to([cx + radius * math.cos(ang), -0.6 + 2.8 * math.sin(ang), 0])
            glow.move_to(sun.get_center())
            glow.set_fill(SUN_COLOR, 0.20 * (1 - t * 0.5))
            # silhouettes darken as light fades
            fade = 1 - 0.55 * t
            pines_back.set_opacity(0.55 * fade)
            pines_mid.set_opacity(0.9 * fade)
            pines_near.set_opacity(fade)

        # ------------------------------------------------------- characters
        def figure(color=PINE_DARK, scale=1.0):
            head = Circle(radius=0.09 * scale, stroke_width=0, fill_color=color, fill_opacity=1)
            body = RoundedRectangle(corner_radius=0.04 * scale, width=0.20 * scale,
                                    height=0.42 * scale, stroke_width=0,
                                    fill_color=color, fill_opacity=1)
            body.move_to(head.get_center() + DOWN * 0.32 * scale)
            return VGroup(head, body)

        zei = figure(PINE_DARK, 1.0).move_to([-0.4, -1.35, 0])
        mu  = figure(PINE_DARK, 1.05).move_to([0.25, -1.38, 0])
        bai = figure(PINE_DARK, 0.95).move_to([-1.3, -1.45, 0])
        self.add(zei, mu)

        # ------------------------------------------------------------ snow FX
        flakes = VGroup()
        for _ in range(60):
            fx = random.uniform(-W / 2, W / 2)
            fy = random.uniform(-H / 2, H / 2)
            r = random.uniform(0.012, 0.035)
            flakes.add(Dot(point=[fx, fy, 0], radius=r, color=SNOW,
                           fill_opacity=random.uniform(0.35, 0.9)))
        flakes.add_updater(lambda m, dt: [
            f.shift(LEFT * dt * random.uniform(0.08, 0.25) +
                    DOWN * dt * random.uniform(0.12, 0.38)) for f in m])
        self.add(flakes)

        # ------------------------------------------------------- subtitle box
        def subtitle(txt, hold=2.2):
            line = Paragraph(txt, font_size=26, color=TEXT_COLOR, line_spacing=0.5,
                             alignment="center")
            plate = RoundedRectangle(corner_radius=0.12, width=line.width + 0.6,
                                     height=line.height + 0.4, stroke_width=0,
                                     fill_color="#000000", fill_opacity=0.55)
            grp = VGroup(plate, line).move_to([0, -2.9, 0])
            self.play(FadeIn(grp, run_time=0.35))
            self.wait(hold)
            self.play(FadeOut(grp, run_time=0.3))

        # =========================================================== SCENE
        # 1) cold open title
        t1 = Text("Elenar Forest, Veridia", font_size=34, color=TEXT_COLOR)
        t2 = Text("Snowmoon 29 — year 3725", font_size=22, color=SILVER).next_to(t1, DOWN)
        self.play(Write(t1), FadeIn(t2), run_time=1.4)
        self.wait(1.2)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.8)
        set_time(0.02)

        # 2) dialogue: Mu & Zei on the hill
        subtitle("Mu: “So this is where our future will be decided.”", 2.4)
        subtitle("Zei: “Do you think we're ready?”", 2.0)
        subtitle("Mu: “No. But nothing meaningful ever happens\nwhen people are ready.”", 3.0)
        subtitle("Mu: “What we hope is that the Arctics are less ready than we are.”", 2.8)

        # 3) Bai arrives — walk in + hug
        self.play(bai.animate.move_to([-0.05, -1.42, 0]), run_time=1.8, rate_func=linear)
        subtitle("Bai: “Whatever happens today, Zei,\nI am happy that I got to know you.”", 3.0)

        # 4) command bunker — briefing overlay (stylized map)
        self.play(AnimationGroup(
            *[Succession(
                Wait(0),
                AnimationGroup()  # placeholder no-op
            )],
        ), run_time=0.01) if False else None
        # animate time to noon-ish manually (frame-based updater)
        time_state = {"t": 0.02}
        def time_updater(_m, dt):
            time_state["t"] = min(1.0, time_state["t"] + dt / 1.6 * 0.43)
            set_time(time_state["t"])
        sky.add_updater(time_updater)
        self.wait(1.6)
        sky.remove_updater(time_updater)
        set_time(0.45)

        map_board = RoundedRectangle(corner_radius=0.15, width=7.2, height=3.4,
                                     stroke_color=SILVER, stroke_width=1.2,
                                     fill_color="#0b1d17", fill_opacity=0.92)
        map_title = Text("OPERATION ORDER — SUNDOWN", font_size=20, color=WARM_ACC)\
            .next_to(map_board.get_top(), DOWN, buff=0.15)
        groups = VGroup()
        data = [("NORTH",  "cross forest → coast perimeter", WARM_ACC),
                ("CENTER", "pin the Arctic drone corps",    SILVER),
                ("SOUTH",  "perimeter on Northglade",       SILVER),
                ("NAVAL",  "seaborne drones — Northshore",  SILVER)]
        for i, (name, task, c) in enumerate(data):
            g_name = Text(name, font_size=22, color=c)
            g_task = Text(task, font_size=15, color=TEXT_COLOR).next_to(g_name, DOWN, buff=0.1)
            row = VGroup(g_name, g_task).arrange(DOWN, buff=0.08)
            groups.add(row)
        groups.arrange(RIGHT, buff=0.5).move_to(map_board.get_center() + DOWN * 0.25)
        self.play(FadeIn(map_board), Write(map_title), LaggedStart(*[FadeIn(g) for g in groups],
                  lag_ratio=0.2), run_time=2.2)
        self.wait(1.6)
        self.play(FadeOut(map_board), FadeOut(map_title), FadeOut(groups), run_time=0.8)

        # 5) the drone fleet + fiber optics at dusk
        #    (remove characters' hill, wide shot feeling)
        def time_updater2(_m, dt):
            time_state["t"] = min(1.0, time_state["t"] + dt / 2.0 * 0.27)
            set_time(time_state["t"])
        sky.add_updater(time_updater2)
        self.wait(2.0)
        sky.remove_updater(time_updater2)
        set_time(0.72)

        drones = VGroup()
        for _ in range(140):
            dx = random.uniform(-W / 2, W / 2)
            dy = random.uniform(-2.9, -1.6)
            drones.add(Dot(point=[dx, dy, 0], radius=random.uniform(0.015, 0.035),
                           color=PINE_DARK, fill_opacity=0.95))
        cables = VGroup()
        anchors = drones[::14]
        for a in anchors:
            start = np.array(a.get_center(), dtype=float)
            seg_points = [start]
            for k in range(1, 6):
                nxt = start + RIGHT * 1.1 * k + DOWN * 0.16 * k + UP * random.uniform(-0.06, 0.06)
                seg_points.append(np.array([nxt[0], nxt[1], 0.0]))
            for i in range(len(seg_points) - 1):
                cables.add(Line(seg_points[i], seg_points[i + 1],
                                stroke_color=SILVER, stroke_width=1.1,
                                stroke_opacity=0.6))
        self.play(FadeIn(drones, lag_ratio=0.02), run_time=1.4)
        self.play(Create(cables), run_time=1.6)

        subtitle("Bai: “Wait — is that a box of printers on one of the drones?”", 2.8)
        subtitle("Fiber optic cables. Hundreds of kilometers,\nstretched to keep a mind in contact with its swarm.", 3.2)

        # 6) night falls — the line that earns the frame
        def time_updater3(_m, dt):
            time_state["t"] = min(1.0, time_state["t"] + dt / 2.4 * 0.28)
            set_time(time_state["t"])
        sky.add_updater(time_updater3)
        self.wait(2.4)
        sky.remove_updater(time_updater3)
        set_time(1.0)
        subtitle("Zei: “All that time, he had been training for\nthe one game that really mattered: tonight.”", 3.4)

        # 7) credits
        c1 = Text("An adaptation of Snowmoon", font_size=28, color=TEXT_COLOR)
        c2 = Text("by Vitalik Buterin — Chapter 29", font_size=20, color=SILVER).next_to(c1, DOWN)
        c3 = Text("AI-assisted motion graphics · pipeline open-sourced (GPLv3)",
                  font_size=16, color=SILVER).next_to(c2, DOWN, buff=0.35)
        self.play(FadeOut(drones), FadeOut(cables), FadeOut(flakes),
                  FadeIn(c1), FadeIn(c2), FadeIn(c3), run_time=1.4)
        self.wait(2.0)
        self.play(FadeOut(c1), FadeOut(c2), FadeOut(c3))
        self.wait(0.3)
