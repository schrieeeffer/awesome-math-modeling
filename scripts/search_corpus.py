"""Search the bundled inventory; extracted-text search requires a local corpus."""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys


def read_rows(path):
    with path.open(encoding="utf-8-sig") as stream:
        for line in stream:
            if line.strip():
                yield json.loads(line)


def resolve_text_root(args, default_config):
    """Explicit text roots use the working directory; config roots use its parent."""
    if args.text_root is not None:
        return args.text_root.expanduser().resolve()
    config = (args.config or default_config).expanduser().resolve()
    if not config.is_file():
        if args.config is not None:
            raise ValueError(f"config file does not exist: {config}")
        return None
    local = json.loads(config.read_text(encoding="utf-8-sig"))
    if not isinstance(local, dict):
        raise ValueError("corpus config must be a JSON object")
    value = local.get("extraction_root")
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError("extraction_root must be a nonempty path string")
    root = pathlib.Path(value).expanduser()
    return (root if root.is_absolute() else config.parent / root).resolve()


def safe_text_path(root, relative):
    """Reject absolute paths, traversal, and symlinks that leave the text root."""
    if not isinstance(relative, str):
        raise ValueError("catalog text_path must be a relative path string")
    # Recognize both separators, including Windows paths when run on Linux/macOS.
    windows_path = pathlib.PureWindowsPath(relative)
    relative_path = pathlib.Path(relative.replace("\\", "/"))
    if windows_path.drive or windows_path.root or relative_path.is_absolute():
        raise ValueError("catalog text path must be relative to text root")
    resolved = (root / relative_path).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError("catalog text path escapes text root")
    return resolved


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    base = pathlib.Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("query", nargs="?", default="", help="Space-separated terms; all must match")
    ap.add_argument("--catalog", type=pathlib.Path, default=base / "references" / "corpus-catalog.jsonl")
    ap.add_argument("--id", help="Return one exact source ID")
    ap.add_argument("--year", type=int, help="Filter inferred source year, not collection date range")
    ap.add_argument("--ext", help="Extension, e.g. pdf or .m")
    ap.add_argument("--content", action="store_true", help="Include locally extracted text in matching")
    ap.add_argument("--text-root", type=pathlib.Path, help="Root containing text/ID.txt; overrides config")
    ap.add_argument("--config", type=pathlib.Path, help="Optional JSON config for --content; relative extraction_root is resolved against this file")
    ap.add_argument("--limit", type=int, default=12)
    ap.add_argument("--include-duplicates", action="store_true")
    args = ap.parse_args()
    if args.limit < 1:
        ap.error("--limit must be positive")
    if not args.catalog.is_file():
        ap.error("catalog file does not exist")

    text_root = None
    if args.content:
        try:
            text_root = resolve_text_root(args, base / "references" / "local-corpus.json")
        except (OSError, ValueError) as exc:
            ap.error(str(exc))
        if text_root is None or not text_root.is_dir():
            ap.error("content search needs an existing --text-root or extraction_root in local corpus config; extracted texts are not bundled")

    terms = args.query.casefold().split()
    ext = "." + args.ext.lstrip(".").lower() if args.ext else None
    count = missing = 0
    seen = set()
    try:
        for row in read_rows(args.catalog):
            if args.id and row["id"] != args.id:
                continue
            if args.year and row.get("year_hint") != args.year:
                continue
            if ext and row["extension"] != ext:
                continue
            text = ""
            textfile = None
            if args.content and row.get("text_path"):
                textfile = safe_text_path(text_root, row["text_path"])
                if textfile.is_file():
                    text = textfile.read_text(encoding="utf-8", errors="replace")
                else:
                    missing += 1
            haystack = (row["path"] + "\n" + text).casefold()
            if not all(term in haystack for term in terms):
                continue
            key = row.get("sha256") or row.get("duplicate_of") or row["id"]
            if not args.id and not args.include_duplicates and key in seen:
                continue
            seen.add(key)
            fields = ("id", "path", "extension", "year_hint", "role_hint", "status", "pages", "cjk_chars", "duplicate_of", "contents_same_as", "review_depth", "review_reference", "case_id", "prompt_source_id")
            result = {key: row[key] for key in fields if key in row}
            if text:
                matches = (re.search(re.escape(term), text, re.IGNORECASE) for term in terms)
                match = next((match for match in matches if match), None)
                position = match.start() if match else 0
                pages = re.findall(r"--- PDF PAGE (\d+) ---", text[:position])
                if pages:
                    result["snippet_pdf_page"] = int(pages[-1])
                result["snippet"] = " ".join(text[max(0, position - 60):position + 260].split())
                result["extracted_text"] = str(textfile)
            print(json.dumps(result, ensure_ascii=False))
            count += 1
            if count >= args.limit:
                break
    except (OSError, ValueError) as exc:
        ap.error(str(exc))
    print(json.dumps({"matches_returned": count, "limit": args.limit, "missing_extracted_texts_seen": missing, "note": "File labels and extraction do not prove awards, correctness, or full review."}, ensure_ascii=False), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
