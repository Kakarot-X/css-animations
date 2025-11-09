import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import axios from "axios";
import { toast } from "sonner";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const categories = [
  "Fade",
  "Slide",
  "Rotate",
  "Bounce",
  "Scale",
  "Special Effects"
];

const shapes = [
  { value: "cube", label: "Cube" },
  { value: "square", label: "Square" },
  { value: "circle", label: "Circle" },
  { value: "rectangle", label: "Rectangle" }
];

const AddAnimationDialog = ({ open, onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    title: "",
    css_code: "",
    category: "",
    shape_type: "cube"
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const token = localStorage.getItem('token');
      await axios.post(
        `${API}/animations?token=${token}`,
        formData
      );
      toast.success("Animation created successfully!");
      setFormData({
        title: "",
        css_code: "",
        category: "",
        shape_type: "cube"
      });
      onSuccess();
    } catch (error) {
      console.error("Error creating animation:", error);
      toast.error(error.response?.data?.detail || "Failed to create animation");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Add New Animation</DialogTitle>
          <DialogDescription>
            Create and share your CSS animation with the community
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="title">Animation Title</Label>
            <Input
              id="title"
              data-testid="animation-title-input"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              placeholder="e.g., Smooth Fade In"
              required
            />
          </div>

          <div>
            <Label htmlFor="category">Category</Label>
            <Select
              value={formData.category}
              onValueChange={(value) => setFormData({ ...formData, category: value })}
              required
            >
              <SelectTrigger data-testid="category-select">
                <SelectValue placeholder="Select a category" />
              </SelectTrigger>
              <SelectContent>
                {categories.map((cat) => (
                  <SelectItem key={cat} value={cat} data-testid={`category-${cat.toLowerCase().replace(' ', '-')}`}>
                    {cat}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div>
            <Label htmlFor="shape">Preview Shape</Label>
            <Select
              value={formData.shape_type}
              onValueChange={(value) => setFormData({ ...formData, shape_type: value })}
              required
            >
              <SelectTrigger data-testid="shape-select">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {shapes.map((shape) => (
                  <SelectItem key={shape.value} value={shape.value} data-testid={`shape-option-${shape.value}`}>
                    {shape.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div>
            <Label htmlFor="css_code">CSS Code</Label>
            <Textarea
              id="css_code"
              data-testid="css-code-input"
              value={formData.css_code}
              onChange={(e) => setFormData({ ...formData, css_code: e.target.value })}
              placeholder={`@keyframes myAnimation {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.animated-element {
  animation: myAnimation 2s ease-in-out infinite;
}`}
              rows={12}
              className="font-mono text-sm"
              required
            />
          </div>

          <div className="flex justify-end gap-3">
            <Button type="button" variant="outline" onClick={onClose} disabled={loading}>
              Cancel
            </Button>
            <Button type="submit" disabled={loading} data-testid="submit-animation-btn">
              {loading ? "Creating..." : "Create Animation"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export default AddAnimationDialog;
