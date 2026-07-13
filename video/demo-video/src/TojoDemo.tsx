import React from "react";
import { useCurrentFrame, interpolate, useVideoConfig } from "remotion";
import { Subtitle } from "../components/Subtitle";
import { SceneLabel } from "../components/SceneLabel";
import { LinkCard } from "../components/LinkCard";
import { Chip } from "../components/Chip";
import { RecommendItem } from "../components/RecommendItem";
import { StationPicker } from "../components/StationPicker";
import { PostFormOverlay } from "../components/PostFormOverlay";

const POSTS = [
  {
    id: "p1",
    stationId: "TJ-13",
    stationName: "鶴瀬",
    title: "鶴瀬駅徒歩5分🌸 甘酒＆麹カフェ Lesson",
    ogTitle: "麹カフェ つるせ",
    ogDesc: "6種類の麹で1day Lesson",
    tags: ["麹", "甘酒", "鶴瀬"],
    clicks: 42,
    commonUsers: 5,
    hasImage: true,
  },
  {
    id: "p2",
    stationId: "TJ-01",
    stationName: "池袋",
    title: "英会話カフェ募集 🇬🇧 池袋〜川越沿線",
    ogTitle: "東上線 英会話カフェ",
    ogDesc: "初心者歓迎・毎週土曜",
    tags: ["英会話", "募集"],
    clicks: 89,
    commonUsers: 12,
    hasImage: false,
  },
  {
    id: "p3",
    stationId: "TJ-17",
    stationName: "川越",
    title: "川越のレコード喫茶 🎵 アナログ1000枚",
    ogTitle: "レコード喫茶 小江戸",
    ogDesc: "コーヒーとレコードの休日",
    tags: ["レコード", "川越"],
    clicks: 156,
    commonUsers: 23,
    hasImage: true,
  },
  {
    id: "p4",
    stationId: "TJ-10",
    stationName: "志木",
    title: "志木駅前 隠れ家パン屋 🥐 朝6時営業",
    ogTitle: "ブーランジェリー 志木",
    ogDesc: "天然酵母・夜はワインバー",
    tags: ["パン", "志木"],
    clicks: 67,
    commonUsers: 8,
    hasImage: true,
  },
  {
    id: "p5",
    stationId: "TJ-26",
    stationName: "東松山",
    title: "東松山やきとり祭り 🍢 2026年秋",
    ogTitle: "やきとり祭り",
    ogDesc: "醤油たれが特徴・毎年10月",
    tags: ["グルメ", "東松山"],
    clicks: 203,
    commonUsers: 31,
    hasImage: true,
  },
];

const STATIONS = [
  { id: "TJ-01", name: "池袋", municipality: "東京都豊島区" },
  { id: "TJ-07", name: "成増", municipality: "東京都板橋区" },
  { id: "TJ-10", name: "志木", municipality: "埼玉県新座市" },
  { id: "TJ-13", name: "鶴瀬", municipality: "埼玉県富士見市" },
  { id: "TJ-17", name: "川越", municipality: "埼玉県川越市" },
  { id: "TJ-26", name: "東松山", municipality: "埼玉県東松山市" },
];

const CHIPS = ["すべて", "鶴瀬", "池袋", "川越", "志木", "東松山"];
const CHIPS_DATA = ["all", "TJ-13", "TJ-01", "TJ-17", "TJ-10", "TJ-26"];

