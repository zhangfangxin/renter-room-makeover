#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合租房改造采购清单汇总工具。

用途：把采购清单从 JSON 汇总成 Markdown 表格，自动计算小计、分档合计、
总价区间、可带走占比，并与预算上限比对。避免人工加总出错。

用法：
    python budget_sheet.py plan.json
    python budget_sheet.py plan.json --out 采购清单.md
    python budget_sheet.py plan.json --tier A B      # 只统计指定档位

输入 JSON 格式：
{
  "title": "合租主卧改造",
  "budget_cap": 800,
  "items": [
    {
      "name": "暖光灯带 5m",
      "price": 35,              # 单一价格；或改用 price_low / price_high 表示区间
      "qty": 2,
      "tier": "A",              # A 急救 / B 舒适 / C 进阶 / D 大改
      "damage": "L1",           # L0 摆放 / L1 可逆粘贴 / L2 免打孔 / L3 微损
      "portable": true,         # 退租能否带走
      "channel": "拼多多",       # 可选
      "purpose": "主氛围光源"    # 可选
    }
  ]
}

说明：任意一项使用 price_low/price_high 时，汇总结果自动切换为区间形式。
"""

import argparse
import json
import sys
from collections import OrderedDict

TIER_NAMES = OrderedDict([
    ("A", "A · 急救包"),
    ("B", "B · 舒适包"),
    ("C", "C · 进阶包"),
    ("D", "D · 大改"),
])
DAMAGE_NAMES = {"L0": "摆放", "L1": "可逆粘贴", "L2": "免打孔", "L3": "微损"}


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def pair(item):
    """返回 (low, high) 单价；缺失字段按 0 处理。"""
    if "price" in item:
        p = float(item["price"])
        return p, p
    return float(item.get("price_low", 0)), float(item.get("price_high", 0))


def money(low, high):
    if abs(high - low) < 0.01:
        return "¥%s" % fmt(low)
    return "¥%s–%s" % (fmt(low), fmt(high))


def fmt(n):
    return ("%d" % n) if abs(n - round(n)) < 0.01 else ("%.2f" % n)


def build(data, tiers=None):
    items = data.get("items", [])
    if tiers:
        tiers = {t.upper() for t in tiers}
        items = [i for i in items if str(i.get("tier", "")).upper() in tiers]

    lines = []
    title = data.get("title", "合租房改造")
    lines.append("# %s · 采购清单\n" % title)

    groups = OrderedDict((k, []) for k in TIER_NAMES)
    for it in items:
        groups.setdefault(str(it.get("tier", "")).upper(), []).append(it)

    total_lo = total_hi = 0.0
    portable_n = 0
    risky = []

    for tier, name in list(groups.items()) + [(k, k) for k in groups if k not in TIER_NAMES]:
        bucket = groups.get(tier) or []
        if not bucket:
            continue
        label = TIER_NAMES.get(tier, tier or "未分档")
        lines.append("\n## %s\n" % label)
        lines.append("| 物品 | 单价 | 数量 | 小计 | 破坏等级 | 可带走 | 渠道 | 作用 |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        sub_lo = sub_hi = 0.0
        for it in bucket:
            lo, hi = pair(it)
            qty = float(it.get("qty", 1))
            lo *= qty
            hi *= qty
            sub_lo += lo
            sub_hi += hi
            if it.get("portable"):
                portable_n += 1
            dmg = str(it.get("damage", "")).upper()
            if dmg == "L3":
                risky.append(it.get("name", "?"))
            lines.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
                it.get("name", ""),
                money(*pair(it)),
                fmt(qty),
                money(lo, hi),
                ("%s %s" % (dmg, DAMAGE_NAMES.get(dmg, ""))).strip(),
                "★" if it.get("portable") else "—",
                it.get("channel", "—"),
                it.get("purpose", "—"),
            ))
        lines.append("\n**小计：%s**\n" % money(sub_lo, sub_hi))
        total_lo += sub_lo
        total_hi += sub_hi

    lines.append("\n---\n")
    lines.append("## 汇总\n")
    lines.append("- 物品总数：**%d** 件" % len(items))
    lines.append("- **总预算：%s**" % money(total_lo, total_hi))
    if items:
        lines.append("- 可带走比例：**%d%%**（%d/%d 件）" % (
            round(portable_n * 100.0 / len(items)), portable_n, len(items)))
    cap = data.get("budget_cap")
    if cap:
        cap = float(cap)
        if total_hi <= cap:
            verdict = "✅ 控制在预算 ¥%s 以内（上限价仍有 ¥%s 余量）" % (
                fmt(cap), fmt(cap - total_hi))
        elif total_lo <= cap:
            verdict = "⚠️ 上限价 ¥%s 略超预算 ¥%s，建议砍掉 C 档或找平替" % (
                fmt(total_hi), fmt(cap))
        else:
            verdict = "❌ 超预算 ¥%s，必须压缩（优先砍非 ★ 项与装饰类）" % fmt(
                total_lo - cap)
        lines.append("- 预算上限 ¥%s：%s" % (fmt(cap), verdict))
    if risky:
        lines.append("- `[需房东同意]` 项：**%s**" % "、".join(risky))
        lines.append("  - 以上项目涉及打孔/更换固定件，需先征得房东同意并保留原件")
    lines.append("\n> 价格为参考区间，随城市与平台浮动，实际以购买时为准。")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="合租房改造采购清单汇总")
    ap.add_argument("plan", help="采购清单 JSON 文件路径")
    ap.add_argument("--out", help="输出 Markdown 文件路径（默认打印到标准输出）")
    ap.add_argument("--tier", nargs="*", help="只统计指定档位，如 A B")
    args = ap.parse_args()

    try:
        data = load(args.plan)
    except FileNotFoundError:
        print("找不到文件：%s" % args.plan, file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print("JSON 解析失败：%s" % e, file=sys.stderr)
        return 1

    text = build(data, args.tier)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print("已写入 %s" % args.out)
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
