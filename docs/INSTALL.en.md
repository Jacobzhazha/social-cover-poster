# Installation

[中文](INSTALL.md) · [Home](../README.en.md)

## Get the code

```bash
git clone https://github.com/Jacobzhazha/social-cover-poster.git
cd social-cover-poster
```

ZIP users should extract the archive and open a terminal in the directory containing `SKILL.md` and `install.py`.

| Agent | Global install | Destination |
| --- | --- | --- |
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `python3 install.py --agent codex` | `~/.agents/skills/social-cover-poster/` |
| [Claude Code](https://code.claude.com/docs/en/skills) | `python3 install.py --agent claude-code` | `~/.claude/skills/social-cover-poster/` |
| [Cursor](https://cursor.com/docs/skills) | `python3 install.py --agent cursor` | `~/.cursor/skills/social-cover-poster/` |
| [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) | `python3 install.py --agent copilot` | `~/.copilot/skills/social-cover-poster/` |
| [Gemini CLI](https://geminicli.com/docs/cli/skills/) | `python3 install.py --agent gemini` | `~/.gemini/skills/social-cover-poster/` |

On Windows, replace `python3` with `python` if needed. The installer copies runtime files only and leaves existing destinations untouched.

Use `--project /path/to/project` for a project install. Copilot uses `.github/skills/` for this scope; the other agents use their respective project skill folders. Use `--dest /path/to/social-cover-poster` for an exact destination.

Gemini CLI also offers:

```bash
gemini skills install https://github.com/Jacobzhazha/social-cover-poster.git
```

## WorkBuddy

Download `social-cover-poster-v1.0.4.zip` from [Releases](https://github.com/Jacobzhazha/social-cover-poster/releases). Open Skills → Add skill → Upload skill, select the ZIP, and start a new task. See [WorkBuddy's upload instructions](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market).

## Rendering requirements

The agent needs Python execution, file access, and browser rendering. Recommended: Python 3.9+.

```bash
python3 -m pip install -r requirements.txt
python3 -m playwright install chromium
```

On Linux, follow Playwright's dependency instructions and install a Chinese font such as Noto CJK. The renderer can also use local Chrome or Edge through `--renderer browser`.

Image generation uses your agent's image tool. Without one, choose a built-in icon or an existing image. Costs and generated-image labels depend on the tool actually used.

## Verify

Start a new agent turn after installation. Invoke `social-cover-poster`, `$social-cover-poster` in Codex, or `/social-cover-poster` in Claude Code.

```bash
python3 scripts/make_poster.py examples/14-resume.json --out output/first-example
```

Open the output directory to view the PNGs and `预览.html`.
