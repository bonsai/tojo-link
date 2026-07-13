/**
 * LinkBoard — メインフィード（カード一覧＋フィルター）
 */
import LinkCard from '../LinkCard/LinkCard.js';

class LinkBoard {
  constructor(options = {}) {
    this.container = options.container || document.querySelector('#link-board');
    this.onPost = options.onPost || (() => {});
    this.posts = options.posts || this._getDummyPosts();
    this.activeFilter = null;

    this._render();
  }

  _getDummyPosts() {
    return [
      {
        id: 'post-001',
        stationId: 'TJ-13',
        stationName: '鶴瀬',
        title: '鶴瀬駅徒歩5分🌸 甘酒＆麹カフェ Lesson開催中',
        url: 'https://example.com/koji-cafe-tsuruse',
        ogTitle: '麹カフェ つるせ — 甘酒・麹スイーツ・レッスン',
        ogDesc: '6種類の麹を使って、1day Lessonを開催。甘酒や麹調味料を作ってみませんか？',
        ogImage: 'https://picsum.photos/seed/koji/120/120',
        tags: ['麹', '甘酒', 'レッスン', '鶴瀬'],
        clicks: 42,
        commonUsers: 5,
        createdAt: Date.now() - 1000 * 60 * 120
      },
      {
        id: 'post-002',
        stationId: 'TJ-01',
        stationName: '池袋',
        title: '英会話カフェ参加者募集 🇬🇧 池袋〜川越沿線',
        url: 'https://example.com/english-cafe-tojo',
        ogTitle: '東上線沿線 英会話カフェ — 気軽に練習しよう',
        ogDesc: 'カフェで英語の練習しませんか？初心者歓迎。毎週土曜開催。',
        ogImage: null,
        tags: ['英会話', '募集', '池袋'],
        clicks: 89,
        commonUsers: 12,
        createdAt: Date.now() - 1000 * 60 * 60 * 5
      },
      {
        id: 'post-003',
        stationId: 'TJ-17',
        stationName: '川越',
        title: '川越のレコード喫茶 🎵 アナログ盤 1000枚以上',
        url: 'https://example.com/record-cafe-kawagoe',
        ogTitle: 'レコード喫茶 小江戸 — 川越で過ごすアナログ時間',
        ogDesc: 'トッド・ラングレンからビル・エヴァンスまで。コーヒーとレコードの休日。',
        ogImage: 'https://picsum.photos/seed/record/120/120',
        tags: ['レコード', '喫茶店', '川越', '音楽'],
        clicks: 156,
        commonUsers: 23,
        createdAt: Date.now() - 1000 * 60 * 60 * 24
      },
      {
        id: 'post-004',
        stationId: 'TJ-10',
        stationName: '志木',
        title: '志木駅前の隠れ家パン屋 🥐 朝6時営業',
        url: 'https://example.com/bakery-shiki',
        ogTitle: 'ブーランジェリー 志木 — 朝のパン、夜のワイン',
        ogDesc: '天然酵母・国産小麦。朝6時から営業。夜はワインバーに早変わり。',
        tags: ['パン', '隠れ家', '志木'],
        clicks: 67,
        commonUsers: 8,
        createdAt: Date.now() - 1000 * 60 * 60 * 3
      },
      {
        id: 'post-005',
        stationId: 'TJ-26',
        stationName: '東松山',
        title: '東松山やきとり祭り情報 🍢 2026年秋開催',
        url: 'https://example.com/yakitori-higashimatsuyama',
        ogTitle: '東松山やきとり祭り — 埼玉県を代表するB級グルメ',
        ogDesc: '醤油ベースの甘辛いたれが特徴。毎年10月開催。',
        ogImage: 'https://picsum.photos/seed/yakitori/120/120',
        tags: ['グルメ', 'イベント', '東松山'],
        clicks: 203,
        commonUsers: 31,
        createdAt: Date.now() - 1000 * 60 * 60 * 8
      }
    ];
  }

  _render() {
    const filtered = this._getFilteredPosts();

    this.container.innerHTML = `
      <div class="link-board">
        <header class="link-board__header">
          <div class="link-board__logo">🚃 東上リンク</div>
          <button class="link-board__post-btn" data-action="post">＋ 投稿する</button>
        </header>

        <div class="link-board__filters" id="board-filters">
          <button class="link-board__filter-chip active" data-filter="all">すべて</button>
          ${this._getUniqueStations().map(s => `
            <button class="link-board__filter-chip" data-filter="${s.id}">${s.name}</button>
          `).join('')}
        </div>

        <div class="link-board__list" id="board-list">
          ${filtered.map(post => this._createCardHtml(post)).join('')}
        </div>
      </div>
    `;

    this._bindEvents();
  }

