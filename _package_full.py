# -*- coding: utf-8 -*-
"""构建《地球Online》完整离线包：全部文档 + 全部素材实物 + 全部脚本。
图片用 ZIP_STORED（PNG 已压缩，再压收益极小但极慢），文本用 DEFLATED。
"""
import sys, zipfile, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

APP = Path(r"E:\ZDY.AI\地球Online算命APP")
AST = Path(r"E:\ZDY.AI\EarthOnline-Assets")
ZIP = Path(r"E:\ZDY.AI\地球Online_完整包_v3.zip")
ROOT = "地球Online_完整包_v3"

# thumbs 保留：gallery.html 依赖它才能预览 165 只劫怪
SKIP = {"_extra", "_deprecated", ".git", "_docs_build",
        "tmp_a", "tmp_b", "fix", "__pycache__"}

# ---------- 完整包说明 ----------
README = """# 地球Online · 中国服 —— 完整离线包 v3

**这个包里有开工所需的全部内容，解压即可用，无需联网。**

> 与轻量版 `地球Online_交付包_v3.zip`（2.29 MB，仅文档）的区别：
> 本包**额外包含 225 MB 素材库实物**（165 只劫怪原图、UI 视觉稿、图标、Logo、空状态、符箓等）。

> **文档只收 md**（pdf / html 不进包）。
> 例外：`02_素材库/02_劫怪/gallery.html` 与 `04_动效规范/motion_spec.html`
> 属**功能性文件**而非文档，予以保留——前者是浏览器可视化验收 165 只劫怪的唯一途径。

---

## 一、目录结构

```
00_先看我.md                  ← 本文件
01_文档/                      ← 全部 md 格式
    算法规格补遗.md               七项算法空缺的填补（引擎必读）
    开发任务书.md                主文档 v3（含第三章美术素材库）
    地球Online_开发方案.md        产品方案（域/阻力/副本定义来源）
    架构设计.md                   分层、模块、引擎接口、数据表
    UI交互与美术设计规格.md        设计令牌、页面规格、组件九态
    素材库说明与接入.md            素材清单与工程接入
    执行清单.md                   按里程碑的可勾选清单（85 项）
02_素材库/                     ← 全部实物，共 225 MB
    01_符箓/           2 SVG        符箓两套皮肤
    02_劫怪/           168          165 只劫怪 1024×1024 白底 PNG
        concept/concept_*.png       正式素材（165 张）
        concept/_deprecated/        （已排除）
        gallery.html + thumbs/      浏览器打开可看全部 165 只
    03_交互框架/       3 SVG
    04_动效规范/       2
    05_页面设计/       7            设置/关于/校准 AI 图
    06_UI视觉稿/       8            移动端 8 屏高保真（实现基准）
    07_PC桌面端/       4
    08_状态页/         6
    09_动效帧/         4
    10_模块拆解/       15           14 个界面模块
    11_图标集/         4            卦象/五行/十二宫/五脏
    12_Logo/           3            标准/小尺寸/带背景
    13_空状态细分/     8
    14_部件库/         slots_165.json（165 劫怪数据源）+ 质检报告
    15_地理数据/       cn_geo.json（3237 条行政区划经纬度）
    画图规范.md                    劫怪画图规范
03_脚本/
    _calibrate.py / _calibrate2.py / _calibrate3.py   五行权重校准
    _fetch_geo.py                                     地名数据抓取
    _qa_check.py / _qa_similarity.py                  素材质检
    _gen_slots.py                                     槽位表生成
    _docs_build/                                      文档构建脚本
```

---

## 二、开工顺序

### 阶段 A —— 规格完整，可立刻开工
| # | 内容 | 依据 |
|---|---|---|
| A1 | 工程骨架 + 目录结构 | 架构设计 §1.3、§2.1 |
| A2 | 数据模型与本地存储 | 架构设计 §3.2 |
| A3 | 界面骨架 | 任务书 §3.5–3.8 + UI规格 |
| A4 | 165 只劫怪接入 + 图鉴页 | 任务书 §3.11 + `slots_165.json` |
| A5 | 状态页与空状态 | 任务书 §3.6 |

### 阶段 B —— 引擎（**先读《算法规格补遗》**）
| # | 内容 | 依据 |
|---|---|---|
| B1 | 历法内核（节气/中气/真太阳时） | 补遗 §5 |
| B2 | 四柱 + 五行权重（相对排名制） | 补遗 §4（已 20 万组校准） |
| B3 | 六壬天地盘 + 四课 | 补遗 §1（含黄金演算样例） |
| B4 | 九宗门（每门一函数 + 单测） | 补遗 §2、§3 |
| B5 | 天将 / 遁干 / 六亲 | 任务书 M3.8–M3.9 |
| B6 | 公理层 | 架构设计 §2.2 axioms |
| B7 | 应用层与解法生成 | 任务书 M6 + 补遗 §6 |

> 出生地经度查 `02_素材库/15_地理数据/cn_geo.json`（3237 条，精度 0.048°）。
> **禁止运行时调地图 API** —— 违反数据本地化红线且泄露出生地。

### 阶段 C —— 内容包
| # | 内容 |
|---|---|
| C1 | 典籍六本 + 敏感剔除（任务书 M8.1、M8.5） |
| C2 | 45 个解法模板（补遗 §6，含结构与示例） |
| C3 | 165 条劫名 → **直接读 `slots_165.json` 的 `name` 字段** |

---

## 三、三条最高纪律（任务书 §0.2）

> **① 术语表里有定义的，一律按术语表来，禁止自行理解或发明新词。**
> **② 做不到的功能必须抛错/返回 Err，禁止静默返回空值、默认值或空列表。**
> **③ 遇到方案未覆盖的情况：停下来记录问题，禁止自行发挥。**

第 ③ 条尤其重要：**命理算法算错了不会报错**，只会静默产出错误结果。

---

## 四、验收总入口

| 阶段 | 命令 | 标准 |
|---|---|---|
| 引擎 | `cargo test -p engine` | 全部通过（含九宗门独立测试） |
| UI | `flutter test test/ui` | 全部通过 |
| 内容 | `node scripts/validate_content.js` | 45 模板 + 165 劫名 + Schema 全过 |
| 发布 | 任务书 M10 九项 | 任一不通过不得发布 |

---

## 五、开工前必须先解决的两件事

| # | 事项 | 说明 |
|---|---|---|
| 1 | **合规审查** | 任务书 M0 要求"取得执业律师的书面合规意见"，**尚未完成**。测测先例表明风险真实存在（中央网信办已将网上算命列为重点整治内容）。**此项应在开发前完成**，否则产品定位若需调整，返工成本极高 |
| 2 | **地理数据商用许可** | `cn_geo.json` 来自阿里云 DataV.GeoAtlas，公开免费抓取，但**商用授权范围未确认**。需法务确认，或改用民政部区划代码 + 自采中心点 |

---

*完整离线包 v3 · 2026-09-05*
"""

