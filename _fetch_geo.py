# -*- coding: utf-8 -*-
"""抓取中国行政区划（省/市/县三级）+ 中心点经纬度
数据源：阿里云 DataV.GeoAtlas 公开数据 (geo.datav.aliyun.com)
输出：15_地理数据/cn_geo.json
"""
import sys, json, time, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://geo.datav.aliyun.com/areas_v3/bound/{}_full.json"
UA = {"User-Agent": "Mozilla/5.0 (compatible; EarthOnline-Assets/1.0)"}


def get(code, retry=3):
    for i in range(retry):
        try:
            req = urllib.request.Request(BASE.format(code), headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if i == retry - 1:
                return None
            time.sleep(1.2 * (i + 1))
    return None


def parse(data, level):
    out = []
    for f in (data or {}).get("features", []):
        p = f.get("properties", {})
        c = p.get("center")
        if not c or len(c) < 2:
            continue
        out.append({
            "code": str(p.get("adcode", "")),
            "name": p.get("name", ""),
            "level": level,
            "lon": round(float(c[0]), 4),
            "lat": round(float(c[1]), 4),
        })
    return out


print("抓取省级 …")
provinces = parse(get(100000), "province")
print(f"  省级 {len(provinces)} 条")

print("抓取地级 …")
cities = []
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = {ex.submit(get, int(p["code"])): p for p in provinces if p["code"].isdigit()}
    for i, fu in enumerate(as_completed(futs), 1):
        p = futs[fu]
        cities += parse(fu.result(), "city")
        if i % 10 == 0:
            print(f"  {i}/{len(futs)}")
print(f"  地级 {len(cities)} 条")

print("抓取县级 …")
counties = []
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = {ex.submit(get, int(c["code"])): c for c in cities if c["code"].isdigit()}
    done = 0
    for fu in as_completed(futs):
        counties += parse(fu.result(), "county")
        done += 1
        if done % 50 == 0:
            print(f"  {done}/{len(futs)}")
print(f"  县级 {len(counties)} 条")

allrows = provinces + cities + counties
print(f"\n合计 {len(allrows)} 条")

# 去重（同一 code 可能重复出现）
seen, uniq = set(), []
for r in allrows:
    if r["code"] and r["code"] not in seen:
        seen.add(r["code"])
        uniq.append(r)
print(f"去重后 {len(uniq)} 条")

# 校验：经度范围应在中国境内
bad = [r for r in uniq if not (73 <= r["lon"] <= 136 and 3 <= r["lat"] <= 54)]
print(f"越界记录: {len(bad)} 条  {' '.join(r['name'] for r in bad[:10])}")

from pathlib import Path
out = Path(r"E:\ZDY.AI\EarthOnline-Assets\15_地理数据")
out.mkdir(exist_ok=True)
(out / "cn_geo.json").write_text(
    json.dump({"source": "DataV.GeoAtlas", "count": len(uniq), "rows": uniq},
              open(out / "cn_geo.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=0) or "", encoding="utf-8")

# 重新写（上面写法有问题，这里干净地写一次）
with open(out / "cn_geo.json", "w", encoding="utf-8") as f:
    json.dump({"source": "DataV.GeoAtlas (geo.datav.aliyun.com)",
               "fetched": time.strftime("%Y-%m-%d"),
               "count": len(uniq), "rows": uniq},
              f, ensure_ascii=False, separators=(",", ":"))

sz = (out / "cn_geo.json").stat().st_size
print(f"\n已写出: {out / 'cn_geo.json'}  ({sz/1024:.0f} KB)")
print("\n样例:")
for r in uniq[:5]:
    print(f"  {r['level']:9s} {r['code']} {r['name']:8s} lon={r['lon']} lat={r['lat']}")