  _getUniqueStations() {
    const seen = new Set();
    return this.posts
      .filter(p => {
        if (seen.has(p.stationId)) return false;
        seen.add(p.stationId);
        return true;
      })
      .map(p => ({ id: p.stationId, name: p.stationName }));
  }

  _getFilteredPosts() {
    if (!this.activeFilter) return this.posts;
    return this.posts.filter(p => p.stationId === this.activeFilter);
  }

  _createCardHtml(post) {
    const isSaved = this._isPostSaved(post.id);
    return `
      <div class="link-card" data-card-id="${post.id}">
        <div class="link-card__header">
          <span class="link-card__station">${post.stationId} ${post.stationName}</span>
          <span class="link-card__time">${this._timeAgo(post.createdAt)}</span>
        </div>
        <div class="link-card__title">${this._escapeHtml(post.title)}</div>
        <a href="${this._escapeHtml(post.url)}" target="_blank" rel="noopener" class="link-card__preview">
          <img class="link-card__favicon" src="${this._getFavicon(post.url)}" alt="" />
          <div class="link-card__og">
            <div class="link-card__og-title">${this._escapeHtml(post.ogTitle || post.title)}</div>
            <div class="link-card__og-desc">${this._escapeHtml(post.ogDesc || '')}</div>
          </div>
          ${post.ogImage ? `<img class="link-card__og-image" src="${post.ogImage}" alt="" loading="lazy" />` : ''}
        </a>
        ${post.tags && post.tags.length > 0 ? `
          <div class="link-card__tags">
            ${post.tags.map(t => `<span class="link-card__tag">#${this._escapeHtml(t)}</span>`).join('')}
          </div>
        ` : ''}
        <div class="link-card__actions">
          <span class="link-card__action">
            <span class="link-card__action-icon">🔗</span>
            ${post.clicks}
          </span>
          ${post.commonUsers ? `
            <span class="link-card__action">
              <span class="link-card__action-icon">👥</span>
              共通 ${post.commonUsers}人
            </span>
          ` : ''}
          <button class="link-card__save-btn ${isSaved ? 'saved' : ''}" data-action="save" data-post-id="${post.id}">
            ${isSaved ? '✓ 保存済' : '📍 行ってみたい'}
          </button>
        </div>
        ${post.commonUsers > 5 ? `
          <div class="link-card__common-users">
            👥 #${post.tags?.[0] || post.stationName} に興味がある人と共通しています
          </div>
        ` : ''}
      </div>
    `;
  }

  _bindEvents() {
    // フィルターチップ
    this.container.querySelectorAll('.link-board__filter-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        this.container.querySelectorAll('.link-board__filter-chip').forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        this.activeFilter = chip.dataset.filter === 'all' ? null : chip.dataset.filter;
        this._render();
      });
    });

    // 保存ボタン
    this.container.querySelectorAll('[data-action="save"]').forEach(btn => {
      btn.addEventListener('click', () => {
        this._toggleSave(btn.dataset.postId, btn);
      });
    });

    // 投稿ボタン
    this.container.querySelector('[data-action="post"]')?.addEventListener('click', () => {
      this.onPost();
    });
  }

  _isPostSaved(postId) {
    try {
      const saved = JSON.parse(localStorage.getItem('tojo_saved_links') || '[]');
      return saved.includes(postId);
    } catch {
      return false;
    }
  }

  _toggleSave(postId, btn) {
    const saved = this._isPostSaved(postId);
    let list = [];
    try { list = JSON.parse(localStorage.getItem('tojo_saved_links') || '[]'); } catch {}

    if (saved) {
      list = list.filter(id => id !== postId);
    } else {
      list.push(postId);
      if (navigator.vibrate) navigator.vibrate(20);
    }

    localStorage.setItem('tojo_saved_links', JSON.stringify(list));
    btn.classList.toggle('saved', !saved);
    btn.textContent = saved ? '📍 行ってみたい' : '✓ 保存済';
  }

  _timeAgo(ts) {
    const diff = Date.now() - ts;
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'たった今';
    if (mins < 60) return `${mins}分前`;
    const hours = Math.floor(mins / 60);
    if (hours < 24) return `${hours}時間前`;
    return `${Math.floor(hours / 24)}日前`;
  }

  _getFavicon(url) {
    try { return `https://www.google.com/s2/favicons?domain=${new URL(url).hostname}&sz=32`; } catch { return ''; }
  }

  _escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  refresh(newPosts) {
    this.posts = newPosts || this.posts;
    this._render();
  }
}

export default LinkBoard;
