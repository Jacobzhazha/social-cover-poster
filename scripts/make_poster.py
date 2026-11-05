#!/usr/bin/env python3
"""封面海报生成器：读 poster.json，检查文案，排版，导出 PNG。

用法：python3 make_poster.py poster.json --out 输出文件夹
只检查不出图：python3 make_poster.py poster.json --check
拿封面顶部图的生图参数：python3 make_poster.py poster.json --out 输出文件夹 --prompts

只用 Python 标准库。出图按顺序尝试：Playwright 自带的 Chromium → 本机 Chrome / Edge / Chromium
→ 自动安装 Playwright 的 Chromium。排版全部由本脚本完成，模型只负责写 poster.json。
"""
import argparse
import html
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from icons import ICONS, PANEL_COLORS, icon_svg  # noqa: E402

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"

SIZE_PRESETS = {
    "3:4": (1080, 1440),
    "1:1": (1080, 1080),
    "16:9": (1920, 1080),
    "2.35:1": (1800, 766),
    "9:16": (1080, 1920),
}
SIZE_ALIASES = {
    "竖版": "3:4", "小红书": "3:4", "3x4": "3:4", "贴图": "3:4",
    "方图": "1:1", "1x1": "1:1",
    "横图": "16:9", "横版": "16:9", "视频封面": "16:9", "b站": "16:9", "16x9": "16:9",
    "公众号": "2.35:1", "公众号封面": "2.35:1", "2.35": "2.35:1",
    "手机海报": "9:16", "竖屏": "9:16", "海报": "9:16", "9x16": "9:16",
}

PAGE_MAX_CHARS = 120
COVER_LINES = (1, 3)
CONTENT_TITLE_LINES = (1, 2)
MAX_POINTS = 3
LABEL_MAX = 6
SUBTITLE_MAX = 30
BADGE_MAIN_MAX = 12
BADGE_NOTE_MAX = 10
POINT_TEXT_MAX = 36
LEAD_MAX = 50
SIGNATURE_MAX = 20
SCENE_MAX = 80
SCENE_TEXT_MAX = 4
WIDE_SCENE_TITLE_LINES = 2
# 生图工具 ImageGen 支持的尺寸
GEN_SIZES = [(1536, 1024), (1024, 1024), (1024, 1536)]
# 顶部图的固定画风，所有封面共用，模型不改这一段
STYLE_PROMPT = (
    "Cute matte 3D toy style, soft studio lighting, rounded chunky shapes, clean premium editorial render. "
    "Palette: brand blue #315cff, signal yellow-green #dfff45, warm ivory #f6f4ed, ink black #141519, "
    "small mint #56e69c accents only. Every object uses only these colors (plus white and soft gray shadows); "
    "no pink, red, orange, purple or brown, except inside real product logos. Seamless light warm ivory background or brand-blue surfaces. "
    "One small scene with one clear focal action; the subject is big and fills the shown area, "
    "easy to read as a small phone thumbnail. No photo realism, no flat vector icons, no glass, no glow, "
    "no neon, no gradient background, no border or frame, no poster layout, no headline text."
)
# 空洞的营销词：只提醒，不拦
HYPE_WORDS = ["赋能", "颠覆", "重新定义", "生态闭环", "范式革命", "重塑未来", "一次讲清", "带你解锁", "史上最", "全网最", "震惊", "王炸", "天花板"]


def visible_len(s):
    return len(re.sub(r"\s", "", s or ""))


def fail(msgs, header="poster.json"):
    print(f"【需要修改】{header}（共 {len(msgs)} 处）：")
    for i, m in enumerate(msgs, 1):
        print(f"  {i}. {m}")
    print("改好 poster.json 后重新运行同一条命令。不要改脚本和样式。")
    sys.exit(1)


# ---------- 读取与检查 ----------

def load_spec(path):
    text = Path(path).read_text(encoding="utf-8").strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        fail([f"不是合法的 JSON：第 {e.lineno} 行第 {e.colno} 列附近，{e.msg}。检查引号、逗号、括号是否成对，字符串里的双引号要写成 \\\""])


