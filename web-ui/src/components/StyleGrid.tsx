import { StyleCard } from "./StyleCard";
import { useStyleStore } from "../store/styleStore";

export const StyleGrid = () => {
  const styles = useStyleStore((state) => state.styles);

  return (
    <div className="image-grid">
      {styles.map((style) => (
        <StyleCard key={style.style_name} style={style} />
      ))}
    </div>
  );
};