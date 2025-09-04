import json
import os
import argparse

def main(input_file: str, outdir: str):
    # Load JSON
    with open(input_file, "r", encoding="utf-8") as f:
        raw = json.load(f)

    entries = raw.get("data", [])
    os.makedirs(outdir, exist_ok=True)

    for g in entries:
        if g.get("type") != "glossaryterm":
            continue  # skip non-glossary entries

        glossary_id = g["id"]
        term = g.get("term", "Untitled").strip()
        alt_title = g.get("alt_title", "").strip()
        status = g.get("status", "unknown")
        definition = g.get("definition", "").strip()

        # Skip deleted terms if you want only active
        if status != "active":
            continue

        # Markdown content
        md = f"# {term}\n\n"
        if alt_title and alt_title.lower() != term.lower():
            md += f"**Alternative title:** {alt_title}\n\n"
        md += f"**Definition:**\n\n{definition}\n"

        # Save file named after the term
        safe_term = term.replace(" ", "_").replace("/", "-").lower()
        out_path = os.path.join(outdir, f"{safe_term}.md")

        with open(out_path, "w", encoding="utf-8") as out:
            out.write(md)

    print(f"Exported {len(entries)} glossary terms to {outdir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert KnowledgeOwl Glossary JSON to Markdown files")
    parser.add_argument("--input", required=True, help="Path to KnowledgeOwl Glossary JSON file")
    parser.add_argument("--outdir", required=True, help="Output directory for markdown files")

    args = parser.parse_args()
    main(args.input, args.outdir)