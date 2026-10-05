# 310 Networks Website

This site is built with **MkDocs + Material** and deployed to GitHub Pages via GitHub Actions.

## Adding New Posts

Create a new Markdown file in the appropriate section:

- `docs/posts/` for posts
- `docs/audio-dramas/` for audio drama reviews

Then:

1. Add an entry to the `nav:` section in `mkdocs.yml`
2. Add a link to the new post on the corresponding index page:
   - `docs/posts/index.md`
   - `docs/audio-dramas/index.md`

The home page (`docs/index.md`) automatically shows the latest post via
`hooks.py`, so no manual work is needed there.

## Local Preview

```bash
pip install -r requirements.txt
mkdocs serve
```

## Local Build

```bash
pip install -r requirements.txt
mkdocs build
```

## Structure

- `mkdocs.yml` - Site configuration and navigation
- `docs/` - All site content
- `docs/assets/` - Images and custom CSS
- `docs/overrides/` - Template overrides (nav, toc, footer)
- `hooks.py` - Injects the latest post onto the home page and feeds the "Recent Posts" sidebar
- `matrix-remote-*` - Reference configs/docs for the self-hosted Matrix server (not served by this site)
- `.github/workflows/mkdocs.yml` - GitHub Pages deploy workflow

## Live Site

You can visit the site at https://www.310networks.com
