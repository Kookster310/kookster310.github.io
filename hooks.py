import os
import re
from datetime import datetime

import yaml


POST_DIRS = ("projects", "thoughts")
POST_PLACEHOLDER = "{{ latest_post }}"


def _load_posts(config):
    posts = []
    docs_dir = config["docs_dir"]
    for section in POST_DIRS:
        section_dir = os.path.join(docs_dir, section)
        if not os.path.isdir(section_dir):
            continue
        for root, _, files in os.walk(section_dir):
            for filename in files:
                if not filename.endswith(".md") or filename == "index.md":
                    continue
                path = os.path.join(root, filename)
                rel_path = os.path.relpath(path, docs_dir).replace("\\", "/")
                with open(path, "r", encoding="utf-8") as handle:
                    raw = handle.read()
                if not raw.startswith("---"):
                    continue
                _, meta_raw, body = raw.split("---", 2)
                meta = yaml.safe_load(meta_raw) or {}
                date_str = str(meta.get("date", "")).strip()
                title = str(meta.get("title", "")).strip()
                if not date_str or not title:
                    continue
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                posts.append(
                    {
                        "title": title,
                        "date": date,
                        "date_display": date.strftime("%B %d, %Y"),
                        "path": rel_path,
                        "url": rel_path[:-3] + "/",
                        "content": body.lstrip(),
                    }
                )
    posts.sort(key=lambda post: post["date"], reverse=True)
    config.extra["recent_posts"] = [
        {
            "title": post["title"],
            "url": post["url"],
            "date_display": post["date_display"],
        }
        for post in posts[:4]
    ]
    config.extra["latest_post"] = posts[0] if posts else None


def on_pre_build(config):
    _load_posts(config)


def on_page_markdown(markdown, page, config, files):
    if page.file.src_path != "index.md":
        return markdown
    latest = config.extra.get("latest_post")
    if not latest:
        return markdown.replace(POST_PLACEHOLDER, "_No posts yet._")
    
    # Remove the first heading (H1 or H2) from the post content
    content = latest['content'].rstrip()
    # Remove leading heading markers (# or ##) followed by title and newline
    content = re.sub(r'^#+\s+.*?\n\n?', '', content, count=1, flags=re.MULTILINE)
    
    latest_markdown = (
        f"## {latest['title']}\n\n"
        f"**Date:** {latest['date_display']}\n\n"
        f"{content}\n"
    )
    return markdown.replace(POST_PLACEHOLDER, latest_markdown)

