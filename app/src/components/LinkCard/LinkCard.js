/**
 * LinkCard — リンク投稿カード（再利用可能）
 * 駅名・URL・タイトル・タグ・保存機能
 */
class LinkCard {
  constructor(data, options = {}) {
    this.data = data;
    this.onSave = options.onSave || (() => {});
    this.savedStations = this._loadSaved();
    this.element = null;
    this._render();
  }

  _loadSaved() {
    try {
      return JSON.parse(localStorage.getItem('tojo_saved_links') || '[]');
    } catch {
      return [];
    }
  }

  _isSaved() {
    return this.savedStations.includes(this.data.id);
  }

  _render() {
    const isSaved = this._isSaved();
    const el = document.createElement('div');
    el.className = 'link-card';
    el.dataset.cardId = this.data.id;

    el.innerHTML = `
      <div class="link-card__header">
        <span class="link-card__station">${this.data.stationId} ${this.data.stationName}</span>
        <span class="link-card__time">${this._timeAgo(this.data.createdAt)}</span>
      </div>

      <div class="link-card__title">${this._escapeHtml(this.data.title)}</div>

      <a href="${this._escapeHtml(this.data.url)}" target="_blank" rel="noopener" class="link-card__preview">
        <img class="link-card__favicon" src="${this._getFaviconUrl(this.data.url)}" alt="" />
        <div class="link-card__og">
          <div class="link-card__og-title">${this._escapeHtml(this.data.ogTitle || this.data.title)}</div>
          <div class="link-card__og-desc">${this._escapeHtml(this.data.ogDesc || '')}</div>
        </div>
        ${this.data.ogImage ? `<img class="link-card__og-image" src="${this._escapeHtml(this.data.ogImage)}" alt="" loading="lazy" />` : ''}
      </a>

      ${this.data.tags && this.data.tags.length > 0 ? `
        <div class="link-card__tags">
          ${this.data.tags.map(t => `<span class="link-card__tag">#${this._escapeHtml(t)}</span>`).join('')}
        </div>
      ` : ''}

      <div class="link-card__actions">
        <span class="link-card__action">
          <span class="link-card__action-icon">🔗</span>
          ${this.data.clicks || 0}
        </span>
        ${this.data.commonUsers && this.data.commonUsers > 0 ? `
          <span class="link-card__action">
            <span class="link-card__action-icon">👥</span>
            共通 ${this.data.commonUsers}人
          </span>
        ` : ''}
        <button class="link-card__save-btn ${isSaved ? 'saved' : ''}"
                data-action="save">
          ${isSaved ? '✓ 保存済' : '📍 行ってみたい'}
        </button>
      </div>
    `;

    // 保存ボタンイベント
    const saveBtn = el.querySelector('[data-action="save"]');
    saveBtn.addEventListener('click', (e) => {
      e.preventDefault();
      this._toggleSave();
    });

    this.element = el;
  }

  _toggleSave() {
    const isSaved = this._isSaved();

    if (isSaved) {
      this.savedStations = this.savedStations.filter(id => id !== this.data.id);
    } else {
      this.savedStations.push(this.data.id);
      if (navigator.vibrate) navigator.vibrate(20);
    }

    localStorage.setItem('tojo_saved_links', JSON.stringify(this.savedStations));

    // ボタン更新
    const btn = this.element.querySelector('.link-card__save-btn');
    btn.classList.toggle('saved', !isSaved);
    btn.textContent = isSaved ? '📍 行ってみたい' : '✓ 保存済';

    // コールバック
    this.onSave(this.data.id, !isSaved);
  }

  _timeAgo(timestamp) {
    const diff = Date.now() - timestamp;
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'たった今';
    if (mins < 60) return `${mins}分前`;
    const hours = Math.floor(mins / 60);
    if (hours < 24) return `${hours}時間前`;
    const days = Math.floor(hours / 24);
    return `${days}日前`;
  }

  _getFaviconUrl(url) {
    try {
      const domain = new URL(url).hostname;
      return `https://www.google.com/s2/favicons?domain=${domain}&sz=32`;
    } catch {
      return '';
    }
  }

  _escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  getElement() {
    return this.element;
  }
}

export default LinkCard;
