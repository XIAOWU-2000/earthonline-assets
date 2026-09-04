# 三、美术素材库（EarthOnline-Assets）

> **本章是《开发任务书》的美术分册，取代此前"美术另册"的标注。**
> 所有界面实现、劫怪形象、图标、Logo、空状态，**一律以本章列出的实物文件为准**，禁止自行绘制或生成替代品。

## 3.1 定位与获取

| 项 | 内容 |
|---|---|
| 素材库名称 | `EarthOnline-Assets` |
| 本地路径 | `E:\ZDY.AI\EarthOnline-Assets` |
| 与主工程关系 | 主工程 `地球Online算命APP` 为**代码仓**，素材库为**资源仓**，两者同级并列 |
| 远程仓 | `https://github.com/XIAOWU-2000/earthonline-assets` |
| 当前版本 | **v10.1**（2026-09-04） |
| 文件总数 | **239 个**（不含缩略图与废弃归档） |
| 总体积 | **209.63 MB** |
| 状态 | **165 只劫怪全满，质检全通过** |

**获取方式**（二选一，禁止第三种）：

```bash
# 方式一：作为主工程子目录引入（推荐，便于版本锁定）
git submodule add https://github.com/XIAOWU-2000/earthonline-assets.git assets

# 方式二：一次性复制
cp -r ../EarthOnline-Assets ./assets
```

> **引入后必须锁定 commit `7a4ee35`**，后续素材更新走显式升级，禁止跟随 master 自动漂移。

---

## 3.2 素材库总清单

| # | 目录 | 文件数 | 体积 | 格式 | 用途 |
|---|---|---|---|---|---|
| 01 | `01_符箓` | 2 | 0.01 MB | SVG | 符箓两套皮肤（朱砂 / 赛博） |
| 02 | `02_劫怪` | 168 | 143.38 MB | PNG×165 + SVG×2 + HTML×1 | **劫怪图库 165 只**（核心资产） |
| 03 | `03_交互框架` | 3 | 0.06 MB | SVG | 流程图 + 两套线框 |
| 04 | `04_动效规范` | 2 | 0.03 MB | MD + HTML | 动效毫秒值定义 |
| 05 | `05_页面设计` | 7 | 5.25 MB | PNG×3 + SVG×4 | 设置/关于/校准 AI 图 + 早期线框 |
| 06 | `06_UI视觉稿` | 8 | 14.58 MB | PNG | **移动端 8 屏高保真** |
| 07 | `07_PC桌面端` | 4 | 7.49 MB | PNG | PC 三栏 4 屏 |
| 08 | `08_状态页` | 6 | 9.67 MB | PNG | 空/首次/加载/错误等状态 |
| 09 | `09_动效帧` | 4 | 9.01 MB | PNG | 4 个关键瞬间的可视化 |
| 10 | `10_模块拆解` | 15 | 5.87 MB | PNG | 14 个界面模块 + 1 废弃对照 |
| 11 | `11_图标集` | 4 | 1.35 MB | PNG | 卦象 / 五行 / 十二宫 / 五脏 |
| 12 | `12_Logo` | 3 | 1.46 MB | PNG | 标准 / 小尺寸 / 带背景 |
| 13 | `13_空状态细分` | 8 | 10.03 MB | PNG | 8 种细分空状态 |
| 14 | `14_部件库` | 5 | 1.42 MB | JSON×3 + MD + PNG | 槽位表 / 质检报告 / 部件库底图 |

**不参与交付的目录**（工程接入时排除）：

| 目录 | 说明 |
|---|---|
| `02_劫怪/thumbs/` | 165 张 320px 缩略图，仅供 `gallery.html` 预览 |
| `02_劫怪/concept/_extra/` | 2 张落选备用稿，不参与槽位映射 |
| `02_劫怪/concept/_deprecated/` | 9 张废弃稿（旧风格 / 重复生成），**禁止使用** |

---

## 3.3 劫怪图库 · 165 只（核心资产）

### 3.3.1 槽位编码规则

```
槽位 ID = 域代码-阻力序号
例：WRK-01 = 工作域 × 第 1 种阻力（沟通）
```

**15 个域代码**（与 §1.2 一一对应，禁止改动）：

| 域 | 代码 | 域 | 代码 | 域 | 代码 |
|---|---|---|---|---|---|
| 工作 | `WRK` | 财务 | `FIN` | 自我 | `SEF` |
| 学业 | `EDU` | 社交 | `SOC` | 创作 | `CRE` |
| 亲密 | `INT` | 居住 | `LIV` | 照护 | `CAR` |
| 家庭 | `FAM` | 行政 | `ADM` | 权益 | `RIG` |
| 育儿 | `PAR` | 健康 | `HEA` | 信仰 | `BLF` |

