# -*- coding: utf-8 -*-
"""全库两两相似度聚类：找出「长得太像」的劫怪组"""
import sys, json, re, itertools
from pathlib import Path
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(r"E:\ZDY.AI\EarthOnline-Assets")
DIR = ROOT / "02_劫怪" / "concept"

# 槽位映射
s = open(ROOT / "_gen_slots.py", encoding="utf-8").read()
m = re.search(r"MAPPED\s*=\s*\{(.*?)\n\}", s, re.S)
pairs = re.findall(r'"([A-Z]{3}-\d{2})":\s*\("([^"]+)",\s*"([^"]+)"\)', m.group(1))
fm = {p[2]: (p[0], p[1]) for p in pairs}

rows = json.load(open(ROOT / "14_部件库" / "slots_165.json", encoding="utf-8"))
rm = {r["id"]: r for r in rows}

files = sorted(DIR.glob("concept_*.png"))
feats = {}
for f in files:
    im = Image.open(f).convert("RGB").resize((32, 32), Image.BILINEAR)
    # 灰度 + 彩色各一半权重：既比轮廓也比配色
    g = im.convert("L")
    flat = [v for px in im.getdata() for v in px]
    feats[f.name] = (list(g.getdata()), flat)

names = list(feats)
N = len(names)
print(f"比对 {N} 张，共 {N*(N-1)//2} 对 ...")

TH = 12.0  # MAE 阈值：低于此判定「高度相似」
close = []
for i in range(N):
    gi, ci = feats[names[i]]
    for j in range(i + 1, N):
        gj, cj = feats[names[j]]
        dg = sum(abs(a - b) for a, b in zip(gi, gj)) / 1024
        dc = sum(abs(a - b) for a, b in zip(ci, cj)) / 3072
        d = dg * 0.6 + dc * 0.4
        if d < TH:
            close.append((round(d, 2), names[i], names[j]))

close.sort()
print(f"\n=== 高度相似对（MAE < {TH}）：{len(close)} 对 ===")

# 并查集聚类
parent = {n: n for n in names}
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[rb] = ra

for d, a, b in close:
    union(a, b)

clusters = {}
for n in names:
    clusters.setdefault(find(n), []).append(n)
big = {k: v for k, v in clusters.items() if len(v) >= 2}

print(f"\n=== 相似簇（≥2 张）：{len(big)} 簇，涉及 {sum(len(v) for v in big.values())} 张 ===\n")
for k, v in sorted(big.items(), key=lambda kv: -len(kv[1])):
    print(f"--- 簇 {len(v)} 张 ---")
    for n in sorted(v):
        sid, nm = fm.get(n, ("?", "?"))
        r = rm.get(sid, {})
        print(f"    {sid:7s} {nm:9s} {r.get('domain','?')}×{r.get('resist','?'):4s}")
    print()

out = ROOT / "14_部件库" / "qa_similarity.json"
json.dump({"pairs": [[d, a, b] for d, a, b in close],
           "clusters": [sorted(v) for v in big.values()]},
          open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"已导出: {out}")
