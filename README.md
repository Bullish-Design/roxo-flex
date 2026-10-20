# Roxo Flex

Roxo Flex is a Hugo theme for studios, teams, and project portfolios. Site owners set the brand, content, section order, and visual style in their own site. The theme contains no site content or example images. The `examples/neutral` and `examples/muted` sites use the same theme files.

This repository is a [fork of Roxo Hugo](https://github.com/sitepins/roxo-hugo). It keeps the upstream Git history and MIT license. The site structure follows the older `roxo-muted` fork. The templates and styles were rebuilt for current Hugo because the old templates used deprecated data access and inconsistent counter fields. The May 2026 upstream build stalled during template rendering in the local baseline check. See [RESEARCH_REPORT.md](RESEARCH_REPORT.md).

## Requirements and installation

Use Hugo Extended 0.162.1 or later. This repository was tested with Hugo Extended 0.162.1 and 0.166.0. The optional development shell uses devenv 2.4.0 and Chromium 155 for viewport checks. A site build needs only Hugo. It does not need Node.js, Go modules, or a CSS build step.

Add the theme to a Hugo site:

```sh
hugo new site mysite
cd mysite
git submodule add https://github.com/Bullish-Design/roxo-flex.git themes/roxo-flex
printf 'theme = "roxo-flex"\n' >> hugo.toml
hugo server
```

Copy `examples/neutral/hugo.toml`, `content/`, and `static/` into a new site for a full starting point. Replace its example contact details and form endpoint before publication. The theme uses each site's `hugo.toml`, `content/`, and `static/` files.

Build the included examples from this repository:

```sh
hugo --source examples/neutral --themesDir ..
hugo --source examples/muted --themesDir ..
devenv test
```

## Site configuration

Set these values in the site's `hugo.toml`:

```toml
[params]
business_name = "Example Studio"
logo = "images/mark.svg"
footer_logo = "images/mark.svg"
favicon = "images/mark.svg"
copyright = "© 2026 Example Studio"
custom_css = "css/site.css"

[params.contact]
address = "100 Example Street"
email = "hello@example.org"
phone = "+1 555 0100"
form_endpoint = "https://example.org/replace-this-endpoint"

[[params.social]]
name = "Social profile"
url = "https://example.org/social"

[[menu.main]]
name = "Contact"
url = "/contact/"
weight = 1
```

All image paths point to the site's `static/` directory. For example, `images/mark.svg` maps to `static/images/mark.svg`. If `logo` or `footer_logo` is empty, the theme shows `business_name`. If `business_name` is empty, it shows the site title. If `form_endpoint` is empty, the contact page shows the email address without a form. Hugo cannot process form submissions. Set an endpoint that you control before you publish a working form.

## Homepage sections

Set the order in the site's `content/_index.md` TOML front matter. Include a section name to place it on the page. Set `enabled = false` to hide it while keeping its content. The muted example hides `team` this way.

```toml
+++
sections = ["hero", "statistics", "portfolio", "testimonials", "clients", "team", "cta"]
[hero]
enabled = true
title = "Good work starts with clear ideas."
text = "A short introduction."
image = "images/scene.svg"
image_alt = "Abstract sample art"
[hero.button]
label = "See work"
url = "/portfolio/"
[statistics]
enabled = true
title = "At a glance"
[[statistics.items]]
before = "~"
number = "12"
after = "+"
label = "Projects"
+++
```

| Section | Content fields |
| --- | --- |
| `hero` | `eyebrow`, `title`, `text`, `image`, `image_alt`, `button.label`, `button.url` |
| `statistics` | `title`, `items`: `before`, `number`, `after`, `label` |
| `portfolio` | `title`, `text`, `limit`, optional `button`; cards come from `content/portfolio/` |
| `testimonials` | `title`, `items`: `quote`, `name`, `role` |
| `clients` | `title`, `items`: `name`, optional `logo` |
| `team` | `title`, `items`: `name`, `role`, optional `image` |
| `cta` | `title`, `text`, optional `button.label` and `button.url` |

Each section also accepts `enabled`. The list order is the render order. The theme ignores unknown section names. The `portfolio` section uses page `weight` to order cards. Keep section content in the site, not the theme.

## Visual system

Set the following values in `[params.style]` in the site's `hugo.toml`. The theme uses these as CSS custom properties. See the neutral and muted configurations for two complete palettes.

| Setting | Default | Meaning |
| --- | --- | --- |
| `background` | `#ffffff` | Page background |
| `surface` | `#f3f4f5` | Section and footer background |
| `text` | `#20262c` | Main text |
| `muted` | `#58636b` | Secondary text |
| `accent` | `#285f70` | Links, numbers, and buttons |
| `on_accent` | `#ffffff` | Text on accent |
| `font_body` | `system-ui, sans-serif` | Body font family |
| `font_heading` | `system-ui, sans-serif` | Heading font family |
| `type_scale` | `1.2` | Large heading size multiplier |
| `spacing` | `1rem` | Section spacing unit |
| `button_radius` | `0.4rem` | Button corner radius |

Use `custom_css = "css/site.css"` for deeper changes. Put the file at `static/css/site.css` in the site. It loads after the theme stylesheet. Use `@font-face` in that file if you need a local font. No generated CSS file needs editing.

## Content types

Create standard Markdown files in these site directories:

- `content/portfolio/`: portfolio cards and detail pages. Use `title`, `description`, `image`, `image_alt`, and `weight`.
- `content/projects/`: project list and detail pages. Use the same fields.
- `content/project_areas/`: groups of projects. Add `_index.md` in each group. Add Markdown pages inside it. A nested page can set `project_images = ["images/a.svg", "images/b.svg"]` for a gallery.
- `content/contact/_index.md`: contact introduction. The form uses `params.contact.form_endpoint`.

The theme supplies list and single layouts for `projects`, `project_areas`, and `portfolio`. The `project_areas` list shows nested groups and direct pages. Its nested single layout links back to the parent group.

## Migration from `roxo-muted`

1. Copy site content and images into your site's `content/` and `static/`. Do not copy them into the theme.
2. Move `businessName`, logo, footer logo, favicon, copyright, contact details, social links, and navigation into `hugo.toml`. Follow the names in `examples/muted/hugo.toml`.
3. Move `params.banner` into `[hero]` in `content/_index.md`. Move `data/counter.yml` into `[statistics]`. Use `before`, `number`, and `after` for each value. The old template expected `operator`, while the old data supplied `number`.
4. Move portfolio, `projects`, and nested `project_areas` Markdown into the same directories in the new site. Use `image` and `project_images` in front matter. The new nested templates handle group and detail pages without the old blog template.
5. Replace old Sass variables with `[params.style]`. Put additional rules in the site's `static/css/site.css`.
6. Set a real form endpoint. The examples contain placeholder endpoints and do not receive submissions.

The old fork's gray palette maps to the muted example. Its business-name header and counter prefix and suffix remain available. The new templates use current Hugo data and layout conventions.

## Verify

Run `devenv test` or `devenv shell -- check`. The check builds both examples. It checks local links, images, branding, section order, optional sections, forms, and custom layouts. Chromium renders each example at 1440 × 900 and 390 × 844. The check tests navigation visibility and horizontal overflow at both widths. Set `ROXO_SCREENSHOT_DIR` to keep the screenshots.
