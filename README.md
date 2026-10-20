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

Copy `examples/neutral/hugo.toml`, `content/`, and `static/` into a new site for a full starting point. Replace its example contact details and form endpoint before publication. The theme uses each site's `hugo.toml`, `content/`, and `static/` files. Change the visual settings in `hugo.toml`. Change homepage text and button icons in `content/_index.md`. Store image, icon, and font files under `static/`.

Build the included examples from this repository:

```sh
hugo --source examples/neutral --themesDir ..
hugo --source examples/muted --themesDir ..
devenv shell -- check
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
menu_icon = "icons/menu.svg"
menu_close_icon = "icons/close.svg"

[params.contact]
address = "100 Example Street"
email = "hello@example.org"
phone = "+1 555 0100"
form_endpoint = "https://example.org/replace-this-endpoint"

[[params.social]]
name = "Social profile"
url = "https://example.org/social"
icon = "icons/social.svg"

[[menu.main]]
name = "Contact"
url = "/contact/"
weight = 1
```

Image and icon paths point to the site's `static/` directory. For example, `icons/menu.svg` maps to `static/icons/menu.svg`. If `logo` or `footer_logo` is empty, the theme shows `business_name`. If `business_name` is empty, it shows the site title. If `form_endpoint` is empty, the contact page shows the email address without a form. Hugo cannot process form submissions. Set an endpoint that you control before you publish a working form.

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
| `hero` | `eyebrow`, `title`, `text`, `image`, `image_alt`, `button.label`, `button.url`, optional `button.icon` |
| `statistics` | `title`, `items`: `before`, `number`, `after`, `label` |
| `portfolio` | `title`, `text`, `limit`, optional `button`; cards come from `content/portfolio/` |
| `testimonials` | `title`, `items`: `quote`, `name`, `role` |
| `clients` | `title`, `items`: `name`, optional `logo` |
| `team` | `title`, `items`: `name`, `role`, optional `image` |
| `cta` | `title`, `text`, optional `button.label`, `button.url`, and `button.icon` |

Each section also accepts `enabled`. The list order is the render order. The theme ignores unknown section names. The `portfolio` section uses page `weight` to order cards. Keep section content in the site, not the theme.

## Visual system

Set the following values in `[params.style]` in the site's `hugo.toml`. The theme uses these as CSS custom properties. See the neutral and muted configurations for two complete palettes.

| Setting | Default | Meaning |
| --- | --- | --- |
| `background` | `#ffffff` | Page background |
| `surface` | `#f3f4f5` | Section and footer background |
| `text` | `#20262c` | Main text |
| `muted` | `#58636b` | Secondary text |
| `border` | `#d4dadd` | Header and card borders |
| `accent` | `#285f70` | Links, numbers, and buttons |
| `on_accent` | `#ffffff` | Text on accent |
| `font_body` | `system-ui, sans-serif` | Body font family |
| `font_heading` | `system-ui, sans-serif` | Heading font family |
| `type_scale` | `1.2` | Large heading size multiplier |
| `spacing` | `1rem` | Section spacing unit |
| `button_radius` | `0.4rem` | Button corner radius |
| `hero_image_radius` | `0` | Hero image corner radius |
| `image_filter` | `none` | Filter for content images |
| `icon_size` | `1.15rem` | Navigation, social, and button icon size |

The examples set visual options in `hugo.toml` and `content/_index.md`. They do not use a site stylesheet. For effects outside these settings, set `custom_css = "css/site.css"`. Put that file at `static/css/site.css`. Hugo loads it after the theme stylesheet.

### Local fonts

Place font files in the site's `static/fonts/` directory. Declare each file in `hugo.toml`. Use the declared family name in `font_body` or `font_heading`.

```toml
[params.style]
font_body = '"Brand Sans", sans-serif'
font_heading = 'Georgia, serif'

[[params.font_faces]]
family = "Brand Sans"
src = "fonts/brand-sans.woff2"
format = "woff2"
weight = "400 700"
style = "normal"
```

Add another `[[params.font_faces]]` entry for each font file or style. The `format` value must match the file. The browser loads the local file from the site. System font families need no `font_faces` entry.

### Icons

Place icon files in the site's `static/icons/` directory. Set these optional paths in `hugo.toml`:

- `params.menu_icon` and `params.menu_close_icon` set the mobile menu icons.
- `params.social[].icon` sets a social link icon.
- `menu.main[].params.icon` sets a navigation item icon.

Set `button.icon = "icons/arrow.svg"` under `[hero.button]` or `[cta.button]` in `content/_index.md`. The theme also accepts `logo`, `footer_logo`, `favicon`, and client `logo` paths.

Use simple SVG icons with an opaque shape and a transparent background. The theme uses the shape as a mask. The icon takes its text color from `[params.style]`. This lets a palette change recolor icons without an SVG edit. Logos and client images keep their own colors.

### Link previews

Use the `preview` shortcode in Markdown to add a detail box to a link. The link still works when JavaScript is unavailable. Desktop readers can hover over the link. Readers can also use the adjacent button to open the box. The button works with a keyboard or touch screen. Press Escape or use the close button to close the box.

For a page on the same site, set `page` to its content path. The shortcode reads the target page's title, description, image, and image alt text from front matter:

```md
Explore the {{< preview page="/portfolio/field-guide/" >}}Field Guide{{< /preview >}}.
```

Set `summary`, `image`, or `image_alt` in the shortcode to replace those page values. For an external link, set its address and preview text yourself:

```md
Read the {{< preview href="https://example.org/guide" title="Example guide" summary="A short guide to the process." >}}guide{{< /preview >}}.
```

The theme does not fetch external pages. It uses only site-owned content. Preview boxes use the colors, fonts, image filter, and button radius from `[params.style]`. Use `static/css/site.css` for other changes.

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
5. Replace old Sass variables with `[params.style]`. Set icon paths and local font files in `hugo.toml`. Use `static/css/site.css` only for additional rules.
6. Set a real form endpoint. The examples contain placeholder endpoints and do not receive submissions.

The old fork's gray palette maps to the muted example. Its business-name header and counter prefix and suffix remain available. The new templates use current Hugo data and layout conventions.

## Verify

Run `devenv shell -- check`. The check builds both examples. It checks local links, images, icons, branding, section order, optional sections, forms, custom layouts, and link previews. Chromium renders each example at 1440 × 900 and 390 × 844. The check tests navigation, preview interaction, and horizontal overflow at both widths. Set `ROXO_SCREENSHOT_DIR` to keep the screenshots.
