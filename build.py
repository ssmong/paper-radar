#!/usr/bin/env python3
"""Parses survey.md → docs/index.html + docs/ko/index.html (dual language)"""

import json
import re
from datetime import datetime
from html import escape, unescape
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).parent
DOCS_DIR = ROOT / "docs"

CHECK = '<span class="badge badge-yes"><svg width="16" height="16" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7.5" fill="currentColor" opacity="0.12"/><path d="M4.5 8.5L7 11l4.5-5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg></span>'
CROSS = '<span class="badge badge-no"><svg width="16" height="16" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7.5" fill="currentColor" opacity="0.12"/><path d="M5.25 5.25l5.5 5.5M10.75 5.25l-5.5 5.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/></svg></span>'
DETAIL_BTN = '<svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="2" y="1.5" width="12" height="13" rx="2"/><path d="M5 5.5h6M5 8h6M5 10.5h4"/></svg>'

UI = {
    "en": {
        "html_lang": "en",
        "survey_file": "content/survey.md",
        "detail_src": "content/detailed",
        "output": "index.html",
        "details_out": "details",
        "css": "style.css", "js": "app.js",
        "page_title": "Contact-Rich Dexterous Manipulation Survey",
        "utility": "Research Survey",
        "updated": "Last updated",
        "logo": "DexManip Survey",
        "search_global": "Search all tables...",
        "search_table": "Search this table...",
        "hero_t": "Contact-Rich<br>Dexterous Manipulation",
        "hero_sub": "A Comprehensive Survey",
        "hero_desc": "Papers, repos, and datasets for dexterous manipulation, force-aware VLAs, impedance learning, RL policies, and related benchmarks.",
        "author": "Yeonseo Lee &middot; Seoul National University",
        "s_entries": "Entries", "s_sections": "Sections", "s_oss": "Open Source", "s_details": "Detailed Reviews",
        "f_filter": "Filter:", "f_hand": "Hand:",
        "f_all": "All", "f_code": "Has Code", "f_weights": "Has Weights",
        "f_dex": "Dexterous", "f_grip": "Gripper", "f_biman": "Bimanual", "f_body": "Full Body",
        "y_all": "All Years", "y_older": "2022 &amp; earlier",
        "ft_title": "Contact-Rich Dexterous Manipulation Survey",
        "ft_desc": "An interactive survey of dexterous manipulation, force-aware VLAs, impedance learning, and related benchmarks.",
        "ft_res": "Resources",
        "ft_bottom": "GitHub links and weight availability were checked as of {d}; links may become stale.",
        "og": "Interactive survey covering {n}+ papers across dexterous manipulation, force-aware VLAs, and impedance control.",
        "lang_links": [("", "ENG", True), ("ko/", "KOR", False), ("zh/", "CHN", False)],
    },
    "ko": {
        "html_lang": "ko",
        "survey_file": "content/survey_ko.md",
        "detail_src": "content/detailed_ko",
        "output": "ko/index.html",
        "details_out": "ko/details",
        "css": "../style.css", "js": "../app.js",
        "page_title": "접촉 풍부 다지 조작 서베이",
        "utility": "연구 서베이",
        "updated": "최종 업데이트",
        "logo": "다지 조작 서베이",
        "search_global": "전체 검색...",
        "search_table": "이 테이블에서 검색...",
        "hero_t": "Contact-Rich<br>Dexterous Manipulation",
        "hero_sub": "종합 서베이",
        "hero_desc": "Dexterous manipulation, force-aware VLA, impedance 학습, RL 정책 및 관련 benchmark에 대한 논문, 저장소, 데이터셋을 정리한 서베이입니다.",
        "author": "이연서 &middot; 서울대학교",
        "s_entries": "항목", "s_sections": "섹션", "s_oss": "Open Source", "s_details": "상세 리뷰",
        "f_filter": "필터:", "f_hand": "Hand:",
        "f_all": "전체", "f_code": "코드 공개", "f_weights": "가중치 공개",
        "f_dex": "Dexterous", "f_grip": "Gripper", "f_biman": "Bimanual", "f_body": "Humanoid",
        "y_all": "전체 연도", "y_older": "2022년 이전",
        "ft_title": "Contact-Rich Dexterous Manipulation 서베이",
        "ft_desc": "Dexterous manipulation, force-aware VLA, impedance 학습 및 관련 benchmark에 대한 인터랙티브 서베이입니다.",
        "ft_res": "참고 자료",
        "ft_bottom": "GitHub 링크 및 가중치 공개 여부는 {d} 기준으로 확인되었으며, 이후 변경될 수 있습니다.",
        "og": "다지 조작, 힘 인식 VLA 및 임피던스 제어에 관한 {n}+편의 논문을 다루는 인터랙티브 서베이.",
        "lang_links": [("../", "ENG", False), ("", "KOR", True), ("../zh/", "CHN", False)],
    },
    "zh": {
        "html_lang": "zh",
        "survey_file": "content/survey_zh.md",
        "detail_src": "content/detailed_zh",
        "output": "zh/index.html",
        "details_out": "zh/details",
        "css": "../style.css", "js": "../app.js",
        "page_title": "接触丰富灵巧操作综述",
        "utility": "研究综述",
        "updated": "最后更新",
        "logo": "灵巧操作综述",
        "search_global": "搜索所有表格...",
        "search_table": "在此表中搜索...",
        "hero_t": "Contact-Rich<br>Dexterous Manipulation",
        "hero_sub": "综合综述",
        "hero_desc": "Dexterous manipulation, force-aware VLA, impedance learning, RL policy 及相关 benchmark 的论文、代码库和数据集综述。",
        "author": "Yeonseo Lee &middot; Seoul National University",
        "s_entries": "条目", "s_sections": "章节", "s_oss": "Open Source", "s_details": "详细评述",
        "f_filter": "筛选:", "f_hand": "Hand:",
        "f_all": "全部", "f_code": "有代码", "f_weights": "有权重",
        "f_dex": "Dexterous", "f_grip": "Gripper", "f_biman": "Bimanual", "f_body": "Humanoid",
        "y_all": "所有年份", "y_older": "2022年及以前",
        "ft_title": "Contact-Rich Dexterous Manipulation 综述",
        "ft_desc": "Dexterous manipulation, force-aware VLA, impedance learning 及相关 benchmark 的交互式综述。",
        "ft_res": "参考资源",
        "ft_bottom": "GitHub链接和权重可用性截至{d}验证，链接可能会失效。",
        "og": "涵盖{n}+篇灵巧操作、力感知VLA及阻抗控制论文的交互式综述。",
        "lang_links": [("../", "ENG", False), ("../ko/", "KOR", False), ("", "CHN", True)],
    },
}