def parse_size(raw, errors):
    if raw is None:
        return "3:4", SIZE_PRESETS["3:4"]
    key = str(raw).strip().lower().replace("：", ":").replace("×", "x").replace("*", "x")
    key = SIZE_ALIASES.get(key, key)
    if key in SIZE_PRESETS:
        return key, SIZE_PRESETS[key]
    m = re.fullmatch(r"(\d{3,4})\s*x\s*(\d{3,4})", key)
    if m:
        w, h = int(m.group(1)), int(m.group(2))
        if 300 <= w <= 4000 and 300 <= h <= 4000 and 0.3 <= h / w <= 3.4:
            return f"{w}x{h}", (w, h)
        errors.append(f"size「{raw}」超出范围：宽高要在 300–4000 像素之间，长边不超过短边的 3.3 倍")
        return None, None
    errors.append(f"size「{raw}」认不出。可选：{', '.join(SIZE_PRESETS)}，或写成「宽x高」，如「1242x1660」")
    return None, None


def as_lines(v):
    if v is None:
        return []
    if isinstance(v, str):
        return [s for s in v.split("\n") if s.strip()]
    return [str(s) for s in v if str(s).strip()]


def check_spec(spec, spec_dir, prompts_mode=False):
    errors, warnings = [], []
    if not isinstance(spec, dict):
        fail(["最外层要是一个 {...} 对象，里面有 size 和 pages"])
    size_name, size = parse_size(spec.get("size"), errors)
    pages = spec.get("pages")
    if not isinstance(pages, list) or not pages:
        errors.append("pages 要是一个列表，至少有一页")
        fail(errors)
    if len(pages) > 18:
        errors.append(f"一次最多 18 页，现在 {len(pages)} 页")
    sig = spec.get("signature")
    if sig and visible_len(sig) > SIGNATURE_MAX:
        errors.append(f"signature 落款最多 {SIGNATURE_MAX} 个字")

    norm = []
    for i, p in enumerate(pages, 1):
        where = f"第{i}页"
        if not isinstance(p, dict):
            errors.append(f"{where} 要是一个 {{...}} 对象")
            continue
        t = p.get("type", "cover" if i == 1 else "content")
        if t not in ("cover", "content"):
            errors.append(f"{where} type 只能是 cover（封面）或 content（内页），现在是「{t}」")
            continue
        title = as_lines(p.get("title"))
        q = {"type": t, "title": title}
        texts = list(title)
        if t == "cover":
            lo, hi = COVER_LINES
            if not lo <= len(title) <= hi:
                errors.append(f"{where}（封面）title 要写 {lo}–{hi} 行，现在 {len(title)} 行")
            hl = p.get("highlight", 2 if len(title) >= 2 else 0)
            if not isinstance(hl, int) or not 0 <= hl <= len(title):
                errors.append(f"{where} highlight 是要标蓝的行号（1–{len(title)}），0 表示不标蓝")
                hl = 0
            q["highlight"] = hl
            sub = p.get("subtitle") or ""
            if visible_len(sub) > SUBTITLE_MAX:
                errors.append(f"{where} subtitle 辅助小字最多 {SUBTITLE_MAX} 个字，现在 {visible_len(sub)} 个，请精简")
            q["subtitle"] = sub
            texts.append(sub)
            panel = p.get("panel", "blue")
            if panel not in PANEL_COLORS:
                errors.append(f"{where} panel 只能是 {', '.join(PANEL_COLORS)}，现在是「{panel}」")
                panel = "blue"
            q["panel"] = panel
            vis = p.get("visual")
            if vis in (None, "", "none"):
                q["visual"] = None
            elif isinstance(vis, dict) and vis.get("scene"):
                scene = str(vis["scene"]).strip()
                if visible_len(scene) > SCENE_MAX:
                    errors.append(f"{where} visual.scene 场景描述最多 {SCENE_MAX} 个字，现在 {visible_len(scene)} 个：只写一个动作和必须出现的东西")
                words = vis.get("text") or []
                if isinstance(words, str):
                    words = [words]
                words = [str(s).strip() for s in words if str(s).strip()]
                if len(words) > SCENE_TEXT_MAX:
                    errors.append(f"{where} visual.text 图里的字最多 {SCENE_TEXT_MAX} 处，现在 {len(words)} 处：只留 Logo 名、产品名或关键数字")
                texts += words  # 图里的字也算进这一页的字数
                img = None
                if vis.get("image"):
                    img = Path(vis["image"]).expanduser()
                    if not img.is_absolute():
                        img = (spec_dir / img).resolve()
                    if not img.is_file():
                        errors.append(f"{where} visual.image 找不到文件：{img}。填 ImageGen 返回的图片路径")
                        img = None
                elif not prompts_mode:
                    errors.append(f"{where} visual 写了 scene，但还没有生成图片：先在命令末尾加 --prompts 拿到生图参数，"
                                  "用 ImageGen 生成后把图片路径填到 visual.image（scene 保留），再出图；不生图就把 visual 改成 {\"icon\": \"图标名\"}")
                q["visual"] = {"scene": scene, "text": words, "image": str(img) if img else None}
            elif isinstance(vis, dict) and vis.get("icon"):
                if vis["icon"] not in ICONS:
                    errors.append(f"{where} visual.icon「{vis['icon']}」不存在。可选：{', '.join(ICONS)}")
                q["visual"] = {"icon": vis["icon"]}
            elif isinstance(vis, dict) and vis.get("image"):
                img = Path(vis["image"]).expanduser()
                if not img.is_absolute():
                    img = (spec_dir / img).resolve()
                if not img.is_file():
                    errors.append(f"{where} visual.image 找不到文件：{img}")
                elif img.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"):
                    errors.append(f"{where} visual.image 只支持 png、jpg、webp、gif、svg")
                fit = vis.get("fit", "contain")
                if fit not in ("contain", "cover"):
                    errors.append(f"{where} visual.fit 只能是 contain（完整显示）或 cover（铺满裁切）")
                q["visual"] = {"image": str(img), "fit": fit}
            else:
                errors.append(f"{where} visual 写成 {{\"scene\": \"场景描述\"}}、{{\"image\": \"图片路径\"}} 或 {{\"icon\": \"名字\"}}，不要主视觉就删掉这一项")
            if q.get("visual") and "icon" not in q["visual"] and size and orientation(*size) == "wide" and len(title) > WIDE_SCENE_TITLE_LINES:
                errors.append(f"{where} 横版封面配场景图或图片时，标题最多 {WIDE_SCENE_TITLE_LINES} 行，现在 {len(title)} 行：合并或精简成两行，细节挪到 subtitle")
        else:
            lo, hi = CONTENT_TITLE_LINES
            if not lo <= len(title) <= hi:
                errors.append(f"{where}（内页）title 要写 {lo}–{hi} 行，现在 {len(title)} 行")
            lead = p.get("lead") or ""
            if visible_len(lead) > LEAD_MAX:
                errors.append(f"{where} lead 导语最多 {LEAD_MAX} 个字，现在 {visible_len(lead)} 个")
            q["lead"] = lead
            texts.append(lead)
            badge = p.get("badge")
            if badge:
                if isinstance(badge, str):
                    badge = {"main": badge}
                main, note = str(badge.get("main", "")), str(badge.get("note", "") or "")
                if not main.strip():
                    errors.append(f"{where} badge 要有 main（大字），不需要就删掉 badge")
                if visible_len(main) > BADGE_MAIN_MAX:
                    errors.append(f"{where} badge.main 最多 {BADGE_MAIN_MAX} 个字，适合放日期、价格、数字")
                if visible_len(note) > BADGE_NOTE_MAX:
                    errors.append(f"{where} badge.note 最多 {BADGE_NOTE_MAX} 个字")
                q["badge"] = {"main": main, "note": note}
                texts += [main, note]
            points = p.get("points") or []
            if not isinstance(points, list):
                errors.append(f"{where} points 要是列表")
                points = []
            if len(points) > MAX_POINTS:
                errors.append(f"{where} points 最多 {MAX_POINTS} 条，现在 {len(points)} 条。先删重复和次要的；确实是两个独立问题再拆成两页")
            qp = []
            for j, pt in enumerate(points, 1):
                if isinstance(pt, str):
                    pt = {"text": pt}
                label, text = str(pt.get("label", "") or ""), str(pt.get("text", "") or "")
                if not text.strip():
                    errors.append(f"{where} 第{j}条要点缺 text")
                if visible_len(label) > LABEL_MAX:
                    errors.append(f"{where} 第{j}条 label「{label}」最多 {LABEL_MAX} 个字")
                if visible_len(text) > POINT_TEXT_MAX:
                    errors.append(f"{where} 第{j}条 text 最多 {POINT_TEXT_MAX} 个字，现在 {visible_len(text)} 个，请精简")
                qp.append({"label": label, "text": text})
                texts += [label, text]
            q["points"] = qp
            if not (qp or q.get("badge") or lead):
                errors.append(f"{where}（内页）除了标题，至少要有 points、badge、lead 其中一项")
        total = sum(visible_len(s) for s in texts)
        if total > PAGE_MAX_CHARS:
            errors.append(f"{where} 文字共 {total} 个字，上限 {PAGE_MAX_CHARS}。删掉重复和次要信息，不要靠缩小字号塞进去")
        for s in texts:
            for w in HYPE_WORDS:
                if w in s:
                    warnings.append(f"{where}「{s}」里有「{w}」，这类词空洞，建议换成具体信息")
        norm.append(q)
    if errors:
        fail(errors)
    return {"size_name": size_name, "size": size, "pages": norm, "signature": sig or ""}, warnings


