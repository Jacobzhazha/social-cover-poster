<div align="center">

# Cover & Poster Maker

**Turn a topic into clean covers, posters, and complete image carousels.**

[中文](README.md) · English

[Install](docs/INSTALL.en.md) · [24 examples](docs/GALLERY.en.md) · [Usage](docs/USAGE.en.md)

![Actual example outputs](assets/showcase.png)

</div>

Give your agent some source material and a target format. Get ready-to-use PNGs with warm ivory backgrounds, bold black and blue typography, and yellow accents.

Use a generated 3D toy-style scene, an existing image, or a built-in icon. **Headlines are typeset by the template, rather than painted into the illustration.**

## See the results

**24 real examples and 34 full-resolution PNGs** cover AI workflows, study, travel, pets, coffee, home organization, resumes, privacy, music, and games. The gallery includes three complete carousels, five preset formats, and a custom canvas.

| AI weekly workflow · 5 pages | Pet album | Travel checklist · 4 pages |
| --- | --- | --- |
| ![Weekly workflow](assets/examples/01-ai-weekly-preview.png) | ![Pet album](assets/examples/04-pet-preview.png) | ![Travel checklist](assets/examples/03-travel-preview.png) |

[Explore the complete gallery →](docs/GALLERY.en.md) Each case includes source material, a reusable request, JSON input, and all exported images. Eight generated visuals retain their original files and full prompts.

## Ask your agent

```text
Use social-cover-poster to turn the material below into a 3:4 image carousel.
Use a 3D toy-style scene on the cover. Give each content page one question.
Use only the supplied facts. Export PNG files and a complete preview.

[Paste your material here]
```

Other requests:

- Make a two-line WeChat article cover for this post.
- Make a 16:9 video thumbnail using my product screenshot.
- Use a built-in icon instead of generating an image.
- Shorten the second page and split it into two pages.

## Install

```bash
git clone https://github.com/Jacobzhazha/social-cover-poster.git
cd social-cover-poster
python3 install.py --agent codex
```

| Agent | Command or method |
| --- | --- |
| Codex | `python3 install.py --agent codex` |
| Claude Code | `python3 install.py --agent claude-code` |
| Cursor | `python3 install.py --agent cursor` |
| GitHub Copilot | `python3 install.py --agent copilot` |
| Gemini CLI | `python3 install.py --agent gemini` |
| WorkBuddy | Download the skill ZIP from [Releases](https://github.com/Jacobzhazha/social-cover-poster/releases), then upload it through Skills → Add skill → Upload skill |

The installer copies runtime files only, excludes the showcase gallery, and refuses to overwrite an existing skill. On Windows, use `python` if `python3` is unavailable.

See the [installation guide](docs/INSTALL.en.md) for locations, project installs, dependencies, and image-tool requirements.

## Output formats

| Format | Size |
| --- | --- |
| `3:4` cover or carousel | 1080 × 1440 |
| `1:1` square | 1080 × 1080 |
| `16:9` thumbnail | 1920 × 1080 |
| `2.35:1` article cover | 1800 × 766 |
| `9:16` mobile poster | 1080 × 1920 |
| Custom, such as `1242x1660` | As configured |

Up to 18 pages per configuration. Content pages allow up to three points and 120 visible characters. The script reports long lines and overflowing content with actionable errors.

## Run without an agent

Requires Python 3.9+ and Chromium, Chrome, or Edge. Recommended setup:

```bash
python3 -m pip install -r requirements.txt
python3 -m playwright install chromium
python3 scripts/make_poster.py examples/14-resume.json --out output/resume
```

This example uses a built-in icon, so image-generation access is unnecessary. Output includes PNGs, `预览.html`, and source HTML. Image generation is provided by your agent's image tool; the repository does not bundle a model or API credentials.

## Project layout

`SKILL.md` contains agent instructions. `scripts/` handles validation, icons, and PNG export; `templates/` holds the fixed layout. `references/` documents fields and writing rules. `examples/` contains inputs; `assets/` holds outputs and original visuals; `docs/` contains bilingual guides.

## Author

**Jacobzhazha · 渣渣的赛博宇宙** — practical AI tools, experiments, and open-source skills. Search for the WeChat public account **渣渣的赛博宇宙**.

[Issues](https://github.com/Jacobzhazha/social-cover-poster/issues) · [Contributing](CONTRIBUTING.md) · [MIT License](LICENSE)