/* ── SCENE 1: Opening (0-5s) ── */
export const OpeningScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const logoX = interpolate(frame, [0, 30], [-80, 0], { extrapolateRight: "clamp" });
  const logoOpacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" });
  const subtitleOpacity = interpolate(frame, [20, 40], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div style={styles.phoneContainer}>
      {/* Header */}
      <div style={styles.header}>
        <div
          style={{
            ...styles.logo,
            transform: `translateX(${logoX}px)`,
            opacity: logoOpacity,
          }}
        >
          🚃 東上リンク
        </div>
      </div>

      {/* Main content */}
      <div style={styles.main}>
        {/* Recommend section */}
        <div
          style={{
            ...styles.recommendSection,
            opacity: interpolate(frame, [40, 60], [0, 1], { extrapolateRight: "clamp" }),
            transform: `translateY(${interpolate(frame, [40, 65], [60, 0], { extrapolateRight: "clamp" })}px)`,
          }}
        >
          <div style={styles.recommendTitle}>✨ あなたへのおすすめ</div>
          {POSTS.slice(0, 3).map((p, i) => (
            <RecommendItem
              key={p.id}
              post={p}
              icon={["🎯", "🔥", "💡"][i]}
              delayFrames={55 + i * 8}
            />
          ))}
        </div>

        {/* Chips */}
        <div
          style={{
            ...styles.chipsRow,
            opacity: interpolate(frame, [70, 85], [0, 1], { extrapolateRight: "clamp" }),
          }}
        >
          {CHIPS.map((c, i) => (
            <Chip key={c} label={c} active={i === 0} />
          ))}
        </div>

        {/* Cards */}
        <div style={styles.cardsList}>
          {POSTS.map((p, i) => (
            <LinkCard
              key={p.id}
              post={p}
              delayFrames={80 + i * 10}
              saved={false}
            />
          ))}
        </div>
      </div>

      {/* Subtitle */}
      <div style={{ opacity: subtitleOpacity }}>
        <Subtitle text="東上線沿線の、リンク発見ボード" />
      </div>
    </div>
  );
};

/* ── SCENE 2: Station Picker (5-15s) ── */
export const StationPickerScene: React.FC = () => {
  const frame = useCurrentFrame();

  const pickerOpen = interpolate(frame, [0, 25], [1, 0], { extrapolateRight: "clamp" });
  const subtitleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  const subtitleHide = interpolate(frame, [240, 270], [1, 0], { extrapolateRight: "clamp" });

  return (
    <div style={styles.phoneContainer}>
      <div style={styles.header}>
        <div style={styles.logo}>🚃 東上リンク</div>
      </div>
      <div style={styles.main}>
        <div style={styles.recommendSection}>
          <div style={styles.recommendTitle}>✨ あなたへのおすすめ</div>
          {POSTS.slice(0, 3).map((p, i) => (
            <RecommendItem key={p.id} post={p} icon={["🎯", "🔥", "💡"][i]} delayFrames={0} />
          ))}
        </div>
        <div style={styles.chipsRow}>
          {CHIPS.map((c, i) => (
            <Chip key={c} label={c} active={i === 0} />
          ))}
        </div>
        <div style={styles.cardsList}>
          {POSTS.map((p, i) => (
            <LinkCard key={p.id} post={p} delayFrames={0} saved={false} />
          ))}
        </div>
      </div>

      {/* Station Picker slides up */}
      <div
        style={{
          ...styles.stationPicker,
          transform: `translateY(${pickerOpen * 100}%)`,
        }}
      >
        <StationPicker stations={STATIONS} fromFrame={25} />
      </div>

      <div style={{ opacity: subtitleOpacity * subtitleHide }}>
        <Subtitle text="ぷるぷる弾む、駅ピッカー" />
      </div>
    </div>
  );
};

/* ── SCENE 3: Filter (15-20s) ── */
export const FilterScene: React.FC = () => {
  const frame = useCurrentFrame();

  const subtitleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  const highlightChip = frame >= 30;
  const subtitleHide = interpolate(frame, [120, 140], [1, 0], { extrapolateRight: "clamp" });

  return (
    <div style={styles.phoneContainer}>
      <div style={styles.header}>
        <div style={styles.logo}>🚃 東上リンク</div>
      </div>
      <div style={styles.main}>
        <div style={styles.recommendSection}>
          <div style={styles.recommendTitle}>✨ あなたへのおすすめ</div>
          {POSTS.slice(0, 3).map((p, i) => (
            <RecommendItem key={p.id} post={p} icon={["🎯", "🔥", "💡"][i]} delayFrames={0} />
          ))}
        </div>

        {/* Chips with highlight on 鶴瀬 */}
        <div style={styles.chipsRow}>
          {CHIPS.map((c, i) => (
            <Chip
              key={c}
              label={c}
              active={highlightChip ? i === 1 : i === 0}
              highlighted={highlightChip && i === 1}
            />
          ))}
        </div>

        {/* Cards - dim non-鶴瀬 when filter active */}
        <div style={styles.cardsList}>
          {POSTS.map((p) => (
            <LinkCard
              key={p.id}
              post={p}
              delayFrames={0}
              saved={false}
              dimmed={highlightChip && p.stationId !== "TJ-13"}
            />
          ))}
        </div>
      </div>

      <div style={{ opacity: subtitleOpacity * subtitleHide }}>
        <Subtitle text="駅ごとに、気になるリンクが並ぶ" />
      </div>
    </div>
  );
};

