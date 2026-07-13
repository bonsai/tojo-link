import React from "react";

interface Props {
  label: string;
  active?: boolean;
  highlighted?: boolean;
}

export const Chip: React.FC<Props> = ({ label, active, highlighted }) => {
  return (
    <div
      style={{
        padding: "10px 22px",
        background: highlighted ? "#fff3e0" : active ? "#5b6abf" : "#fff",
        color: highlighted || active ? "#fff" : "#333",
        border: highlighted
          ? "2px solid #ff6b35"
          : active
          ? "2px solid #5b6abf"
          : "2px solid #e0e0e0",
        borderRadius: 28,
        fontSize: 20,
        fontWeight: 500,
        whiteSpace: "nowrap",
        flexShrink: 0,
      }}
    >
      {label}
    </div>
  );
};