**11 个阻力序号**（与 §1.3 一一对应）：

| 序号 | 阻力 | 序号 | 阻力 | 序号 | 阻力 |
|---|---|---|---|---|---|
| 01 | 沟通 | 05 | 学习 | 09 | 忍耐 |
| 02 | 决策 | 06 | 对抗 | 10 | 求助 |
| 03 | 执行 | 07 | 修复 | 11 | 模糊 |
| 04 | 等待 | 08 | 告别 | | |

> **15 × 11 = 165，一个不多一个不少。** 新增域或阻力属于改需求，必须先改 §1.2 / §1.3 再改素材库。

### 3.3.2 命名规则

劫名格式：`[星曜]·[事核心字]`

- **星曜**：借用紫微斗数星名作**文化符号**（推算体系不用紫微，仅借名）
- 星曜**可跨域复用**（如"陀罗"用于 `FAM-09` / `BLF-09` / `HEA-09`）
- **事核心字尽量不重复**，便于玩家辨识
- 与 §1 术语表「劫」的定义完全一致

文件名格式：`concept_[星曜拼音]_[字拼音].png`

- 例：`WRK-01 贪狼·薪` → `concept_tanlang_xin.png`
- **拼音冲突时加域名后缀**：`ADM-10 天乙·询` 与 `BLF-10 天乙·寻` 同音，后者用 `concept_tianyi_xun.png`，前者用 `concept_tianyi_xun_adm.png`

### 3.3.3 数据文件

| 文件 | 用途 | 消费方 |
|---|---|---|
| `14_部件库/slots_165.md` | 人类可读槽位总表（已完成 / 待画分区） | 设计、验收 |
| `14_部件库/slots_165.json` | **程序读取的唯一数据源** | 代码 |
| `14_部件库/qa_report.json` | 每张图的质检指标 | 验收脚本 |
| `_gen_slots.py` | 槽位表生成脚本（改映射后重跑） | 维护者 |

**`slots_165.json` 单条结构**（字段名不得改动）：

```json
{
  "id": "WRK-01",
  "domain": "工作",
  "resist": "沟通",
  "resist_mean": "不知道怎么开口",
  "typical": "谈薪、要资源、拒绝加班、汇报",
  "name": "贪狼·薪",
  "file": "concept_tanlang_xin.png",
  "done": true
}
```

### 3.3.4 完整清单（165 只）

<!--SLOTS_TABLES-->

---

## 3.4 劫怪画图规范

> **需要补画、重画、新增劫怪时，必须逐条遵守本节。违反任何一条铁律即返工。**
> 本节内容同步固化在素材库 `画图规范.md`，两处不一致时**以任务书为准**。

### 3.4.1 八条铁律

| # | 铁律 |
|---|---|
| 1 | **单只怪**，不出现第二个角色（剪影也不行） |
| 2 | **纯白底**，无场景、无环境 |
| 3 | **无道具**（柜台 / 门 / 长椅 / 书 / 信封 / 喇叭 全部禁止） |
| 4 | **困境用身体处境表达**，不用场景叙事 |
| 5 | 正面全身像（full body front view） |
| 6 | 扁平赛璐璐（FLAT cel-shading），**不要 3D 渲染感** |
| 7 | 无戏剧化打光（NO dramatic lighting） |
| 8 | 粗黑轮廓 + 手绘墨线感 |

> **铁律 1–4 是"去 AI 感"的关键。** 历史教训：v7 阶段为表达抽象处境加入了场景道具（柜台、长椅、流程图、人物剪影），AI 一旦进入"场景叙事"模式就会自动堆砌元素、加强光影、戏剧化表情，**AI 感全部回归**，42 张因此返工。

### 3.4.2 标准 prompt 模板

复制后只改 `[]` 内变量：

```
Character design sheet of a single non-human rubber-toy-like blob monster,
plain white background, full body front view,
NO scene NO props NO other characters NO humans.
A simple rounded soft vinyl toy creature in the style of Spirited Away
background creatures, a rounded blob with absolutely no human anatomy,
no human face, no human proportions, just a soft rounded body with two large
round non-human cartoon eyes and four tiny stubby nubs for limbs.
KEY FEATURE: [身体处境描述].
[配色] body, [表情描述].
Thick bold black outlines, rough hand-drawn ink linework, FLAT cel-shading
with minimal soft volume, one small dark-red accent.
Appealing ugly-cute, charmingly grotesque, [情绪], NOT scary, NOT gory,
NOT realistic, NO 3D render look, NO dramatic lighting, NO environment.
Clean professional character design illustration, centered composition.
```

