/**
 * PostForm — 投稿フォーム（スライドアップ）
 * 1投稿/24h制限・URL検証・駅選択
 */
class PostForm {
  constructor(options = {}) {
    this.container = options.container || document.querySelector('#post-form-overlay');
    this.onSubmit = options.onSubmit || (() => {});
    this.stations = options.stations || [];
    this.isOpen = false;

    this._render();
    this._bindEvents();
  }

  _render() {
    this.container.innerHTML = `
      <div class="post-form-overlay" id="post-form-overlay-inner">
        <div class="post-form">
          <div class="post-form__handle" data-action="close"></div>
          <div class="post-form__title">📎 リンクを投稿する</div>

          <form id="post-form-body" autocomplete="off">
            <div class="post-form__field">
              <label class="post-form__label" for="post-station">🚃 駅</label>
              <select class="post-form__input post-form__station-select" id="post-station" required>
                <option value="">駅を選んでください</option>
                ${this.stations.map(s => `<option value="${s.id}">${s.id} ${s.name}（${s.municipality}）</option>`).join('')}
              </select>
            </div>

            <div class="post-form__field">
              <label class="post-form__label" for="post-title">タイトル</label>
              <input type="text" class="post-form__input" id="post-title"
                placeholder="例: 鶴瀬駅徒歩5分🌸 カフェオープン" maxlength="80" required />
            </div>

            <div class="post-form__field">
              <label class="post-form__label" for="post-url">URL</label>
              <input type="url" class="post-form__input" id="post-url"
                placeholder="https://..." required />
              <div class="post-form__error" id="url-error">有効なURLを入力してください</div>
            </div>

            <div class="post-form__field">
              <label class="post-form__label" for="post-tags">タグ（カンマ区切り、任意）</label>
              <input type="text" class="post-form__input" id="post-tags"
                placeholder="例: カフェ,甘酒,鶴瀬" maxlength="60" />
            </div>

            <button type="submit" class="post-form__submit" id="post-submit">投稿する</button>
            <div class="post-form__note">24時間に1回投稿できます</div>
          </form>
        </div>
      </div>
    `;
  }

  _bindEvents() {
    const overlay = this.container.querySelector('#post-form-overlay-inner');
    const form = this.container.querySelector('#post-form-body');
    const closeHandle = this.container.querySelector('[data-action="close"]');

    // オーバークリックで閉じる
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) this.close();
    });

    // ハンドルで閉じる
    closeHandle?.addEventListener('click', () => this.close());

    // フォーム送信
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      this._submit();
    });
  }

  open() {
    const overlay = this.container.querySelector('#post-form-overlay-inner');
    if (!overlay) return;
    overlay.classList.add('open');
    this.isOpen = true;
  }

  close() {
    const overlay = this.container.querySelector('#post-form-overlay-inner');
    if (!overlay) return;
    overlay.classList.remove('open');
    this.isOpen = false;
  }

  _canPost() {
    const lastPost = localStorage.getItem('tojo_last_post');
    if (!lastPost) return true;
    const elapsed = Date.now() - parseInt(lastPost, 10);
    return elapsed >= 24 * 60 * 60 * 1000; // 24時間
  }

  _submit() {
    // 24時間制限チェック
    if (!this._canPost()) {
      const errorEl = this.container.querySelector('#url-error');
      errorEl.textContent = '24時間に1回まで投稿できます';
      errorEl.classList.add('visible');
      return;
    }

    const stationId = this.container.querySelector('#post-station').value;
    const title = this.container.querySelector('#post-title').value.trim();
    const url = this.container.querySelector('#post-url').value.trim();
    const tagsRaw = this.container.querySelector('#post-tags').value.trim();
    const tags = tagsRaw ? tagsRaw.split(',').map(t => t.trim()).filter(Boolean) : [];

    // URL検証
    try {
      new URL(url);
    } catch {
      const errorEl = this.container.querySelector('#url-error');
      errorEl.classList.add('visible');
      return;
    }

    // 投稿データ
    const postData = {
      id: `post-${Date.now()}`,
      stationId,
      stationName: this.stations.find(s => s.id === stationId)?.name || '',
      title,
      url,
      tags,
      createdAt: Date.now()
    };

    // 制限記録
    localStorage.setItem('tojo_last_post', Date.now().toString());

    // コールバック
    this.onSubmit(postData);

    // フォームリセット＋閉じる
    this.container.querySelector('#post-form-body').reset();
    this.close();
  }

  isOpenState() {
    return this.isOpen;
  }
}

export default PostForm;
