import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";
import { useStyleStore } from "../store/styleStore";
import { Style } from "../types/style";

interface JsonInputProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export const JsonInput = ({ open, onOpenChange }: JsonInputProps) => {
  const [jsonText, setJsonText] = useState("");
  const setStyles = useStyleStore((state) => state.setStyles);

  const handleSubmit = () => {
    try {
      const data = JSON.parse(jsonText);
      const styles = Array.isArray(data) ? data : [data];
      setStyles(styles as Style[]);
      onOpenChange(false);
      setJsonText("");
    } catch (error) {
      console.error("Error parsing JSON:", error);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add JSON Data</DialogTitle>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <Textarea
            value={jsonText}
            onChange={(e) => setJsonText(e.target.value)}
            placeholder="Paste your JSON here..."
            className="min-h-[200px]"
          />
          <Button onClick={handleSubmit}>Submit</Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};