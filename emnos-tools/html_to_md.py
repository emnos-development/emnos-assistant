import os
import argparse
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag  # pip install beautifulsoup4 lxml
from markdownify import markdownify as md  # pip install markdownify

# --- Helpers -----------------------------------------------------------------

def choose_content_root(soup: BeautifulSoup) -> Tag:
    """
    Pick the main article container if it exists, else fall back to <body>.
    KnowledgeOwl exports typically place content under .hg-article-body /
    .documentation-article.
    """
    for sel in [".hg-article-body", ".documentation-article", "#ko-article-cntr", "article"]:
        node = soup.select_one(sel)
        if node:
            return node
    return soup.body or soup  # fallback

def clean_dom(soup: BeautifulSoup) -> None:
    # Drop noise
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

def replace_videos_with_links(soup: BeautifulSoup, node: Tag, transcripts_dir: Path | None) -> None:
    """
    Replace <video> with a Markdown-like placeholder:
      - [Video: filename](src)
      - If a transcript matching the basename exists in transcripts_dir (.txt/.md/.srt/.vtt), inline it.
    """
    videos = node.find_all("video")
    for v in videos:
        src = None
        # Prefer <source src> if present
        source = v.find("source")
        if source and source.get("src"):
            src = source["src"]
        elif v.get("src"):
            src = v["src"]

        link_text = "Video"
        if src:
            filename = os.path.basename(src)
            link_text = f"Video: {filename}"

        # Build replacement content
        parts = [f"[{link_text}]({src})" if src else "**Video** (no src found)"]

        # Try to inline transcript if available
        if transcripts_dir and src:
            base = Path(os.path.basename(src)).stem
            for ext in (".md", ".txt", ".srt", ".vtt"):
                cand = transcripts_dir / f"{base}{ext}"
                if cand.exists():
                    try:
                        transcript = cand.read_text(encoding="utf-8")
                        parts.append("\n\n### Transcript\n")
                        parts.append(transcript.strip())
                        break
                    except Exception:
                        pass
        else:
            parts.append("\n\n_Transcript not provided._")

        replacement = soup.new_tag("p")
        replacement.append(NavigableString("\n".join(parts)))
        v.replace_with(replacement)

def escape_pipes(s: str) -> str:
    return s.replace("|", r"\|")

def compact_inline(md_text: str) -> str:
    """
    Collapse newlines inside a table cell's converted content to keep table intact.
    """
    # keep hard line breaks minimal in cells
    return " ".join(md_text.split())

def table_to_markdown(tbl: Tag) -> str:
    """
    Convert a <table> into GitHub-flavored Markdown table.
    - Uses <thead> if present; otherwise first row as header if it has <th>.
    - Otherwise synthesizes Column 1..N.
    - Cell content is converted with markdownify to preserve links/formatting.
    """
    # Gather rows
    thead = tbl.find("thead")
    tbody = tbl.find("tbody")
    rows = []

    if tbody:
        rows.extend(tbody.find_all("tr"))
    else:
        rows.extend(tbl.find_all("tr"))

    # Determine headers
    headers = []
    used_first_as_header = False

    if thead:
        ths = thead.find_all(["th", "td"])
        headers = [compact_inline(escape_pipes(md(str(th)).strip())) for th in ths]
    else:
        # check first row for th
        if rows:
            first_cells = rows[0].find_all(["th", "td"])
            if any(c.name == "th" for c in first_cells):
                headers = [compact_inline(escape_pipes(md(str(c)).strip())) for c in first_cells]
                used_first_as_header = True

    # If still no headers, synthesize
    if not headers:
        # Determine column count from first non-empty row
        col_count = 0
        for r in rows:
            cells = r.find_all(["td", "th"])
            if len(cells) > 0:
                col_count = len(cells)
                break
        if col_count == 0:
            return ""  # empty table
        headers = [f"Column {i+1}" for i in range(col_count)]

    # Body rows
    body_rows = rows[1:] if used_first_as_header else rows
    md_rows = []
    for r in body_rows:
        cells = r.find_all(["td", "th"])
        if not cells:
            continue
        md_cells = [compact_inline(escape_pipes(md(str(c)).strip())) for c in cells]
        # pad to header length
        if len(md_cells) < len(headers):
            md_cells += [""] * (len(headers) - len(md_cells))
        elif len(md_cells) > len(headers):
            md_cells = md_cells[:len(headers)]
        md_rows.append("| " + " | ".join(md_cells) + " |")

    # Header + separator
    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    return "\n".join([header_line, separator_line] + md_rows) + "\n"

