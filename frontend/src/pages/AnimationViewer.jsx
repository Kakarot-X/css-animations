import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Copy, Heart, Play, Pause, ChevronLeft } from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import axios from "axios";
import { toast } from "sonner";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import AnimationPreview from "@/components/AnimationPreview";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AnimationViewer = ({ user }) => {
  const { animationId } = useParams();
  const navigate = useNavigate();
  const [animation, setAnimation] = useState(null);
  const [isPlaying, setIsPlaying] = useState(true);
  const [selectedShape, setSelectedShape] = useState("cube");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnimation();
  }, [animationId]);

  const loadAnimation = async () => {
    try {
      const response = await axios.get(`${API}/animations/${animationId}`);
      setAnimation(response.data);
      setSelectedShape(response.data.shape_type);
      setLoading(false);
    } catch (error) {
      console.error("Error loading animation:", error);
      toast.error("Failed to load animation");
    }
  };

  const handleCopyCode = () => {
    if (animation) {
      navigator.clipboard.writeText(animation.css_code);
      toast.success("CSS code copied to clipboard!");
    }
  };

  const handleLike = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`${API}/animations/${animationId}/like?token=${token}`);
      setAnimation(prev => ({
        ...prev,
        likes_count: response.data.likes_count,
        likes: response.data.liked 
          ? [...(prev.likes || []), user.id]
          : (prev.likes || []).filter(id => id !== user.id)
      }));
    } catch (error) {
      console.error("Error liking animation:", error);
    }
  };

  if (loading || !animation) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading animation...</p>
      </div>
    );
  }

  const isLiked = animation.likes?.includes(user.id);

  const shapes = [
    { id: "cube", label: "Cube" },
    { id: "square", label: "Square" },
    { id: "circle", label: "Circle" },
    { id: "rectangle", label: "Rectangle" }
  ];

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <Button variant="ghost" onClick={() => navigate(-1)} className="mb-6" data-testid="back-btn">
          <ChevronLeft className="mr-2 h-4 w-4" />
          Back
        </Button>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left side - Animation Preview */}
          <div>
            <Card className="p-6">
              <div className="mb-4 flex items-center justify-between">
                <h2 className="text-2xl font-bold">{animation.title}</h2>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setIsPlaying(!isPlaying)}
                  data-testid="play-pause-btn"
                >
                  {isPlaying ? <Pause className="h-5 w-5" /> : <Play className="h-5 w-5" />}
                </Button>
              </div>

              <div className="mb-4">
                <p className="text-sm text-muted-foreground mb-2">Select Shape:</p>
                <div className="flex gap-2 flex-wrap">
                  {shapes.map(shape => (
                    <Button
                      key={shape.id}
                      variant={selectedShape === shape.id ? "default" : "outline"}
                      size="sm"
                      onClick={() => setSelectedShape(shape.id)}
                      data-testid={`shape-${shape.id}-btn`}
                    >
                      {shape.label}
                    </Button>
                  ))}
                </div>
              </div>

              <AnimationPreview
                cssCode={animation.css_code}
                shape={selectedShape}
                isPlaying={isPlaying}
              />

              <div className="mt-6 flex items-center justify-between">
                <div 
                  className="flex items-center gap-3 cursor-pointer hover:opacity-80"
                  onClick={() => navigate(`/profile/${animation.user_id}`)}
                >
                  <Avatar className="h-10 w-10">
                    <AvatarImage src={animation.user_profile_picture} />
                    <AvatarFallback>{animation.username[0].toUpperCase()}</AvatarFallback>
                  </Avatar>
                  <div>
                    <p className="font-medium">{animation.username}</p>
                    <p className="text-sm text-muted-foreground">{animation.category}</p>
                  </div>
                </div>

                <Button
                  variant={isLiked ? "default" : "outline"}
                  onClick={handleLike}
                  data-testid="like-btn"
                >
                  <Heart className={`mr-2 h-4 w-4 ${isLiked ? 'fill-current' : ''}`} />
                  {animation.likes_count}
                </Button>
              </div>
            </Card>
          </div>

          {/* Right side - CSS Code */}
          <div>
            <Card className="p-6 h-full">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold">CSS Code</h2>
                <Button onClick={handleCopyCode} data-testid="copy-code-btn">
                  <Copy className="mr-2 h-4 w-4" />
                  Copy Code
                </Button>
              </div>

              <div className="bg-muted rounded-lg p-4 overflow-auto" style={{ maxHeight: '600px' }}>
                <pre className="text-sm">
                  <code data-testid="css-code-display">{animation.css_code}</code>
                </pre>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnimationViewer;
