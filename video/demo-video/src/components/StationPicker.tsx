import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

interface Station {
  id: string;
  name: string;
  municipality: string;
}

interface Props {
  stations: Station[];
  fromFrame?: number;
}

export const StationPicker: React.FC<Props> = ({ stations, fromFrame = 0 }) => {
  const frame = useCurrentFrame();

  return (
    <div
      style={{
        background: "#fff",
        borderRadius: "30px 30px 0 0",
        boxShadow: "0 -8px 32px rgba(0,0,0,0.1)",
        maxHeight: "70%",
        overflow: "hidden",
      }}
    >
      {/* Handle */}
      <div
        style={{
          width: 60,
          height: 8,
          background: "#ccc",
          borderRadius: 4,
          margin: "16px auto",
        }}
      />

      {/* Header */}
      <div
        style={{
          padding: "0 24px 16px",
          borderBottom: "1px solid #eee",
        }}
      >
        <div style={{ fontSize: 22, fontWeight: 600, color: "#666" }}>
          🚃 駅を選んでください
        </div>
        <div
          style={{
            marginTop: 12,
            padding: "14px 16px",
            border: "1px solid #e0e0e0",
            borderRadius: 14,
            background: "#f8f9fa",
            fontSize: 20,
            color: "#999",
          }}
        >
          🔍 駅名・自治体で検索
        </div>
      </div>

      {/* Station List */}
      <div style={{ padding: "12px 0" }}>
        {stations.map((s, i) => {
          const isRecommended =
            s.id === "TJ-13" || s.id === "TJ-01" || s.id === "TJ-17";
          const itemDelay = i * 5;
          const adjustedFrame = Math.max(0, frame - fromFrame - itemDelay);
          const itemOpacity = interpolate(
            adjustedFrame,
            [0, 8],
            [0, 1],
            { extrapolateRight: "clamp" }
          );

          return (
            <div
              key={s.id}
              style={{
                padding: "16px 24px",
                display: "flex",
                alignItems: "center",
                gap: 16,
                opacity: itemOpacity,
                background: isRecommended ? "#f0f4ff" : "transparent",
              }}
            >
              <div
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  justifyContent: "center",
                  minWidth: 60,
                  height: 36,
                  padding: "0 8px",
                  background: "#ff6b35",
                  color: "#fff",
                  fontSize: 16,
                  fontWeight: 700,
                  borderRadius: 18,
                }}
              >
                {s.id}
              </div>
              <div
                style={{
                  fontSize: 26,
                  fontWeight: 500,
                  flex: 1,
                }}
              >
                {s.name}
              </div>
              <div
                style={{
                  fontSize: 16,
                  color: "#999",
                }}
              >
                {s.municipality}
              </div>
              {isRecommended && (
                <div style={{ fontSize: 24 }}>⭐</div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