/* ── SCENE 4: Save (20-30s) ── */
export const SaveScene: React.FC = () => {
  const frame = useCurrentFrame();

  const subtitleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  const subtitleHide = interpolate(frame, [270, 290], [1, 0], { extrapolateRight: "clamp" });
  const tapCircle = interpolate(frame, [40, 55], [0, 1], { extrapolateRight: "clamp" });

  // Scroll simulation - we animate the main content upward
  const scrollY = interpolate(frame, [0, 30], [0, 120], { extrapolateRight: "clamp" });

  // Save button pulse starts at frame 50
  const savePulse = interpolate(frame, [50, 58], [1, 1.2, 0.95, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const isSaved = frame >= 60;

  return (
    <div style={styles.phoneContainer}>
      <div style={styles.header}>
        <div style={styles.logo}>🚃 東上リンク</div>
      </div>
      <div
        style={{
          ...styles.main,
          transform: `translateY(-${scrollY}px)`,
        }}
      >
        <div style={styles.recommendSection}>
          <div style={styles.recommendTitle}>✨ あなたへのおすすめ</div>
          {POSTS.slice(0, 3).map((p, i) => (
            <RecommendItem key={p.id} post={p} icon={["🎯", "🔥", "💡"][i]} delayFrames={0} />
          ))}
        </div>
        <div style={styles.chipsRow}>
          {CHIPS.map((c, i) => (
            <Chip key={c} label={c} active={i === 0} />
          ))}
        </div>
        <div style={styles.cardsList}>
          {POSTS.map((p) => (
            <LinkCard
              key={p.id}
              post={p}
              delayFrames={0}
              saved={isSaved && p.id === "p3"}
              saveButtonScale={p.id === "p3" ? savePulse : 1}
            />
          ))}
        </div>
      </div>

      {/* Tap circle indicator on save button (p3 is card #3, approx y=580) */}
      {frame >= 35 && frame <= 55 && (
        <div
          style={{
            position: "absolute",
            left: 780,
            top: 620,
            width: 80 * tapCircle,
            height: 80 * tapCircle,
            borderRadius: "50%",
            background: `rgba(255, 107, 53, ${0.4 * (1 - tapCircle)})`,
            transform: "translate(-50%, -50%)",
          }}
        />
      )}

      <div style={{ opacity: subtitleOpacity * subtitleHide }}>
        <Subtitle text="「行ってみたい」を、ワンタップで保存" />
      </div>
    </div>
  );
};

/* ── SCENE 5: Connection (30-35s) ── */
export const ConnectionScene: React.FC = () => {
  const frame = useCurrentFrame();

  const subtitleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  const subtitleHide = interpolate(frame, [120, 140], [1, 0], { extrapolateRight: "clamp" });

  const scrollY = interpolate(frame, [0, 20], [0, 80], { extrapolateRight: "clamp" });
  const commonUsersOpacity = interpolate(frame, [30, 50], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div style={styles.phoneContainer}>
      <div style={styles.header}>
        <div style={styles.logo}>🚃 東上リンク</div>
      </div>
      <div style={{ ...styles.main, transform: `translateY(-${scrollY}px)` }}>
        <div style={styles.recommendSection}>
          <div style={styles.recommendTitle}>✨ あなたへのおすすめ</div>
          {POSTS.slice(0, 3).map((p, i) => (
            <RecommendItem key={p.id} post={p} icon={["🎯", "🔥", "💡"][i]} delayFrames={0} />
          ))}
        </div>
        <div style={styles.chipsRow}>
          {CHIPS.map((c, i) => (
            <Chip key={c} label={c} active={i === 0} />
          ))}
        </div>
        <div style={styles.cardsList}>
          {POSTS.map((p) => (
            <LinkCard
              key={p.id}
              post={p}
              delayFrames={0}
              saved={p.id === "p3"}
              showCommonUsers={true}
              commonUsersOpacity={p.commonUsers > 5 ? commonUsersOpacity : 0}
            />
          ))}
        </div>
      </div>

      <div style={{ opacity: subtitleOpacity * subtitleHide }}>
        <Subtitle text="共通の趣味の人と、出会えるかも" />
      </div>
    </div>
  );
};

/* ── SCENE 6: Post (35-42s) ── */
export const PostScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const subtitleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  const subtitleHide = interpolate(frame, [240, 260], [1, 0], { extrapolateRight: "clamp" });

  const formOpen = interpolate(frame, [10, 35], [1, 0], { extrapolateRight: "clamp" });
  const field1Active = frame >= 45;
  const field2Active = frame >= 60;
  const field3Active = frame >= 75;
  const submitVisible = frame >= 90;
  const submitted = frame >= 110;

  // New card flash
  const flashOpacity = interpolate(frame, [110, 130], [0.3, 0], { extrapolateRight: "clamp" });

  // New card appears
  const newCardOpacity = interpolate(frame, [115, 135], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div style={styles.phoneContainer}>
      <div style={styles.header}>
        <div style={styles.logo}>🚃 東上リンク</div>
      </div>
      <div style={styles.main}>
        <div style={styles.recommendSection}>
          <div style={styles.recommendTitle}>✨ あなたへのおすすめ</div>
          {POSTS.slice(0, 3).map((p, i) => (
            <RecommendItem key={p.id} post={p} icon={["🎯", "🔥", "💡"][i]} delayFrames={0} />
          ))}
        </div>
        <div style={styles.chipsRow}>
          {CHIPS.map((c, i) => (
            <Chip key={c} label={c} active={i === 0} />
          ))}
        </div>
        <div style={styles.cardsList}>
          {/* New card at top */}
          <div
            style={{
              opacity: newCardOpacity,
              transform: `translateY(${interpolate(frame, [115, 130], [-30, 0], { extrapolateRight: "clamp" })}px)`,
              border: submitted ? "2px solid #5b6abf" : "none",
            }}
          >
            <LinkCard
              post={{
                id: "p-new",
                stationId: "TJ-13",
                stationName: "鶴瀬",
                title: "鶴瀬駅🌸 新しいカフェ オープン",
                ogTitle: "新カフェ 鶴瀬",
                ogDesc: "駅から徒歩3分。本格派コーヒー",
                tags: ["カフェ", "鶴瀬"],
                clicks: 0,
                commonUsers: 0,
                hasImage: false,
              }}
              delayFrames={0}
              saved={false}
            />
          </div>
          {POSTS.map((p) => (
            <LinkCard key={p.id} post={p} delayFrames={0} saved={false} />
          ))}
        </div>
      </div>

      {/* Post form overlay */}
      {!submitted && (
        <div
          style={{
            ...styles.postFormOverlay,
            opacity: 1 - formOpen,
            pointerEvents: "none",
          }}
        >
          <PostFormOverlay
            fieldsActive={{ station: field1Active, title: field2Active, url: field3Active }}
            submitVisible={submitVisible}
          />
        </div>
      )}

      {/* Toast notification */}
      {submitted && frame < 200 && (
        <div
          style={{
            position: "absolute",
            top: 120,
            left: "50%",
            transform: "translateX(-50%)",
            background: "#333",
            color: "#fff",
            padding: "12px 24px",
            borderRadius: 20,
            fontSize: 22,
            fontWeight: 600,
            opacity: interpolate(frame, [110, 120, 200], [0, 1, 0], { extrapolateRight: "clamp" }),
            zIndex: 100,
          }}
        >
          📎 投稿しました！
        </div>
      )}

      {/* Flash */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "rgba(91,106,191,0.1)",
          opacity: flashOpacity,
          pointerEvents: "none",
        }}
      />

      <div style={{ opacity: subtitleOpacity * subtitleHide }}>
        <Subtitle text="あなたも、1日1回投稿できる" />
      </div>
    </div>
  );
};

