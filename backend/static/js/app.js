(function () {
  'use strict';

  const API = '';
  const el = (id) => document.getElementById(id);
  const qs = (sel, ctx = document) => ctx.querySelector(sel);
  const qsAll = (sel, ctx = document) => ctx.querySelectorAll(sel);

  const els = {
    searchInput: el('search-input'),
    sortSelect: el('sort-select'),
    btnSearch: el('btn-search'),
    summarySection: el('summary-section'),
    summaryText: el('summary-text'),
    newsSection: el('news-section'),
    newsList: el('news-list'),
    newsCount: el('news-count'),
    chatMessages: el('chat-messages'),
    chatInput: el('chat-input'),
    btnSend: el('btn-send'),
    errorBox: el('error-box'),
    loadingNews: el('loading-news'),
    dbLogSection: el('db-log-section'),
    dbLogList: el('db-log-list'),
  };

  function showError(msg) {
    const b = els.errorBox;
    b.textContent = msg || '';
    b.classList.toggle('hidden', !msg);
  }

  function setLoading(loading) {
    els.loadingNews.classList.toggle('hidden', !loading);
    els.btnSearch.disabled = loading;
  }

  function renderSummary(summary) {
    const sec = els.summarySection;
    const txt = els.summaryText;
    if (!summary || !summary.trim()) {
      sec.classList.add('hidden');
      return;
    }
    txt.textContent = summary;
    sec.classList.remove('hidden');
  }

  function renderNews(data) {
    const { keyword, sort, total, items = [] } = data;
    const list = els.newsList;
    const countEl = els.newsCount;

    list.innerHTML = '';
    countEl.textContent = `"${keyword}" ${sort} · ${total}건`;

    items.forEach((it, i) => {
      const li = document.createElement('li');
      li.className = 'news-card';
      li.innerHTML = `
        <a href="${escapeHtml(it.link)}" target="_blank" rel="noopener">${escapeHtml(it.title)}</a>
        <div class="meta">${escapeHtml(it.pubDate || '')}</div>
        ${it.description ? `<div class="desc">${escapeHtml(it.description)}</div>` : ''}
      `;
      list.appendChild(li);
    });

    els.newsSection.classList.remove('hidden');
  }

  function escapeHtml(s) {
    if (!s) return '';
    const div = document.createElement('div');
    div.textContent = s;
    return div.innerHTML;
  }

  function addChatMessage(role, text) {
    const wrap = els.chatMessages;
    const empty = wrap.querySelector('.empty');
    if (empty) empty.remove();
    const msg = document.createElement('div');
    msg.className = 'chat-msg ' + role;
    const label = role === 'user' ? 'You' : 'Assistant';
    msg.innerHTML = '<div class="label">' + escapeHtml(label) + '</div>' + escapeHtml(text).replace(/\n/g, '<br>');
    wrap.appendChild(msg);
    wrap.scrollTop = wrap.scrollHeight;
  }

  function addDbLog(log) {
    if (!log || !log.message) return;
    const section = els.dbLogSection;
    const list = els.dbLogList;
    const item = document.createElement('div');
    item.className = 'db-log-item ' + (log.success ? 'success' : 'error');
    item.textContent = log.message;
    list.appendChild(item);
    section.classList.remove('hidden');
    // 최대 5개까지만 표시
    while (list.children.length > 5) {
      list.removeChild(list.firstChild);
    }
  }

  async function searchNews() {
    const keyword = (els.searchInput.value || '').trim();
    if (!keyword) {
      showError('검색어를 입력해주세요.');
      return;
    }
    showError('');
    setLoading(true);
    try {
      const sort = els.sortSelect.value || 'date';
      const res = await fetch(`${API}/api/news?keyword=${encodeURIComponent(keyword)}&sort=${sort}`);
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(typeof data.detail === 'string' ? data.detail : '검색 실패');
      renderSummary(data.summary);
      renderNews(data);
      if (data.db_log) {
        addDbLog(data.db_log);
      }
    } catch (e) {
      showError(e.message || '뉴스 검색 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  }

  async function sendChat() {
    const input = els.chatInput;
    const msg = (input.value || '').trim();
    if (!msg) return;
    input.value = '';
    addChatMessage('user', msg);
    els.btnSend.disabled = true;
    try {
      const res = await fetch(`${API}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg }),
      });
      const data = await res.json().catch(() => ({}));
      const reply = data.reply || (res.ok ? '답변을 생성하지 못했습니다.' : '전송 실패');
      addChatMessage('bot', reply);
      if (data.db_log && Array.isArray(data.db_log)) {
        data.db_log.forEach(log => addDbLog(log));
      } else if (data.db_log) {
        addDbLog(data.db_log);
      }
    } catch (e) {
      addChatMessage('bot', '오류: ' + (e.message || '전송 실패'));
    } finally {
      els.btnSend.disabled = false;
    }
  }

  const chatForm = document.getElementById('chat-form');
  chatForm.addEventListener('submit', (e) => { e.preventDefault(); sendChat(); });
  els.btnSearch.addEventListener('click', searchNews);
  els.searchInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') searchNews(); });
  els.btnSend.addEventListener('click', sendChat);
  els.chatInput.addEventListener('keydown', (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendChat(); } });
})();
