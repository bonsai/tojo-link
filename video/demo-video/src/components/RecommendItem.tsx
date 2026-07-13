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
  icon: string;
  delayFrames?: number;
}

export const RecommendItem: React.FC<Props> = ({ post, icon, delayFrames = 0 }) => {
  const frame = useCurrentFrame();
  const adjustedFrame = Math.max(0, frame - delayFrames);

  const slideX = interpolate(adjustedFrame, [0, 15], [-30, 0], {
    extrapolateRight: "clamp",
  });
  const opacity = interpolate(adjustedFrame, [0, 10], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 16,
        padding: "16px 18px",
        background: "#fff",
        borderRadius: 14,
        marginBottom: 12,
        boxShadow: "0 2px 6px rgba(0,0,0,0.06)",
        transform: `translateX(${slideX}px)`,
        opacity,
      }}
    >
      <div style={{ fontSize: 36, flexShrink: 0 }}>{icon}</div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div
          style={{
            fontSize: 22,
            fontWeight: 600,
            whiteSpace: "nowrap",
            overflow: "hidden",
            textOverflow: "ellipsis",
          }}
        >
          {post.title}
        </div>
        <div style={{ fontSize: 16, color: "#999", marginTop: 4 }}>
          {post.stationId} {post.stationName}
        </div>
      </div>
      {post.commonUsers > 5 && (
        <div
          style={{
            fontSize: 16,
            padding: "4px 12px",
            background: "#ff6b35",
            color: "#fff",
            borderRadius: 14,
            fontWeight: 600,
            flexShrink: 0,
          }}
        >
          共通{post.commonUsers}人
        </div>
      )}
    </div>
  );
};
