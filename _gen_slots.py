# -*- coding: utf-8 -*-
"""生成 165 个劫怪槽位表（15 域 x 11 阻力），并把已画的 52 只归入标准槽位"""
import json
from pathlib import Path

DOMAINS = [
    ("WRK", "工作", "谈薪、要资源、拒绝加班、汇报"),
    ("EDU", "学业", "答辩、请教老师、选课题、备考"),
    ("INT", "亲密", "表白、吵架后沟通、要不要继续"),
    ("FAM", "家庭", "与父母沟通、夫妻沟通、家事安排"),
    ("PAR", "育儿", "辅导作业、选学校、叛逆期沟通"),
    ("HEA", "健康", "向医生描述症状、选治疗方案、坚持康复"),
    ("FIN", "财务", "谈钱、催款、催报销、预算沟通"),
    ("SOC", "社交", "寒暄、拒绝邀约、化解尴尬"),
    ("LIV", "居住", "与房东谈、与物业谈、邻里纠纷"),
    ("ADM", "行政", "办手续、提交材料、申诉"),
    ("SEF", "自我", "表达自己、内耗、迷茫、自律"),
    ("CRE", "创作", "阐释作品、选方向、突破瓶颈"),
    ("CAR", "照护", "代老人表达、选养老方式、长期陪护"),
    ("RIG", "权益", "维权沟通、是否起诉、索赔"),
    ("BLF", "信仰", "表达困惑、选择信什么、寻找意义"),
]

RESIST = [
    ("01", "沟通", "不知道怎么开口"),
    ("02", "决策", "不知道选哪个"),
    ("03", "执行", "知道怎么做但推不动"),
    ("04", "等待", "结果不在你手上"),
    ("05", "学习", "得先搞懂新东西"),
    ("06", "对抗", "有人跟你对着干"),
    ("07", "修复", "搞砸了要补救"),
    ("08", "告别", "该放下了"),
    ("09", "忍耐", "短期无解只能扛"),
    ("10", "求助", "得开口找人"),
    ("11", "模糊", "说不清哪里不对"),
]