def convert_tables_inline(original_soup: BeautifulSoup, content_root: Tag) -> None:
    """
    Replace every <table> in-place with a <pre> node containing Markdown table text.
    Using <pre> as a carrier ensures markdownify doesn't try to re-convert it.
    """
    for tbl in content_root.find_all("table"):
        md_table = table_to_markdown(tbl)
        pre = original_soup.new_tag("pre")
        pre.string = md_table
        tbl.replace_with(pre)

def to_markdown(original_soup: BeautifulSoup, content_root: Tag) -> str:
    """
    Convert cleaned soup to Markdown.
    We use markdownify for general HTML -> MD,
    and we inject Markdown tables before conversion via <pre>.
    """
    # Convert tables to <pre> blocks containing Markdown tables
    convert_tables_inline(original_soup, content_root)

    # Convert remaining HTML to Markdown
    content_md = md(str(content_root), heading_style="ATX")

    # Convert the <pre> blocks (rendered as code blocks) back into raw text by stripping code fences.
    # markdownify wraps <pre> with triple backticks; remove them.
    lines = []
    inside_code = False
    for line in content_md.splitlines():
        if line.strip().startswith("```"):
            inside_code = not inside_code
            continue  # drop the fence
        lines.append(line)
    final = "\n".join(lines)

    # De-duplicate excessive blank lines
    packed = []
    prev_blank = False
    for line in final.splitlines():
        blank = (line.strip() == "")
        if blank and prev_blank:
            continue
        packed.append(line)
        prev_blank = blank
    return "\n".join(packed).strip()

# --- Main --------------------------------------------------------------------

def process_html_file(html_path: Path, out_root: Path, transcripts_dir: Path | None) -> None:
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "lxml")

    clean_dom(soup)

    # Title: prefer <h1> inside content root, else <title>, else filename
    root = choose_content_root(soup)
    h1 = root.find(["h1", "h2"])
    title = (h1.get_text(strip=True) if h1 else (soup.title.string if soup.title else html_path.stem))

    # Replace videos with links (+ transcript if available)
    replace_videos_with_links(soup, root, transcripts_dir)

    # Build markdown
    md_body = to_markdown(soup, root)

    # Compose final MD
    md_full = f"# {title}\n\n{md_body}\n"

    # Mirror folder structure
    rel = html_path.relative_to(html_path.parents[0])  # keep 1-level-up structure by default
    out_path = out_root / rel.with_suffix(".md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md_full, encoding="utf-8")
    print(f"Converted: {html_path} -> {out_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert KnowledgeOwl HTML export to Markdown (recursive, tables+links preserved).")
    parser.add_argument("--inputdir", required=True, help="Path to unzipped KnowledgeOwl HTML export")
    parser.add_argument("--outdir", required=True, help="Output directory for markdown files")
    parser.add_argument("--transcripts", required=False, help="Optional directory holding transcripts (.md/.txt/.srt/.vtt) matching video basenames")
    args = parser.parse_args()

    input_dir = Path(args.inputdir)
    out_dir = Path(args.outdir)
    transcripts_dir = Path(args.transcripts) if args.transcripts else None

    out_dir.mkdir(parents=True, exist_ok=True)

    for root, _, files in os.walk(input_dir):
        for fname in files:
            if fname.lower().endswith(".html"):
                process_html_file(Path(root) / fname, out_dir, transcripts_dir)

if __name__ == "__main__":
    main()