/* ── SCENE 7: End (42-45s) ── */
export const EndScene: React.FC = () => {
  const frame = useCurrentFrame();

  const bgOpacity = interpolate(frame, [0, 30], [0, 0.9], { extrapolateRight: "clamp" });
  const textScale = interpolate(frame, [10, 40], [0.8, 1], { extrapolateRight: "clamp" });
  const textOpacity = interpolate(frame, [10, 30], [0, 1], { extrapolateRight: "clamp" });
  const subtitleOpacity = interpolate(frame, [30, 50], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div style={styles.phoneContainer}>
      <div style={styles.header}>
        <div style={styles.logo}>🚃 東上リンク</div>
      </div>
      <div style={styles.main}>
        <div style={styles.recommendSection}>
          <div style={styles.recommendTitle}>✨ あなたへのおすすめ</div>
          {POSTS.slice(0, 3).map((p, i) => (
            <RecommendItem key={p.id} post={p} icon={["🎯", "🔥", "💡"][i]} delayFrames={0} />
          ))}
        </div>
      </div>

      {/* Dark overlay with end message */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: `rgba(10, 10, 26, ${bgOpacity})`,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          gap: 20,
        }}
      >
        <div
          style={{
            fontSize: 64,
            transform: `scale(${textScale})`,
            opacity: textOpacity,
          }}
        >
          🚃
        </div>
        <div
          style={{
            fontSize: 42,
            fontWeight: 800,
            background: "linear-gradient(135deg, #ff6b35, #5b6abf)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            transform: `scale(${textScale})`,
            opacity: textOpacity,
          }}
        >
          東上リンク
        </div>
        <div
          style={{
            fontSize: 22,
            color: "#999",
            fontWeight: 500,
            transform: `scale(${textScale})`,
            opacity: textOpacity,
          }}
        >
          もうすぐ開始
        </div>
      </div>

      <div style={{ opacity: subtitleOpacity }}>
        <Subtitle text="写真もログインも、いらない 🚃" />
      </div>
    </div>
  );
};

