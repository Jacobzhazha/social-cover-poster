// 排版检查：文字放不下时先在允许范围内统一缩小，再放不下就报出要改哪里。结果写到 window.__report 和 <html data-report>
(function () {
  const errors = [];
  const page = document.querySelector('.page');
  const H = page.clientHeight;
  const u = parseFloat(getComputedStyle(page).getPropertyValue('--u'));

  const contentWidth = el => {
    const cs = getComputedStyle(el);
    return el.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
  };
  const ratio = el => el.firstElementChild.getBoundingClientRect().width / contentWidth(el);
  const text = el => el.textContent.trim();
  const perLine = el => Math.max(1, Math.floor(contentWidth(el) / parseFloat(getComputedStyle(el.querySelector('.badge-main') || el).fontSize)));

  // 一组文字共用一个缩放比例，保证同一角色字号一致
  function fitGroup(els, host, name, minScale) {
    els = els.filter(Boolean);
    if (!els.length) return;
    const worst = Math.max(...els.map(ratio));
    if (worst <= 1.001) return;
    host.style.setProperty(name, Math.max(minScale, 0.995 / worst));
    for (const el of els) {
      if (ratio(el) > 1.001) errors.push(`${el.dataset.name}「${text(el)}」太长：这个尺寸每行最多约 ${perLine(el)} 个字，请缩短或改分行`);
    }
  }

  function checkWrap(el) {
    const cs = getComputedStyle(el);
    const lines = Math.round(el.getBoundingClientRect().height - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom)) / parseFloat(cs.lineHeight);
    const max = +el.dataset.maxLines;
    if (Math.round(lines) > max) errors.push(`${el.dataset.name}「${text(el)}」超过 ${max} 行：请缩短到约 ${perLine(el) * max - 2} 个字以内`);
  }

  function run() {
    if (page.classList.contains('cover')) {
      const group = page.querySelector('.title-group');
      fitGroup([...group.querySelectorAll('.line')], group, '--s', 0.85);
      fitGroup([group.querySelector('.subtitle')], group, '--ss', 0.85);
      const hero = page.querySelector('.hero');
      if (page.classList.contains('wide') && page.classList.contains('scene-hero')) {
        // 场景左边 = 标题和辅助小字里最长一行的右边 + 44，最多到画布宽度的 63.33%
        const uw = parseFloat(getComputedStyle(page).getPropertyValue('--uw'));
        const right = Math.max(...[...group.querySelectorAll('.line > span, .subtitle > span')].map(s => s.getBoundingClientRect().right));
        page.style.setProperty('--scene-left', Math.min(right + 44 * uw, page.clientWidth * 0.6333) + 'px');
      }
      const box = group.getBoundingClientRect();
      if (page.classList.contains('wide') || page.classList.contains('no-hero')) {
        if (box.height > H - 96 * u) errors.push('标题和辅助小字太多，竖向放不下：减少一行标题或去掉辅助小字');
      } else if (hero && hero.getBoundingClientRect().height < H * 0.2) {
        errors.push('标题和辅助小字占得太多，主视觉区被挤得太小：减少一行标题、去掉辅助小字，或去掉 visual 改成纯文字封面');
      } else if (box.bottom > H - 40 * u) {
        errors.push('标题超出画面底部：减少一行标题或去掉辅助小字');
      }
    } else {
      const title = page.querySelector('.ctitle');
      fitGroup([...title.querySelectorAll('.line')], title, '--s', 72 / 84);
      const badge = page.querySelector('.badge');
      fitGroup([badge], badge || page, '--s', 0.7);
      page.querySelectorAll('.wrap').forEach(checkWrap);
      const group = page.querySelector('.content-group');
      const avail = group.clientHeight;
      const parts = page.classList.contains('wide') ? [title, page.querySelector('.cbody')] : [group];
      const used = Math.max(...parts.map(p => p === group
        ? [...group.children].reduce((s, c) => s + c.getBoundingClientRect().height + parseFloat(getComputedStyle(c).marginTop), 0)
        : p.getBoundingClientRect().height));
      if (used > avail + 1) errors.push(`内容太多，竖向放不下（超出约 ${Math.round((used - avail) / H * 100)}% 画面高度）：删掉一条要点、去掉导语或 badge，或缩短文字`);
    }
    const report = {errors};
    const scene = page.querySelector('.hero.scene');
    if (scene) {
      const r = scene.getBoundingClientRect();
      report.hero = {w: Math.round(r.width), h: Math.round(r.height)};
      const img = scene.querySelector('img.scene');
      if (img && img.naturalWidth) {
        const k = Math.max(r.width / img.naturalWidth, r.height / img.naturalHeight);
        report.sceneCrop = {x: 1 - r.width / k / img.naturalWidth, y: 1 - r.height / k / img.naturalHeight};
      }
    }
    window.__report = report;
    document.documentElement.setAttribute('data-report', JSON.stringify(report));
  }

  const start = () => (document.fonts ? document.fonts.ready : Promise.resolve()).then(run);
  if (document.readyState === 'complete') start();
  else window.addEventListener('load', start);
})();
