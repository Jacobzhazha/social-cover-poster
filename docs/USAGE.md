# 使用方法

[English](USAGE.en.md) · [首页](../README.md)

## 从 Agent 开始

告诉 Agent 主题、原始材料、平台、张数，以及要用生图、已有素材还是图标。没有指定尺寸时默认 3:4。只要封面就只出封面；要一套图文时再按内容拆页。

```text
用封面海报生成器做一张公众号封面。
主题是桌面整理，标题两行：「桌面整理」「从常用区开始」。
用我提供的图片完整展示，不加账号水印。
```

## 从 JSON 开始

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

保存为 `poster.json` 后运行：

```bash
python3 scripts/make_poster.py poster.json --check
python3 scripts/make_poster.py poster.json --out output/my-poster
```

## 三种主视觉

- `visual.scene`：描述一个动作，再运行 `--prompts` 获取固定画风的完整提示词。按参数生图，把路径填入 `visual.image` 后导出。
- `visual.image`：使用已有素材，默认完整显示；文件路径相对 JSON 所在目录解析。
- `visual.icon`：选择内置图标，直接出图，不调用图片模型。

已有素材和场景图的铺图方式不同。希望完整保留素材时使用只含 `image` 的配置；场景模式按主视觉区铺满，先按提示词中的可见范围构图。

```bash
python3 scripts/make_poster.py poster.json --out output/my-poster --prompts
```

## 多页图文

第一张使用 `cover`，后续用 `content`。内页可写标题、导语、重点数字和最多三个要点。每页只解决一个问题；文字过多时删减或拆页。多页自动显示页码。

完整示例见 [AI 周报](../examples/01-ai-weekly.json)、[旅行准备](../examples/03-travel.json)、[读书笔记](../examples/11-reading.json)。字段与图标表见 [配置规范](../references/spec.md)。

## 出错时

脚本会指出过长的标题、超过两行的要点或放不下的内容。优先修改 JSON 中的文案与分行。找不到图片时检查路径；出图环境失败时检查浏览器依赖。已有 Chrome / Edge 可以尝试 `--renderer browser`。
