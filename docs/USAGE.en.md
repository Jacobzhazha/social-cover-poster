# Usage

[中文](USAGE.md) · [Home](../README.en.md)

Tell the agent your topic, source material, target platform, page count, and visual choice. The default format is 3:4. Ask for a single cover or a full carousel as needed.

```text
Use Cover & Poster Maker to create a WeChat article cover.
Use two title lines: “桌面整理” and “从常用区开始”.
Show my supplied image completely. Do not add an account watermark.
```

## JSON input

```json
{
  "size": "3:4",
  "pages": [{
    "type": "cover",
    "title": ["简历别堆词", "把工作经历", "写成具体结果"],
    "subtitle": "任务 行动 结果",
    "visual": {"icon": "briefcase"}
  }]
}
```

```bash
python3 scripts/make_poster.py poster.json --check
python3 scripts/make_poster.py poster.json --out output/my-poster
```

## Visual options

- `visual.scene`: describe one action. Run `--prompts`, use the resulting fixed-style prompt with your image tool, then put the generated path into `visual.image`.
- `visual.image`: use existing artwork. It is fully contained by default; relative paths resolve from the JSON file's directory.
- `visual.icon`: choose a built-in icon and render without image generation.

Scene mode fills the visual region and may crop the image. Use the image-only mode when the complete source must remain visible.

## Carousels

Use `cover` for the first page and `content` for following pages. Content pages can include a title, lead, numeric badge, and up to three points. Keep one question per page. Multi-page sets include page numbers.

Explore complete inputs for [weekly reports](../examples/01-ai-weekly.json), [travel](../examples/03-travel.json), and [reading notes](../examples/11-reading.json). The [field reference](../references/spec.md) includes supported fields and icons.

Long headlines and overflowing content produce actionable messages. Edit the input text or line breaks first. For missing images, check paths. For rendering errors, check browser dependencies or try `--renderer browser` with local Chrome or Edge.