t0 = time.time()
if ZIP.exists():
    ZIP.unlink()

ndoc = nimg = nother = 0
timg = tdoc = 0

with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    # ---- 0. 说明 ----
    z.writestr(f"{ROOT}/00_先看我.md", README)
    ndoc += 1

    # ---- 1. 文档 ----
    # 只收 md：pdf/html 不进包（素材库内的 gallery.html / motion_spec.html 属功能文件，另行保留）
    docs = [
        (APP / "算法规格补遗.md", "01_文档/算法规格补遗.md"),
        (APP / "开发任务书.md", "01_文档/开发任务书.md"),
        (APP / "地球Online_开发方案.md", "01_文档/地球Online_开发方案.md"),
        (APP / "架构设计.md", "01_文档/架构设计.md"),
        (APP / "01_产品文档(给人看)" / "UI交互与美术设计规格_代码道场.md",
         "01_文档/UI交互与美术设计规格.md"),
        (APP / "05_素材库说明与接入.md", "01_文档/素材库说明与接入.md"),
        (APP / "07_执行清单.md", "01_文档/执行清单.md"),
        (APP / "补丁_001_性别字段与大运算法.md", "01_文档/补丁_001_性别字段与大运算法.md"),
        (APP / "补丁_002_定盘问卷判据.md", "01_文档/补丁_002_定盘问卷判据.md"),
    ]
    for src, dst in docs:
        if src.exists():
            z.write(src, f"{ROOT}/{dst}")
            tdoc += src.stat().st_size
            ndoc += 1

    # ---- 2. 素材库全部实物 ----
    for f in sorted(AST.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(AST)
        if any(p in rel.parts for p in SKIP):
            continue
        if rel.name.startswith("."):
            continue
        # 文件自身标注为废弃的对照稿（如 mod_00_deprecated_ai_v1.png）一并排除
        if "deprecated" in rel.name.lower():
            continue
        data = f.read_bytes()
        # 图片已压缩格式 → 存储模式，避免无谓 CPU 开销
        if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
            zi = zipfile.ZipInfo(f"{ROOT}/02_素材库/{rel.as_posix()}", date_time=time.localtime()[:6])
            zi.compress_type = zipfile.ZIP_STORED
            z.writestr(zi, data)
            nimg += 1
            timg += len(data)
        else:
            z.write(f, f"{ROOT}/02_素材库/{rel.as_posix()}")
            nother += 1

    # ---- 3. 脚本 ----
    for name in ("_calibrate.py", "_calibrate2.py", "_calibrate3.py",
                 "_fetch_geo.py", "_qa_check.py", "_qa_similarity.py",
                 "_gen_slots.py", "画图规范.md", "README.md"):
        p = APP / name if name.startswith("_calibrate") else AST / name
        if p.exists():
            z.write(p, f"{ROOT}/03_脚本/{name}")
            nother += 1

print(f"文档 {ndoc} 个 ({tdoc/1024/1024:.2f} MB)")
print(f"图片 {nimg} 个 ({timg/1024/1024:.2f} MB)  [STORED]")
print(f"其他 {nother} 个")
print(f"\n压缩包: {ZIP.stat().st_size/1024/1024:.2f} MB")
print(f"耗时: {time.time()-t0:.1f}s")

# 校验
z = zipfile.ZipFile(ZIP)
print("\n完整性校验:", z.testzip() or "OK(无损坏)")
print(f"总条目: {len(z.infolist())}")
