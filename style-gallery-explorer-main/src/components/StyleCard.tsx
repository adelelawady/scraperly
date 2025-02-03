import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Style } from "../types/style";
import { Link } from "react-router-dom";

interface StyleCardProps {
  style: Style;
}

export const StyleCard = ({ style }: StyleCardProps) => {
  return (
    <Link to={`/style/${encodeURIComponent(style.style_name)}`}>
      <Card className="overflow-hidden card-hover">
        <CardHeader className="p-4">
          <CardTitle className="text-lg">{style.style_name}</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <img
            src={style.images[0].src}
            alt={style.images[0].alt}
            className="h-48 w-full object-cover"
          />
          <div className="p-4">
            <div className="flex flex-wrap gap-2">
              {style.keywords.slice(0, 3).map((keyword) => (
                <span
                  key={keyword}
                  className="rounded-full bg-primary/10 px-2 py-1 text-xs text-primary"
                >
                  {keyword}
                </span>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
};