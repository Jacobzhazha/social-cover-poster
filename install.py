#!/usr/bin/env python3
"""Install the skill's runtime files without copying the showcase gallery."""
import argparse
from pathlib import Path
import shutil

TARGETS = {
    'codex': '.agents/skills',
    'claude-code': '.claude/skills',
    'cursor': '.cursor/skills',
    'copilot': '.copilot/skills',
    'gemini': '.gemini/skills',
}
RUNTIME = ['SKILL.md', 'scripts', 'templates', 'references', 'agents', 'LICENSE']

def main():
    parser = argparse.ArgumentParser(description='安装封面海报生成器 / Install Cover & Poster Maker')
    parser.add_argument('--agent', choices=TARGETS, default='codex')
    parser.add_argument('--dest', type=Path, help='完整目标目录 / Exact destination directory')
    parser.add_argument('--project', type=Path, help='安装到项目 / Install into a project')
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    if args.dest and args.project:
        parser.error('--dest and --project cannot be used together')
    if args.dest:
        destination = args.dest.expanduser().resolve()
    else:
        base = args.project.expanduser().resolve() if args.project else Path.home()
        folder = '.github/skills' if args.project and args.agent == 'copilot' else TARGETS[args.agent]
        destination = base / folder / 'social-cover-poster'
    missing = [name for name in RUNTIME if not (source / name).exists()]
    if missing:
        parser.error('Source package is incomplete: ' + ', '.join(missing))
    if destination.exists():
        parser.error(f'Destination exists; nothing changed: {destination}')
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Stage the complete package before making it discoverable.
    import tempfile
    with tempfile.TemporaryDirectory(prefix='.poster-install-', dir=destination.parent) as temp:
        staged = Path(temp) / 'social-cover-poster'
        staged.mkdir()
        for name in RUNTIME:
            src, dst = source / name, staged / name
            if src.is_dir():
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(src, dst)
        staged.rename(destination)
    print(f'已安装 / Installed: {destination}')
    print('在 Agent 中新开一轮对话后使用 / Start a new Agent turn to use the skill.')

if __name__ == '__main__':
    main()
