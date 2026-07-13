import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

interface Props {
  text: string;
}

export const SceneLabel: React.FC<Props> = ({ text }) => {
  const frame = useCurrentFrame();

  return (
    <div
      style={{
        position: "absolute",
        top: 100,
        left: 24,
        background: "rgba(0,0,0,0.7)",
        color: "#fff",
        padding: "6px 16px",
        borderRadius: 14,
        fontSize: 16,
        fontWeight: 600,
        zIndex: 40,
      }}
    >
      {text}
    </div>
  );
};
