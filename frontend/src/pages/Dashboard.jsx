import { useState, useEffect } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import axios from "axios";
import AnimationCard from "@/components/AnimationCard";
import AddAnimationDialog from "@/components/AddAnimationDialog";
import { toast } from "sonner";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = ({ user }) => {
  const [globalAnimations, setGlobalAnimations] = useState([]);
  const [followingAnimations, setFollowingAnimations] = useState([]);
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("global");

  const loadGlobalAnimations = async () => {
    try {
      const response = await axios.get(`${API}/animations`);
      setGlobalAnimations(response.data);
    } catch (error) {
      console.error("Error loading animations:", error);
      toast.error("Failed to load animations");
    }
  };

  const loadFollowingAnimations = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API}/animations/following?token=${token}`);
      setFollowingAnimations(response.data);
    } catch (error) {
      console.error("Error loading following animations:", error);
    }
  };

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      await Promise.all([loadGlobalAnimations(), loadFollowingAnimations()]);
      setLoading(false);
    };
    loadData();
  }, []);

  const handleAnimationAdded = () => {
    loadGlobalAnimations();
    loadFollowingAnimations();
    setShowAddDialog(false);
  };

  const handleLike = async (animationId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`${API}/animations/${animationId}/like?token=${token}`);
      loadGlobalAnimations();
      loadFollowingAnimations();
    } catch (error) {
      console.error("Error liking animation:", error);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold mb-2" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>Discover Animations</h1>
            <p className="text-muted-foreground">Explore CSS animations from around the world</p>
          </div>
          <Button onClick={() => setShowAddDialog(true)} data-testid="add-animation-btn">
            <Plus className="mr-2 h-4 w-4" />
            Add Animation
          </Button>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="mb-6">
            <TabsTrigger value="global" data-testid="global-feed-tab">Global Feed</TabsTrigger>
            <TabsTrigger value="following" data-testid="following-feed-tab">Following</TabsTrigger>
          </TabsList>

          <TabsContent value="global" data-testid="global-feed-content">
            {loading ? (
              <div className="text-center py-12">Loading animations...</div>
            ) : globalAnimations.length === 0 ? (
              <div className="text-center py-12 text-muted-foreground">
                No animations yet. Be the first to create one!
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {globalAnimations.map((animation) => (
                  <AnimationCard
                    key={animation.id}
                    animation={animation}
                    currentUserId={user.id}
                    onLike={handleLike}
                  />
                ))}
              </div>
            )}
          </TabsContent>

          <TabsContent value="following" data-testid="following-feed-content">
            {loading ? (
              <div className="text-center py-12">Loading animations...</div>
            ) : followingAnimations.length === 0 ? (
              <div className="text-center py-12 text-muted-foreground">
                No animations from people you follow. Start following creators to see their work here!
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {followingAnimations.map((animation) => (
                  <AnimationCard
                    key={animation.id}
                    animation={animation}
                    currentUserId={user.id}
                    onLike={handleLike}
                  />
                ))}
              </div>
            )}
          </TabsContent>
        </Tabs>
      </div>

      <AddAnimationDialog
        open={showAddDialog}
        onClose={() => setShowAddDialog(false)}
        onSuccess={handleAnimationAdded}
      />
    </div>
  );
};

export default Dashboard;
