import { useStyleStore } from "../store/styleStore";
import { Link } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Navbar } from "../components/Navbar";

const LexicaImages = () => {
  const styles = useStyleStore((state) => state.styles);

  // Flatten all lexica images from all styles into a single array
  const allLexicaImages = styles.flatMap((style) =>
    style.lexica_images.map((image) => ({
      ...image,
      styleName: style.style_name,
    }))
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="container mx-auto py-8">
        <h1 className="mb-8 text-3xl font-bold">All Lexica Images</h1>
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {allLexicaImages.map((image, index) => (
            <Link
              to={`/style/${encodeURIComponent(image.styleName)}`}
              key={index}
              className="transition-transform hover:scale-105"
            >
              <Card className="overflow-hidden">
                <img
                  src={image.src}
                  alt={image.alt}
                  className="aspect-square w-full object-cover"
                />
                <div className="p-4">
                  <h3 className="mb-2 font-semibold">{image.styleName}</h3>
                  <p className="mb-2 text-sm text-gray-600">{image.prompt}</p>
                  <p className="text-xs text-gray-500">{image.dimensions}</p>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      </main>
    </div>
  );
};

export default LexicaImages;