def norm(name: str) -> str:
    name = re.sub(r"(\d+)\.\d+", r"\1", name)
    return re.sub(r"[^a-z0-9]", "", name.lower())


# ── Detail file scanning ──────────────────────────────────────────────

def scan_details(detail_dir: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    if not detail_dir.exists():
        return mapping
    for sec_dir in sorted(detail_dir.iterdir()):
        if not sec_dir.is_dir():
            continue
        for md_file in sec_dir.glob("*.md"):
            if md_file.name.startswith("_"):
                continue
            first = md_file.read_text(encoding="utf-8", errors="replace").split("\n")[0]
            title = re.sub(r"^#+\s*(\d+(\.\d+)?\s+)?", "", first).strip()
            n = norm(title)
            if n:
                mapping[n] = f"{sec_dir.name}/{md_file.stem}"
            fn = norm(md_file.stem)
            if fn and fn not in mapping:
                mapping[fn] = f"{sec_dir.name}/{md_file.stem}"
    return mapping


def render_detail_md(md_text: str) -> str:
    lines = md_text.split("\n")
    parts: list[str] = []
    in_ul = False
    in_tbl = False

    def close_ul():
        nonlocal in_ul
        if in_ul:
            parts.append("</ul>"); in_ul = False

    def close_tbl():
        nonlocal in_tbl
        if in_tbl:
            parts.append("</tbody></table></div>"); in_tbl = False

    for line in lines:
        s = line.strip()
        if not s:
            close_ul(); close_tbl(); continue
        if s == "---":
            close_ul(); close_tbl(); parts.append("<hr>"); continue
        if s.startswith("### "):
            close_ul(); close_tbl()
            parts.append(f'<h3 class="dp-h3">{render_inline(s[4:])}</h3>'); continue
        if s.startswith("## "):
            close_ul(); close_tbl()
            parts.append(f'<h2 class="dp-h2">{render_inline(s[3:])}</h2>'); continue
        if s.startswith("> "):
            close_ul(); close_tbl()
            parts.append(f'<blockquote class="dp-quote">{render_inline(s[2:])}</blockquote>'); continue
        if s.startswith("- "):
            close_tbl()
            if not in_ul:
                parts.append('<ul class="dp-list">'); in_ul = True
            parts.append(f"<li>{render_inline(s[2:])}</li>"); continue
        if s.startswith("|") and "|" in s[1:]:
            close_ul()
            if re.match(r"^\|[\s\-:|]+\|$", s):
                continue
            cells = [c.strip() for c in s.strip("|").split("|")]
            if not in_tbl:
                in_tbl = True
                parts.append('<div class="dp-tbl-wrap"><table class="dp-tbl"><thead><tr>')
                for c in cells:
                    parts.append(f"<th>{render_inline(c)}</th>")
                parts.append("</tr></thead><tbody>")
            else:
                parts.append("<tr>")
                for c in cells:
                    parts.append(f"<td>{render_inline(c)}</td>")
                parts.append("</tr>")
            continue
        close_ul(); close_tbl()
        parts.append(f'<p class="dp-p">{render_inline(s)}</p>')

    close_ul(); close_tbl()
    return "\n".join(parts)


def load_reviews() -> dict:
    p = ROOT / "reviews" / "data.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


REVIEW_UI = {
    "en": {"title": "Peer Reviews", "avg": "Average", "reviews": "reviews"},
    "ko": {"title": "피어 리뷰", "avg": "평균", "reviews": "개 리뷰"},
    "zh": {"title": "同行评审", "avg": "平均分", "reviews": "条评审"},
}

def safe_href(value: str) -> str:
    value = unescape(value)
    try:
        if urlsplit(value).scheme.lower() not in {"", "http", "https"}:
            return "#"
    except ValueError:
        return "#"
    return escape(value, quote=True)


def render_review_section(review_data: dict, lang: str = "en") -> str:
    ru = REVIEW_UI.get(lang, REVIEW_UI["en"])
    if not review_data.get("found") or not review_data.get("reviews"):
        if review_data.get("url"):
            return f'<details class="dp-reviews"><summary>{ru["title"]}</summary><div class="dp-review-body"><p class="dp-p"><a href="{safe_href(review_data["url"])}" target="_blank" rel="noopener">OpenReview</a></p></div></details>'
        return ""
    url = safe_href(review_data["url"])
    avg = review_data.get("avg_rating")
    n = review_data.get("num_reviews", len(review_data["reviews"]))
    venue = review_data.get("venue", "")

    h = f'<details class="dp-reviews"><summary>{ru["title"]}'
    if avg is not None:
        h += f' <span class="dp-review-score-badge">{escape(str(avg))}</span>'
    h += '</summary>\n<div class="dp-review-body">\n'
    h += f'<p class="dp-review-meta">'
    if avg is not None:
        h += f'{ru["avg"]}: <strong>{escape(str(avg))}</strong> · '
    h += f'{escape(str(n))} {ru["reviews"]}'
    if venue:
        h += f' · {escape(str(venue))}'
    h += f' · <a href="{url}" target="_blank" rel="noopener">OpenReview</a></p>\n'

    for i, r in enumerate(review_data["reviews"]):
        rating = r.get("rating", "—")
        summary = r.get("summary", "")
        h += f'<div class="dp-review-item">'
        h += f'<span class="dp-review-r">R{i+1}: {escape(str(rating))}</span>'
        if summary:
            short = summary[:200] + ("…" if len(summary) > 200 else "")
            h += f' <span class="dp-review-text">{escape(short, quote=False)}</span>'
        h += '</div>\n'

    h += '</div>\n</details>\n'
    return h


def build_detail_pages(detail_map: dict[str, str], detail_dir: Path, out_base: Path, lang: str = "en") -> int:
    reviews = load_reviews()
    count = 0
    for key, rel_path in detail_map.items():
        parts = rel_path.split("/")
        src = detail_dir / parts[0] / f"{parts[1]}.md"
        if not src.exists():
            continue
        md = src.read_text(encoding="utf-8", errors="replace")
        html = render_detail_md(md)
        rd = reviews.get(key)
        if rd:
            html += "\n" + render_review_section(rd, lang)
        out_dir = out_base / parts[0]
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{parts[1]}.html"
        if not out_path.exists() or out_path.read_text(encoding="utf-8", errors="replace") != html:
            out_path.write_text(html, encoding="utf-8")
        count += 1
    return count


# ── Inline markdown ───────────────────────────────────────────────────

def render_inline(text: str) -> str:
    if not text:
        return ""
    text = escape(text, quote=False)
    text = re.sub(r"\[(\*\*(.+?)\*\*)\]\(([^)]+)\)",
                  lambda m: f'<a href="{safe_href(m[3])}" target="_blank" rel="noopener"><strong>{m[2]}</strong></a>', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                  lambda m: f'<a href="{safe_href(m[2])}" target="_blank" rel="noopener">{m[1]}</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\w)\*([^*]+)\*(?!\w)", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


# ── Badge rendering ───────────────────────────────────────────────────

def badge(text: str) -> str:
    s = text.strip()
    if s == "—":
        return '<span class="badge badge-na">—</span>'
    has_y = "✅" in s
    has_n = "✗" in s
    if not has_y and not has_n:
        return render_inline(s)
    remaining = s.replace("✅", "").replace("✗", "").strip()
    b = CHECK if has_y else CROSS
    if remaining:
        return b + " " + render_inline(remaining)
    return b


# ── Hand type classification ─────────────────────────────────────────

DEX_KW = ["allegro", "shadow", "leap", "inspire", "xhand", "d'claw", "multi-finger",
          "dexterous", "sharpa", "ability", "oymotion", "wuji", "schunk", "rohand",
          "adroit", "mano", "dex-ee", "anthropomorphic", "5-finger", "dex hand",
          "dclaw", "fourier", "faive", "orca", "isyhand", "ruka", "psyonic",
          "다지", "덱스"]

def classify_hand(cells: list[str], headers: list[str]) -> list[str]:
    hl = [h.lower() for h in headers]
    hand_txt = ""
    robot_txt = ""
    for i, h in enumerate(hl):
        if i >= len(cells):
            break
        cl = cells[i].lower()
        if any(k in h for k in ("hand", "dex hand", "dof", "target hand", "핸드", "자유도", "다지")):
            hand_txt += " " + cl
        if any(k in h for k in ("robot", "로봇")):
            robot_txt += " " + cl
    combined = hand_txt + " " + robot_txt
    tags: list[str] = []
    if any(k in combined for k in DEX_KW) or ("✅" in hand_txt):
        tags.append("dex")
    if any(k in combined for k in ("gripper", "parallel", "그리퍼")):
        tags.append("gripper")
    if "✗" in hand_txt and "dex" not in tags and "gripper" not in tags:
        tags.append("gripper")
    if any(k in combined for k in ["bimanual", "2x ", "dual", "2×", "양손"]):
        tags.append("bimanual")
    if any(k in combined for k in ["humanoid", "unitree", " g1 ", " h1", "휴머노이드"]):
        tags.append("fullbody")
    return tags


# ── Table parsing & rendering ─────────────────────────────────────────

def parse_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]

def is_sep(line: str) -> bool:
    return bool(re.match(r"^\|[\s\-:|]+\|$", line.strip()))

def row_meta(cells: list[str], headers: list[str]) -> dict[str, str]:
    meta: dict[str, str] = {}
    hl = [h.lower() for h in headers]
    for i, h in enumerate(hl):
        if i >= len(cells):
            break
        c = cells[i]
        if h in ("year", "date", "연도", "날짜"):
            m = re.search(r"(20\d{2})", c)
            if m:
                meta["year"] = m.group(1)
        if any(k in h for k in ("code", "open code", "design files", "install", "코드", "설계", "설치")):
            meta["code"] = "true" if ("✅" in c or "github" in c.lower() or "pip" in c.lower()) else "false"
        if any(k in h for k in ("weights", "open weights", "가중치", "공개 가중치")):
            meta["weights"] = "true" if ("✅" in c or "ckpt" in c.lower() or "hf" in c.lower() or "apache" in c.lower()) else "false"
        if any(k in h for k in ("download", "다운로드")):
            meta["code"] = "true" if "✅" in c else "false"
    hand_tags = classify_hand(cells, headers)
    if hand_tags:
        meta["hand"] = " ".join(hand_tags)
    return meta


def extract_paper_name(cell: str) -> str:
    m = re.search(r"\*\*([^*]+)\*\*", cell)
    return m.group(1) if m else cell.strip()[:30]


def render_table(headers: list[str], rows: list[list[str]], sec_id: str,
                 detail_map: dict[str, str], search_ph: str) -> str:
    n = len(rows)
    h = '<div class="table-card">\n'
    h += '  <div class="table-controls">\n'
    h += '    <div class="table-search-wrap"><svg class="search-icon" viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/></svg>'
    h += f'<input type="search" class="table-search" placeholder="{search_ph}"></div>\n'
    h += f'    <span class="table-count"><span class="count-visible">{n}</span> / {n}</span>\n'
    h += '  </div>\n  <div class="table-scroll">\n'
    h += f'    <table class="survey-table" data-section="{sec_id}" data-total="{n}">\n'
    h += '      <thead><tr>\n'
    for col in headers:
        h += f'        <th class="sortable">{escape(col)}</th>\n'
    h += '      </tr></thead>\n      <tbody>\n'
    for row in rows:
        m = row_meta(row, headers)
        attrs = " ".join(f'data-{k}="{v}"' for k, v in m.items())
        h += f'      <tr {attrs}>\n'
        for ci, cell in enumerate(row):
            rendered = badge(cell)
            if ci == 0:
                pname = extract_paper_name(cell)
                nk = norm(pname)
                dp = detail_map.get(nk)
                if dp:
                    rendered += f' <button class="detail-btn" data-detail="details/{escape(dp)}.html" data-title="{escape(pname)}" title="View details">{DETAIL_BTN}</button>'
            h += f'        <td>{rendered}</td>\n'
        h += '      </tr>\n'
    h += '      </tbody>\n    </table>\n  </div>\n</div>\n'
    return h


# ── Section parsing ───────────────────────────────────────────────────

def parse_md(md: str, detail_map: dict[str, str], search_ph: str) -> tuple[str, list[dict], str]:
    lines = md.split("\n")
    sections: list[dict] = []
    cur: dict | None = None
    content: list[tuple] = []
    in_table = False
    t_hdr: list[str] | None = None
    t_rows: list[list[str]] = []

    date_match = re.search(r"Last updated:\s*(\d{4}-\d{2}-\d{2})", md)
    if not date_match:
        date_match = re.search(r"최종 업데이트:\s*(\d{4}-\d{2}-\d{2})", md)
    if date_match:
        d = datetime.strptime(date_match.group(1), "%Y-%m-%d")
        date_str = d.strftime("%Y년 %m월 %d일") if "최종" in (date_match.group(0)) else d.strftime("%B %d, %Y")
    else:
        date_str = "May 14, 2026"

    def flush_table():
        nonlocal in_table, t_hdr, t_rows
        if t_hdr and t_rows:
            sid = cur["id"] if cur else "intro"
            content.append(("table", render_table(t_hdr, t_rows, sid, detail_map, search_ph)))
        in_table = False; t_hdr = None; t_rows = []

    def flush_section():
        nonlocal cur, content
        flush_table()
        if cur:
            cur["content"] = content; sections.append(cur); content = []

    for line in lines:
        if line.startswith("## "):
            flush_section()
            title = line[3:].strip()
            m = re.match(r"(\d+(?:\.\d+)?)\.\s*(.*)", title)
            num, ttl = (m.group(1), m.group(2)) if m else ("", title)
            sec_id = f"sec-{num}" if num else re.sub(r"[^a-z0-9]+", "-", ttl.lower()).strip("-")
            cur = {"id": sec_id, "number": num, "title": ttl, "content": []}; content = []
            continue
        if line.startswith("### "):
            flush_table()
            title = line[4:].strip()
            m = re.match(r"(\d+(?:\.\d+)?)\s*(.*)", title)
            num, ttl = (m.group(1), m.group(2)) if m else ("", title)
            sub_id = re.sub(r"[^a-z0-9]+", "-", ttl.lower()).strip("-")
            content.append(("sub", num, ttl, sub_id)); continue
        if line.strip().startswith("|") and "|" in line.strip()[1:]:
            if is_sep(line):
                continue
            cells = parse_row(line)
            if not in_table:
                in_table = True; t_hdr = cells
            else:
                t_rows.append(cells)
            continue
        if in_table:
            flush_table()
        if line.strip() in ("---", "") or line.startswith("# ") or line.startswith("> "):
            continue
        if cur:
            content.append(("text", line.strip()))

    flush_section()

    sb = ""
    for sec in sections:
        if sec["number"]:
            n = sec["number"].zfill(2) if len(sec["number"]) == 1 else sec["number"]
            short = sec["title"][:30] + "…" if len(sec["title"]) > 32 else sec["title"]
            subs = [it for it in sec["content"] if it[0] == "sub"]
            sb += f'<div class="sb-group" data-section="{sec["id"]}">\n'
            sb += f'  <a href="#{sec["id"]}" class="sb-link" data-target="{sec["id"]}"><span class="sb-num">{n}</span>{escape(short)}</a>\n'
            if subs:
                sb += '  <div class="sb-subs">\n'
                for it in subs:
                    _, sn, st, si = it
                    ss = st[:26] + "…" if len(st) > 26 else st
                    sb += f'    <a href="#sub-{si}" class="sb-sub">{sn} {escape(ss)}</a>\n'
                sb += '  </div>\n'
            sb += '</div>\n'

    return sb, sections, date_str


def render_sections(sections: list[dict]) -> str:
    bands = ["band-canvas", "band-cloud"]
    out = ""
    for idx, sec in enumerate(sections):
        band = bands[idx % 2]
        out += f'<section class="section {band}" id="{sec["id"]}">\n  <div class="container">\n'
        out += '    <div class="section-header">\n'
        if sec["number"]:
            n = sec["number"].zfill(2) if len(sec["number"]) == 1 else sec["number"]
            out += f'      <span class="section-number">{n}</span>\n'
        out += f'      <h2>{escape(sec["title"])}</h2>\n    </div>\n'
        for item in sec["content"]:
            if item[0] == "text":
                rendered = render_inline(item[1])
                cls = "note" if item[1].startswith("Note:") or item[1].startswith("참고:") else "section-text"
                out += f'    <p class="{cls}">{rendered}</p>\n'
            elif item[0] == "sub":
                _, num, title, sub_id = item
                out += f'    <div class="subsection" id="sub-{sub_id}"><h3>'
                if num:
                    out += f'<span class="sub-number">{num}</span> '
                out += f'{escape(title)}</h3></div>\n'
            elif item[0] == "table":
                out += f'    {item[1]}\n'
        out += '  </div>\n</section>\n\n'
    return out


def count_stats(md: str) -> dict[str, int]:
    rows = code = secs = 0
    in_t = False; is_hdr = True
    for line in md.split("\n"):
        if line.startswith("## "):
            secs += 1
        if line.strip().startswith("|") and "|" in line.strip()[1:]:
            if is_sep(line):
                continue
            if not in_t:
                in_t = True; is_hdr = True
            elif is_hdr:
                is_hdr = False
            else:
                rows += 1
                if "github" in line.lower():
                    code += 1
        else:
            if in_t:
                in_t = False; is_hdr = True
    return {"entries": rows, "sections": secs, "open_source": code}


# ── Page template ─────────────────────────────────────────────────────

def build(md: str, lang: str = "en") -> tuple[str, int]:
    u = UI[lang]
    parts = []
    for url, label, active in u["lang_links"]:
        if active:
            parts.append(f'<span class="lang-toggle lang-active">{label}</span>')
        else:
            parts.append(f'<a href="{url}" class="lang-toggle">{label}</a>')
    lang_links_html = '<span class="lang-sep">|</span>'.join(parts)
    detail_dir = ROOT / u["detail_src"]
    details_out = DOCS_DIR / u["details_out"]
    detail_map = scan_details(detail_dir)
    detail_count = build_detail_pages(detail_map, detail_dir, details_out, lang)
    sidebar_html, sections, date_str = parse_md(md, detail_map, u["search_table"])
    stats = count_stats(md)
    sections_html = render_sections(sections)
    n = stats["entries"]

    html = f"""<!DOCTYPE html>
<html lang="{u['html_lang']}" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{u['page_title']}</title>
<meta name="description" content="{u['og'].format(n=n)}">
<meta property="og:title" content="{u['page_title']}">
<meta property="og:description" content="{u['og'].format(n=n)}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css">
<link rel="stylesheet" href="{u['css']}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🤖</text></svg>">
</head>
<body>

<div class="utility-strip">
  <div class="container utility-inner">
    <span class="utility-label">{u['utility']} &mdash; {u['updated']} {date_str}</span>
    <div class="utility-actions">
      {lang_links_html}
      <button class="font-toggle" id="font-toggle" aria-label="Toggle font size" title="Font size">
        <span id="font-label">A+</span>
      </button>
      <button class="theme-toggle" id="theme-toggle" aria-label="Toggle theme">
        <svg class="icon-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
        <svg class="icon-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>
      </button>
    </div>
  </div>
</div>

<nav class="nav-bar" id="nav-bar">
  <div class="container nav-inner">
    <a href="#" class="nav-logo">{u['logo']}</a>
    <div class="nav-actions">
      <div class="global-search-wrap">
        <svg class="search-icon" viewBox="0 0 20 20" fill="currentColor" width="16" height="16"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/></svg>
        <input type="search" id="global-search" class="global-search" placeholder="{u['search_global']}">
      </div>
    </div>
  </div>
</nav>

<section class="hero-section">
  <div class="container">
    <div class="hero-card">
      <div class="chevron chevron-left"></div>
      <div class="hero-content">
        <h1>{u['hero_t']}</h1>
        <p class="hero-subtitle">{u['hero_sub']}</p>
        <p class="hero-author">{u['author']}</p>
        <p class="hero-desc">{u['hero_desc']}</p>
        <div class="hero-stats">
          <div class="stat"><span class="stat-number">{n}+</span><span class="stat-label">{u['s_entries']}</span></div>
          <div class="stat"><span class="stat-number">{stats['sections']}</span><span class="stat-label">{u['s_sections']}</span></div>
          <div class="stat"><span class="stat-number">{stats['open_source']}+</span><span class="stat-label">{u['s_oss']}</span></div>
          <div class="stat"><span class="stat-number">{detail_count}</span><span class="stat-label">{u['s_details']}</span></div>
        </div>
      </div>
      <div class="chevron chevron-right"></div>
    </div>
  </div>
</section>

<div class="filter-band band-cloud">
  <div class="container">
    <div class="filter-row">
      <div class="filter-group">
        <span class="filter-label">{u['f_filter']}</span>
        <button class="chip chip-active" data-filter="all">{u['f_all']}</button>
        <button class="chip" data-filter="code">{u['f_code']}</button>
        <button class="chip" data-filter="weights">{u['f_weights']}</button>
      </div>
      <div class="filter-group">
        <span class="filter-label">{u['f_hand']}</span>
        <button class="chip chip-toggle" data-hand="dex">{u['f_dex']}</button>
        <button class="chip chip-toggle" data-hand="gripper">{u['f_grip']}</button>
        <button class="chip chip-toggle" data-hand="bimanual">{u['f_biman']}</button>
        <button class="chip chip-toggle" data-hand="fullbody">{u['f_body']}</button>
      </div>
      <select class="year-select" id="year-filter">
        <option value="">{u['y_all']}</option>
        <option value="2026">2026</option>
        <option value="2025">2025</option>
        <option value="2024">2024</option>
        <option value="2023">2023</option>
        <option value="older">{u['y_older']}</option>
      </select>
    </div>
  </div>
</div>

<div class="layout">
  <aside class="sidebar" id="sidebar">
    <nav class="sb-nav">
      {sidebar_html}
    </nav>
  </aside>
  <div class="main-content">
    {sections_html}
  </div>
</div>

<footer class="footer-dark">
  <div class="container">
    <div class="footer-content">
      <div class="footer-main">
        <h3>{u['ft_title']}</h3>
        <p>{u['ft_desc']}</p>
      </div>
      <div class="footer-links">
        <h4>{u['ft_res']}</h4>
        <a href="https://github.com/Physical-Intelligence/openpi" target="_blank" rel="noopener">OpenPI (pi0)</a>
        <a href="https://github.com/NVIDIA/Isaac-GR00T" target="_blank" rel="noopener">Isaac-GR00T</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>{u['ft_bottom'].format(d=date_str)}</span>
    </div>
  </div>
</footer>

<div class="detail-panel" id="detail-panel">
  <div class="dp-header">
    <div class="dp-tabs" id="dp-tabs"></div>
    <div class="dp-actions">
      <button class="dp-btn" id="dp-minimize" title="Minimize">
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 8h10"/></svg>
      </button>
      <button class="dp-btn" id="dp-maximize" title="Maximize">
        <svg class="icon-max" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="3" width="10" height="10" rx="1.5"/></svg>
        <svg class="icon-restore" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="5" y="1.5" width="9" height="9" rx="1.5"/><rect x="2" y="5.5" width="9" height="9" rx="1.5"/></svg>
      </button>
      <button class="dp-btn" id="dp-close-all" title="Close all">
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4l8 8M12 4l-8 8"/></svg>
      </button>
    </div>
  </div>
  <div class="dp-body" id="dp-body"></div>
</div>

<script src="{u['js']}"></script>
</body>
</html>"""
    return html, detail_count


def main():
    DOCS_DIR.mkdir(exist_ok=True)

    for lang, u in UI.items():
        survey_path = ROOT / u["survey_file"]
        if not survey_path.exists():
            print(f"[{lang}] {survey_path.name} not found, skipping")
            continue
        md = survey_path.read_text(encoding="utf-8")
        out_path = DOCS_DIR / u["output"]
        out_path.parent.mkdir(parents=True, exist_ok=True)
        html, dc = build(md, lang)
        out_path.write_text(html, encoding="utf-8")
        print(f"[{lang}] Built -> {out_path} ({len(html):,} bytes, {dc} detail pages)")


if __name__ == "__main__":
    main()
