/**
 * 東上リンク — メインアプリ
 * 「素人はカメラ＋駅名だけ」×「AIが全部まとめる」×「格安ストレージ」
 */
import StationPicker from './components/StationPicker/StationPicker.js';
import LinkBoard from './components/LinkBoard/LinkBoard.js';
import PostForm from './components/PostForm/PostForm.js';
import CustomRecommend from './components/CustomRecommend/CustomRecommend.js';

class App {
  constructor() {
    this.stations = [];
    this.picker = null;
    this.board = null;
    this.postForm = null;
    this.recommend = null;

    this._init();
  }

  async _init() {
    // 駅データ読み込み
    this.stations = await this._loadStations();

    // 駅ピッカー初期化
    this.picker = new StationPicker({
      container: document.querySelector('#station-picker'),
      stationsUrl: '/data/stations.json',
      onSelect: (station) => {
        this._showToast(`${station.name} を選択中`);
        this.board?.refresh(
          this.board.posts.map(p => ({
            ...p,
            _highlight: p.stationId === station.id
          }))
        );
      }
    });

    // 投稿フォーム初期化
    this.postForm = new PostForm({
      container: document.querySelector('#post-form-overlay'),
      stations: this.stations,
      onSubmit: (postData) => {
        this._handlePost(postData);
      }
    });

    // メインフィード初期化
    this.board = new LinkBoard({
      container: document.querySelector('#link-board'),
      onPost: () => {
        this.postForm.open();
      }
    });

    // カスタム推薦初期化
    this.recommend = new CustomRecommend({
      container: document.querySelector('#custom-recommend'),
      posts: this.board.posts
    });

    console.log('🚃 東上リンク initialized');
  }

  async _loadStations() {
    const res = await fetch('/data/stations.json');
    const data = await res.json();
    return data.stations;
  }

  _handlePost(postData) {
    // 投稿をフィードに追加
    const newPost = {
      ...postData,
      clicks: 0,
      commonUsers: 0,
      ogTitle: postData.title,
      ogDesc: '',
      ogImage: null
    };

    this.board.posts.unshift(newPost);
    this.board.refresh();
    this.recommend.refresh(this.board.posts);

    this._showToast('📎 投稿しました！');
  }

  _showToast(message) {
    let toast = document.querySelector('.toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.className = 'toast';
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2000);
  }
}

// アプリ起動
document.addEventListener('DOMContentLoaded', () => {
  window.app = new App();
});

export default App;
