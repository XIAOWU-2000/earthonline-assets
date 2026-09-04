# -*- coding: utf-8 -*-
"""劫怪图库自动化质检：尺寸 / 白底纯度 / 重复图 / 主体占比 / 色彩统计
不依赖人眼，输出可疑清单供人工复核。
"""
import os, sys, json, hashlib
from pathlib import Path
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"E:\ZDY.AI\EarthOnline-Assets")
DIR = ROOT / "02_劫怪" / "concept"

files = sorted(DIR.glob("concept_*.png"))
print(f"扫描文件: {len(files)}")

recs = []
hashes = {}

for f in files:
    try:
        im = Image.open(f).convert("RGB")
    except Exception as e:
        print(f"[损坏] {f.name}: {e}")
        continue
    w, h = im.size
    px = im.load()

    # --- 白底纯度：四角 40x40 区域平均亮度 & 与纯白的距离 ---
    corners = []
    cw = 40
    for (x0, y0) in [(0, 0), (w - cw, 0), (0, h - cw), (w - cw, h - cw)]:
        tot = [0, 0, 0]
        n = 0
        for x in range(x0, x0 + cw, 4):
            for y in range(y0, y0 + cw, 4):
                r, g, b = px[x, y]
                tot[0] += r; tot[1] += g; tot[2] += b; n += 1
        corners.append([c / n for c in tot])
    # 与纯白的最大通道距离
    bg_dist = max(max(255 - c[0], 255 - c[1], 255 - c[2]) for c in corners)
    bg_avg = sum(sum(c) / 3 for c in corners) / 4

    # --- 主体占比：非白像素比例（粗采样）---
    step = 8
    nonwhite = 0
    total = 0
    rs = gs = bs = 0
    for x in range(0, w, step):
        for y in range(0, h, step):
            r, g, b = px[x, y]
            total += 1
            rs += r; gs += g; bs += b
            if (255 - r) + (255 - g) + (255 - b) > 60:  # 明显非白
                nonwhite += 1
    fill = nonwhite / total
    avg = (rs / total, gs / total, bs / total)
    sat = max(avg) - min(avg)  # 整体彩度

    # --- 感知哈希（去重用）---
    small = im.resize((16, 16), Image.LANCZOS).convert("L")
    bits = "".join("1" if p > 128 else "0" for p in small.getdata())
    phash = hashlib.md5(bits.encode()).hexdigest()[:16]

    recs.append({
        "file": f.name,
        "size": f"{w}x{h}",
        "bytes": f.stat().st_size,
        "bg_dist": round(bg_dist, 1),
        "bg_avg": round(bg_avg, 1),
        "fill": round(fill, 3),
        "avg_rgb": [round(c) for c in avg],
        "sat": round(sat, 1),
        "phash": phash,
    })
    hashes.setdefault(phash, []).append(f.name)

# ---------- 报告 ----------
print("\n=== 1. 尺寸异常（非 1024x1024）===")
bad_size = [r for r in recs if r["size"] != "1024x1024"]
print("\n".join(f"  {r['file']}  {r['size']}" for r in bad_size) or "  无")

print("\n=== 2. 白底污染（bg_dist > 25，疑似有背景/场景）===")
bad_bg = sorted([r for r in recs if r["bg_dist"] > 25], key=lambda r: -r["bg_dist"])
print("\n".join(f"  {r['file']}  bg_dist={r['bg_dist']}  bg_avg={r['bg_avg']}" for r in bad_bg[:30]) or "  无")
print(f"  共 {len(bad_bg)} 张")

print("\n=== 3. 重复/近似图（phash 相同）===")
dups = {k: v for k, v in hashes.items() if len(v) > 1}
for k, v in dups.items():
    print(f"  [{k}] {', '.join(v)}")
if not dups:
    print("  无")

print("\n=== 4. 主体占比异常（fill < 0.05 主体过小 / fill > 0.75 铺满）===")
bad_fill = [r for r in recs if r["fill"] < 0.05 or r["fill"] > 0.75]
print("\n".join(f"  {r['file']}  fill={r['fill']}" for r in bad_fill) or "  无")

print("\n=== 5. 尺寸/饱和度分布（供参考）===")
fills = sorted(r["fill"] for r in recs)
print(f"  fill: min={fills[0]} p25={fills[len(fills)//4]} median={fills[len(fills)//2]} p75={fills[len(fills)*3//4]} max={fills[-1]}")
sats = sorted(r["sat"] for r in recs)
print(f"  sat : min={sats[0]} median={sats[len(sats)//2]} max={sats[-1]}")

# 极暗/极亮异常
print("\n=== 6. 整体过暗或过亮（avg亮度 <120 或 >245）===")
bad_lum = [r for r in recs if sum(r["avg_rgb"]) / 3 < 120 or sum(r["avg_rgb"]) / 3 > 245]
print("\n".join(f"  {r['file']}  avg={r['avg_rgb']}" for r in bad_lum) or "  无")

out = ROOT / "14_部件库" / "qa_report.json"
json.dump(recs, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n详细数据已导出: {out}")