# 已画的 52 只 -> 标准槽位（近似归类，形象通用）
MAPPED = {
    "WRK-01": ("贪狼·薪", "concept_tanlang_xin.png"),
    "WRK-02": ("巨门·歧", "concept_jumeng_qi.png"),
    "WRK-03": ("武曲·践", "concept_wuqu_jian.png"),
    "WRK-04": ("计都·候", "concept_jdu_hou.png"),
    "WRK-06": ("七杀·锋", "concept_qisha_feng.png"),
    "WRK-07": ("太乙·补", "concept_taiyi_bu.png"),
    "WRK-09": ("玄武·忍", "concept_xuanwu_ren.png"),
    "WRK-11": ("破军·破", "concept_pojun_po.png"),
    "EDU-02": ("算筹·乱", "concept_suanchou_luan.png"),
    "EDU-03": ("焚膏·竭", "concept_fengao_jie.png"),
    "EDU-04": ("磨蹭·慢", "concept_moceng_man.png"),
    "EDU-05": ("文曲·学", "concept_wenqu_xue.png"),
    "EDU-09": ("砚台·沉", "concept_yantai_chen.png"),
    "INT-01": ("缠绕·缠", "concept_chanrao_chan.png"),
    "INT-04": ("折枝·离", "concept_zhezhi_li.png"),
    "INT-06": ("天同·和", "concept_tiantong_he.png"),
    "INT-07": ("化骨·蚀", "concept_huagu_shi.png"),
    "INT-08": ("玄冥·缘", "concept_xuanming_yuan.png"),
    "INT-10": ("天乙·援", "concept_tianyi_yuan.png"),
    "INT-11": ("绣衣·蔽", "concept_xiuyi_bi.png"),
    "HEA-03": ("青囊·动", "concept_qingnang_dong.png"),
    "FIN-02": ("贪财·算", "concept_tancai_suan.png"),
    "FIN-03": ("天府·守", "concept_tianfu_shou.png"),
    "FIN-04": ("通胀·蚀", "concept_tongpeng_shi.png"),
    "FIN-06": ("债主·逼", "concept_zhai_zhu_bi.png"),
    "FIN-07": ("漏卮·亏", "concept_louzhi_kui.png"),
    "FIN-08": ("失金·丧", "concept_shijin_sang.png"),
    "SOC-01": ("误听·曲", "concept_wuting_qu.png"),
    "SOC-04": ("焦等·躁", "concept_jiaodeng_zao.png"),
    "SOC-06": ("急躁·抢", "concept_jizao_qiang.png"),
    "SOC-02": ("天机·赴", "concept_tianji_fu.png"),
    "SOC-03": ("武曲·寒", "concept_wuqu_han.png"),
    "SOC-05": ("文曲·礼", "concept_wenqu_li.png"),
    "SOC-07": ("太乙·圆", "concept_taiyi_yuan.png"),
    "SOC-08": ("地劫·散", "concept_dijie_san.png"),
    "SOC-09": ("陀罗·沉", "concept_tuoluo_chen.png"),
    "SOC-10": ("天乙·赠", "concept_tianyi_zeng.png"),
    "SOC-11": ("天空·涣", "concept_tiankong_huan.png"),
    "LIV-02": ("风水·乱", "concept_fengshui_luan.png"),
    "LIV-03": ("居诸·家", "concept_juzhu_jia.png"),
    "LIV-09": ("借居·挤", "concept_jieju_ji.png"),
    "LIV-11": ("漂泊·萍", "concept_piaobo_ping.png"),
    "ADM-03": ("印绶·章", "concept_yinshou_zhang.png"),
    "ADM-04": ("排队·长", "concept_paichang_zhang.png"),
    "ADM-01": ("巨门·陈", "concept_jumen_chen.png"),
    "ADM-02": ("天机·径", "concept_tianji_jing.png"),
    "ADM-05": ("文曲·政", "concept_wenqu_zheng.png"),
    "ADM-06": ("擎羊·推", "concept_qingyang_tui.png"),
    "SEF-01": ("廉贞·掩", "concept_lianzhen_yan.png"),
    "SEF-02": ("内在·裂", "concept_neizai_lie.png"),
    "SEF-09": ("蜗角·藏", "concept_wojiao_cang.png"),
    "SEF-11": ("罗睺·昧", "concept_luohou_mei.png"),
    "CRE-01": ("烛阴·显", "concept_zhuyin_xian.png"),
    "CRE-02": ("文昌·创", "concept_wenchang_chuang.png"),
    "CRE-03": ("灵光·竭", "concept_lingguang_jie.png"),
    "CRE-11": ("模仿·仿", "concept_mofang_fang.png"),
    "CAR-03": ("天梁·担", "concept_tianliang_dan.png"),
    "CAR-09": ("太一·养", "concept_taiyi_yang.png"),
    "RIG-06": ("公门·争", "concept_gongmen_zheng.png"),
    "RIG-08": ("玄冥·留", "concept_xuanming_liu.png"),
    "RIG-09": ("忍让·吞", "concept_renrang_tun.png"),
    "RIG-11": ("公正·疑", "concept_gongzheng_yi.png"),
    "FAM-01": ("巨门·噎", "concept_jumen_ye.png"),
    "FAM-02": ("天机·扯", "concept_tianji_che.png"),
    "FAM-06": ("擎羊·峙", "concept_qingyang_zhi.png"),
    "FAM-09": ("陀罗·承", "concept_tuoluo_cheng.png"),
    "PAR-01": ("天同·呐", "concept_tiantong_na.png"),
    "PAR-03": ("武曲·推", "concept_wuqu_tui.png"),
    "PAR-06": ("火星·叛", "concept_huoxing_pan.png"),
    "PAR-09": ("天梁·扛", "concept_tianliang_kang.png"),
    "BLF-01": ("天机·问", "concept_tianji_wen.png"),
    "BLF-02": ("太阴·择", "concept_taiyin_ze.png"),
    "BLF-08": ("地劫·舍", "concept_dijie_she.png"),
    "BLF-11": ("天空·茫", "concept_tiankong_mang.png"),
    "BLF-03": ("武曲·修", "concept_wuqu_xiu.png"),
    "BLF-04": ("计都·待", "concept_jidu_dai.png"),
    "BLF-05": ("文曲·诵", "concept_wenqu_song.png"),
    "BLF-06": ("七杀·诤", "concept_qisha_zheng.png"),
    "BLF-07": ("太乙·塑", "concept_taiyi_su.png"),
    "BLF-09": ("陀罗·守", "concept_tuoluo_shou.png"),
    "BLF-10": ("天乙·寻", "concept_tianyi_xun.png"),
    "HEA-01": ("巨门·述", "concept_jumen_shu.png"),
    "HEA-02": ("天机·决", "concept_tianji_jue.png"),
    "HEA-04": ("天同·候", "concept_tiantong_hou.png"),
    "HEA-05": ("文曲·索", "concept_wenqu_suo.png"),
    "HEA-06": ("七杀·执", "concept_qisha_zhi.png"),
    "HEA-07": ("太乙·复", "concept_taiyi_fu.png"),
    "HEA-08": ("地劫·别", "concept_dijie_bie.png"),
    "HEA-09": ("陀罗·磨", "concept_tuoluo_mo.png"),
    "CAR-01": ("巨门·代", "concept_jumen_dai.png"),
    "CAR-02": ("天机·安", "concept_tianji_an.png"),
    "CAR-04": ("廉贞·候", "concept_lianzhen_hou.png"),
    "CAR-05": ("文曲·护", "concept_wenqu_hu.png"),
    "CAR-06": ("火星·争", "concept_huoxing_zheng.png"),
    "CAR-07": ("太乙·弥", "concept_taiyi_mi.png"),
    "CAR-08": ("地劫·送", "concept_dijie_song.png"),
    "CAR-10": ("天乙·借", "concept_tianyi_jie.png"),
    "FAM-03": ("武曲·滞", "concept_wuqu_zhi.png"),
    "FAM-04": ("计都·守", "concept_jidu_shou.png"),
    "FAM-05": ("文曲·习", "concept_wenqu_xi.png"),
    "FAM-07": ("太乙·缝", "concept_taiyi_feng.png"),
    "FAM-08": ("地劫·辞", "concept_dijie_ci.png"),
    "FAM-10": ("天乙·托", "concept_tianyi_tuo.png"),
    "FAM-11": ("天空·惑", "concept_tiankong_huo.png"),
    "PAR-02": ("天机·择", "concept_tianji_ze.png"),
    "PAR-04": ("计都·盼", "concept_jidu_pan.png"),
    "PAR-05": ("文曲·迷", "concept_wenqu_mi.png"),
    "PAR-07": ("太乙·歉", "concept_taiyi_qian.png"),
    "PAR-08": ("地劫·放", "concept_dijie_fang.png"),
    "PAR-10": ("天乙·叩", "concept_tianyi_kou.png"),
    "PAR-11": ("天空·忧", "concept_tiankong_you.png"),
}

