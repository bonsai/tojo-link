import React from "react";

interface Props {
  fieldsActive: {
    station: boolean;
    title: boolean;
    url: boolean;
  };
  submitVisible: boolean;
}

export const PostFormOverlay: React.FC<Props> = ({
  fieldsActive,
  submitVisible,
}) => {
  return (
    <div
      style={{
        width: "100%",
        background: "#fff",
        borderRadius: "30px 30px 0 0",
        padding: "28px 24px",
        paddingBottom: 40,
      }}
    >
      <div
        style={{
          width: 50,
          height: 6,
          background: "#ccc",
          borderRadius: 3,
          margin: "0 auto 20px",
        }}
      />

      <div
        style={{
          fontSize: 28,
          fontWeight: 700,
          textAlign: "center",
          marginBottom: 20,
        }}
      >
        📎 リンクを投稿する
      </div>

      {/* Station field */}
      <div style={{ marginBottom: 14 }}>
        <div style={{ fontSize: 16, fontWeight: 600, color: "#666", marginBottom: 6 }}>
          🚃 駅
        </div>
        <div
          style={{
            padding: "14px 16px",
            border: fieldsActive.station ? "2px solid #5b6abf" : "2px solid #e0e0e0",
            borderRadius: 14,
            background: fieldsActive.station ? "#fff" : "#f8f9fa",
            fontSize: 22,
            boxShadow: fieldsActive.station
              ? "0 0 0 4px rgba(91,106,191,0.1)"
              : "none",
          }}
        >
          鶴瀬（TJ-13）
        </div>
      </div>

      {/* Title field */}
      <div style={{ marginBottom: 14 }}>
        <div style={{ fontSize: 16, fontWeight: 600, color: "#666", marginBottom: 6 }}>
          タイトル
        </div>
        <div
          style={{
            padding: "14px 16px",
            border: fieldsActive.title ? "2px solid #5b6abf" : "2px solid #e0e0e0",
            borderRadius: 14,
            background: fieldsActive.title ? "#fff" : "#f8f9fa",
            fontSize: 22,
            boxShadow: fieldsActive.title
              ? "0 0 0 4px rgba(91,106,191,0.1)"
              : "none",
          }}
        >
          鶴瀬駅🌸 新しいカフェ オープン
        </div>
      </div>

      {/* URL field */}
      <div style={{ marginBottom: 14 }}>
        <div style={{ fontSize: 16, fontWeight: 600, color: "#666", marginBottom: 6 }}>
          URL
        </div>
        <div
          style={{
            padding: "14px 16px",
            border: fieldsActive.url ? "2px solid #5b6abf" : "2px solid #e0e0e0",
            borderRadius: 14,
            background: fieldsActive.url ? "#fff" : "#f8f9fa",
            fontSize: 22,
            boxShadow: fieldsActive.url
              ? "0 0 0 4px rgba(91,106,191,0.1)"
              : "none",
          }}
        >
          https://example.com/new-cafe
        </div>
      </div>

      {/* Submit button */}
      {submitVisible && (
        <div
          style={{
            width: "100%",
            padding: "16px 0",
            background: "#5b6abf",
            color: "#fff",
            fontSize: 26,
            fontWeight: 600,
            borderRadius: 16,
            textAlign: "center",
            marginTop: 8,
          }}
        >
          投稿する
        </div>
      )}
    </div>
  );
};
