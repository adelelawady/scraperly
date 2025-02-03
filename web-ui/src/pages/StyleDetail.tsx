import { useParams, Link } from "react-router-dom";
import { useStyleStore } from "../store/styleStore";
import { ArrowLeft, Copy } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/use-toast";

const StyleDetail = () => {
  const { styleName } = useParams();
  const styles = useStyleStore((state) => state.styles);
  const { toast } = useToast();
  
  const style = styles.find(
    (s) => s.style_name === decodeURIComponent(styleName || "")
  );

  if (!style) {
    return <div>Style not found</div>;
  }

  const handleCopyKeywords = () => {
    const keywordsText = style.keywords.join(" ");
    navigator.clipboard.writeText(keywordsText).then(() => {
      toast({
        title: "Keywords copied!",
        description: "Keywords have been copied to your clipboard",
      });
    });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto py-8">
        <Link to="/">
          <Button variant="outline" className="mb-6 flex items-center gap-2">
            <ArrowLeft className="h-4 w-4" />
            Back to Gallery
          </Button>
        </Link>
        
        <h1 className="mb-8 text-4xl font-bold">{style.style_name}</h1>
        
        <div className="mb-12">
          <h2 className="mb-4 text-2xl font-semibold">Gallery</h2>
          <div className="image-grid">
            {style.images.map((image, index) => (
              <img
                key={index}
                src={image.src}
                alt={image.alt}
                className="rounded-lg shadow-md w-full h-64 object-cover"
              />
            ))}
          </div>
        </div>

        <div className="mb-12">
          <h2 className="mb-4 text-2xl font-semibold">Lexica Images</h2>
          <div className="image-grid">
            {style.lexica_images.map((image, index) => (
              <div key={index} className="rounded-lg bg-white p-4 shadow-md">
                <img
                  src={image.src}
                  alt={image.alt}
                  className="mb-4 rounded-lg w-full h-64 object-cover"
                />
                <p className="text-sm text-gray-600">Prompt: {image.prompt}</p>
                <p className="text-sm text-gray-500">
                  Dimensions: {image.dimensions}
                </p>
              </div>
            ))}
          </div>
        </div>

        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-semibold">Keywords</h2>
            <Button
              variant="outline"
              size="sm"
              onClick={handleCopyKeywords}
              className="flex items-center gap-2"
            >
              <Copy className="h-4 w-4" />
              Copy Keywords
            </Button>
          </div>
          <div className="flex flex-wrap gap-2">
            {style.keywords.map((keyword) => (
              <span
                key={keyword}
                className="rounded-full bg-primary/10 px-3 py-1 text-sm text-primary"
              >
                {keyword}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default StyleDetail;