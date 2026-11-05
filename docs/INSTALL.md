# 安装指南

[English](INSTALL.en.md) · [返回首页](../README.md)

## 准备代码

```bash
git clone https://github.com/Jacobzhazha/social-cover-poster.git
cd social-cover-poster
```

下载 ZIP 的用户请先解压，并在包含 `SKILL.md` 与 `install.py` 的目录运行命令。安装器复制运行文件，不复制案例库；目标已存在时停止，原技能保持原样。

## 选择 Agent

| Agent | 全局安装命令 | 安装位置 |
| --- | --- | --- |
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `python3 install.py --agent codex` | `~/.agents/skills/social-cover-poster/` |
| [Claude Code](https://code.claude.com/docs/en/skills) | `python3 install.py --agent claude-code` | `~/.claude/skills/social-cover-poster/` |
| [Cursor](https://cursor.com/docs/skills) | `python3 install.py --agent cursor` | `~/.cursor/skills/social-cover-poster/` |
| [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) | `python3 install.py --agent copilot` | `~/.copilot/skills/social-cover-poster/` |
| [Gemini CLI](https://geminicli.com/docs/cli/skills/) | `python3 install.py --agent gemini` | `~/.gemini/skills/social-cover-poster/` |

Windows 中 `~` 对应用户目录；可将命令中的 `python3` 换成 `python`。

项目内安装使用 `--project`，例如：

```bash
python3 install.py --agent codex --project /path/to/project
python3 install.py --agent copilot --project /path/to/project
```

Copilot 项目安装使用 `.github/skills/social-cover-poster/`；其他 Agent 使用对应的项目技能目录。需要自定义位置时使用 `--dest /path/to/social-cover-poster`。

Gemini CLI 也可以通过官方命令从仓库安装：

```bash
gemini skills install https://github.com/Jacobzhazha/social-cover-poster.git
```

## WorkBuddy

从 [Releases](https://github.com/Jacobzhazha/social-cover-poster/releases) 下载 `social-cover-poster-v1.0.4.zip`。在 WorkBuddy 的「技能」中选择「添加技能 → 上传技能」，选中该文件导入。安装后新开任务，输入「用封面海报生成器做一张 3:4 封面」。[官方导入说明](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)

## 准备出图环境

本技能需要执行 Python、读写文件，并使用浏览器渲染。推荐 Python 3.9+：

```bash
python3 -m pip install -r requirements.txt
python3 -m playwright install chromium
```

Linux 若缺系统依赖，可按 Playwright 安装提示补齐；中文字体建议安装 Noto CJK。已有本机 Chrome / Edge 时，原导出脚本也支持 `--renderer browser`。

本技能不内置生图服务。Agent 有图片工具时可生成 3D 主视觉；没有时可用 `visual.icon` 或已有图片。实际价格与标识以调用平台为准。

## 确认能用

安装后新开一轮对话，指定技能名 `social-cover-poster` 或「封面海报生成器」。Codex 可用 `$social-cover-poster`，Claude Code 可用 `/social-cover-poster`。

```bash
python3 scripts/make_poster.py examples/14-resume.json --out output/first-example
```

运行后打开输出目录中的 PNG 与 `预览.html`。


