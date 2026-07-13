/**
 * CustomRecommend — カスタム3件推薦
 * 好み学習 + 多様性確保で「話題の情報3つ」を表示
 */
class CustomRecommend {
  constructor(options = {}) {
    this.container = options.container || document.querySelector('#custom-recommend');
    this.posts = options.posts || [];
    this.preferences = this._loadPreferences();
    this.savedLinks = this._loadSavedLinks();
    this.element = null;
    this._render();
  }

  _loadPreferences() {
    try {
      return JSON.parse(localStorage.getItem('tojo_prefs') || '{}');
    } catch {
      return {};
    }
  }

  _loadSavedLinks() {
    try {
      return JSON.parse(localStorage.getItem('tojo_saved_links') || '[]');
    } catch {
      return [];
    }
  }

  /**
   * 推薦ロジック:
   * 1. タグスコア計算（保存した投稿のタグ × 重み）
   * 2. 未クリックの投稿から上位3件
   * 3. 多様性確保（同じ駅/タグが連続しない）
   */
  _getTop3() {
    // タグ重み計算
    const tagWeights = {};
    this.savedLinks.forEach(savedId => {
      const post = this.posts.find(p => p.id === savedId);
      if (post && post.tags) {
        post.tags.forEach(tag => {
          tagWeights[tag] = (tagWeights[tag] || 0) + 1;
        });
      }
    });

    // 駅重み計算
    const stationWeights = {};
    Object.entries(this.preferences).forEach(([stationId, count]) => {
      stationWeights[stationId] = count;
    });

    // 各投稿にスコア付与
    const scored = this.posts
      .filter(p => !this.savedLinks.includes(p.id)) // 保存済みは除外
      .map(p => {
        let score = 0;

        // タグマッチ
        if (p.tags) {
          p.tags.forEach(tag => {
            score += (tagWeights[tag] || 0) * 2;
          });
        }

        // 駅マッチ
        score += (stationWeights[p.stationId] || 0) * 3;

        // 人気ブースト
        score += (p.clicks || 0) * 0.1;

        // 新規ブースト（新しい投稿を優先）
        const ageHours = (Date.now() - p.createdAt) / (1000 * 60 * 60);
        if (ageHours < 6) score += 5;

        return { ...p, score };
      });

    // スコア順ソート
    scored.sort((a, b) => b.score - a.score);

    // 多様性確保（上位5件から異なる駅/タグを選択）
    const result = [];
    const usedStations = new Set();
    const usedTags = new Set();

    for (const post of scored) {
      if (result.length >= 3) break;

      // 同じ駅が既にある場合はスキップ（多様性）
      if (usedStations.has(post.stationId) && scored.length > 5) continue;

      result.push(post);
      usedStations.add(post.stationId);
      if (post.tags) post.tags.forEach(t => usedTags.add(t));
    }

    return result;
  }

  _render() {
    const top3 = this._getTop3();

    if (top3.length === 0) {
      this.container.innerHTML = '';
      return;
    }

    this.element = document.createElement('div');
    this.element.className = 'custom-recommend';
    this.element.innerHTML = `
      <div class="custom-recommend__title">✨ あなたへのおすすめ</div>
      <div class="custom-recommend__list">
        ${top3.map((p, i) => `
          <div class="custom-recommend__item" data-recommend-id="${p.id}" data-recommend-url="${p.url}">
            <span class="custom-recommend__icon">${['🎯', '🔥', '💡'][i]}</span>
            <div class="custom-recommend__content">
              <div class="custom-recommend__text">${this._escapeHtml(p.title)}</div>
              <div class="custom-recommend__sub">${p.stationId} ${p.stationName} ${p.tags ? '· ' + p.tags.slice(0, 2).map(t => `#${t}`).join(' ') : ''}</div>
            </div>
            ${p.commonUsers > 5 ? `<span class="custom-recommend__badge">共通${p.commonUsers}人</span>` : ''}
          </div>
        `).join('')}
      </div>
    `;

    // クリックイベント
    this.element.querySelectorAll('.custom-recommend__item').forEach(item => {
      item.addEventListener('click', () => {
        const url = item.dataset.recommendUrl;
        if (url) window.open(url, '_blank', 'noopener');
      });
    });

    this.container.innerHTML = '';
    this.container.appendChild(this.element);
  }

  _escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  refresh(posts) {
    this.posts = posts || this.posts;
    this.preferences = this._loadPreferences();
    this.savedLinks = this._loadSavedLinks();
    this._render();
  }
}

export default CustomRecommend;
