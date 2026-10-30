# renter-room-makeover 🏠

[中文](README.md) | English

<img src="assets/icon.svg" width="96" align="right" alt="icon">

A room-makeover design Skill for **urban renters and people in shared flats**.

Send it a few photos of your room and it reads the layout, diagnoses the problems,
and produces a makeover plan — low-budget first, no-drill first, and everything
portable when you move out, with feng shui handled in a reversible way.
It can also **render a photorealistic "after" image** so you can see the result at a glance.

> The goal is not "pretty". It's a **sense of belonging** — turning a temporary
> place you might leave at any moment into "my place".

---

## The four bottom lines

Any plan that breaks one of these gets down-ranked or replaced.

| Bottom line | How it's enforced |
| --- | --- |
| **Spend little** | Default total budget ¥200–800 (roughly US$30–110), single items under ¥150. A "spending-efficiency" ranking cuts from the back when over budget |
| **Cause little damage** | Methods graded L0 place-only / L1 removable adhesive / L2 no-drill / L3 minor. L3 must be marked `[landlord approval]` with a restoration method; no wall removal, flooring, or plumbing/electrical changes |
| **Portable** | Prefer things you can pack and take when you move out, marked with ★ |
| **Feng shui, but rationally** | Resolve everything by "move, screen, soften, add" — never structural change. Every tip includes an environmental-psychology explanation; no absolute claims |

---

## Directory structure

```
renter-room-makeover/
├── SKILL.md                      # Main flow: 6-step workflow + 4 hard constraints + key rules
├── references/
│   ├── photo-analysis.md         # Reading photos: shot list, scale-based area estimate, room profile template
│   ├── no-damage-playbook.md     # L0–L3 no-damage techniques, wall-adhesion table, move-out restoration kit
│   ├── fengshui.md               # Reversible feng shui (bed / door / workstation / light color / wealth corner / plants)
│   ├── budget-catalog.md         # Spending-efficiency ranking, 4 budget tiers, price lookup, upgrades → swaps
│   ├── style-recipes.md          # 7 practical style recipes (cream / Japanese / wabi-sabi / industrial / Nordic / dopamine / gaming)
│   └── render-prompts.md         # Photorealistic render prompts (multi-model: MJ / SD / Jimeng / Tongyi Wanxiang / Kling …)
├── scripts/
│   └── budget_sheet.py           # Shopping-list JSON → Markdown summary (tier subtotals / range prices / budget check)
└── assets/
    ├── plan-template.html        # Visual plan-page template (with SVG floor plan, printable)
    └── sample-plan.json          # Example input for budget_sheet.py
```

## Installation

**User-level (available to all projects, recommended):**

```bash
git clone https://github.com/zhangfangxin/renter-room-makeover.git \
  ~/.workbuddy/skills/renter-room-makeover
```

**Project-level (shared with your team):**

```bash
git clone https://github.com/zhangfangxin/renter-room-makeover.git \
  .workbuddy/skills/renter-room-makeover
```

## How to use

After installing, just talk normally — no commands to memorize:

- "I rent the master bedroom in a shared flat. Here are photos — help me redo it, budget $100, no drilling."
- "Can you tell me if the bed is positioned right in this photo?"
- "How do I make my rented room feel cozy?"
- "Give me an after-render so I can see what it'll look like."
- "I'm moving out next month — how do I restore all these changes?"

**How to photograph the room** (the skill will send you this, or check here first):

```
1. One shot from the doorway looking in (door + main furniture)
2. Four diagonal panoramas from each corner (lights on, curtains open, landscape, 0.5x wide)
3. One of the window (frame + sill + view), plus one in natural daylight
4. One of the ceiling (beams, light position)   5. One of the floor (material, damage)
6. One of each landlord-provided fixed furniture   7. One each of bathroom and kitchen
8. Positions of outlets, network port, AC hole   9. Close-ups of flaws: mold, leaks, cracks
```

## What it outputs

1. **Room profile** — area (estimated using a 0.85 m door / 60 cm tile as a ruler), ceiling height, orientation & daylight grade A–D, beams/columns, fixed furniture, outlets, flaws
2. **Problem diagnosis** — each stated as "current state → why it feels bad → how to fix within constraints"
3. **Layout** — SVG floor plan, current vs. after; 1 primary + 1 alternative arrangement
4. **Zone design** — sleep / work / healing corner / storage
5. **Feng shui checklist** — prioritized P0/P1/P2, each with resolution method, reversibility, psychology note
6. **Shopping list** — A/B/C tiers, price ranges, damage grade, ★portable, channel suggestions
7. **Execution plan** — Day 1 (free wins) / Week 1 / Month 1 / move-out restoration
8. **Photorealistic after-render** — with a photo it's image-to-image (keep layout, change only soft furnishing + lighting), without one it's text-to-image (style preview); can produce a "before → after" same-angle comparison. The built-in tool renders directly, or it outputs paste-ready prompts for the platform you name (Midjourney / SD / Jimeng / Tongyi Wanxiang / Kling, etc.)

When you want a "viewable, savable" version, it uses `assets/plan-template.html` to build a visual plan page, with the renders embedded.

---

## A few design trade-offs

Judgments made while writing this skill — not necessarily mainstream, with reasons:

- **Lighting before everything.** Swapping that cold-white ceiling light improves the experience more than almost any other single purchase. 2700–3000K in the bedroom, 4000K at the desk, keep within 500K in one room.
- **Large surfaces before details.** Without touching walls, ~60% of a room's look comes from bedding + curtains + rug. Spend on those first; art and ornaments last.
- **Store by hiding, not by buying cabinets.** Under-bed bins, door-hung pockets, floor-to-ceiling shelves are cheaper and take less space than new cabinets.
- **The first lever of belonging is "control", not "beauty".** A curtain you can close, a lamp you can dim, a rug that's yours, a 0.6 m² corner — these matter far more than art.
- **Don't invent what you can't see.** Orientation, area, beams — if you can't tell, put them in a "to confirm" list instead of guessing.

---

## Budget summary script

Use it when the shopping list is long, to avoid manual adding mistakes:

```bash
python scripts/budget_sheet.py assets/sample-plan.json
python scripts/budget_sheet.py my-plan.json --out shopping-list.md
python scripts/budget_sheet.py my-plan.json --tier A B    # only count specific tiers
```

Input format is in `assets/sample-plan.json`. Supports price ranges (`price_low` / `price_high`) and sums them into a range total, then flags over-budget.

## Notes

- All prices are reference ranges that vary by city and platform; confirm at purchase time.
- Feng shui content is a reference combining traditional dwelling customs and environmental psychology; no luck/fortune promises. What actually matters for living experience — light, ventilation, noise, flow, tidiness — is prioritized first.
- Any suggestion involving drilling or changing fixed fixtures is marked `[landlord approval]`; talk to the landlord and keep the originals.

## License

MIT — modify and use freely.
