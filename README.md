# 310 Networks Website

A modern blog-style Jekyll website for www.310networks.com with sidebar navigation and category filtering.

## Features

- **Blog-style layout** - Easy to update with markdown posts
- **Sidebar navigation** - Quick access to Personal Projects and Audio Dramas
- **Category filtering** - Posts organized by category
- **Responsive design** - Works on all devices

## Adding New Posts

Create a new markdown file in the `_posts/` directory with the following format:

```markdown
---
layout: post
category: Personal Projects
title: Your Post Title
date: 2024-01-15
---
Your post content goes here. You can use markdown formatting.
```

### Categories

Posts can be categorized as:
- **Personal Projects** - Technical projects, experiments, and builds
- **Audio Dramas** - Reviews, recommendations, and thoughts on audio dramas

Posts will automatically appear on the homepage and in their respective category pages.

## Structure

- `_layouts/blog.html` - Main blog layout with sidebar
- `_layouts/post.html` - Individual post layout
- `_layouts/category.html` - Category page layout
- `personal-projects/` - Personal Projects category page
- `audio-dramas/` - Audio Dramas category page
- `_posts/` - All blog posts

## Check Out The Website
You can visit my website [here](http://www.310networks.com) 

===

For more Jekyll details, read [documentation](http://jekyllrb.com/).