/* ── SHARED STYLES ── */
const styles: Record<string, React.CSSProperties> = {
  phoneContainer: {
    width: 1080,
    height: 1920,
    background: "#f8f9fa",
    position: "relative",
    overflow: "hidden",
    fontFamily: '-apple-system, "Hiragino Kaku Gothic ProN", "Noto Sans JP", sans-serif',
  },
  header: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    height: 140,
    background: "#fff",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    boxShadow: "0 2px 8px rgba(0,0,0,0.04)",
    zIndex: 10,
    paddingTop: 50,
  },
  logo: {
    fontSize: 40,
    fontWeight: 800,
    background: "linear-gradient(135deg, #ff6b35, #5b6abf)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  },
  main: {
    position: "absolute",
    top: 140,
    left: 0,
    right: 0,
    bottom: 0,
    overflow: "hidden",
  },
  recommendSection: {
    padding: "24px 24px 12px",
    background: "linear-gradient(135deg, #fff8e1, #f8f9fa)",
  },
  recommendTitle: {
    fontSize: 22,
    fontWeight: 700,
    color: "#8d6e00",
    marginBottom: 16,
  },
  chipsRow: {
    display: "flex",
    gap: 12,
    padding: "16px 24px",
    overflow: "hidden",
  },
  cardsList: {
    padding: "0 24px 40px",
  },
  stationPicker: {
    position: "absolute",
    bottom: 0,
    left: 0,
    right: 0,
    zIndex: 20,
  },
  postFormOverlay: {
    position: "absolute",
    inset: 0,
    background: "rgba(0,0,0,0.4)",
    display: "flex",
    alignItems: "flex-end",
    zIndex: 50,
  },
};
