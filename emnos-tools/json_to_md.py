import json
import os
import argparse
from bs4 import BeautifulSoup  # pip install beautifulsoup4

def main(input_file: str, outdir: str):
    # Load JSON
    with open(input_file, "r", encoding="utf-8") as f:
        raw = json.load(f)

    articles = raw.get("data", [])
    os.makedirs(outdir, exist_ok=True)

    for a in articles:
        article_id = a["id"]
        title = (
            a.get("name")
            or a.get("current_version", {}).get("en", {}).get("title", "Untitled")
        )
        html_text = a.get("current_version", {}).get("en", {}).get("text", "")

        # Convert HTML to plain text/markdown
        text = BeautifulSoup(html_text, "html.parser").get_text(separator="\n")

        url = f"https://help.emnos.com/help/{a.get('url_hash', '')}"

        md = f"# {title}\n\n{text.strip()}\n\n[Read more]({url})"

        with open(
            os.path.join(outdir, f"{article_id}.md"), "w", encoding="utf-8"
        ) as out:
            out.write(md)

    print(f"Exported {len(articles)} articles to {outdir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert KnowledgeOwl JSON to Markdown files")
    parser.add_argument("--input", required=True, help="Path to KnowledgeOwl JSON file")
    parser.add_argument("--outdir", required=True, help="Output directory for markdown files")

    args = parser.parse_args()
    main(args.input, args.outdir)