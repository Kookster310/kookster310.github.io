# 310 Networks Website

This site is built with **MkDocs + Material** and deployed to GitHub Pages via GitHub Actions.

## Adding New Posts

Create a new Markdown file in the appropriate section:

- `docs/projects/` for project posts
- `docs/audio-dramas/` for audio drama reviews
- `docs/thoughts/` for thoughts

Then add a link to the new post on the corresponding index page:

- `docs/index.md` (home page, excludes Audio Dramas)
- `docs/projects/index.md`
- `docs/audio-dramas/index.md`
- `docs/thoughts/index.md`

## Local Preview

```bash
pip install -r requirements.txt
mkdocs serve
```

## Structure

- `mkdocs.yml` - Site configuration and navigation
- `docs/` - All site content
- `docs/assets/` - Images and custom CSS
- `.github/workflows/mkdocs.yml` - GitHub Pages deploy workflow

## Live Site

You can visit the site at https://www.310networks.com
