import { Upload, FileJson, Images } from "lucide-react";
import { Button } from "@/components/ui/button";
import { JsonInput } from "./JsonInput";
import { useState } from "react";
import { Link } from "react-router-dom";

export const Navbar = () => {
  const [showJsonInput, setShowJsonInput] = useState(false);

  return (
    <nav className="border-b bg-white shadow-sm">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4">
        <div className="flex items-center gap-6">
          <Link to="/" className="text-xl font-bold text-primary">
            Style Gallery
          </Link>
          <Link
            to="/lexica-images"
            className="flex items-center gap-2 text-gray-600 hover:text-primary"
          >
            <Images className="h-4 w-4" />
            Lexica Images
          </Link>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            onClick={() => setShowJsonInput(true)}
            className="flex items-center gap-2"
          >
            <FileJson className="h-4 w-4" />
            Add JSON
          </Button>
          <Button
            variant="outline"
            onClick={() => document.getElementById("file-input")?.click()}
            className="flex items-center gap-2"
          >
            <Upload className="h-4 w-4" />
            Upload JSON
          </Button>
          <input
            type="file"
            id="file-input"
            accept=".json"
            className="hidden"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                  try {
                    const json = JSON.parse(e.target?.result as string);
                    // Handle JSON data
                  } catch (error) {
                    console.error("Error parsing JSON:", error);
                  }
                };
                reader.readAsText(file);
              }
            }}
          />
        </div>
        <JsonInput open={showJsonInput} onOpenChange={setShowJsonInput} />
      </div>
    </nav>
  );
};