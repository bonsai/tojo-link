import { Composition } from "remotion";
import { TojoDemo } from "./TojoDemo";

export const RemotionRoot = () => {
  return (
    <>
      <Composition
        id="TojoDemo"
        component={TojoDemo}
        durationInFrames={45 * 30} // 45 seconds at 30fps
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{}}
      />
    </>
  );
};