# ---------- 生成网页 ----------

def esc(s):
    return html.escape(s or "", quote=True)


def orientation(w, h):
    r = h / w
    if r >= 1.2:
        return "tall"
    if r >= 0.85:
        return "square"
    return "wide"


def unit(w, h, orient):
    if orient == "wide":
        return h / 880
    return w / 1080


def page_html(spec, idx, workdir):
    w, h = spec["size"]
    orient = orientation(w, h)
    u = unit(w, h, orient)
    p = spec["pages"][idx]
    if orient == "wide" and p["type"] == "content":
        u *= 0.8  # 横图内页分左右两栏，字号小一档
    n = len(spec["pages"])
    css = (TEMPLATE_DIR / "poster.css").read_text(encoding="utf-8")
    js = (TEMPLATE_DIR / "fit.js").read_text(encoding="utf-8")
    meta = ""
    if n > 1:
        meta += f'<div class="pnum">{idx + 1:02d} / {n:02d}</div>'
    if spec["signature"]:
        meta += f'<div class="sign">{esc(spec["signature"])}</div>'

    if p["type"] == "cover":
        lines = "".join(
            f'<div class="line fit{" hl" if p["highlight"] == k else ""}" data-name="封面标题第{k}行"><span>{esc(s)}</span></div>'
            for k, s in enumerate(p["title"], 1))
        sub = f'<div class="subtitle fit" data-name="辅助小字"><span>{esc(p["subtitle"])}</span></div>' if p["subtitle"] else ""
        hero = ""
        vis = p["visual"]
        if vis and "scene" in vis:
            # 生图场景：不加底板，铺满主视觉区；图片对齐右下角，生成图右下角的「AI生成」标识不会被裁掉
            if vis["image"]:
                src = Path(vis["image"])
                dst = workdir / f"img-{idx + 1:02d}{src.suffix.lower()}"
                shutil.copyfile(src, dst)
                inner = f'<img class="pic scene" src="{dst.name}" alt="">'
            else:
                inner = ""  # --prompts 阶段还没有图，只量主视觉区的大小
            hero = f'<div class="hero scene">{inner}</div>'
        elif vis and "icon" in vis:
            # 不生图时的图标版：彩色底板＋图标
            panel = PANEL_COLORS[p["panel"]]
            stripe = "#141519" if p["panel"] == "yellow" else "#dfff45"
            hero = (f'<div class="hero" style="background:{panel["bg"]};--stripe:{stripe}">'
                    f'<div class="icon">{icon_svg(vis["icon"], p["panel"])}</div></div>')
        elif vis:
            # 用户自己的图：不加底板，放在暖白底上，默认完整显示
            src = Path(vis["image"])
            dst = workdir / f"img-{idx + 1:02d}{src.suffix.lower()}"
            shutil.copyfile(src, dst)
            hero = f'<div class="hero scene photo"><img class="pic photo {vis["fit"]}" src="{dst.name}" alt=""></div>'
        cls = f"cover {'with-hero' if hero else 'no-hero'}{' scene-hero' if vis and 'icon' not in vis else ''}"
        body = f'{hero}<div class="title-group">{lines}{sub}</div>'
    else:
        cls = "content"
        lines = "".join(
            f'<div class="line fit{" hl" if k == 2 else ""}" data-name="内页标题第{k}行"><span>{esc(s)}</span></div>'
            for k, s in enumerate(p["title"], 1))
        side = ""
        if p["lead"]:
            side += f'<div class="lead wrap" data-name="导语" data-max-lines="2">{esc(p["lead"])}</div>'
        if p.get("badge"):
            b = p["badge"]
            note = f'<span class="badge-note">{esc(b["note"])}</span>' if b["note"] else ""
            side += f'<div class="badge fit" data-name="突出数字"><span><span class="badge-main">{esc(b["main"])}</span>{note}</span></div>'
        if p["points"]:
            has_label = any(pt["label"] for pt in p["points"])
            rows = ""
            for j, pt in enumerate(p["points"], 1):
                if has_label:
                    rows += f'<div class="plabel">{esc(pt["label"])}</div>'
                rows += f'<div class="ptext wrap" data-name="第{j}条要点" data-max-lines="2">{esc(pt["text"])}</div>'
            side += f'<div class="points{" labeled" if has_label else ""}">{rows}</div>'
        body = f'<div class="content-group"><div class="ctitle">{lines}</div><div class="cbody">{side}</div></div>'

    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>page {idx + 1}</title>
