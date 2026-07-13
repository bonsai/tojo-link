import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

interface Props {
  text: string;
}

export const Subtitle: React.FC<Props> = ({ text }) => {
  const frame = useCurrentFrame();

  return (
    <div
      style={{
        position: "absolute",
        bottom: 80,
        left: "50%",
        transform: "translateX(-50%)",
        background: "rgba(0,0,0,0.85)",
        color: "#fff",
        padding: "14px 36px",
        borderRadius: 30,
        fontSize: 26,
        fontWeight: 600,
        whiteSpace: "nowrap",
        zIndex: 50,
      }}
    >
      {text}
    </div>
  );
};