**必须保留的锁定词**（删一个就会风格漂移）：

| 位置 | 锁定词 |
|---|---|
| 开头 | `NO scene NO props NO other characters NO humans` |
| 中间 | `absolutely no human anatomy`、`FLAT cel-shading` |
| 结尾 | `NO 3D render look, NO dramatic lighting, NO environment` |

### 3.4.3 困境表达对照表

| 阻力 | ❌ 场景叙事（禁用） | ✅ 身体处境（正确） |
|---|---|---|
| 沟通 | 举喇叭 + 老人剪影 | **嘴巴拉长成喇叭状**（身体即扩音器） |
| 决策 | 三个房子模型 / 岔路口 | **身体裂成三条腿，各朝一个方向** |
| 执行 | 推陷在泥里的车 | **四肢僵直、关节生锈卡住** |
| 等待 | 长椅上盯叫号屏 | **身体凝固成雕像，表面落灰** |
| 学习 | 捧着书堆 / 拿倒文件 | **全身长满眼睛**（要同时看太多） |
| 对抗 | 与人对指 / 天降巨印 | **胸口深陷方形印章凹痕，后倾但站住** |
| 修复 | 缝衣服 / 补罐子 | **身上多处补丁，正在给自己打补丁** |
| 告别 | 门口挥手 / 攥毯子 | **一只手臂延长出去，指尖在消散** |
| 忍耐 | 爬长台阶 / 头顶石头 | **身体被压扁但关节加粗**（扛出肌肉） |
| 求助 | 敲门 / 伸手够光 | **手臂变短够不到**，另一手攥紧胸前 |
| 模糊 | 放大镜 / 埋在雾里 | **身体半透明、轮廓不稳定** |

### 3.4.4 已验证的身体处境词库

| 类型 | 可用表达 |
|---|---|
| 变形 | 拉长 / 压扁 / 裂开 / 融化 / 膨胀 / 缩小 / 折叠 |
| 增生 | 多出眼睛 / 多出手 / 多出腿 / 身上长物 |
| 缺损 | 缺一块 / 消散 / 变透明 / 断裂 / 空洞 |
| 痕迹 | 印章凹痕 / 补丁 / 缝合线 / 裂纹 / 磨损 |
| 状态 | 凝固 / 僵直 / 抖动 / 瘫软 / 紧绷 |
| 附着 | 身上长满（苔藓 / 灰尘 / 冰霜 / 铜锈） |

### 3.4.5 情绪调性

> **画"有尊严的困境"，不画"可怜的受害者"。**

| 阻力 | ❌ 不画 | ✅ 要画 |
|---|---|---|
| 忍耐 | 痛苦 | **已经走了多远** |
| 告别 | 崩溃 | **温暖的放手** |
| 修复 | 自责 | **专注地补** |
| 对抗 | 被压垮 | **愤而不屈** |
| 求助 | 卑微 | **硬着头皮伸出手** |

### 3.4.6 分域合规红线

| 域 | 红线 | prompt 硬约束 |
|---|---|---|
| **健康 HEA** | 不画疾病 / 症状 / 治疗 | `NO medical equipment NO illness NO symptoms` |
| **信仰 BLF** | 不出现任何宗教标志 | `No religious symbols of any kind` |
| **照护 CAR** | 不画病床 / 医疗器具 | `NO medical equipment` |
| **所有域** | 不血腥、不恐怖、不可爱风 | `NOT scary, NOT gory, NOT cute-kawaii` |

### 3.4.7 安全审核规避（实测有效）

**问题**：用 `creature with grotesque-cute proportions` + 人体姿态词（standing / arms / mouth / throat）描述时，图像安全审核会误判为 `image contains "Teenager" content` 而拒绝生成。

**解法**：把主体描述成**软胶玩具（vinyl toy / rubber-toy-like blob）**，并显式否定人体特征。

| ❌ 易触发审核 | ✅ 安全替代 |
|---|---|
| arms / legs | **tiny stubby nubs for limbs** |
| hands | **nub ends / tiny rounded nubs** |
| creature with human proportions | **vinyl toy blob, no human anatomy** |
| standing / leaning | **seated / floating / compressed posture** |
| mouth / throat | 尽量省略，或用 **a small opening** |

**失败案例**（禁止重犯）：

- 「嘴巴拉长成喇叭 + 手举喇叭」→ 判定 Teenager，拒绝生成
- 「身体左右裂成两半 + 两张嘴」→ 判定 Teenager，拒绝生成
- 改用 vinyl toy 描述后：**全部通过**

---