<style>{css}</style></head>
<body><div class="page {orient} {cls}" style="--u:{u:.5f}px;--uw:{w / 1800:.5f}px;--w:{w}px;--h:{h}px">{body}{meta}</div>
<script>{js}</script></body></html>"""


# ---------- 生图参数 ----------

def pick_gen_size(box_w, box_h, wide):
    """选和主视觉区比例最接近的生图尺寸。竖版宁可裁上边，横版宁可裁左边（左边有渐变），右下角始终保留。"""
    r = box_w / box_h
    if wide:
        fits = [s for s in GEN_SIZES if s[0] / s[1] >= r]
        return min(fits, key=lambda s: s[0] / s[1]) if fits else GEN_SIZES[0]
    fits = [s for s in GEN_SIZES if s[0] / s[1] <= r]
    return max(fits, key=lambda s: s[0] / s[1]) if fits else GEN_SIZES[-1]


def shown_area(iw, ih, box_w, box_h):
    """图片铺满主视觉区、对齐右下角时，原图上能看到的区域（左边、上边各裁掉多少）。"""
    scale = max(box_w / iw, box_h / ih)
    return 1 - box_w / scale / iw, 1 - box_h / scale / ih


def build_prompt(vis, box_w, box_h, wide):
    gw, gh = pick_gen_size(box_w, box_h, wide)
    cut_x, cut_y = shown_area(gw, gh, box_w, box_h)
    parts = [STYLE_PROMPT, f"Scene: {vis['scene'].rstrip('。.')}."]
    if vis["text"]:
        words = "、".join(f"「{s}」" for s in vis["text"])
        parts.append(f"Text in the image, spelled exactly: {words}. No other words, letters or numbers.")
    else:
        parts.append("No words, letters, numbers or logos in the image.")
    if cut_x > 0.02 or cut_y > 0.02:
        parts.append(f"Composition: the left {cut_x:.0%} and the top {cut_y:.0%} of the image will be cropped off. "
                     "Keep the whole subject inside the remaining area and center it there.")
    else:
        parts.append("Composition: the whole image is shown; center the subject.")
    if wide:
        parts.append("The left edge of the shown area fades softly into the warm ivory background.")
    parts.append("Keep the bottom-right corner plain, without important details.")
    return {"size": f"{gw}x{gh}", "quality": "high", "prompt": " ".join(parts)}


def print_prompts(spec, reports, out):
    gen_dir = out / "生图原图"
    items = []
    for i, (p, rep) in enumerate(zip(spec["pages"], reports)):
        vis = p.get("visual") if p["type"] == "cover" else None
        if not vis or "scene" not in vis or not rep.get("hero"):
            continue
        box = rep["hero"]
        item = {"page": i + 1, **build_prompt(vis, box["w"], box["h"], orientation(*spec["size"]) == "wide"),
                "output_dir": str(gen_dir)}
        items.append(item)
    if not items:
        print("【提示】没有需要生图的封面：要生图就在封面的 visual 里写 scene。")
        return
    gen_dir.mkdir(parents=True, exist_ok=True)
    (out / "生图参数.json").write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"【生图】共 {len(items)} 张。先告诉用户：封面顶部图建议用 WorkBuddy 的生图功能画成 3D 场景图，效果最好；"
          "每张约 5–10 积分，生成的图右下角带「AI生成」标识，会保留在封面上；不想花积分可以说「不用生图」，"
          "改用内置图标，画面会简单一些。说完直接继续。")
    for it in items:
        print(f"\n第{it['page']}页封面：调用 ImageGen，参数原样照抄，不改 prompt，不传 footnote")
        print(f"  size: {it['size']}")
        print(f"  quality: {it['quality']}")
        print(f"  output_dir: {it['output_dir']}")
        print(f"  prompt: {it['prompt']}")
    print(f"\n参数也存在：{out / '生图参数.json'}")
    print("生成后把 ImageGen 返回的图片路径填到这一页的 visual.image（scene 和 text 保留），再去掉 --prompts 重新运行。")


# ---------- 出图 ----------

def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


class PlaywrightRenderer:
    name = "Playwright"

    def __init__(self):
        from playwright.sync_api import sync_playwright
        self._pw = sync_playwright().start()
        last = None
        for kw in ({}, {"channel": "chrome"}, {"channel": "msedge"}):
            try:
                self.browser = self._pw.chromium.launch(args=["--no-sandbox"], **kw)
                self.name = "Playwright " + (kw.get("channel") or "Chromium")
                return
            except Exception as e:  # noqa: BLE001
                last = e
        self._pw.stop()
        raise RuntimeError(last)

    def run(self, html_path, w, h, png_path=None):
        page = self.browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        try:
            page.goto(Path(html_path).as_uri())
            page.wait_for_function("window.__report !== undefined", timeout=15000)
            report = page.evaluate("window.__report")
            if png_path:
                page.screenshot(path=str(png_path), clip={"x": 0, "y": 0, "width": w, "height": h})
            return report
        finally:
            page.close()

    def close(self):
        self.browser.close()
        self._pw.stop()


def find_browser():
    cands = []
    if sys.platform == "darwin":
        for app, exe in [("Google Chrome", "Google Chrome"), ("Microsoft Edge", "Microsoft Edge"),
                         ("Chromium", "Chromium"), ("Brave Browser", "Brave Browser")]:
            for root in ("/Applications", str(Path.home() / "Applications")):
                cands.append(f"{root}/{app}.app/Contents/MacOS/{exe}")
    elif os.name == "nt":
        roots = [os.environ.get(k, "") for k in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA")]
        for r in filter(None, roots):
            cands += [rf"{r}\Google\Chrome\Application\chrome.exe", rf"{r}\Microsoft\Edge\Application\msedge.exe"]
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "msedge", "chrome"):
        found = shutil.which(name)
        if found:
            cands.append(found)
    return next((c for c in cands if Path(c).is_file()), None)


REPORT_RE = re.compile(rb'data-report="([^"]*)"')


class CliRenderer:
    """直接调用本机浏览器的无头模式。有的浏览器写完结果不退出，所以拿到结果就结束进程。"""

    def __init__(self, exe):
        self.exe = exe
        self.name = Path(exe).stem
        self.headless = "--headless=new"

    def _call(self, args, w, h, done, timeout=60):
        # --no-sandbox：WorkBuddy 等客户端本身跑在系统沙箱里，浏览器再开自己的沙箱会失败。这里只打开本脚本生成的本地网页
        cmd = [self.exe, self.headless, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
               "--no-default-browser-check", "--allow-file-access-from-files", "--force-device-scale-factor=1",
               f"--window-size={w},{h}", "--virtual-time-budget=4000"] + args
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        chunks = []
        reader = threading.Thread(target=lambda: chunks.extend(iter(lambda: proc.stdout.read(65536), b"")), daemon=True)
        reader.start()
        deadline = time.time() + timeout
        while time.time() < deadline and proc.poll() is None and not done(b"".join(chunks)):
            time.sleep(0.2)
        if proc.poll() is None:
            time.sleep(0.3)
            proc.kill()
        proc.wait()
        reader.join(2)
        return b"".join(chunks)

    def run(self, html_path, w, h, png_path=None):
        uri = Path(html_path).as_uri()
        out = self._call(["--dump-dom", uri], w, h, done=lambda b: b.rstrip().endswith(b"</html>"))
        m = REPORT_RE.search(out)
        if not m and self.headless == "--headless=new":
            self.headless = "--headless"  # 旧版浏览器不认识 --headless=new
            out = self._call(["--dump-dom", uri], w, h, done=lambda b: b.rstrip().endswith(b"</html>"))
            m = REPORT_RE.search(out)
        if not m:
            raise RuntimeError(f"{self.name} 没有返回排版结果")
        report = json.loads(html.unescape(m.group(1).decode("utf-8")))
        if png_path:
            png = Path(png_path)
            png.unlink(missing_ok=True)
            seen = []

            def written(_):
                if not png.exists() or png_size(png) is None:
                    return False
                seen.append(png.stat().st_size)
                return len(seen) >= 2 and seen[-1] == seen[-2]

            self._call([f"--screenshot={png}", uri], w, h, done=written)
        return report

    def close(self):
        pass


def get_renderer(mode="auto"):
    tried = []
    if mode == "browser":
        exe = find_browser()
        if not exe:
            print("【失败】没找到 Chrome、Edge 或 Chromium")
            sys.exit(2)
        return CliRenderer(exe)
    try:
        return PlaywrightRenderer()
    except ImportError:
        tried.append("没装 Playwright")
    except Exception as e:  # noqa: BLE001
        tried.append(f"Playwright 启动浏览器失败（{str(e).splitlines()[0][:120]}）")
    exe = find_browser()
    if exe:
        return CliRenderer(exe)
    tried.append("没找到 Chrome、Edge 或 Chromium")
    try:
        import playwright  # noqa: F401
        print("正在下载出图用的 Chromium（只需一次，约 150MB）……")
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True, timeout=900)
        return PlaywrightRenderer()
    except Exception:  # noqa: BLE001
        tried.append("自动安装 Chromium 失败")
    print("【失败】没法导出 PNG：" + "；".join(tried) + "。")
    print("请用户安装 Google Chrome 或 Microsoft Edge（Windows 自带 Edge）后重新运行；"
          "或者运行：python3 -m pip install playwright && python3 -m playwright install chromium")
    sys.exit(2)


def render_failed(renderer, err):
    print(f"【失败】出图失败（出图方式：{renderer.name}）：{str(err).splitlines()[0][:200] if str(err) else type(err).__name__}")
    print("这是运行环境的问题，不是文案的问题，不要改 poster.json。可以依次试：")
    print("  1. 换一种出图方式重跑：在命令末尾加 --renderer browser")
    print("  2. 让用户确认电脑上装了 Google Chrome 或 Microsoft Edge")
    print("  3. 把 poster.json 和这段报错发给用户，说明网页源文件已生成在输出文件夹的「_网页源文件」里")
    sys.exit(2)


def safe_name(s):
    s = re.sub(r'[\\/:*?"<>|\s]+', "", s)
    return s[:16] or "page"


def main():
    # Windows 中文系统的命令行是 GBK，打不出的字符用 ? 代替，不让脚本因为打印崩掉
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except AttributeError:
            pass
    ap = argparse.ArgumentParser(description="封面海报生成器")
    ap.add_argument("spec", help="poster.json 路径")
    ap.add_argument("--out", default=None, help="输出文件夹，默认是 poster.json 同目录下的「封面海报」")
    ap.add_argument("--check", action="store_true", help="只检查文案和排版，不导出 PNG")
    ap.add_argument("--prompts", action="store_true", help="检查文案和排版，给出封面顶部图的生图参数，不导出 PNG")
    ap.add_argument("--renderer", choices=["auto", "browser"], default="auto", help="出图方式，默认自动选择；browser 表示直接调用本机浏览器（排查问题用）")
    a = ap.parse_args()

    spec_path = Path(a.spec).resolve()
    if not spec_path.is_file():
        print(f"【失败】找不到 {spec_path}")
        sys.exit(1)
    spec, warnings = check_spec(load_spec(spec_path), spec_path.parent, prompts_mode=a.prompts)
    out = Path(a.out).resolve() if a.out else spec_path.parent / "封面海报"
    # 只检查时不在用户文件夹里留下文件
    work = Path(tempfile.mkdtemp(prefix="poster-check-")) if a.check or a.prompts else out / "_网页源文件"
    work.mkdir(parents=True, exist_ok=True)
    w, h = spec["size"]

    htmls = []
    for i, p in enumerate(spec["pages"]):
        f = work / f"page-{i + 1:02d}.html"
        f.write_text(page_html(spec, i, work), encoding="utf-8")
        htmls.append(f)

    renderer = get_renderer(a.renderer)
    try:
        try:
            reports = [renderer.run(f, w, h) for f in htmls]
        except Exception as e:  # noqa: BLE001
            exe = find_browser()
            if isinstance(renderer, PlaywrightRenderer) and exe:
                renderer.close()
                renderer = CliRenderer(exe)
                try:
                    reports = [renderer.run(f, w, h) for f in htmls]
                except Exception as e2:  # noqa: BLE001
                    render_failed(renderer, e2)
            else:
                render_failed(renderer, e)
        problems = []
        for i, rep in enumerate(reports):
            problems += [f"第{i + 1}页 {m}" for m in rep.get("errors", [])]
        if problems:
            fail(problems, header=f"排版放不下（尺寸 {spec['size_name']}，{w}×{h}）")
        if a.check:
            print(f"【检查通过】{len(htmls)} 页，尺寸 {spec['size_name']}（{w}×{h}）。去掉 --check 即可出图。")
            return
        if a.prompts:
            print_prompts(spec, reports, out)
            return
        for i, rep in enumerate(reports):
            crop = rep.get("sceneCrop")
            if crop and max(crop["x"], crop["y"]) > 0.35:
                warnings.append(f"第{i + 1}页生成图和主视觉区比例差得多，左边裁掉约 {crop['x']:.0%}、上边裁掉约 {crop['y']:.0%}："
                                "打开 PNG 看主体是否完整，不完整就按 --prompts 给的 size 重新生成")
        files = []
        for i, (f, p) in enumerate(zip(htmls, spec["pages"])):
            label = "封面" if i == 0 and p["type"] == "cover" else safe_name(p["title"][0])
            png = out / f"{i + 1:02d}-{label}.png"
            try:
                renderer.run(f, w, h, png)
            except Exception as e:  # noqa: BLE001
                render_failed(renderer, e)
            got = png_size(png) if png.exists() else None
            if got != (w, h):
                print(f"【失败】第{i + 1}页导出失败（得到 {got}，应为 {w}×{h}），出图方式：{renderer.name}")
                sys.exit(2)
            files.append(png)
    finally:
        renderer.close()

    imgs = "".join(f'<figure><img src="{esc(p.name)}"><figcaption>{esc(p.name)}</figcaption></figure>' for p in files)
    (out / "预览.html").write_text(
        f'<!doctype html><meta charset="utf-8"><title>预览</title><style>body{{margin:24px;background:#e9e7e0;font:14px sans-serif}}'
        f'main{{display:flex;flex-wrap:wrap;gap:20px}}figure{{margin:0}}img{{display:block;max-width:{min(420, w // 2)}px;'
        f'box-shadow:0 2px 12px rgba(0,0,0,.15)}}</style><main>{imgs}</main>', encoding="utf-8")
    for m in warnings:
        print("【提醒】" + m)
    if any(p["type"] == "cover" and p.get("visual") and "icon" in p["visual"] for p in spec["pages"]):
        print("【提醒】封面用的是内置图标。交付时把引号里这句话告诉用户（只说引号里的内容）："
              "“这张用的是内置图标，画面比较简单；建议生成 3D 场景图，效果会好很多，每张约 5–10 积分，想换直接说『换成生图』。”")
    print(f"【完成】{len(files)} 张 PNG，尺寸 {spec['size_name']}（{w}×{h}），出图方式：{renderer.name}")
    for p in files:
        print("  " + str(p))
    print("  预览：" + str(out / "预览.html"))


if __name__ == "__main__":
    main()
