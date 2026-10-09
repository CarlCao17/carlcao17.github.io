(() => {
  const input = document.querySelector('#search-input');
  const status = document.querySelector('#search-status');
  const results = document.querySelector('#search-results');
  let pages = [];
  const render = () => {
    const q = input.value.trim().toLocaleLowerCase();
    results.replaceChildren();
    if (!q) { status.textContent = '输入关键词查找文章。'; return; }
    const found = pages.filter(p => [p.title, ...(p.tags || []), p.content].join(' ').toLocaleLowerCase().includes(q));
    status.textContent = `找到 ${found.length} 篇文章。`;
    for (const p of found) {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.textContent = p.title; a.href = p.url;
      li.append(a); results.append(li);
    }
  };
  fetch('/index.json').then(r => { if (!r.ok) throw new Error(); return r.json(); })
    .then(data => { pages = data; input.addEventListener('input', render); render(); })
    .catch(() => { status.textContent = '索引加载失败，请刷新重试。'; });
})();