rows = []
for dcode, dname, devents in DOMAINS:
    for rcode, rname, rmean in RESIST:
        sid = f"{dcode}-{rcode}"
        name, fname = MAPPED.get(sid, ("", ""))
        rows.append({
            "id": sid,
            "domain": dname,
            "resist": rname,
            "resist_mean": rmean,
            "typical": devents,
            "name": name,
            "file": fname,
            "done": bool(name),
        })

done = [r for r in rows if r["done"]]
todo = [r for r in rows if not r["done"]]

print(f"总槽位: {len(rows)}")
print(f"已完成: {len(done)}")
print(f"待画:   {len(todo)}")
print()

# 按域统计
print("=== 各域完成情况 ===")
for dcode, dname, _ in DOMAINS:
    sub = [r for r in rows if r["id"].startswith(dcode)]
    d = len([r for r in sub if r["done"]])
    print(f"  {dname:4s} {dcode}  {d:2d}/11  {'#'*d}{'.'*(11-d)}")
print()

# 导出待画清单
out_dir = Path(r"E:\ZDY.AI\EarthOnline-Assets\14_部件库")
out_dir.mkdir(exist_ok=True)
with open(out_dir / "slots_165.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=1)

lines = ["# 165 劫怪槽位表（15 域 × 11 阻力）", ""]
lines.append(f"已完成 {len(done)} / 165　待画 {len(todo)}")
lines.append("")
lines.append("## 已完成")
lines.append("")
lines.append("| 槽位 | 域 | 阻力 | 劫名 | 文件 |")
lines.append("|---|---|---|---|---|")
for r in done:
    lines.append(f"| {r['id']} | {r['domain']} | {r['resist']} | {r['name']} | `{r['file']}` |")
lines.append("")
lines.append("## 待画")
lines.append("")
lines.append("| 槽位 | 域 | 阻力 | 阻力含义 | 典型事件 |")
lines.append("|---|---|---|---|---|")
for r in todo:
    lines.append(f"| {r['id']} | {r['domain']} | {r['resist']} | {r['resist_mean']} | {r['typical']} |")

(out_dir / "slots_165.md").write_text("\n".join(lines), encoding="utf-8")
print("已导出:")
print(f"  {out_dir / 'slots_165.md'}")
print(f"  {out_dir / 'slots_165.json'}")
print()
print("=== 前 12 个待画槽位 ===")
for r in todo[:12]:
    print(f"  {r['id']:8s} {r['domain']}×{r['resist']}  {r['resist_mean']}")
