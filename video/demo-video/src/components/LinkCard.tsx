import React from "react";
import { interpolate, useCurrentFrame, spring } from "remotion";

interface PostData {
  id: string;
  stationId: string;
  stationName: string;
  title: string;
  ogTitle: string;
  ogDesc: string;
  tags: string[];
  clicks: number;
  commonUsers: number;
  hasImage: boolean;
}

interface Props {
  post: PostData;
  delayFrames?: number;
  saved?: boolean;
  dimmed?: boolean;
  saveButtonScale?: number;
  showCommonUsers?: boolean;
  commonUsersOpacity?: number;
}

const timeAgo = (minutes: number): string => {
  if (minutes < 1) return "たった今";
  if (minutes < 60) return `${minutes}分前`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}時間前`;
  return `${Math.floor(hours / 24)}日前`;
};

export const LinkCard: React.FC<Props> = ({
  post,
  delayFrames = 0,
  saved,
  dimmed,
  saveButtonScale,
  showCommonUsers,
  commonUsersOpacity,
}) => {
  const frame = useCurrentFrame();
  const adjustedFrame = Math.max(0, frame - delayFrames);

  const slideY = interpolate(adjustedFrame, [0, 15], [40, 0], {
    extrapolateRight: "clamp",
  });
  const opacity = interpolate(adjustedFrame, [0, 10], [0, dimmed ? 0.3 : 1], {
    extrapolateRight: "clamp",
  });

  const minutesAgo = post.id === "p-new" ? 0 : (post.clicks * 2);

  return (
    <div
      style={{
        background: "#fff",
        borderRadius: 18,
        padding: 20,
        marginBottom: 16,
        boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
        transform: `translateY(${slideY}px)`,
        opacity,
      }}
    >
      {/* Header */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: 8,
        }}
      >
        <span
          style={{
            fontSize: 18,
            fontWeight: 600,
            color: "#ff6b35",
          }}
        >
          {post.stationId} {post.stationName}
        </span>
        <span style={{ fontSize: 14, color: "#999" }}>
          {timeAgo(minutesAgo)}
        </span>
      </div>

      {/* Title */}
      <div
        style={{
          fontSize: 24,
          fontWeight: 600,
          marginBottom: 10,
          lineHeight: 1.3,
        }}
      >
        {post.title}
      </div>

      {/* URL Preview */}
      <div
        style={{
          display: "flex",
          gap: 12,
          padding: 12,
          background: "#f8f9fa",
          borderRadius: 12,
          marginBottom: 10,
        }}
      >
        <div
          style={{
            width: 28,
            height: 28,
            background: "#ddd",
            borderRadius: 6,
            flexShrink: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 14,
          }}
        >
          🔗
        </div>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div
            style={{
              fontSize: 18,
              fontWeight: 500,
              whiteSpace: "nowrap",
              overflow: "hidden",
              textOverflow: "ellipsis",
            }}
          >
            {post.ogTitle}
          </div>
          <div
            style={{
              fontSize: 14,
              color: "#666",
              marginTop: 4,
            }}
          >
            {post.ogDesc}
          </div>
        </div>
        {post.hasImage && (
          <div
            style={{
              width: 80,
              height: 80,
              borderRadius: 10,
              background: "linear-gradient(135deg, #667eea, #764ba2)",
              flexShrink: 0,
            }}
          />
        )}
      </div>

      {/* Tags */}
      {post.tags.length > 0 && (
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            gap: 8,
            marginBottom: 12,
          }}
        >
          {post.tags.map((t) => (
            <span
              key={t}
              style={{
                fontSize: 14,
                padding: "4px 10px",
                background: "#e8ecff",
                color: "#5b6abf",
                borderRadius: 12,
                fontWeight: 500,
              }}
            >
              #{t}
            </span>
          ))}
        </div>
      )}

      {/* Actions */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 18,
        }}
      >
        <span style={{ fontSize: 16, color: "#999" }}>
          🔗 {post.clicks}
        </span>
        {post.commonUsers > 0 && (
          <span style={{ fontSize: 16, color: "#999" }}>
            👥 {post.commonUsers}
          </span>
        )}
        <div
          style={{
            marginLeft: "auto",
            padding: "8px 18px",
            background: saved ? "#ccc" : "#ff6b35",
            color: "#fff",
            fontSize: 16,
            fontWeight: 600,
            borderRadius: 22,
            transform: saveButtonScale ? `scale(${saveButtonScale})` : undefined,
          }}
        >
          {saved ? "✓ 保存済" : "📍 行ってみたい"}
        </div>
      </div>

      {/* Common Users Banner */}
      {showCommonUsers && post.commonUsers > 5 && (
        <div
          style={{
            marginTop: 10,
            padding: "10px 14px",
            background: "#fff8e1",
            borderRadius: 10,
            fontSize: 16,
            color: "#8d6e00",
            opacity: commonUsersOpacity,
          }}
        >
          👥 #{post.tags[0]} に興味がある人と共通しています
        </div>
      )}
    </div>
  );
};
