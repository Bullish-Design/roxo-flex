# Build research, 2026-10-20

## Baseline and decision

The current [sitepins/roxo-hugo](https://github.com/sitepins/roxo-hugo) head was `53e7b02`. Its [May 2026 rewrite](https://github.com/sitepins/roxo-hugo/commit/f8b297e) added Tailwind CSS, many Hugo modules, and a new layout structure. I cloned that head and ran Hugo Extended 0.162.1 against `exampleSite`. The command reached template assembly but did not finish rendering after three minutes. I stopped it. The log ended after `build: step assemble`. This does not identify the exact stalled component.

The older [roxo-muted fork](https://github.com/Bullish-Intelligence/roxo-muted) head was `2107b8f`. Its example built in 112 ms with Hugo Extended 0.162.1. It reported deprecated `.Site.LanguageCode` and `.Site.Data` use. The header showed a site-owned business name. Its palette used gray values and a small accent. Its counter template read `before`, `operator`, and `after`, while the example data supplied `number`. The `projects` and nested `project_areas` layouts existed, but the nested single page used a blog layout. These defects made a direct copy unsuitable. Possible causes of the upstream stall include a Hugo module or Tailwind resource. The log did not distinguish them. The old build result rules out a general Hugo failure on this machine.

I kept the current upstream fork and MIT license. I rebuilt the working page structure from the older fork with current Hugo templates and plain CSS. This removed the upstream module and Tailwind build dependencies from site builds. It kept upstream ancestry so the fork can track changes through the `upstream` remote.

## Fix and evidence

The theme uses site-owned configuration and homepage content. A single `home-section.html` renders both examples. CSS variables expose colors, fonts, type scale, spacing, and button radius. Static example images live only under `examples/*/static/`.

`devenv test` passed with Hugo Extended 0.166.0 and Chromium 155.0.8059.39. The static build check also passed with Hugo Extended 0.162.1. Both sites rendered 11 HTML pages. The check covered local links, images, section order, optional sections, forms, and project layouts. Chromium rendered desktop and mobile screenshots and found no horizontal overflow. It confirmed desktop navigation visibility and mobile toggle behavior.

The baseline stall remains unclassified because I did not trace the upstream Hugo process. The new theme no longer uses that build path. There is no temporary compatibility patch to remove. Form submissions remain unverified because the example endpoints are placeholders. The check proves the rendered form markup, not service delivery.
