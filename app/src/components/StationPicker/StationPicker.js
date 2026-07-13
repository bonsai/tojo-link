/**
 * StationPicker — ぷるぷる弾む駅選択コンポーネント
 * 位置情報×好み学習でレコメンデーション
 * 再利用可能: new StationPicker({ container, onSelect, stationsUrl })
 */
class StationPicker {
  constructor(options = {}) {
    this.container = options.container || document.querySelector('#station-picker');
    this.onSelect = options.onSelect || (() => {});
    this.stationsUrl = options.stationsUrl || '/data/stations.json';
    this.stations = [];
    this.selectedId = null;
    this.preferences = this._loadPreferences();
    this.userLocation = null;

    this._init();
  }

  async _init() {
    // 駅データ読み込み
    this.stations = await this._fetchStations();

    // 位置情報取得（許可時のみ）
    this.userLocation = await this._getLocation();

    // 描画
    this._render();

    // 推薦スコア計算
    this._applyRecommendation();
  }

  async _fetchStations() {
    const res = await fetch(this.stationsUrl);
    const data = await res.json();
    return data.stations;
  }

  _getLocation() {
    return new Promise((resolve) => {
      if (!navigator.geolocation) return resolve(null);
      navigator.geolocation.getCurrentPosition(
        (pos) => resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
        () => resolve(null),
        { enableHighAccuracy: false, timeout: 5000 }
      );
    });
  }

  _loadPreferences() {
    try {
      return JSON.parse(localStorage.getItem('tojo_prefs') || '{}');
    } catch {
      return {};
    }
  }

  _savePreference(stationId) {
    this.preferences[stationId] = (this.preferences[stationId] || 0) + 1;
    localStorage.setItem('tojo_prefs', JSON.stringify(this.preferences));
  }

  /**
   * 推薦スコア: 距離 + 選択履歴
   * score = -(距離km) + (選択回数 × 10)
   */
  _calcRecommendationScore(station) {
    let score = 0;

    // 距離スコア（現在地から近いほど高スコア）
    if (this.userLocation) {
      const dist = this._haversineDistance(
        this.userLocation.lat, this.userLocation.lng,
        station.lat, station.lng
      );
      score -= dist;
    }

    // 好み学習スコア
    if (this.preferences[station.id]) {
      score += this.preferences[station.id] * 10;
    }

    return score;
  }

  _haversineDistance(lat1, lng1, lat2, lng2) {
    const R = 6371;
    const toRad = (d) => (d * Math.PI) / 180;
    const dLat = toRad(lat2 - lat1);
    const dLng = toRad(lng2 - lng1);
    const a = Math.sin(dLat / 2) ** 2 +
              Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
              Math.sin(dLng / 2) ** 2;
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  }

  _applyRecommendation() {
    // スコア計算
    const scored = this.stations.map(s => ({
      ...s,
      _score: this._calcRecommendationScore(s)
    }));

    // ソート（スコア順）
    scored.sort((a, b) => b._score - a._score);

    // 上位3駅に recommended マーク付与
    const top3 = scored.slice(0, 3).map(s => s.id);
    top3.forEach(id => {
      const el = this.container.querySelector(`[data-station-id="${id}"]`);
      if (el) el.classList.add('recommended');
    });
  }

  _render() {
    this.container.innerHTML = `
      <div class="station-picker collapsed" role="dialog" aria-label="駅選択">
        <div class="station-picker__handle" id="picker-handle"></div>
        <div class="station-picker__header">
          <div class="station-picker__title">🚃 駅を選んでください</div>
          <input type="text" class="station-picker__search"
            placeholder="🔍 駅名・自治体で検索" aria-label="駅検索" />
        </div>
        <div class="station-picker__list" id="station-list">
          ${this._renderStations()}
        </div>
      </div>
    `;

    this._bindEvents();
  }

  _renderStations(filtered = null) {
    const list = filtered || this.stations;
    return list.map(s => `
      <div class="station-picker__item"
           data-station-id="${s.id}"
           data-station-name="${s.name}"
           data-municipality="${s.municipality}"
           role="option"
           tabindex="0">
        <span class="station-picker__number">${s.id}</span>
        <span class="station-picker__name">${s.name}</span>
        <span class="station-picker__municipality">${s.municipality}</span>
        <span class="station-picker__recommend">⭐</span>
      </div>
    `).join('');
  }

  _bindEvents() {
    const picker = this.container.querySelector('.station-picker');
    const handle = this.container.querySelector('#picker-handle');
    const searchInput = this.container.querySelector('.station-picker__search');
    const stationList = this.container.querySelector('#station-list');

    // ハンドルドラッグで展開/折りたたみ
    let startY = 0;
    handle.addEventListener('touchstart', (e) => { startY = e.touches[0].clientY; });
    handle.addEventListener('touchend', (e) => {
      const deltaY = e.changedTouches[0].clientY - startY;
      picker.classList.toggle('collapsed', deltaY > 50);
      picker.classList.toggle('expanded', deltaY < -50);
    });

    // タップで展開
    handle.addEventListener('click', () => {
      picker.classList.toggle('collapsed');
      picker.classList.toggle('expanded');
    });

    // 検索フィルタ
    searchInput.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase();
      const filtered = this.stations.filter(s =>
        s.name.includes(q) ||
        s.name_kana.includes(q) ||
        s.municipality.includes(q) ||
        s.id.toLowerCase().includes(q)
      );
      stationList.innerHTML = this._renderStations(filtered);
      this._bindStationClick();
    });

    // 駅クリック
    this._bindStationClick();
  }

  _bindStationClick() {
    const items = this.container.querySelectorAll('.station-picker__item');
    items.forEach(item => {
      item.addEventListener('click', () => {
        const stationId = item.dataset.stationId;
        const station = this.stations.find(s => s.id === stationId);

        // ぷるぷるアニメーション
        item.classList.add('just-selected');
        if (navigator.vibrate) navigator.vibrate(15);

        // 選択状態更新
        if (this.selectedId) {
          const prev = this.container.querySelector(`[data-station-id="${this.selectedId}"]`);
          if (prev) prev.classList.remove('selected');
        }
        item.classList.add('selected');
        this.selectedId = stationId;

        // 好み保存
        this._savePreference(stationId);

        // コールバック
        this.onSelect(station);

        // 1秒後にアニメーションクラス除去
        setTimeout(() => item.classList.remove('just-selected'), 600);
      });
    });
  }

  // 外部からデータ更新用
  async refresh() {
    this.stations = await this._fetchStations();
    this.userLocation = await this._getLocation();
    this._render();
    this._applyRecommendation();
  }
}

export default StationPicker;
